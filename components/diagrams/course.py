"""Course-level diagrams: course map, learning journey, full knowledge map."""

import plotly.graph_objects as go
import streamlit as st

from components.diagrams import flow, register, show
from components.layout import FALLBACK_COLOR, MODULE_COLORS
from utils.content import load_course, load_modules

# Pedagogical chain from the specification (section 24), mapped to the 13 modules.
CHAIN = [
    ("الأسس", "Foundations", [1]),
    ("تاريخ الذكاء الاصطناعي", "AI History", [2]),
    ("أنواع الذكاء الاصطناعي", "AI Types", [3]),
    ("AI / ML / DL", "AI vs ML vs DL", [4]),
    ("الذكاء الاصطناعي التوليدي والنماذج اللغوية", "Generative AI · LLMs", [7]),
    ("هندسة الأوامر", "Prompt Engineering", [5, 6]),
    ("نص · صورة · صوت · فيديو", "Text / Image / Audio / Video", [8, 9]),
    ("الاقتصاد", "Economics", [10]),
    ("الأخلاق · الخصوصية · الأمان", "Ethics / Privacy / Security", [11, 12]),
    ("الرقابة البشرية", "Human Oversight", [13]),
]

# Prerequisite edges between modules (a → b means "a is needed for b").
MODULE_EDGES = [
    (1, 2), (1, 3), (2, 3), (3, 4), (1, 4), (4, 7), (7, 5), (5, 6), (7, 6), (6, 8), (7, 8),
    (4, 9), (7, 9), (4, 10), (8, 10), (4, 11), (10, 11), (9, 11), (7, 12), (6, 12),
    (11, 13), (12, 13), (8, 13),
]


@register("course_map")
def course_map() -> None:
    st.caption("السلسلة المفاهيمية للمقرر: كل حلقة تعتمد على ما قبلها. مرّر المؤشر على العقدة لرؤية المحاور المرتبطة.")
    mods = {m.number: m for m in load_modules()}
    xs, ys, labels, hovers, colors = [], [], [], [], []
    for i, (ar, en, nums) in enumerate(CHAIN):
        col, row = i % 5, i // 5
        x = 4 - col if row == 0 else col  # snake layout, reading right-to-left first
        y = 1 - row
        xs.append(x)
        ys.append(y)
        labels.append(ar)
        hovers.append(f"<b>{ar}</b><br>{en}<br>" + "<br>".join(f"المحور {n}: {mods[n].title}" for n in nums if n in mods))
        colors.append(MODULE_COLORS.get(nums[0], FALLBACK_COLOR).accent)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color="#DDD7D0", width=4, shape="spline"),
                             hoverinfo="skip", showlegend=False))
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="markers+text", text=labels, textposition="bottom center",
                             hovertext=hovers, hoverinfo="text",
                             marker=dict(size=46, color=colors, line=dict(color="#FFFFFF", width=4)),
                             textfont=dict(size=13), showlegend=False))
    for i, (x, y) in enumerate(zip(xs, ys)):
        fig.add_annotation(x=x, y=y, text=f"<b>{i + 1}</b>", showarrow=False, font=dict(color="#FFFFFF", size=15))
    fig.update_xaxes(visible=False, range=[-0.6, 4.6])
    fig.update_yaxes(visible=False, range=[-0.55, 1.35])
    show(fig, 360, key="course-map")


@register("learning_journey")
def learning_journey() -> None:
    steps = [(ar, en) for ar, en, _ in load_course()["journey"]]
    flow(steps, caption="الدخول ← الأسس ← النماذج اللغوية والأوامر ← التوليد والتطبيقات ← المسؤولية ← الخروج")
    for ar, en, text in load_course()["journey"]:
        st.markdown(f"- **{ar}** (<span class='term-en'>{en}</span>): {text}", unsafe_allow_html=True)


@register("knowledge_map")
def knowledge_map() -> None:
    import math

    mods = load_modules()
    n = len(mods)
    pos = {}
    for i, m in enumerate(mods):
        a = math.pi / 2 - 2 * math.pi * i / n
        pos[m.number] = (math.cos(a), math.sin(a))
    fig = go.Figure()
    for a, b in MODULE_EDGES:
        if a not in pos or b not in pos:   # a module that is not written yet
            continue
        (x0, y0), (x1, y1) = pos[a], pos[b]
        fig.add_annotation(x=x1, y=y1, ax=x0, ay=y0, xref="x", yref="y", axref="x", ayref="y",
                           showarrow=True, arrowhead=3, arrowwidth=1.5, arrowcolor="#DDB49B",
                           standoff=24, startstandoff=24, text="")
    fig.add_trace(go.Scatter(
        x=[pos[m.number][0] for m in mods], y=[pos[m.number][1] for m in mods],
        mode="markers+text", text=[f"{m.number}. {m.meta.get('short_title', m.title)}" for m in mods],
        textposition=["top center" if pos[m.number][1] >= 0 else "bottom center" for m in mods],
        hovertext=[f"<b>المحور {m.number}</b><br>{m.title}<br>{m.meta.get('title_en', '')}" for m in mods],
        hoverinfo="text",
        marker=dict(size=40,
                    color=[MODULE_COLORS.get(m.number, FALLBACK_COLOR).accent for m in mods],
                    line=dict(color="#FFFFFF", width=3)),
        showlegend=False))
    fig.update_xaxes(visible=False, range=[-1.5, 1.5])
    fig.update_yaxes(visible=False, range=[-1.35, 1.35], scaleanchor="x")
    show(fig, 640, key="knowledge-map")
