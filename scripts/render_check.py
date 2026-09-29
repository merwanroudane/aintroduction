"""Headless render check with Streamlit's AppTest.

Opens every view of a module (entry, each lecture, post-test, exit) in both
Learner and Instructor Mode, plus every static page, and reports exceptions and
unregistered diagrams/labs/references.

    python scripts/render_check.py --module 7
    python scripts/render_check.py            # all modules + static pages
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from streamlit.testing.v1 import AppTest  # noqa: E402

from utils.content import load_modules  # noqa: E402
from utils.nav import STATIC_PAGES, lecture_key  # noqa: E402

BAD_MARKERS = ("غير معرّف", "رابط غير صالح")


def _open(page_path: str | None, mode: str, state: dict | None = None) -> AppTest:
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=90)
    at.session_state["mode"] = mode
    at.run()
    if page_path:
        at.switch_page(page_path)
    for k, v in (state or {}).items():
        at.session_state[k] = v
    at.run()
    return at


def _report(at: AppTest, label: str, failures: list[str]) -> None:
    if at.exception:
        msg = at.exception[0].message
        failures.append(f"{label}: {msg}")
        print(f"FAIL {label} — {msg[:300]}")
        return
    texts = [str(x.value) for x in [*at.warning, *at.error, *at.caption]]
    bad = [t for t in texts if any(mk in t for mk in BAD_MARKERS)]
    failures.extend(f"{label}: {b}" for b in bad)
    print(("FAIL " if bad else "ok   ") + label + (f" — {bad}" if bad else ""))


def check_module(number: int, failures: list[str]) -> None:
    m = next(x for x in load_modules() if x.number == number)
    views = ["overview"] + [lec.id for lec in m.lectures] + ["quiz", "exit"]
    page_path = f"app_pages/modules/module_{number:02d}.py"
    for mode in ("learner", "instructor"):
        for v in views:
            at = _open(page_path, mode, {lecture_key(number): v})
            _report(at, f"module {number} [{mode}] {v}", failures)


def check_static(failures: list[str]) -> None:
    for name, (path, _, _) in STATIC_PAGES.items():
        for mode in ("learner", "instructor"):
            at = _open(None if name == "home" else path, mode)
            _report(at, f"page {name} [{mode}]", failures)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--module", type=int)
    ap.add_argument("--static", action="store_true", help="static pages only")
    args = ap.parse_args()
    failures: list[str] = []
    if args.module:
        check_module(args.module, failures)
    elif args.static:
        check_static(failures)
    else:
        check_static(failures)
        for m in load_modules():
            check_module(m.number, failures)
    print(f"\n{len(failures)} failure(s)")
    for f in failures:
        print(" -", f)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
