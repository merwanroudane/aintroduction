"""مقدمة في الذكاء الاصطناعي — Introduction to Artificial Intelligence.

Entry point: ``streamlit run app.py``. Builds the right-hand navigation (the app
is RTL, so Streamlit's sidebar sits on the right), the Instructor/Learner mode
switch and the progress summary, then runs the selected page.
"""

import streamlit as st

from components.layout import inject_css
from utils.content import all_lectures, load_modules
from utils.nav import module_page, page
from utils.state import MODES, init_state

st.set_page_config(
    page_title="مقدمة في الذكاء الاصطناعي",
    page_icon=":material/psychology:",
    layout="wide",
    initial_sidebar_state="expanded",
)
init_state()
inject_css()

pages = {
    "": [page("home"), page("map")],
    "نظام الدخول": [page("pretest")],
    "محاور المقرر": [module_page(m.number) for m in load_modules()],
    "التطبيق والتقييم": [page("labs"), page("posttest"), page("capstone")],
    "الموارد": [page("glossary"), page("search"), page("references"), page("knowledge")],
    "للأستاذ": [page("toolkit"), page("td")],
    "المتابعة": [page("progress")],
}
current = st.navigation(pages, position="sidebar", expanded=True)

with st.sidebar:
    st.divider()
    st.segmented_control(
        "وضع الاستخدام", list(MODES), format_func=MODES.get, key="mode",
        required=True, width="stretch",
        help="وضع الأستاذ يُظهر ملاحظات التدريس ومفاتيح الإجابة وأفكار التقييم.",
    )
    total = len(all_lectures())
    done = len(st.session_state.completed)
    st.progress(done / max(total, 1), text=f"التقدم العام: {done} / {total} محاضرة")
    st.caption("إعداد وتصميم: الدكتور مروان رودان · Dr. Marwan Roudane")

current.run()
