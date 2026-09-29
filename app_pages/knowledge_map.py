import plotly.graph_objects as go
import streamlit as st

from components.diagrams import render as render_diagram, show
from components.layout import breadcrumbs, footer, page_header
from utils.content import all_lectures, load_modules

breadcrumbs("المقرر", "الخريطة الشاملة للمقرر")
page_header("الخريطة الشاملة للمقرر", "Course knowledge map",
            "الروابط بين المحاور الثلاثة عشر: الأسهم تمثل علاقات التمهيد، ومصفوفة الإحالات تبين "
            "كم مرة تحيل محاضرات محور ما إلى محور آخر.")

render_diagram("knowledge_map")

mods = load_modules()
nums = [m.number for m in mods]
idx = {n: i for i, n in enumerate(nums)}
mat = [[0] * len(nums) for _ in nums]
for lec in all_lectures():
    for rid in lec.meta.get("related", []) + [b for b in lec.meta.get("builds_on", []) if str(b).startswith("m")]:
        try:
            target = int(str(rid)[1:3])
        except ValueError:
            continue
        if target in idx and target != lec.module:
            mat[idx[lec.module]][idx[target]] += 1

st.subheader("مصفوفة الإحالات المتبادلة")
labels = [f"{m.number}. {m.meta.get('short_title', m.title)}" for m in mods]
fig = go.Figure(go.Heatmap(z=mat, x=labels, y=labels,
                           colorscale=[[0, "#FFF9F3"], [0.4, "#FFD8B8"], [1, "#C45A44"]],
                           hovertemplate="من %{y}<br>إلى %{x}<br>%{z} إحالة<extra></extra>"))
fig.update_yaxes(autorange="reversed")
show(fig, 620, key="xref-heatmap")
st.caption("الصف: المحور الذي تُكتب فيه الإحالة. العمود: المحور المحال إليه.")

st.subheader("خلاصة كل محور")
for m in mods:
    with st.expander(f"{m.number}. {m.title}"):
        st.markdown(m.meta.get("subtitle", ""))
        for lec in m.lectures:
            st.markdown(f"- **{m.number}.{lec.number} {lec.title}**: " + "؛ ".join(lec.meta.get("summary", [])[:2]))
footer()
