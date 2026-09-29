"""Quiz engine for module quizzes, the pre-test and the post-test.

Question schema (YAML):

    - id: m01-q03
      type: mcq | multi | tf | scenario        scenario = mcq preceded by a case text
      bloom: remember | understand | apply | analyze | evaluate | create
      scenario: optional case text (Markdown)
      prompt: question text
      options: [..]                            omitted for tf
      answer: 1 | [0, 2] | true                index, list of indices, or boolean
      explanation: why the correct answer is correct
      why_wrong: {0: "...", 2: "..."}          optional, per distractor
      review: m01-l02                          lecture to revisit if missed
      topic: optional tag (used by the pre-test diagnostic profile)

Learner Mode: answers and feedback appear only after submission.
Instructor Mode: an answer key with explanations is always available.
"""

from __future__ import annotations

from collections import defaultdict

import streamlit as st

from utils.nav import link_to_lecture
from utils.state import is_instructor, record_quiz

BLOOM_AR = {
    "remember": "تذكّر", "understand": "فهم", "apply": "تطبيق",
    "analyze": "تحليل", "evaluate": "تقييم", "create": "إبداع",
}
# Bloom's six levels climb through the spectrum, cool to warm, so the cognitive demand
# of an objective or a question is visible before it is read.
BLOOM_COLOR = {
    "remember": "gray", "understand": "blue", "apply": "green",
    "analyze": "orange", "evaluate": "violet", "create": "red",
}
TYPE_AR = {"mcq": "اختيار من متعدد", "multi": "اختيار متعدد الإجابات",
           "tf": "صح أم خطأ", "scenario": "سؤال سيناريو"}
TF_OPTIONS = ["صحيح", "خطأ"]


def _correct_set(q: dict) -> set[int]:
    if q["type"] == "tf":
        return {0 if q["answer"] else 1}
    ans = q["answer"]
    return set(ans) if isinstance(ans, list) else {int(ans)}


def _options(q: dict) -> list[str]:
    return TF_OPTIONS if q["type"] == "tf" else q["options"]


def _is_correct(q: dict, response) -> bool:
    if response is None:
        return False
    chosen = set(response) if isinstance(response, (list, tuple, set)) else {response}
    return chosen == _correct_set(q)


TYPE_COLOR = {"mcq": "blue", "multi": "violet", "tf": "green", "scenario": "orange"}


def _question_header(i: int, q: dict) -> None:
    tags = [(TYPE_COLOR.get(q["type"], "gray"), TYPE_AR.get(q["type"], q["type"]))]
    if q.get("bloom"):
        tags.append((BLOOM_COLOR.get(q["bloom"], "gray"),
                     f"مستوى بلوم: {BLOOM_AR.get(q['bloom'], q['bloom'])}"))
    st.markdown(f"**السؤال {i}.** "
                + " · ".join(f":{colour}-badge[{text}]" for colour, text in tags))
    if q.get("scenario"):
        with st.container(key=f"card-case-quiz-{q['id']}"):
            st.markdown(f":material/cases: **سيناريو**  \n{q['scenario']}")
    st.markdown(q["prompt"])


def _input(q: dict, key: str):
    opts = _options(q)
    idx = list(range(len(opts)))
    if q["type"] == "multi":
        st.caption("اختر كل الإجابات الصحيحة.")
        return [j for j in idx if st.checkbox(opts[j], key=f"{key}-{j}")]
    return st.radio("الإجابة", idx, format_func=lambda j: opts[j], index=None,
                    key=key, label_visibility="collapsed")


def _feedback(q: dict, response, ok: bool) -> None:
    opts = _options(q)
    correct = ", ".join(opts[j] for j in sorted(_correct_set(q)))
    if ok:
        st.success(f"إجابة صحيحة. {q.get('explanation', '')}", icon=":material/check_circle:")
    else:
        st.error(f"الإجابة الصحيحة: **{correct}**. {q.get('explanation', '')}",
                 icon=":material/cancel:")
        chosen = response if isinstance(response, list) else ([] if response is None else [response])
        why = q.get("why_wrong") or {}
        for j in chosen:
            if j in why or str(j) in why:
                st.markdown(f"- لماذا «{opts[j]}» غير صحيح؟ {why.get(j, why.get(str(j)))}")
        if q.get("review"):
            link_to_lecture(q["review"], label="راجع المحاضرة المرتبطة", icon=":material/replay:")


def answer_key(questions: list[dict]) -> None:
    """Instructor-only key: correct answer, explanation, distractor notes, Bloom level."""
    with st.expander("مفتاح الإجابة (للأستاذ)", icon=":material/key:"):
        for i, q in enumerate(questions, 1):
            opts = _options(q)
            correct = "؛ ".join(opts[j] for j in sorted(_correct_set(q)))
            bloom = BLOOM_AR.get(q.get("bloom", ""), "")
            st.markdown(f"**{i}. {q['prompt']}**  \n✅ {correct}"
                        + (f"  \n:gray[مستوى بلوم: {bloom}]" if bloom else "")
                        + f"  \n{q.get('explanation', '')}")
            for j, txt in (q.get("why_wrong") or {}).items():
                st.markdown(f"  - ✗ {opts[int(j)]}: {txt}")


def run_quiz(quiz_id: str, questions: list[dict], *, title: str = "",
             diagnostic: bool = False, topic_labels: dict[str, str] | None = None) -> None:
    """Render a quiz in a form; grade on submit; keep the best score in session state."""
    if not questions:
        return
    if is_instructor():
        answer_key(questions)
    submitted_key = f"{quiz_id}-submitted"
    with st.form(key=f"form-{quiz_id}", border=True):
        if title:
            st.markdown(f"### {title}")
        responses = {}
        for i, q in enumerate(questions, 1):
            with st.container(key=f"q-{quiz_id}-{i}"):
                _question_header(i, q)
                responses[q["id"]] = _input(q, f"{quiz_id}-{q['id']}")
            st.divider()
        c1, c2 = st.columns([1, 1])
        submit = c1.form_submit_button("صحّح إجاباتي", icon=":material/task_alt:", type="primary")
        if submit:
            st.session_state[submitted_key] = True
    if not st.session_state.get(submitted_key):
        return

    score = sum(_is_correct(q, responses[q["id"]]) for q in questions)
    total = len(questions)
    record_quiz(quiz_id, score, total)
    missed = []
    for q in questions:
        if not _is_correct(q, responses[q["id"]]) and q.get("review") and q["review"] not in missed:
            missed.append(q["review"])
    st.session_state.setdefault("quiz_missed", {})[quiz_id] = missed
    pct = round(100 * score / total)
    st.metric("النتيجة", f"{score} / {total}", f"{pct}%", delta_color="off")
    if diagnostic:
        _diagnostic_profile(questions, responses, topic_labels or {})
    else:
        if pct >= 80:
            st.success("تمكّن جيد من محتوى هذا المحور. انتقل إلى المحور التالي أو إلى الأنشطة المتقدمة.")
        elif pct >= 50:
            st.warning("فهم جزئي. راجع الأسئلة الخاطئة والمحاضرات المقترحة أدناه ثم أعد المحاولة.")
        else:
            st.error("يلزم مراجعة المحور. ابدأ بملخصات المحاضرات ثم أعد الاختبار.")
    with st.expander("التغذية الراجعة التفصيلية", expanded=True, icon=":material/feedback:"):
        for i, q in enumerate(questions, 1):
            st.markdown(f"**{i}. {q['prompt']}**")
            _feedback(q, responses[q["id"]], _is_correct(q, responses[q["id"]]))


def _diagnostic_profile(questions, responses, topic_labels) -> None:
    by_topic: dict[str, list[bool]] = defaultdict(list)
    for q in questions:
        by_topic[q.get("topic", "general")].append(_is_correct(q, responses[q["id"]]))
    st.markdown("#### الملف التشخيصي | Diagnostic profile")
    st.caption("الاختبار القبلي تشخيصي وليس عقابيًا: يحدد نقاط الانطلاق وما يحتاج إلى عناية أكبر.")
    rows = []
    for topic, marks in by_topic.items():
        rate = sum(marks) / len(marks)
        level = "متمكن" if rate >= 0.75 else "جزئي" if rate >= 0.4 else "يحتاج تأسيسًا"
        rows.append({"المجال": topic_labels.get(topic, topic),
                     "صحيحة": f"{sum(marks)}/{len(marks)}", "المستوى": level,
                     "نسبة": rate})
    st.dataframe(rows, hide_index=True, column_config={
        "نسبة": st.column_config.ProgressColumn("نسبة الإتقان", min_value=0.0, max_value=1.0, format="percent"),
    })
