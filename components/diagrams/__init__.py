"""Diagram registry.

Lectures embed a diagram with a line ``[[diagram:name]]``. Each module keeps its
diagrams in ``components/diagrams/mXX.py`` and registers them with ``@register``;
the files are imported lazily the first time any diagram is requested.

Shared helpers so every diagram looks like part of one system:

    flow(steps, vertical=False, loop=False, caption="")   box-and-arrow process
    nested(layers, caption="")                            nested sets (AI ⊃ ML ⊃ DL)
    grid_cards(items, cols=3)                             labelled concept tiles
    network(nodes, edges, height=460)                     Plotly concept map
    style_fig(fig, height=None)                           warm Plotly theme + Arabic font
"""

from __future__ import annotations

import importlib
import math
import pkgutil
from typing import Callable

import plotly.graph_objects as go
import streamlit as st

from components.layout import esc, flow_html

REGISTRY: dict[str, Callable[[], None]] = {}
_loaded = False

# Ordered so that consecutive entries are far apart on the wheel: a grid of tiles or a
# chart with four series gets four obviously different hues, not four neighbouring ones.
# Same thirteen hues as MODULE_COLORS, and SOFT holds each one's tint at the same index.
PALETTE = ["#E4695A", "#3E8FD0", "#46AB68", "#A257C8", "#D97D2E",
           "#2E9FB8", "#D95B7E", "#7F9C2B", "#7B5FD6", "#B98A0E",
           "#2FA391", "#C455A6", "#4A72D8"]
SOFT = ["#FFF0EE", "#EBF4FD", "#EBF8EF", "#F5EDFA", "#FFF4E9",
        "#E5F5F9", "#FDEDF1", "#F4FAE4", "#F1EEFC", "#FFF7E0",
        "#E6F7F4", "#FBEDF7", "#EDF1FD"]
# Text weight of each PALETTE entry, dark enough to read on the matching SOFT tint.
DEEP = ["#8E3427", "#1B4E7C", "#1B5A32", "#5C2A7B", "#7A3E0C",
        "#0C5263", "#842944", "#40520F", "#40308B", "#664B03",
        "#0D564C", "#722A5E", "#243C82"]
FONT = "Tajawal, Cairo, 'Noto Sans Arabic', sans-serif"


def register(name: str):
    def deco(fn: Callable[[], None]):
        REGISTRY[name] = fn
        return fn

    return deco


def _load_all() -> None:
    global _loaded
    if _loaded:
        return
    for info in pkgutil.iter_modules(__path__):
        importlib.import_module(f"{__name__}.{info.name}")
    _loaded = True


def names() -> list[str]:
    _load_all()
    return sorted(REGISTRY)


def render(name: str) -> None:
    _load_all()
    fn = REGISTRY.get(name)
    if fn is None:
        st.warning(f"رسم غير معرّف: {name}")
        return
    fn()


# ---------------------------------------------------------------- helpers

def flow(steps: list[tuple[str, str]], **kw) -> None:
    st.html(flow_html(steps, **kw))


def nested(layers: list[tuple[str, str, str]], caption: str = "") -> None:
    """layers = [(arabic, english, description), ...] from outermost to innermost."""
    html = ""
    for i, (ar, en, desc) in reversed(list(enumerate(layers))):
        color = PALETTE[i % len(PALETTE)]
        bg = SOFT[i % len(SOFT)]
        html = (
            f'<div class="nested" style="border-color:{color};background:{bg}">'
            f'<div class="label" style="color:{color}">{esc(ar)} <small>{esc(en)}</small></div>'
            f'<div style="font-size:0.92rem;color:#5A4A45;margin-bottom:0.4rem">{esc(desc)}</div>'
            f"{html}</div>"
        )
    cap = f'<div class="flow-caption" style="margin-top:0.2rem">{esc(caption)}</div>' if caption else ""
    st.html(html + cap)


def grid_cards(items: list[tuple[str, str, str]], cols: int = 3) -> None:
    """items = [(title_ar, title_en, text)] as small coloured tiles in a responsive grid."""
    tiles = []
    for i, (ar, en, text) in enumerate(items):
        color, bg = PALETTE[i % len(PALETTE)], SOFT[i % len(SOFT)]
        tiles.append(
            f'<div class="tile" style="background:{bg};border-top:5px solid {color}">'
            f'<b>{esc(ar)}</b><small>{esc(en)}</small><p>{esc(text)}</p></div>'
        )
    st.html(f'<div class="tiles" style="--cols:{cols}">{"".join(tiles)}</div>')


def style_fig(fig: go.Figure, height: int | None = None) -> go.Figure:
    fig.update_layout(
        font=dict(family=FONT, size=14, color="#2F2C33"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FDFCFB",
        margin=dict(l=20, r=20, t=50, b=30),
        colorway=PALETTE,
        hoverlabel=dict(font_family=FONT, bgcolor="#FFFFFF"),
        legend=dict(bgcolor="rgba(255,255,255,0.6)"),
    )
    if height:
        fig.update_layout(height=height)
    return fig


def show(fig: go.Figure, height: int | None = None, key: str | None = None) -> None:
    st.plotly_chart(style_fig(fig, height), key=key, config={"displayModeBar": False})


def network(nodes: list[dict], edges: list[tuple[str, str]], height: int = 460,
            title: str = "", key: str | None = None) -> None:
    """Concept map. nodes = [{id, label, group?, x?, y?, hover?}]; missing x/y → circle layout."""
    n = len(nodes)
    pos = {}
    for i, node in enumerate(nodes):
        if "x" in node and "y" in node:
            pos[node["id"]] = (node["x"], node["y"])
        else:
            a = 2 * math.pi * i / max(n, 1)
            pos[node["id"]] = (math.cos(a), math.sin(a))
    fig = go.Figure()
    for a, b in edges:
        (x0, y0), (x1, y1) = pos[a], pos[b]
        fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode="lines",
                                 line=dict(color="#D8D3CD", width=2), hoverinfo="skip",
                                 showlegend=False))
        fig.add_annotation(x=x1, y=y1, ax=x0, ay=y0, xref="x", yref="y", axref="x", ayref="y",
                           showarrow=True, arrowhead=3, arrowsize=1.2, arrowwidth=1.6,
                           arrowcolor="#B9B3AC", standoff=22, text="")
    groups = sorted({node.get("group", 0) for node in nodes}, key=str)
    for gi, g in enumerate(groups):
        members = [node for node in nodes if node.get("group", 0) == g]
        fig.add_trace(go.Scatter(
            x=[pos[m["id"]][0] for m in members], y=[pos[m["id"]][1] for m in members],
            mode="markers+text", text=[m["label"] for m in members], textposition="bottom center",
            hovertext=[m.get("hover", m["label"]) for m in members], hoverinfo="text",
            marker=dict(size=30, color=PALETTE[gi % len(PALETTE)], line=dict(color="#FFFFFF", width=3)),
            name=str(g), showlegend=False,
        ))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    if title:
        fig.update_layout(title=dict(text=title, x=0.5))
    show(fig, height, key=key)
