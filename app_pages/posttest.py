import streamlit as st

from components.layout import breadcrumbs, footer, page_header
from components.quiz import run_quiz
from utils.content import load_assessments
from utils.nav import page

a = load_assessments()
post = a["posttest"]
breadcrumbs("المقرر", "التطبيق والتقييم", "الاختبار البعدي")
page_header("الاختبار البعدي العام", "Final post-test", post["intro"])

pre = st.session_state.quiz_scores.get("pretest")
if pre:
    st.caption(f"نتيجتك في الاختبار القبلي: {pre[0]}/{pre[1]}. قارنها بنتيجتك هنا لقياس التقدم.")

run_quiz("posttest", post["questions"], diagnostic=True, topic_labels=a["pretest"]["topics"])

post_score = st.session_state.quiz_scores.get("posttest")
if post_score and pre:
    gain = post_score[0] / post_score[1] - pre[0] / pre[1]
    st.metric("التقدم بين الاختبارين (بالنقاط المئوية)", f"{gain * 100:+.0f}")
if st.session_state.get("posttest-submitted"):
    st.page_link(page("capstone"), label="انتقل إلى المشروع العملي الختامي", icon=":material/rocket_launch:")
footer()
