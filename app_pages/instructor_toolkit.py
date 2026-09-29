import streamlit as st

from components.layout import breadcrumbs, footer, page_header
from components.quiz import answer_key
from utils.content import format_reference, load_assessments, load_capstone, load_course, load_modules, load_references
from utils.nav import link_to_lecture, page
from utils.state import is_instructor

breadcrumbs("المقرر", "أدوات الأستاذ")
page_header("أدوات الأستاذ", "Instructor Toolkit",
            "كل ما يحتاجه الأستاذ لتدريس المقرر مجمّعًا من المحاور الثلاثة عشر: التسلسل والتوقيت، "
            "والأخطاء الشائعة، وأسئلة النقاش، والأنشطة، وبنك التقييم، والحالات الدراسية، وسلالم التقييم.")

if not is_instructor():
    st.warning("هذه الصفحة موجهة إلى الأستاذ. فعّل «وضع الأستاذ» من القائمة الجانبية لعرض مفاتيح الإجابة "
               "وملاحظات التدريس كاملة.", icon=":material/lock:")

# This page serves the lecture hour; the TD guide serves the tutorial hour. They are used
# by the same person, so each points at the other.
with st.container(border=True, key="toolkit-td-link"):
    st.markdown(
        "**تشرف على حصص الأعمال الموجّهة (TD)؟** هناك دليل مستقل لها: بنك من 65 موضوع بحث "
        "قصير مرتبط بمحاور المقرر، وصيغ نشاط بديلة عن العرض التقليدي، وسلّم تقييم جاهز."
    )
    st.page_link(page("td"), label="افتح دليل حصص الأعمال الموجّهة", icon=":material/groups:")

course = load_course()
mods = load_modules()


def blocks_of(kind: str):
    for m in mods:
        for lec in m.lectures:
            for b in lec.blocks(kind):
                yield m, lec, b


tabs = st.tabs(["المخرجات والخريطة", "التسلسل والتوقيت", "الأخطاء الشائعة", "أسئلة النقاش",
                "الأنشطة الصفية", "بنك التقييم", "الحالات الدراسية", "سلالم المشروع",
                "ملاحظات التدريس", "القراءات والعلاج"])

with tabs[0]:
    st.markdown("##### الأهداف العامة (البطاقة الرسمية)")
    for i, o in enumerate(course["syllabus"]["general_objectives"], 1):
        st.markdown(f"{i}. {o}")
    st.markdown("##### مخرجات التعلم")
    for o in course["learning_outcomes"]:
        st.markdown(f"- {o}")
    st.page_link(page("map"), label="خريطة المقرر والخطة الفصلية", icon=":material/hub:")

with tabs[1]:
    for m in mods:
        ins = m.meta.get("instructor", {})
        with st.expander(f"المحور {m.number}: {m.title} — {m.meta.get('estimated_duration', '')}"):
            st.markdown("**التسلسل المقترح**")
            for x in ins.get("sequence", []):
                st.markdown(f"- {x}")
            st.markdown("**التوقيت المقترح**")
            for x in ins.get("timing", []):
                st.markdown(f"- {x}")

with tabs[2]:
    for m in mods:
        items = m.meta.get("exit", {}).get("common_mistakes", [])
        mis = list(blocks_of("misconception"))
        with st.expander(f"المحور {m.number}: {m.title}"):
            for x in items:
                st.markdown(f"- {x}")
            for mm, lec, b in mis:
                if mm.number == m.number:
                    st.markdown(f"- **{b.title}** (المحاضرة {m.number}.{lec.number})")

with tabs[3]:
    for m in mods:
        with st.expander(f"المحور {m.number}: {m.title}"):
            for x in m.meta.get("instructor", {}).get("discussion", []):
                st.markdown(f"- {x}")
            for mm, lec, b in blocks_of("discussion"):
                if mm.number == m.number:
                    st.markdown(f"- {b.title or b.text.splitlines()[0]} · :gray[{m.number}.{lec.number}]")

with tabs[4]:
    acts = list(blocks_of("activity"))
    st.caption(f"{len(acts)} نشاطًا صفيًا")
    for m, lec, b in acts:
        with st.expander(f"{m.number}.{lec.number} · {b.title}"):
            st.markdown(b.text)

with tabs[5]:
    if is_instructor():
        a = load_assessments()
        st.markdown("##### الاختبار القبلي العام")
        answer_key(a["pretest"]["questions"])
        st.markdown("##### الاختبار البعدي العام")
        answer_key(a["posttest"]["questions"])
        for m in mods:
            st.markdown(f"##### المحور {m.number}: اختبار الدخول والاختبار البعدي")
            answer_key(m.entry_quiz + m.quiz)
        for m in mods:
            ideas = m.meta.get("instructor", {}).get("assessment_ideas", [])
            if ideas:
                with st.expander(f"أفكار تقييم إضافية · المحور {m.number}"):
                    for x in ideas:
                        st.markdown(f"- {x}")
    else:
        st.info("بنك التقييم ومفاتيح الإجابة متاحة في وضع الأستاذ فقط.")

with tabs[6]:
    cases = list(blocks_of("case"))
    st.caption(f"{len(cases)} حالة دراسية")
    for m, lec, b in cases:
        with st.expander(f"{m.number}.{lec.number} · {b.title}"):
            st.markdown(b.text)
            link_to_lecture(lec.id, label="في سياق المحاضرة")

with tabs[7]:
    cap = load_capstone()
    st.dataframe([{"المعيار": r["criterion"], "الوزن": r["weight"], "ممتاز": r["levels"][0],
                   "جيد": r["levels"][1], "مقبول": r["levels"][2], "غير كافٍ": r["levels"][3]}
                  for r in cap["rubric"]], hide_index=True)
    st.page_link(page("capstone"), label="تفاصيل المسارات الستة", icon=":material/rocket_launch:")

with tabs[8]:
    if is_instructor():
        for m in mods:
            notes = [(lec, b) for mm, lec, b in blocks_of("instructor") if mm.number == m.number]
            with st.expander(f"المحور {m.number}: {len(notes)} ملاحظة"):
                for lec, b in notes:
                    st.markdown(f"**{m.number}.{lec.number} · {b.title}**")
                    st.markdown(b.text)
    else:
        st.info("ملاحظات التدريس متاحة في وضع الأستاذ فقط.")

with tabs[9]:
    refs = load_references()
    for m in mods:
        ex = m.meta.get("exit", {})
        with st.expander(f"المحور {m.number}: {m.title}"):
            st.markdown("**أنشطة علاجية**")
            for x in ex.get("remediation", []):
                st.markdown(f"- {x}")
            st.markdown("**قراءات مقترحة**")
            for rid in ex.get("suggested_reading", []):
                if rid in refs:
                    st.markdown(f"- {format_reference(refs[rid])}")
footer()
