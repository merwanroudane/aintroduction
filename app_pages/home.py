import streamlit as st

from components.diagrams import render as render_diagram
from components.layout import FALLBACK_COLOR, MODULE_COLORS, esc, footer
from utils.content import load_course, load_modules
from utils.nav import MODULE_ICONS, lecture_key, module_page, page
from utils.state import is_instructor

c = load_course()
syl = c["syllabus"]
modules = load_modules()
done = st.session_state.completed

st.html(
    f"""<div class="hero">
    <h1>{esc(c['title'])}</h1>
    <h2>{esc(c['title_en'])}</h2>
    <div class="subtitle">{esc(c['subtitle'])}</div>
    <div class="subtitle" style="font-size:1rem;color:#7D6E68">{esc(c['tagline'])}</div>
    <div class="author">إعداد وتصميم: {esc(c['author_ar'])} · <span>{esc(c['author_en'])}</span></div>
    </div>"""
)

total_lec = sum(len(m.lectures) for m in modules)
quizzes_done = sum(1 for k in st.session_state.quiz_scores if k.startswith("quiz-"))
with st.container(horizontal=True, key="home-kpis"):
    st.metric("المحاور", len(modules), border=True)
    st.metric("المحاضرات", total_lec, border=True)
    st.metric("محاضرات مكتملة", f"{len(done)} / {total_lec}", border=True)
    st.metric("اختبارات بعدية أُنجزت", f"{quizzes_done} / {len(modules)}", border=True)

with st.container(horizontal=True, key="home-actions"):
    st.page_link(page("pretest"), label="ابدأ بالاختبار القبلي", icon=":material/play_circle:")
    st.page_link(module_page(1), label="ابدأ المقرر: المحور 1", icon=":material/school:")
    st.page_link(page("search"), label="البحث", icon=":material/search:")
    st.page_link(page("glossary"), label="القاموس", icon=":material/translate:")
    st.page_link(page("posttest"), label="الاختبار البعدي", icon=":material/assignment_turned_in:")
    st.page_link(page("references"), label="المراجع", icon=":material/library_books:")

st.header("وصف المقرر")
st.markdown(c["description"])

st.header("البطاقة الرسمية للمقرر")
st.caption("مطابقة لبطاقة المادة التعليمية المعتمدة. الأهداف والمحاور أدناه منقولة بنصها.")
t_obj, t_axes, t_comp, t_struct, t_sys, t_needs = st.tabs(
    ["الهدف العام", "محاور المادة", "الكفاءات المستهدفة", "الهيكل التنظيمي",
     "نظام الدخول والتعلم والخروج", "تحليل الاحتياجات"]
)
with t_obj:
    st.markdown(f"**{syl['general_objectives_intro']}**")
    for i, o in enumerate(syl["general_objectives"], 1):
        st.markdown(f"{i}. {o}")
    st.markdown("##### الكلمات المفتاحية للمادة التعليمية")
    st.html("<div>" + "".join(f'<span class="pill">{esc(k)}</span>' for k in syl["keywords"]) + "</div>")
    with st.expander("توسيع الأهداف وفق تصنيف بلوم | Bloom's Taxonomy", icon=":material/stairs:"):
        names = {"remember": "تذكّر", "understand": "فهم", "apply": "تطبيق",
                 "analyze": "تحليل", "evaluate": "تقييم", "create": "إبداع"}
        for level, items in c["bloom_objectives"].items():
            st.markdown(f"**{names[level]}** · <span class='term-en'>{level.capitalize()}</span>",
                        unsafe_allow_html=True)
            for it in items:
                st.markdown(f"- {it}")
with t_axes:
    for i, axis in enumerate(syl["axes"], 1):
        st.markdown(f"{i}. {axis}")
with t_comp:
    st.info(syl["competencies_note"], icon=":material/info:")
    for comp in syl["competencies"]:
        st.markdown(f"- {comp}")
with t_struct:
    rows = syl["structure"]["rows"]
    st.markdown(f"**{syl['structure']['title']}**")
    st.table({"العنصر": [r["item"] for r in rows], "المحتوى": [r["detail"] for r in rows]})
    st.caption("في المنصة: لكل محور بطاقة مفاهيمية ذهنية في صفحة الدخول، وموارد متنوعة داخل المحاضرات "
               "(صور ومخططات وجداول ومعادلات وروابط لفيديوهات توضيحية مُتحقق منها).")
with t_sys:
    for block in ("entry_system", "learning_system", "exit_system"):
        b = syl[block]
        st.markdown(f"**{b['title']}**")
        st.table({"العنصر": [r["item"] for r in b["rows"]], "التفصيل": [r["detail"] or "—" for r in b["rows"]]})
with t_needs:
    st.markdown(syl["needs_analysis"])

st.header("خريطة المقرر | Course map")
render_diagram("course_map")

st.header("محاور المقرر الثلاثة عشر")
cols = st.columns(3, gap="medium")
for i, m in enumerate(modules):
    colour = MODULE_COLORS.get(m.number, FALLBACK_COLOR)
    n_done = sum(lec.id in done for lec in m.lectures)
    with cols[i % 3]:
        with st.container(key=f"modcard-{m.number}"):
            st.html(
                f'<div style="--mod-accent:{colour.accent}"><span class="modnum">{m.number}</span>'
                f'<b style="font-size:1.05rem">{esc(m.title)}</b></div>'
                f'<div class="term-en" style="font-size:0.88rem;margin:0.2rem 0">{esc(m.meta.get("title_en", ""))}</div>'
                f'<div style="font-size:0.9rem;color:#6B5A55;line-height:1.7">{esc(m.meta.get("subtitle", ""))}</div>'
            )
            st.progress(n_done / max(len(m.lectures), 1),
                        text=f"{len(m.lectures)} محاضرات · {n_done} مكتملة")
            st.page_link(module_page(m.number), label="ادخل المحور", icon=MODULE_ICONS[m.number])
        st.html(f"<style>.st-key-modcard-{m.number}{{--mod-accent:{colour.accent};--mod-bg:{colour.tint};--mod-deep:{colour.deep}}}</style>")

st.header("مسار التعلم | Learning journey")
render_diagram("learning_journey")

st.header("مخرجات التعلم")
for o in c["learning_outcomes"]:
    st.markdown(f"- {o}")

st.header("وضعا الاستخدام")
c1, c2 = st.columns(2, gap="large")
with c1:
    with st.container(key="card-key-learner"):
        st.markdown("**:material/person: وضع الطالب | Learner Mode**")
        st.markdown("يعرض المحتوى التعليمي والتمارين والاختبارات مع تغذية راجعة بعد الإجابة، "
                    "دون مفاتيح الإجابة الكاملة وملاحظات الأستاذ.")
with c2:
    with st.container(key="card-instructor-mode"):
        st.markdown("**:material/school: وضع الأستاذ | Instructor Mode**")
        st.markdown("يضيف ملاحظات التدريس، وتسلسلًا وتوقيتًا مقترحين لكل محور، وأسئلة النقاش، "
                    "ومفاتيح الإجابة، وأفكار التقييم، والأنشطة العلاجية. غيّر الوضع من القائمة الجانبية.")
if is_instructor():
    st.page_link(page("toolkit"), label="افتح أدوات الأستاذ", icon=":material/school:")

footer()
