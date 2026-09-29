import streamlit as st

from components.layout import breadcrumbs, footer, page_header
from components.quiz import run_quiz
from utils.content import load_assessments
from utils.nav import module_page

a = load_assessments()["pretest"]
breadcrumbs("المقرر", "نظام الدخول", "الاختبار القبلي")
page_header("الاختبار القبلي العام", "Diagnostic pre-test", a["intro"])

with st.container(key="card-key-pretest"):
    st.markdown(":material/info: **كيف تُستخدم نتيجة هذا الاختبار؟**")
    for line in a["how_to_use"]:
        st.markdown(f"- {line}")

run_quiz("pretest", a["questions"], diagnostic=True, topic_labels=a["topics"])

if st.session_state.get("pretest-submitted"):
    st.page_link(module_page(1), label="ابدأ المقرر من المحور 1", icon=":material/play_circle:")
footer()
