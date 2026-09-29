import plotly.graph_objects as go
import streamlit as st

from components.diagrams import show
from components.layout import MODULE_COLORS, breadcrumbs, footer, page_header
from utils.content import load_modules
from utils.nav import link_to_module
from utils.state import export_progress, import_progress

breadcrumbs("المقرر", "تقدمي")
page_header("تقدمي في المقرر", "My progress",
            "يُحفظ التقدم داخل جلسة المتصفح الحالية (دون حساب أو تسجيل دخول). "
            "يمكنك تنزيل ملف التقدم واستعادته لاحقًا.")

modules = load_modules()
done = st.session_state.completed
visited = st.session_state.visited
scores = st.session_state.quiz_scores
total = sum(len(m.lectures) for m in modules)
mods_done = sum(all(lec.id in done for lec in m.lectures) for m in modules)
cur = st.session_state.get("current_module")

with st.container(horizontal=True):
    st.metric("النسبة العامة", f"{round(100 * len(done) / max(total, 1))}%", border=True)
    st.metric("محاضرات مكتملة", f"{len(done)} / {total}", border=True)
    st.metric("محاور مكتملة", f"{mods_done} / {len(modules)}", border=True)
    st.metric("اختبارات منجزة", len(scores), border=True)
    st.metric("المحور الحالي", cur if cur else "—", border=True)

fig = go.Figure()
fig.add_bar(
    y=[f"{m.number}. {m.meta.get('short_title', m.title)}" for m in modules],
    x=[100 * sum(lec.id in done for lec in m.lectures) / max(len(m.lectures), 1) for m in modules],
    orientation="h", marker_color=[MODULE_COLORS[m.number].accent for m in modules],
    hovertemplate="%{y}<br>%{x:.0f}% مكتمل<extra></extra>",
)
fig.update_xaxes(range=[0, 100], title="نسبة الإكمال %")
fig.update_yaxes(autorange="reversed", side="right")
show(fig, 480, key="progress-bars")

st.subheader("نتائج الاختبارات")
rows = []
for m in modules:
    for kind, label in (("entry", "اختبار الدخول"), ("quiz", "الاختبار البعدي")):
        s = scores.get(f"{kind}-{m.id}")
        rows.append({"المحور": f"{m.number}. {m.title}", "الاختبار": label,
                     "النتيجة": f"{s[0]}/{s[1]}" if s else "—",
                     "النسبة": (s[0] / s[1]) if s else None})
for k, label in (("pretest", "الاختبار القبلي العام"), ("posttest", "الاختبار البعدي العام")):
    s = scores.get(k)
    rows.append({"المحور": "المقرر كاملًا", "الاختبار": label,
                 "النتيجة": f"{s[0]}/{s[1]}" if s else "—", "النسبة": (s[0] / s[1]) if s else None})
st.dataframe(rows, hide_index=True, column_config={
    "النسبة": st.column_config.ProgressColumn("النسبة", min_value=0.0, max_value=1.0, format="percent")})

weak = [m for m in modules if (s := scores.get(f"quiz-{m.id}")) and s[0] / s[1] < 0.7]
if weak:
    st.subheader("محاور تحتاج إلى مراجعة")
    for m in weak:
        link_to_module(m.number)

st.subheader("حفظ التقدم واستعادته")
c1, c2 = st.columns(2)
c1.download_button("تنزيل ملف التقدم (JSON)", export_progress(), file_name="ai_intro_progress.json",
                   mime="application/json", icon=":material/download:")
up = c2.file_uploader("استعادة ملف تقدم", type=["json"], key="progress_upload")
if up is not None and st.session_state.get("progress_loaded") != up.file_id:
    try:
        import_progress(up.getvalue().decode("utf-8"))
        st.session_state.progress_loaded = up.file_id
        st.success("تمت استعادة التقدم.")
        st.rerun()
    except (ValueError, KeyError) as exc:
        st.error(f"تعذّرت قراءة الملف: {exc}")

st.caption(f"محاضرات فُتحت: {len(visited)}")
footer()
