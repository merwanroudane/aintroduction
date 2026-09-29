"""The TD research-topic bank.

Every topic promises the reader two things: a module of this course that actually covers
it, and a concrete applied task. Both are easy to break silently when topics are edited.
"""

import pytest

from utils.content import load_td_projects

EXPECTED_TOPICS = 65
KINDS = {"نظري", "مختلط", "تطبيقي"}


@pytest.fixture(scope="session")
def td():
    return load_td_projects()


@pytest.fixture(scope="session")
def topics(td):
    return [(ax, t) for ax in td["axes"] for t in ax["topics"]]


def test_seven_axes_and_all_topics_present(td, topics):
    assert len(td["axes"]) == 7, f"expected 7 axes, found {len(td['axes'])}"
    assert len(topics) == EXPECTED_TOPICS, f"expected {EXPECTED_TOPICS} topics, found {len(topics)}"


def test_topic_numbering_is_contiguous(topics):
    """The numbers are what a professor writes on the board when assigning work."""
    numbers = [t["n"] for _, t in topics]
    assert numbers == list(range(1, EXPECTED_TOPICS + 1)), "topic numbers must run 1..65 in order"


def test_every_topic_has_the_required_fields(topics):
    for ax, t in topics:
        where = f"{ax['id']} topic {t.get('n')}"
        for field in ("n", "title", "modules", "kind", "level", "applied", "fits"):
            assert t.get(field), f"{where}: missing {field!r}"
        assert t["kind"] in KINDS, f"{where}: bad kind {t['kind']!r}"
        assert t["level"] in (1, 2, 3), f"{where}: bad level {t['level']!r}"


def test_every_topic_maps_to_real_modules(topics, modules):
    known = {m.number for m in modules}
    for ax, t in topics:
        unknown = [n for n in t["modules"] if n not in known]
        assert not unknown, f"topic {t['n']}: maps to non-existent module(s) {unknown}"


def test_every_axis_maps_to_real_modules(td, modules):
    known = {m.number for m in modules}
    for ax in td["axes"]:
        assert ax.get("title") and ax.get("note"), f"{ax['id']}: missing title or note"
        unknown = [n for n in ax["modules"] if n not in known]
        assert not unknown, f"{ax['id']}: maps to non-existent module(s) {unknown}"


def test_applied_task_is_concrete(topics):
    """A one-word 'applied' field would defeat the whole point of the bank."""
    for ax, t in topics:
        assert len(t["applied"]) >= 40, (
            f"topic {t['n']}: the applied task is too vague to act on — {t['applied']!r}"
        )


def test_levels_are_documented(td):
    assert set(td["levels"]) == {1, 2, 3}
    for n, text in td["levels"].items():
        assert text.strip(), f"level {n} has no description"


def test_every_module_is_reachable_from_some_topic(topics, modules):
    """If a module is covered by no topic, students never research a third of the course."""
    covered = {n for _, t in topics for n in t["modules"]}
    missing = sorted({m.number for m in modules} - covered)
    assert not missing, f"no TD topic covers module(s) {missing}"


def test_mix_of_kinds_and_levels(topics):
    kinds = {t["kind"] for _, t in topics}
    levels = {t["level"] for _, t in topics}
    assert kinds == KINDS, f"the bank should offer all three kinds, has {kinds}"
    assert levels == {1, 2, 3}, f"the bank should span all three levels, has {levels}"
    applied = sum(1 for _, t in topics if t["kind"] == "تطبيقي")
    assert applied >= 10, f"only {applied} hands-on topics — the bank leans too theoretical"
