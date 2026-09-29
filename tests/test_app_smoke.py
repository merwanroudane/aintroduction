"""Does the app actually run?

`render_check.py` opens every module view in both modes and takes minutes; this file is
the fast subset meant for `pytest`: the app boots, the navigation is built, a module page
renders in both modes, and the two rendering bugs that have already bitten this project
cannot come back silently.

Run the exhaustive pass separately:  python scripts/render_check.py
"""

import re
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parent.parent
TIMEOUT = 60


def _open(page: str | None = None, mode: str = "learner") -> AppTest:
    """Boot through app.py — it is what calls init_state() — then switch to the page.
    Opening a page file directly would fail on uninitialised session state, which is a
    property of the harness, not a defect in the page."""
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=TIMEOUT)
    at.session_state["mode"] = mode
    at.run()
    if page:
        at.switch_page(page)
        at.run()
    return at


def test_app_boots_without_exception():
    at = _open()
    assert not at.exception, f"app.py raised: {[e.message for e in at.exception]}"


def test_every_module_has_a_page_file(modules):
    """st.navigation builds from these paths, so a missing file breaks the whole app."""
    for m in modules:
        assert (ROOT / f"app_pages/modules/module_{m.number:02d}.py").exists(), \
            f"module {m.number}: page file missing"


@pytest.mark.parametrize("mode", ["learner", "instructor"])
def test_first_module_renders_in_both_modes(mode):
    at = _open("app_pages/modules/module_01.py", mode=mode)
    assert not at.exception, f"module 1 in {mode} mode raised: {[e.message for e in at.exception]}"


@pytest.mark.parametrize("page", [
    "home", "course_map", "glossary", "references", "search",
    "pretest", "posttest", "labs", "capstone", "knowledge_map",
    "instructor_toolkit", "progress", "td_guide",
])
def test_static_pages_render(page):
    at = _open(f"app_pages/{page}.py")
    assert not at.exception, f"{page} raised: {[e.message for e in at.exception]}"


def test_no_unregistered_diagram_or_lab_warning():
    """The renderer warns instead of crashing on an unknown name, so a typo in a
    `[[diagram:…]]` token would otherwise pass every other test silently."""
    at = _open("app_pages/modules/module_01.py")
    bad = [w.value for w in at.warning
           if "غير معرّف" in str(w.value) or "غير صالح" in str(w.value)]
    assert not bad, f"module 1 rendered with warnings: {bad}"


# --- regressions -----------------------------------------------------------------

def test_stylesheet_contains_no_angle_bracket():
    """Regression: `st.html` runs its input through a sanitizer. A single `<` anywhere in
    the stylesheet — even inside a comment — made it drop the whole block, and the app
    rendered completely unstyled. The fix was to forbid `<` in the CSS file."""
    css = (ROOT / "assets/css").glob("*.css")
    files = list(css)
    assert files, "no stylesheet found under assets/css"
    for path in files:
        text = path.read_text(encoding="utf-8")
        assert "<" not in text, (
            f"{path.name}: contains '<', which the HTML sanitizer will use to drop the "
            f"entire stylesheet. Rewrite the comment or selector without it."
        )


def test_lecture_query_param_uses_the_lecture_id(modules):
    """Regression: binding the lecture picker to `query-params` wrote the *formatted Arabic
    label* into the URL, so id-based deep links from search and cross-links silently
    failed. The view must sync on the lecture id instead."""
    source = (ROOT / "app_pages/module_view.py").read_text(encoding="utf-8")
    # The file explains the trap in a comment, so only real code lines are checked.
    code = "\n".join(ln for ln in source.splitlines() if not ln.lstrip().startswith("#"))
    assert 'bind="query-params"' not in code, (
        "module_view.py binds a widget to query-params again: that stores the display "
        "label, not the lecture id, and breaks deep links."
    )
    assert "st.query_params" in code, "module_view.py no longer syncs the URL at all"


def test_every_module_page_is_a_thin_wrapper(modules):
    """Spec §54: lectures live in content/module_XX/*.md, never inline in a page file."""
    for m in modules:
        path = ROOT / f"app_pages/modules/module_{m.number:02d}.py"
        lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
        assert len(lines) <= 12, (
            f"{path.name} has {len(lines)} lines — page files stay thin and delegate to "
            f"module_view; lecture prose belongs in content/."
        )
