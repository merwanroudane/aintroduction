"""Shared fixtures. The content is loaded once per session: parsing 72 lectures on every
test would dominate the run time, and nothing in the suite mutates what it loads."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from utils.content import (  # noqa: E402
    all_lectures, load_assessments, load_capstone, load_course, load_glossary,
    load_modules, load_references,
)


@pytest.fixture(scope="session")
def modules():
    return load_modules()


@pytest.fixture(scope="session")
def lectures():
    return all_lectures()


@pytest.fixture(scope="session")
def references():
    return load_references()


@pytest.fixture(scope="session")
def glossary():
    return load_glossary()


@pytest.fixture(scope="session")
def course():
    return load_course()


@pytest.fixture(scope="session")
def assessments():
    return load_assessments()


@pytest.fixture(scope="session")
def capstone():
    return load_capstone()


@pytest.fixture(scope="session")
def all_quiz_questions(modules):
    """Every module question and entry question, tagged with where it came from."""
    out = []
    for m in modules:
        for q in m.entry_quiz:
            out.append(("entry", m.number, q))
        for q in m.quiz:
            out.append(("post", m.number, q))
    return out
