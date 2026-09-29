"""Structural invariants of the course content.

These are the rules that CONTENT_GUIDE.md states and that a human editor can break
silently: a module that stops matching the official syllabus card, a lecture whose id
no longer matches its folder, a cross-link to a lecture that was renamed. The validator
script checks depth and style; this file checks the things that must never drift.
"""

import re

import pytest

EXPECTED_MODULES = 13

# The 13 axis titles exactly as the official syllabus card lists them. If a module title
# is edited, this test fails — which is the point: the card is the binding source.
CARD_AXES = [
    "مقدمة في الذكاء الاصطناعي: المفهوم، الأهمية، والمجالات",
    "تاريخ الذكاء الاصطناعي: مراحل التطور",
    "أنواع الذكاء الاصطناعي: الضيق، العام، والفائق",
    "مقارنة بين الذكاء الاصطناعي، التعلم الآلي، والتعلم العميق",
    "المفاهيم الأساسية في هندسة الأوامر (Prompt Engineering)",
    "تقنيات بناء الأوامر للنماذج اللغوية الكبيرة",
    "تطبيقات النماذج اللغوية (ChatGPT، Google Gemini، Claude...)",
    "التفاعل مع نماذج الذكاء الاصطناعي لتوليد النصوص",
    "النماذج التوليدية للصور والصوت (DALL·E، Midjourney، Suno...)",
    "استخدام الذكاء الاصطناعي في الاقتصاد",
    "أخلاقيات الذكاء الاصطناعي: الإنصاف، الشفافية، والتحيز",
    "قضايا الخصوصية والأمان في أدوات الذكاء الاصطناعي",
    "دور الإنسان في الرقابة على الذكاء الاصطناعي",
]


def test_all_thirteen_modules_present(modules):
    assert [m.number for m in modules] == list(range(1, EXPECTED_MODULES + 1))


def test_module_titles_match_the_syllabus_card(modules):
    for m, expected in zip(modules, CARD_AXES):
        assert m.meta["title"] == expected, (
            f"module {m.number} title drifted from the official card.\n"
            f"  card: {expected}\n  file: {m.meta['title']}"
        )


def test_course_axes_match_the_syllabus_card(course):
    assert course["syllabus"]["axes"] == CARD_AXES


def test_every_module_has_at_least_three_lectures(modules):
    for m in modules:
        assert len(m.lectures) >= 3, f"module {m.number} has only {len(m.lectures)} lectures"


def test_lecture_ids_match_their_position(modules):
    for m in modules:
        for i, lec in enumerate(m.lectures, start=1):
            assert lec.id == f"m{m.number:02d}-l{i:02d}", (
                f"{lec.path.name}: id {lec.id!r} does not match module {m.number} position {i}"
            )
            assert lec.number == i


def test_lecture_ids_are_unique(lectures):
    ids = [lec.id for lec in lectures]
    assert len(ids) == len(set(ids)), "duplicate lecture ids"


def test_required_front_matter_present(lectures):
    required = ("id", "title", "objectives", "keywords", "summary",
                "references", "self_study", "duration")
    for lec in lectures:
        missing = [f for f in required if not lec.meta.get(f)]
        assert not missing, f"{lec.id}: front matter missing {missing}"


LECTURE_ID = re.compile(r"^m\d{2}-l\d{2}$")


def test_cross_links_resolve(lectures):
    """`builds_on` may name prior knowledge in prose (lecture 1.1 has nothing to build on),
    so only entries shaped like a lecture id are resolved — the same rule the validator uses."""
    known = {lec.id for lec in lectures}
    for lec in lectures:
        targets = set(lec.meta.get("related") or []) | set(lec.meta.get("builds_on") or [])
        targets = {t for t in targets if LECTURE_ID.match(str(t))}
        targets |= {s.text for s in lec.segments if s.kind == "link"}
        unknown = sorted(targets - known)
        assert not unknown, f"{lec.id}: links to non-existent lecture(s) {unknown}"


def test_every_lecture_reference_id_exists(lectures, references):
    for lec in lectures:
        for item in lec.meta.get("references") or []:
            rid = item["id"] if isinstance(item, dict) else item
            assert rid in references, f"{lec.id}: unknown reference id {rid!r}"


def test_suggested_reading_ids_exist(modules, references):
    for m in modules:
        for rid in m.meta.get("exit", {}).get("suggested_reading", []):
            assert rid in references, f"module {m.number} exit: unknown reference id {rid!r}"


def test_objectives_are_bloom_tagged(modules):
    bloom = {"remember", "understand", "apply", "analyze", "evaluate", "create"}
    for m in modules:
        objectives = m.meta.get("objectives") or []
        assert objectives, f"module {m.number} has no objectives"
        for obj in objectives:
            assert isinstance(obj, dict), f"module {m.number}: objective must be a mapping"
            assert obj.get("bloom") in bloom, f"module {m.number}: bad bloom tag {obj.get('bloom')!r}"
            assert obj.get("text"), f"module {m.number}: objective without text"


def test_entry_and_exit_systems_present(modules):
    """The course card mandates an entry system and an exit system for every module."""
    for m in modules:
        entry, exit_ = m.meta.get("entry") or {}, m.meta.get("exit") or {}
        assert entry.get("prior_knowledge"), f"module {m.number}: entry.prior_knowledge missing"
        assert entry.get("diagnostic_questions"), f"module {m.number}: entry.diagnostic_questions missing"
        for field in ("competencies", "assessment_activities", "common_mistakes",
                      "remediation", "suggested_reading", "bridge"):
            assert exit_.get(field), f"module {m.number}: exit.{field} missing"


def test_instructor_notes_present(modules):
    for m in modules:
        ins = m.meta.get("instructor") or {}
        for field in ("sequence", "timing", "discussion", "assessment_ideas"):
            assert ins.get(field), f"module {m.number}: instructor.{field} missing"


@pytest.mark.parametrize("bad", ["وNorvig", "وRussell", "وChatGPT"])
def test_no_bidi_broken_conjunction(lectures, bad):
    """An Arabic waw glued to a Latin word renders reversed; CONTENT_GUIDE requires a space."""
    offenders = [lec.id for lec in lectures if bad in lec.body]
    assert not offenders, f"{bad!r} (waw glued to Latin) found in {offenders}"


def test_no_placeholder_text(lectures):
    placeholders = ("TODO", "TBD", "FIXME", "XXX", "Lorem ipsum", "[[أكمل", "...أكمل")
    for lec in lectures:
        for p in placeholders:
            assert p not in lec.body, f"{lec.id}: placeholder {p!r} left in body"


def test_every_lecture_has_a_recap_and_a_check(lectures):
    """Every lecture closes the loop: a self-check question and a concept recap."""
    for lec in lectures:
        kinds = {s.block_type for s in lec.segments if s.kind == "block"}
        assert "check" in kinds, f"{lec.id}: no :::check block"
        assert "recap" in kinds, f"{lec.id}: no :::recap block"


def test_self_study_items_are_sourced_and_dated(lectures):
    for lec in lectures:
        for item in lec.meta.get("self_study") or []:
            assert str(item.get("url", "")).startswith("http"), \
                f"{lec.id}: self_study item without a URL: {item.get('title')}"
            assert item.get("verified"), \
                f"{lec.id}: self_study item not dated: {item.get('title')}"
            assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(item["verified"])), \
                f"{lec.id}: verified date must be YYYY-MM-DD, got {item['verified']!r}"
