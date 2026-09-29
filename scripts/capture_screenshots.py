"""Capture publication-quality screenshots of the running app.

    streamlit run app.py                      # in one terminal
    python scripts/capture_screenshots.py     # in another

Writes PNGs to screenshots/ at 2x device scale, which is what a journal or a slide deck
needs — a 1x capture of a 1600px-wide page looks soft the moment it is printed or
projected. Both Learner and Instructor Mode are covered, because the mode switch is the
thing a reader of a paper about this platform will want to see.

    --out DIR        where to write (default: screenshots/)
    --url URL        the running app (default: http://localhost:8501)
    --width N        CSS viewport width (default: 1600)
    --scale N        device pixel ratio (default: 2)
    --only NAME      capture a single shot by name, for iterating
    --list           print the shot list and exit
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    from playwright.sync_api import Page, sync_playwright
except ImportError:  # pragma: no cover - guidance, not logic
    sys.exit("playwright is not installed.\n"
             "    pip install playwright && python -m playwright install chromium")

# name, url path, mode, what to wait for, and whether to shoot the full scrollable page.
# `settle` is extra seconds for Plotly figures, which draw after Streamlit reports ready.
# A full-page shot of a very long page becomes unusable as a figure and slow to render,
# so the capture is capped. In CSS pixels, before the 2x device scale is applied.
MAX_FULL_HEIGHT = 9000

def _static_path(key: str) -> str:
    """Resolve a nav key to the URL Streamlit actually serves that page at.

    Hardcoding these cost two silently wrong screenshots: /map and /toolkit do not exist,
    the app fell back to the home page, and the wait-text happened to match a sidebar
    label so nothing complained. Deriving them from the registry cannot drift.
    """
    from utils.nav import STATIC_PAGES

    path, _title, _icon = STATIC_PAGES[key]
    return "/" if key == "home" else "/" + Path(path).stem


# name, url, mode, a phrase that appears ONLY on that page, full-page, settle seconds.
# `settle` is extra time for Plotly figures, which draw after Streamlit reports ready.
SHOTS = [
    ("01-home",               _static_path("home"),       "learner",    "وصف المقرر",                False, 2.5),
    ("02-home-full",          _static_path("home"),       "learner",    "وصف المقرر",                True,  3.5),
    ("03-course-map",         _static_path("map"),        "learner",    "السلسلة المفاهيمية",      True,  4.0),
    ("04-module-overview",    "/module-05",               "learner",    "Foundations of Prompt", False, 3.0),
    ("05-lecture",            "/module-05?lec05=m05-l03", "learner",    "البنية والفواصل",          False, 3.0),
    ("06-lecture-cards",      "/module-09?lec09=m09-l02", "learner",    "نماذج الانتشار",           True,  4.0),
    ("07-lecture-instructor", "/module-05?lec05=m05-l03", "instructor", "البنية والفواصل",          True,  3.5),
    ("08-labs",               _static_path("labs"),       "learner",    "المختبرات التفاعلية",    False, 4.0),
    ("09-knowledge-map",      _static_path("knowledge"),  "learner",    "مصفوفة الإحالات",         False, 4.5),
    ("10-glossary",           _static_path("glossary"),   "learner",    "قاموس الذكاء",            False, 2.5),
    ("11-references",         _static_path("references"), "learner",    "المصادر والمراجع",       False, 2.5),
    ("12-pretest",            _static_path("pretest"),    "learner",    "الاختبار القبلي العام",  False, 2.5),
    ("13-td-guide",           _static_path("td"),         "instructor", "دليل حصص الأعمال",        False, 2.5),
    ("14-td-topics",          _static_path("td"),         "instructor", "دليل حصص الأعمال",        True,  3.0),
    ("15-instructor-toolkit", _static_path("toolkit"),    "instructor", "أدوات الأستاذ",           False, 3.0),
    ("16-capstone",           _static_path("capstone"),   "learner",    "المشروع الختامي",        False, 2.5),
]


def _set_mode(page: Page, mode: str) -> None:
    """Flip the sidebar's Learner/Instructor control if it is not already there."""
    label = "وضع الأستاذ" if mode == "instructor" else "وضع الطالب"
    try:
        control = page.get_by_text(label, exact=True).last
        control.click(timeout=4000)
        page.wait_for_timeout(2500)
    except Exception:
        pass  # already in that mode, or the page has no switch


def _scroll_to_top(page: Page) -> None:
    """Streamlit keeps each pane's scroll position across navigations, so without this the
    sidebar can be captured halfway down its own list."""
    page.evaluate("""
        () => {
            window.scrollTo(0, 0);
            document.querySelectorAll(
                'section[data-testid="stSidebar"], section[data-testid="stMain"],'
                + ' [data-testid="stSidebarContent"], [data-testid="stMainBlockContainer"]'
            ).forEach(el => { el.scrollTop = 0; });
        }
    """)
    page.wait_for_timeout(400)


def _hide_chrome(page: Page) -> None:
    """Remove Streamlit's own toolbar and the deploy button: they are not part of the
    platform and only clutter a figure in a paper."""
    page.add_style_tag(content="""
        [data-testid="stToolbar"], [data-testid="stDecoration"],
        [data-testid="stStatusWidget"], .stAppDeployButton,
        iframe[title="streamlitApp"] ~ div { display: none !important; }
        [data-testid="stAppViewContainer"] { padding-top: 0 !important; }
    """)


def _unlock_page_height(page: Page) -> int:
    """Let the whole page be captured in one image.

    Playwright's full_page option grows the *document*, but Streamlit scrolls inside its
    own panes, so the document never grows and full_page silently returns just the
    viewport. Releasing those containers and then resizing the viewport to the real
    content height is what actually produces a full-page shot. Returns that height.
    """
    page.add_style_tag(content="""
        html, body, [data-testid="stAppViewContainer"], section[data-testid="stMain"],
        [data-testid="stMainBlockContainer"], .main, .block-container {
            height: auto !important;
            max-height: none !important;
            overflow: visible !important;
        }
        /* The sidebar is normally fixed to the viewport. On a tall capture that would
           leave it floating over a slice of the page, so stretch it the full height and
           pin its contents to the top: the navigation stays readable and the coloured
           panel runs the length of the figure. */
        section[data-testid="stSidebar"] {
            position: relative !important;
            align-self: stretch !important;
            height: auto !important;
            min-height: 100% !important;
            overflow: visible !important;
        }
        section[data-testid="stSidebar"] [data-testid="stSidebarContent"],
        section[data-testid="stSidebar"] > div {
            height: auto !important; overflow: visible !important;
            position: sticky !important; top: 0 !important;
        }
    """)
    page.wait_for_timeout(700)
    return page.evaluate("""
        () => Math.max(
            document.body.scrollHeight, document.documentElement.scrollHeight,
            ...[...document.querySelectorAll('[data-testid="stMainBlockContainer"]')]
                .map(el => el.getBoundingClientRect().height + 80)
        )
    """)


def capture(out: Path, url: str, width: int, scale: int, only: str | None) -> int:
    out.mkdir(parents=True, exist_ok=True)
    shots = [s for s in SHOTS if not only or s[0] == only]
    if not shots:
        sys.exit(f"no shot named {only!r}. Use --list to see the names.")

    written = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(
            viewport={"width": width, "height": 1000},
            device_scale_factor=scale,
            locale="ar",
        )
        page = ctx.new_page()
        current_mode = None

        for name, path, mode, wait_text, full, settle in shots:
            target = url.rstrip("/") + path
            print(f"  {name:24} {path}", flush=True)
            page.goto(target, wait_until="load", timeout=60_000)
            # Streamlit renders after load; wait for real content, not just the shell.
            try:
                page.wait_for_selector('[data-testid="stAppViewContainer"]', timeout=30_000)
                page.get_by_text(wait_text).first.wait_for(timeout=25_000)
            except Exception:
                print(f"    (warning: {wait_text!r} not found — capturing anyway)")
            if mode != current_mode:
                _set_mode(page, mode)
                current_mode = mode
                page.wait_for_timeout(1500)
            _hide_chrome(page)
            time.sleep(settle)  # let Plotly finish drawing
            _scroll_to_top(page)
            target_file = out / f"{name}.png"
            if full:
                height = min(int(_unlock_page_height(page)), MAX_FULL_HEIGHT)
                page.set_viewport_size({"width": width, "height": height})
                page.wait_for_timeout(1200)  # relayout, and Plotly redraws on resize
                _scroll_to_top(page)
            page.screenshot(path=str(target_file), full_page=full)
            if full:  # restore, so the next shot is not captured at a freak height
                page.set_viewport_size({"width": width, "height": 1000})
                page.wait_for_timeout(500)
            written.append(target_file)

        browser.close()

    print(f"\nwrote {len(written)} screenshot(s) to {out.relative_to(ROOT)}/ "
          f"at {width}px × {scale}x")
    for f in written:
        kb = f.stat().st_size / 1024
        print(f"  {f.name:28} {kb:7.0f} KB")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="screenshots", help="output directory")
    ap.add_argument("--url", default="http://localhost:8501", help="running app URL")
    ap.add_argument("--width", type=int, default=1600, help="CSS viewport width")
    ap.add_argument("--scale", type=int, default=2, help="device pixel ratio")
    ap.add_argument("--only", help="capture one shot by name")
    ap.add_argument("--list", action="store_true", help="print the shot list and exit")
    args = ap.parse_args()

    if args.list:
        print(f"{'name':26} {'mode':11} {'full page':10} path")
        for name, path, mode, _w, full, _s in SHOTS:
            print(f"{name:26} {mode:11} {str(full):10} {path}")
        return 0

    import urllib.request
    try:
        urllib.request.urlopen(args.url, timeout=10)
    except Exception:
        sys.exit(f"nothing is serving {args.url}.\n    Start it first:  streamlit run app.py")

    return capture(ROOT / args.out, args.url, args.width, args.scale, args.only)


if __name__ == "__main__":
    sys.exit(main())
