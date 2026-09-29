"""Project-level files stay in step with the content.

SOURCES.md is generated, so it goes stale the moment a reference is added; README numbers
are the kind of thing nobody re-counts. These tests fail instead.
"""

import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _read(name: str) -> str:
    path = ROOT / name
    assert path.exists(), f"{name} is missing"
    return path.read_text(encoding="utf-8")


@pytest.mark.parametrize("name", ["README.md", "CHANGELOG.md", "SOURCES.md",
                                  "CONTENT_GUIDE.md", "requirements.txt",
                                  "requirements-dev.txt", ".gitignore"])
def test_project_file_exists_and_is_not_empty(name):
    assert _read(name).strip(), f"{name} is empty"


def _imports_under(*dirs: str) -> set[str]:
    """Third-party module names imported anywhere under the given directories."""
    stdlib = set(sys.stdlib_module_names)
    local = {"app_pages", "components", "utils", "scripts", "tests"}
    found = set()
    for d in dirs:
        base = ROOT / d if d else ROOT
        paths = base.rglob("*.py") if base.is_dir() else [base]
        for path in paths:
            if any(part in {".venv", "__pycache__"} for part in path.parts):
                continue
            for line in path.read_text(encoding="utf-8").splitlines():
                m = re.match(r"^\s*(?:import|from)\s+([A-Za-z_][A-Za-z0-9_]*)", line)
                if m:
                    found.add(m.group(1))
    return found - stdlib - local - {"__future__"}


def test_requirements_cover_every_third_party_import():
    """A dependency that is imported but unpinned breaks a fresh install, and the failure
    lands on whoever clones the repo rather than on us.

    The split matters for deployment: requirements.txt is what a host installs to *run*
    the app, so a package used only by the tests or the authoring scripts is dead weight
    in production — a headless browser especially. Anything the app imports must be in
    requirements.txt; anything imported only under tests/ or scripts/ may live in
    requirements-dev.txt instead.
    """
    alias = {"yaml": "pyyaml"}  # import name → distribution name
    runtime = _read("requirements.txt").lower()
    dev = _read("requirements-dev.txt").lower()

    # What the deployed app imports must be in requirements.txt.
    app_imports = _imports_under("app.py", "app_pages", "components", "utils")
    missing = [m for m in sorted(app_imports) if alias.get(m, m) not in runtime]
    assert not missing, f"imported by the app but not in requirements.txt: {missing}"

    # The tests and the authoring scripts never run on the host, so either file will do.
    tooling = _imports_under("tests", "scripts")
    unpinned = [m for m in sorted(tooling)
                if alias.get(m, m) not in runtime and alias.get(m, m) not in dev]
    assert not unpinned, f"imported by tests/ or scripts/ but pinned nowhere: {unpinned}"


def test_dev_requirements_include_the_runtime_ones():
    """`pip install -r requirements-dev.txt` alone should give a working checkout."""
    assert "-r requirements.txt" in _read("requirements-dev.txt"), (
        "requirements-dev.txt should start from requirements.txt so one command sets up "
        "a development environment"
    )


def test_sources_file_is_up_to_date():
    """SOURCES.md is generated from references.yml; regenerate it after adding a source:
        python scripts/build_sources.py
    """
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/build_sources.py"), "--check"],
        capture_output=True, text=True, cwd=ROOT, encoding="utf-8", errors="replace",
    )
    assert result.returncode == 0, (
        (result.stdout or "") + (result.stderr or "")
        + "\nRun: python scripts/build_sources.py"
    )


def test_readme_counts_match_the_content(modules, lectures, references, glossary,
                                         assessments, all_quiz_questions):
    """Counts in the README are a promise to the reader; keep them true."""
    readme = _read("README.md")
    module_questions = len(all_quiz_questions)
    totals = {
        "lectures": len(lectures),
        "questions": module_questions
        + len(assessments["pretest"]["questions"])
        + len(assessments["posttest"]["questions"]),
        "references": len(references),
        "glossary": len(glossary),
        "modules": len(modules),
    }
    for label, value in totals.items():
        assert str(value) in readme, (
            f"README does not mention the real {label} count ({value}). "
            f"Update the totals after changing content."
        )


def test_readme_lists_every_module_title(modules):
    readme = _read("README.md")
    for m in modules:
        assert m.meta["title"] in readme, \
            f"README is missing module {m.number}: {m.meta['title']}"


def test_readme_documents_how_to_run():
    readme = _read("README.md")
    assert "streamlit run app.py" in readme, "README does not say how to start the app"
    assert "pip install -r requirements.txt" in readme, "README does not say how to install"


def test_every_script_is_documented_in_the_readme():
    readme = _read("README.md")
    undocumented = [p.name for p in sorted((ROOT / "scripts").glob("*.py"))
                    if p.name not in readme and p.name != "__init__.py"]
    assert not undocumented, f"scripts not mentioned in README.md: {undocumented}"


def test_changelog_has_a_released_version():
    changelog = _read("CHANGELOG.md")
    assert re.search(r"^## \[\d+\.\d+\.\d+\] — \d{4}-\d{2}-\d{2}", changelog, re.M), \
        "CHANGELOG.md has no released version heading like '## [1.0.0] — 2026-09-29'"


def test_research_log_per_module(modules):
    for m in modules:
        path = ROOT / f"research/logs/m{m.number:02d}.md"
        assert path.exists(), f"module {m.number}: no research log at {path.name}"
        assert path.read_text(encoding="utf-8").strip(), f"{path.name} is empty"
