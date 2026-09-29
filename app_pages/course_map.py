import streamlit as st

from components.diagrams import render as render_diagram
from components.diagrams.course import CHAIN, MODULE_EDGES
from components.layout import breadcrumbs, footer, page_header
from utils.content import load_modules
from utils.nav import link_to_module

breadcrumbs("المقرر", "خريطة المقرر")
page_header("خريطة المقرر", "Course map",
            "تسلسل المفاهيم من الأسس إلى الرقابة البشرية. كل حلقة تبني على ما قبلها، "
            "ولكل حلقة محور أو أكثر في المنصة.")

render_diagram("course_map")
mods = {m.number: m for m in load_modules()}

st.subheader("الحلقات والمحاور المقابلة")
for i, (ar, en, nums) in enumerate(CHAIN, 1):
    if not any(n in mods for n in nums):
        continue
    with st.container(border=True, key=f"chain-{i}"):
        st.markdown(f"**{i}. {ar}** · <span class='term-en'>{en}</span>", unsafe_allow_html=True)
        with st.container(horizontal=True):
            for n in nums:
                if n in mods:
                    link_to_module(n)

st.subheader("المتطلبات بين المحاور")
st.caption("قراءة الجدول: المحور في العمود الأول شرط مسبق لفهم المحور في العمود الثاني.")
rows = [{"يُدرس قبل": f"{a}. {mods[a].title}", "لفهم": f"{b}. {mods[b].title}"}
        for a, b in MODULE_EDGES if a in mods and b in mods]
st.dataframe(rows, hide_index=True)

st.subheader("خطة فصلية مقترحة (14 أسبوعًا)")
plan = [
    ("1", "الاختبار القبلي + المحور 1"), ("2", "المحور 2"), ("3", "المحور 3"), ("4", "المحور 4 (1)"),
    ("5", "المحور 4 (2) + إطلاق المشروع الختامي"), ("6", "المحور 7"), ("7", "المحور 5"),
    ("8", "المحور 6"), ("9", "المحور 8"), ("10", "المحور 9"), ("11", "المحور 10"),
    ("12", "المحور 11"), ("13", "المحوران 12 و13"), ("14", "الاختبار البعدي + عرض المشاريع"),
]
st.table({"الأسبوع": [p[0] for p in plan], "المحتوى": [p[1] for p in plan]})
st.caption("يُدرَّس المحور 7 (النماذج اللغوية) قبل المحورين 5 و6 في هذه الخطة لأن هندسة الأوامر "
           "تُفهم أعمق بعد فهم آلية التنبؤ بالرمز التالي. ويمكن للأستاذ اتباع الترتيب الرسمي للمحاور "
           "مع تقديم المحاضرة 7.1 مدخلًا مختصرًا قبل المحور 5.")
footer()
