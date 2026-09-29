"""Generic module page: Entry system (overview) → lectures → quiz → Exit system.

The open view is a pills widget bound to the URL (``?lec07=m07-l03``) so search
results, cross-links and the browser back button all land on the right lecture.
"""

from __future__ import annotations

import re

import streamlit as st

from components.diagrams import render as render_diagram
from components.layout import FALLBACK_COLOR, MODULE_COLORS, breadcrumbs, esc, footer
from components.quiz import BLOOM_AR, BLOOM_COLOR, run_quiz
from components.render import card, lecture_references, render_lecture_body
from utils.content import Lecture, Module, get_module, load_references, format_reference
from utils.nav import link_to_lecture, link_to_module, lecture_key
from utils.state import is_instructor, mark_visited, toggle_complete

OVERVIEW, QUIZ, EXIT = "overview", "quiz", "exit"
LECTURE_ID = re.compile(r"^m\d{2}-l\d{2}$")


def _set_view(key: str, value: str) -> None:
    st.session_state[key] = value


def _module_banner(m: Module) -> None:
    colour = MODULE_COLORS.get(m.number, FALLBACK_COLOR)
    meta = m.meta
    pills = "".join(f'<span class="pill">{esc(k)}</span>' for k in meta.get("keywords", [])[:10])
    st.html(
        f'<div class="modbanner" style="--mod-accent:{colour.accent};--mod-bg:{colour.tint};--mod-deep:{colour.deep}">'
        f'<div class="modbanner-num">المحور {m.number}</div>'
        f'<h1>{esc(m.title)}</h1>'
        f'<div class="term-en modbanner-en">{esc(meta.get("title_en", ""))}</div>'
        f'<p class="lead">{esc(meta.get("subtitle", ""))}</p>'
        f'<div class="modbanner-meta"><span>⏱ {esc(meta.get("estimated_duration", ""))}</span>'
        f'<span>📚 {len(m.lectures)} محاضرات</span><span>📈 {esc(meta.get("difficulty", ""))}</span></div>'
        f"<div>{pills}</div></div>"
    )


def _progress_line(m: Module) -> None:
    done = st.session_state.completed
    n_done = sum(lec.id in done for lec in m.lectures)
    st.progress(n_done / max(len(m.lectures), 1),
                text=f"تقدمك في هذا المحور: {n_done} من {len(m.lectures)} محاضرات مكتملة")


# ------------------------------------------------------------------ overview

def _overview(m: Module, key: str) -> None:
    meta = m.meta
    st.markdown(meta.get("description", ""))
    if meta.get("concept_diagram"):
        st.subheader("البطاقة المفاهيمية الذهنية | Carte conceptuelle")
        st.caption("الخارطة الذهنية المعرفية لهذا المحور: المفاهيم الرئيسة والعلاقات بينها.")
        render_diagram(meta["concept_diagram"])

    st.subheader("نظام الدخول | Le système d'entrée")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("##### أهداف التعلم (وفق تصنيف بلوم)")
        for obj in meta.get("objectives", []):
            if isinstance(obj, dict):
                st.markdown(f"- :{BLOOM_COLOR.get(obj['bloom'], 'gray')}-badge"
                            f"[{BLOOM_AR.get(obj['bloom'], obj['bloom'])}] {obj['text']}")
            else:
                st.markdown(f"- {obj}")
    with c2:
        st.markdown("##### المتطلبات والمكتسبات القبلية")
        for p in meta.get("prerequisites", []):
            st.markdown(f"- {p}")
        entry = meta.get("entry", {})
        for p in entry.get("prior_knowledge", []):
            st.markdown(f"- {p}")
    diag = meta.get("entry", {}).get("diagnostic_questions", [])
    if diag:
        with st.container(key="card-discussion-diag"):
            st.markdown(":material/help: **أسئلة تشخيصية قبل البدء** · <span class='term-en'>Diagnostic questions</span>",
                        unsafe_allow_html=True)
            for q in diag:
                st.markdown(f"- {q}")
            st.caption("لا تبحث عن الإجابة الآن: دوّن إجابتك الأولى، وستعود إليها في نظام الخروج.")

    if m.entry_quiz:
        st.markdown("##### اختبار الدخول (Test d'entrée): المكتسبات القبلية")
        st.caption("اختبار قصير يربط ما تعرفه مسبقًا بمحتوى هذا المحور. التغذية الراجعة فورية، "
                   "ولا تُحتسب نتيجته في التقييم: هدفه توجيهك إلى ما يجب مراجعته قبل البدء.")
        run_quiz(f"entry-{m.id}", m.entry_quiz)

    st.subheader("نظام التعلم: محاضرات المحور | Système d'apprentissage")
    st.caption("كل محاضرة تجمع ثلاث طبقات: المعرفة (savoir)، والتعلم الذاتي (auto-apprentissage)، "
               "والتطبيق (savoir-faire) عبر تمرين الدرس والأنشطة.")
    done = st.session_state.completed
    for lec in m.lectures:
        with st.container(border=True, key=f"leccard-{lec.id}"):
            c1, c2 = st.columns([5, 1.4], vertical_alignment="center")
            with c1:
                status = " :green-badge[مكتملة]" if lec.id in done else ""
                st.markdown(f"**المحاضرة {m.number}.{lec.number} — {lec.title}**{status}  \n"
                            f"<span class='term-en'>{esc(lec.meta.get('title_en', ''))}</span>",
                            unsafe_allow_html=True)
                if lec.subtitle:
                    st.caption(lec.subtitle)
            with c2:
                st.button("افتح المحاضرة", key=f"open-{lec.id}", icon=":material/arrow_back:",
                          on_click=_set_view, args=(key, lec.id), width="stretch")

    if is_instructor():
        _instructor_panel(m)


def _instructor_panel(m: Module) -> None:
    ins = m.meta.get("instructor", {})
    if not ins:
        return
    st.subheader("لوحة الأستاذ | Instructor panel")
    with st.container(key="card-instructor-panel"):
        tabs = st.tabs(["تسلسل التدريس", "التوقيت", "أسئلة النقاش", "أفكار التقييم", "توسعات متقدمة"])
        fields = ["sequence", "timing", "discussion", "assessment_ideas", "extensions"]
        for tab, field in zip(tabs, fields):
            with tab:
                items = ins.get(field, [])
                if not items:
                    st.caption("لا توجد عناصر إضافية لهذا الجانب في هذا المحور.")
                for it in items:
                    st.markdown(f"- {it}")


# ------------------------------------------------------------------ lecture

def _lecture(m: Module, lec: Lecture, key: str) -> None:
    mark_visited(lec.id)
    meta = lec.meta
    colour = MODULE_COLORS.get(m.number, FALLBACK_COLOR)
    st.html(
        f'<div class="lechead" style="--mod-accent:{colour.accent};--mod-bg:{colour.tint};--mod-deep:{colour.deep}">'
        f'<div class="lechead-num">المحاضرة {m.number}.{lec.number}</div>'
        f"<h1>{esc(lec.title)}</h1>"
        f'<div class="term-en">{esc(meta.get("title_en", ""))}</div>'
        + (f'<p class="lead">{esc(lec.subtitle)}</p>' if lec.subtitle else "")
        + '<div class="modbanner-meta">'
        + (f'<span>⏱ {esc(meta["duration"])} دقيقة</span>' if meta.get("duration") else "")
        + (f'<span>📈 {esc(meta["difficulty"])}</span>' if meta.get("difficulty") else "")
        + "</div></div>"
    )

    c1, c2 = st.columns(2, gap="large")
    with c1:
        if meta.get("objectives"):
            st.markdown("##### أهداف المحاضرة")
            for o in meta["objectives"]:
                st.markdown(f"- {o}")
    with c2:
        if meta.get("prerequisites"):
            st.markdown("##### قبل أن تبدأ")
            for p in meta["prerequisites"]:
                st.markdown(f"- {p}")

    if meta.get("builds_on"):
        with st.container(key="card-crosslink-buildson"):
            st.markdown(":material/foundation: **نبني على ما سبق** · <span class='term-en'>Prior knowledge</span>",
                        unsafe_allow_html=True)
            for b in meta["builds_on"]:
                if isinstance(b, str) and LECTURE_ID.match(b):
                    link_to_lecture(b)
                else:
                    st.markdown(f"- {b}")

    st.html(
        '<div class="layers"><span class="layer l1"><b>المعرفة</b> savoir</span>'
        '<span class="layer l2"><b>التعلم الذاتي</b> auto-apprentissage</span>'
        '<span class="layer l3"><b>التطبيق</b> savoir-faire</span></div>'
    )

    heads = lec.headings
    if heads:
        with st.expander("فهرس المحاضرة | Table of contents", icon=":material/toc:"):
            for h in heads:
                st.markdown(f"- [{h.text}](#{h.anchor})")

    render_lecture_body(lec)

    if meta.get("summary"):
        card("recap", "خلاصة المحاضرة", "\n".join(f"- {s}" for s in meta["summary"]))

    _self_study(lec)

    related = meta.get("related", [])
    if related:
        st.markdown("##### مفاهيم ومحاضرات مرتبطة | Related")
        with st.container(horizontal=True, key=f"rel-{lec.id}"):
            for rid in related:
                link_to_lecture(rid)

    lecture_references(lec)

    st.divider()
    done = lec.id in st.session_state.completed
    ids = [x.id for x in m.lectures]
    i = ids.index(lec.id)
    with st.container(horizontal=True, horizontal_alignment="distribute", key=f"lecnav-{lec.id}"):
        if i > 0:
            st.button("المحاضرة السابقة", icon=":material/arrow_forward:", key=f"prev-{lec.id}",
                      on_click=_set_view, args=(key, ids[i - 1]))
        else:
            st.button("نظرة عامة على المحور", icon=":material/arrow_forward:", key=f"prev-{lec.id}",
                      on_click=_set_view, args=(key, OVERVIEW))
        st.button("إلغاء الإكمال" if done else "تم إكمال المحاضرة",
                  icon=":material/undo:" if done else ":material/check_circle:",
                  type="secondary" if done else "primary", key=f"done-{lec.id}",
                  on_click=toggle_complete, args=(lec.id,))
        if i < len(ids) - 1:
            st.button("المحاضرة التالية", icon=":material/arrow_back:", key=f"next-{lec.id}",
                      on_click=_set_view, args=(key, ids[i + 1]))
        else:
            st.button("الاختبار البعدي للمحور", icon=":material/quiz:", key=f"next-{lec.id}",
                      on_click=_set_view, args=(key, QUIZ))


RES_ICONS = {"video": ":material/smart_display:", "reading": ":material/menu_book:",
             "doc": ":material/description:", "course": ":material/school:",
             "tool": ":material/build:", "dataset": ":material/dataset:"}
RES_AR = {"video": "فيديو توضيحي", "reading": "قراءة", "doc": "وثيقة رسمية", "course": "مقرر مفتوح",
          "tool": "أداة", "dataset": "بيانات"}
# One colour per kind of resource, so the mix in a lecture is legible at a glance.
RES_COLOR = {"video": "red", "reading": "blue", "doc": "violet", "course": "green",
             "tool": "orange", "dataset": "gray"}


def _self_study(lec: Lecture) -> None:
    items = lec.meta.get("self_study", [])
    if not items:
        return
    st.subheader("التعلم الذاتي | Auto-apprentissage")
    st.caption("موارد مختارة للتعمق خارج القاعة. الروابط خارجية ومُتحقق منها في التاريخ المذكور.")
    for j, it in enumerate(items):
        kind = it.get("type", "reading")
        with st.container(border=True, key=f"res-{lec.id}-{j}"):
            st.markdown(f"{RES_ICONS.get(kind, ':material/link:')} "
                        f":{RES_COLOR.get(kind, 'gray')}-badge[{RES_AR.get(kind, kind)}] "
                        f"**{it['title']}**  \n"
                        f"<span class='term-en'>{esc(it.get('source', ''))}</span>",
                        unsafe_allow_html=True)
            if it.get("why"):
                st.markdown(it["why"])
            st.markdown(f"[{it['url']}]({it['url']})"
                        + (f"  \n:gray[تم التحقق: {it['verified']}]" if it.get("verified") else ""))


# ------------------------------------------------------------------ quiz + exit

def _quiz(m: Module, key: str) -> None:
    st.subheader(f"الاختبار البعدي للمحور {m.number} | Post-test")
    st.caption("اختبار تقييمي (post-test) بمستويات مختلفة من تصنيف بلوم. تظهر التغذية الراجعة بعد التصحيح، "
               "مع رابط إلى المحاضرة التي ينبغي مراجعتها عند الخطأ.")
    run_quiz(f"quiz-{m.id}", m.quiz)
    st.button("الانتقال إلى نظام الخروج", icon=":material/logout:", key=f"toexit-{m.id}",
              on_click=_set_view, args=(key, EXIT))


def _exit(m: Module) -> None:
    ex = m.meta.get("exit", {})
    st.subheader("نظام الخروج | Système de sortie")
    score = st.session_state.quiz_scores.get(f"quiz-{m.id}")
    if score is None:
        st.info("لم تُجرِ الاختبار البعدي لهذا المحور بعد. نتيجته تحدد هل تنتقل إلى المحور التالي "
                "أم تبدأ بالأنشطة التدعيمية.", icon=":material/info:")
    else:
        pct = score[0] / max(score[1], 1)
        if pct >= 0.7:
            st.success(f"نتيجة الاختبار البعدي: {score[0]}/{score[1]}. الكفايات المستهدفة متحققة في معظمها.",
                       icon=":material/verified:")
        else:
            st.warning(f"نتيجة الاختبار البعدي: {score[0]}/{score[1]}. ابدأ بالأنشطة التدعيمية أدناه ثم أعد الاختبار.",
                       icon=":material/healing:")
        missed = st.session_state.get("quiz_missed", {}).get(f"quiz-{m.id}", [])
        if missed:
            st.markdown("**محاضرات ينبغي مراجعتها بناءً على إجاباتك:**")
            for rid in missed:
                link_to_lecture(rid, icon=":material/replay:")

    st.markdown("##### تقييم الكفاءات المستهدفة حسب الأهداف المسطرة")
    objs = [o["text"] if isinstance(o, dict) else o for o in m.meta.get("objectives", [])]
    if objs:
        st.caption("قيّم نفسك بصدق مقابل كل هدف من أهداف المحور.")
        levels = ["لم يتحقق", "جزئيًا", "متحقق"]
        for j, o in enumerate(objs):
            st.segmented_control(o, levels, key=f"selfeval-{m.id}-{j}")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("##### الكفايات: هل أستطيع…؟")
        for ci, comp in enumerate(ex.get("competencies", [])):
            st.checkbox(comp, key=f"comp-{m.id}-{ci}")
    with c2:
        st.markdown("##### أخطاء شائعة ينبغي تجنبها")
        for mis in ex.get("common_mistakes", []):
            st.markdown(f"- {mis}")
    if ex.get("assessment_activities"):
        st.markdown("##### أنشطة تقييمية مختلفة الطرح")
        for a in ex["assessment_activities"]:
            st.markdown(f"- {a}")
    if ex.get("remediation"):
        with st.container(key="card-warning-remed"):
            st.markdown(":material/healing: **أنشطة تدعيمية للطالب في حالة التعثر** · <span class='term-en'>Remédiation</span>",
                        unsafe_allow_html=True)
            for r in ex["remediation"]:
                st.markdown(f"- {r}")
    if ex.get("suggested_reading"):
        st.markdown("##### موارد لتعويض النقص وقراءات مقترحة")
        refs = load_references()
        for rid in ex["suggested_reading"]:
            if rid in refs:
                st.markdown(f"- {format_reference(refs[rid])}")
    if ex.get("bridge"):
        card("crosslink", "الجسر نحو المحور التالي", ex["bridge"])
        if m.number < 13:
            link_to_module(m.number + 1, label=f"انتقل إلى المحور {m.number + 1}")


# ------------------------------------------------------------------ entry point

def render_module(number: int) -> None:
    m = get_module(number)
    st.session_state.current_module = number
    key = lecture_key(number)
    options = [OVERVIEW] + [lec.id for lec in m.lectures] + [QUIZ, EXIT]
    labels = {OVERVIEW: "الدخول والبطاقة المفاهيمية", QUIZ: "الاختبار البعدي", EXIT: "نظام الخروج"}
    labels.update({lec.id: f"{m.number}.{lec.number} {lec.meta.get('short_title', lec.title)}" for lec in m.lectures})
    # URL ↔ view sync by lecture id. (bind="query-params" would store the formatted
    # Arabic label in the URL, which breaks id-based links from search and cross-links.)
    url_val = st.query_params.get(key)
    applied = f"_{key}_applied"
    if url_val in options and st.session_state.get(applied) != url_val:
        st.session_state[key] = url_val
        st.session_state[applied] = url_val
    if st.session_state.get(key) not in options:
        st.session_state[key] = OVERVIEW

    crumb_slot = st.container()
    _module_banner(m)
    _progress_line(m)
    view = st.pills("محتوى المحور", options, format_func=lambda o: labels[o], key=key,
                    required=True, label_visibility="collapsed", width="stretch") or OVERVIEW
    if st.query_params.get(key) != view:
        st.query_params[key] = view
        st.session_state[applied] = view
    crumbs = ["المقرر", f"المحور {m.number}: {m.title}"]
    if view != OVERVIEW:
        crumbs.append(labels[view])
    with crumb_slot:
        breadcrumbs(*crumbs)

    lec = next((x for x in m.lectures if x.id == view), None)
    if view == OVERVIEW:
        _overview(m, key)
    elif view == QUIZ:
        _quiz(m, key)
    elif view == EXIT:
        _exit(m)
    elif lec is not None:
        _lecture(m, lec, key)
    footer()
