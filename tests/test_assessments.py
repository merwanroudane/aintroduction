"""Quiz correctness.

A wrong answer key is the worst defect this platform can ship: it teaches the opposite of
the truth, and nobody notices until a student is marked wrong for being right. These tests
check every one of the 286 questions mechanically against the schema that
``components/quiz.py`` actually renders — answer in range, options distinct, feedback
present, review link resolvable.

The four question types, as the renderer handles them:
    mcq       one correct option;      answer = int index
    multi     several correct options; answer = list of int indexes
    scenario  a scenario + one correct option; answer = int index
    tf        true/false;              answer = bool (rendered as صحيح/خطأ)
"""

import re

SINGLE_CHOICE = {"mcq", "scenario"}
VALID_TYPES = SINGLE_CHOICE | {"multi", "tf"}
BLOOM = {"remember", "understand", "apply", "analyze", "evaluate", "create"}


def _questions(assessments, all_quiz_questions):
    """Every question in the course: module entry, module post, pre-test, post-test."""
    items = [(f"module {n} {where}", q) for where, n, q in all_quiz_questions]
    items += [("pretest", q) for q in assessments["pretest"]["questions"]]
    items += [("posttest", q) for q in assessments["posttest"]["questions"]]
    return items


def _correct_set(q):
    """Mirrors components.quiz._correct_set — the renderer's own notion of 'correct'."""
    if q["type"] == "tf":
        return {0 if q["answer"] else 1}
    ans = q["answer"]
    return set(ans) if isinstance(ans, list) else {int(ans)}


def test_question_ids_unique(assessments, all_quiz_questions):
    ids = [q["id"] for _, q in _questions(assessments, all_quiz_questions)]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    assert not dupes, f"duplicate question ids: {dupes}"


def test_every_question_has_required_fields(assessments, all_quiz_questions):
    for where, q in _questions(assessments, all_quiz_questions):
        assert q.get("id"), f"{where}: question without an id"
        assert q.get("prompt"), f"{where} {q.get('id')}: no prompt"
        assert q.get("type") in VALID_TYPES, f"{where} {q['id']}: bad type {q.get('type')!r}"
        assert q.get("explanation"), f"{where} {q['id']}: no explanation"
        assert "answer" in q, f"{where} {q['id']}: no answer key"


def test_scenario_questions_carry_a_scenario(assessments, all_quiz_questions):
    for where, q in _questions(assessments, all_quiz_questions):
        if q["type"] == "scenario":
            assert q.get("scenario"), f"{where} {q['id']}: type is scenario but no scenario text"


def test_answer_indexes_are_in_range(assessments, all_quiz_questions):
    """The defect that actually happened once: an answer index pointing past the options."""
    for where, q in _questions(assessments, all_quiz_questions):
        if q["type"] == "tf":
            continue
        options = q.get("options") or []
        assert len(options) >= 3, f"{where} {q['id']}: needs at least 3 options"
        for idx in _correct_set(q):
            assert isinstance(idx, int) and not isinstance(idx, bool), \
                f"{where} {q['id']}: answer {idx!r} is not an index"
            assert 0 <= idx < len(options), (
                f"{where} {q['id']}: answer index {idx} out of range for {len(options)} options"
            )


def test_single_choice_has_exactly_one_answer(assessments, all_quiz_questions):
    for where, q in _questions(assessments, all_quiz_questions):
        if q["type"] in SINGLE_CHOICE:
            assert isinstance(q["answer"], int) and not isinstance(q["answer"], bool), \
                f"{where} {q['id']}: {q['type']} answer must be a single index, got {q['answer']!r}"


def test_multi_has_at_least_two_answers_but_not_all(assessments, all_quiz_questions):
    """A `multi` with one answer is really an mcq; a `multi` where everything is correct
    tests nothing."""
    for where, q in _questions(assessments, all_quiz_questions):
        if q["type"] != "multi":
            continue
        answers = q["answer"]
        assert isinstance(answers, list), f"{where} {q['id']}: multi answer must be a list"
        assert len(set(answers)) == len(answers), f"{where} {q['id']}: repeated answer index"
        assert len(answers) >= 2, f"{where} {q['id']}: multi with a single answer — use mcq"
        assert len(answers) < len(q["options"]), \
            f"{where} {q['id']}: every option is correct, so the question discriminates nothing"


def test_options_are_distinct_and_non_empty(assessments, all_quiz_questions):
    for where, q in _questions(assessments, all_quiz_questions):
        if q["type"] == "tf":
            continue
        options = q["options"]
        assert all(str(o).strip() for o in options), f"{where} {q['id']}: empty option"
        assert len(set(options)) == len(options), f"{where} {q['id']}: duplicate options"


def test_tf_answer_is_boolean(assessments, all_quiz_questions):
    for where, q in _questions(assessments, all_quiz_questions):
        if q["type"] == "tf":
            assert isinstance(q["answer"], bool), \
                f"{where} {q['id']}: true/false answer must be a boolean, got {q['answer']!r}"
            assert "options" not in q, \
                f"{where} {q['id']}: tf questions render صحيح/خطأ; remove the options list"


def test_why_wrong_keys_point_at_real_distractors(assessments, all_quiz_questions):
    """`why_wrong` explains a distractor, so its keys must be option indexes — and never a
    correct answer, which would contradict the answer key in front of the student."""
    for where, q in _questions(assessments, all_quiz_questions):
        why = q.get("why_wrong") or {}
        if not why:
            continue
        assert q["type"] != "tf", f"{where} {q['id']}: why_wrong does not apply to tf questions"
        correct = _correct_set(q)
        for key in why:
            idx = int(key)
            assert 0 <= idx < len(q["options"]), \
                f"{where} {q['id']}: why_wrong index {idx} out of range"
            assert idx not in correct, \
                f"{where} {q['id']}: why_wrong explains index {idx}, which is a correct answer"
            assert str(why[key]).strip(), f"{where} {q['id']}: empty why_wrong text for {idx}"


def test_bloom_tags_valid(assessments, all_quiz_questions):
    for where, q in _questions(assessments, all_quiz_questions):
        if "bloom" in q:
            assert q["bloom"] in BLOOM, f"{where} {q['id']}: bad bloom tag {q['bloom']!r}"


def test_review_links_resolve(assessments, all_quiz_questions, lectures):
    """Every question points back at the lecture that teaches it."""
    known = {lec.id for lec in lectures}
    for where, q in _questions(assessments, all_quiz_questions):
        review = q.get("review")
        if review is None:
            continue
        for target in (review if isinstance(review, list) else [review]):
            assert target in known, f"{where} {q['id']}: review → unknown lecture {target!r}"


def test_module_questions_are_id_prefixed_by_their_module(all_quiz_questions):
    for where, number, q in all_quiz_questions:
        prefix = f"m{number:02d}-"
        assert q["id"].startswith(prefix), \
            f"module {number} {where}: question id {q['id']!r} should start with {prefix!r}"


def test_every_module_has_entry_and_post_questions(modules):
    for m in modules:
        assert len(m.entry_quiz) >= 3, f"module {m.number}: only {len(m.entry_quiz)} entry questions"
        assert len(m.quiz) >= 8, f"module {m.number}: only {len(m.quiz)} post questions"


def test_post_quizzes_span_bloom_levels(modules):
    """A module quiz that is all `remember` does not assess the module's own objectives."""
    for m in modules:
        levels = {q.get("bloom") for q in m.quiz if q.get("bloom")}
        assert len(levels) >= 3, f"module {m.number}: quiz only reaches bloom levels {levels}"


def test_pretest_and_posttest_cover_the_course(assessments):
    pre = assessments["pretest"]["questions"]
    post = assessments["posttest"]["questions"]
    assert len(pre) >= 12, f"pre-test has only {len(pre)} questions"
    assert len(post) >= 25, f"post-test has only {len(post)} questions"
    # The post-test is the course exit, so it should reach across most of the 13 modules.
    touched = set()
    for q in post:
        review = q.get("review")
        for target in (review if isinstance(review, list) else [review] if review else []):
            touched.add(int(re.match(r"m(\d{2})-", target).group(1)))
    assert len(touched) >= 10, f"post-test only reviews modules {sorted(touched)}"


def test_pretest_questions_are_topic_tagged(assessments):
    """The pre-test reports per-topic results, so every question needs a known topic."""
    topics = set(assessments["pretest"]["topics"])
    for q in assessments["pretest"]["questions"]:
        assert q.get("topic") in topics, \
            f"pretest {q['id']}: topic {q.get('topic')!r} not in {sorted(topics)}"


def test_capstone_is_complete(capstone):
    for field in ("intro", "general", "phases", "tracks", "rubric"):
        assert capstone.get(field), f"capstone: {field} missing"
    for track in capstone["tracks"]:
        assert track.get("title"), "capstone track without a title"
