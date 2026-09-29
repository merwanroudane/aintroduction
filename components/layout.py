"""Shared page chrome: CSS injection, breadcrumbs, headers, footer, HTML flow helpers."""

from __future__ import annotations

import html
from pathlib import Path
from typing import NamedTuple

import streamlit as st

from utils.content import load_course

CSS_PATH = Path(__file__).resolve().parent.parent / "assets" / "css" / "style.css"

class ModuleColor(NamedTuple):
    """One hue per module, in three weights.

    accent  the hue itself — borders, badges, chart series, the number chip
    tint    the same hue at ~96% lightness — card and banner backgrounds
    deep    the same hue dark enough to read as text on its own tint (7:1 or better)
    """

    accent: str
    tint: str
    deep: str


# The thirteen modules walk once around the colour wheel: 337° of it, with no gap under
# 16°, so the course reads as an ordered spectrum rather than thirteen arbitrary colours.
# Every accent is mid-tone — light enough never to look dark, saturated enough to carry a
# 6px border. Lightness is tuned per hue, not held constant: yellow at the same nominal
# lightness as blue looks washed out, so the warm band is darkened to match.
MODULE_COLORS: dict[int, ModuleColor] = {
    1:  ModuleColor("#E4695A", "#FFF0EE", "#8E3427"),   # مرجاني   ·   6°
    2:  ModuleColor("#D97D2E", "#FFF4E9", "#7A3E0C"),   # برتقالي  ·  28°
    3:  ModuleColor("#B98A0E", "#FFF7E0", "#664B03"),   # كهرماني  ·  44°
    4:  ModuleColor("#7F9C2B", "#F4FAE4", "#40520F"),   # زيتوني   ·  75°
    5:  ModuleColor("#46AB68", "#EBF8EF", "#1B5A32"),   # أخضر     · 139°
    6:  ModuleColor("#2FA391", "#E6F7F4", "#0D564C"),   # زمردي    · 171°
    7:  ModuleColor("#2E9FB8", "#E5F5F9", "#0C5263"),   # فيروزي   · 191°
    8:  ModuleColor("#3E8FD0", "#EBF4FD", "#1B4E7C"),   # سماوي    · 207°
    9:  ModuleColor("#4A72D8", "#EDF1FD", "#243C82"),   # أزرق     · 223°
    10: ModuleColor("#7B5FD6", "#F1EEFC", "#40308B"),   # نيلي     · 254°
    11: ModuleColor("#A257C8", "#F5EDFA", "#5C2A7B"),   # بنفسجي   · 280°
    12: ModuleColor("#C455A6", "#FBEDF7", "#722A5E"),   # أرجواني  · 316°
    13: ModuleColor("#D95B7E", "#FDEDF1", "#842944"),   # وردي     · 343°
}

FALLBACK_COLOR = ModuleColor("#3E8FD0", "#EBF4FD", "#1B4E7C")


def inject_css() -> None:
    # A Path to a .css file is wrapped in <style> and sent to the event container.
    # Never write "<" in the stylesheet (even in comments): the HTML sanitizer drops the block.
    st.html(CSS_PATH)


def esc(text: str) -> str:
    return html.escape(str(text))


def breadcrumbs(*parts: str) -> None:
    items = " › ".join(
        f"<b>{esc(p)}</b>" if i == len(parts) - 1 else esc(p) for i, p in enumerate(parts)
    )
    st.html(f'<div class="crumbs">{items}</div>')


def page_header(title: str, en: str = "", lead: str = "") -> None:
    st.title(title)
    if en:
        st.html(f'<div class="term-en" style="font-size:1.15rem;margin-top:-0.8rem">{esc(en)}</div>')
    if lead:
        st.html(f'<p class="lead">{esc(lead)}</p>')


def flow_html(steps: list[tuple[str, str]], *, vertical: bool = False, loop: bool = False,
              colors: list[str] | None = None, caption: str = "") -> str:
    """Box-and-arrow process diagram. steps = [(arabic, english), ...]."""
    palette = colors or ["#FFF1E4", "#FFF4D6", "#F3EEFF", "#EAF5FE", "#FFEAF0", "#F7F0E3", "#E8F6F8"]
    borders = ["#E9B99A", "#E8C36A", "#C4B3EA", "#9CC3E8", "#E9AFC0", "#D2BC91", "#93CAD6"]
    parts = []
    arrow = "↓" if vertical else "←"
    for i, (ar, en) in enumerate(steps):
        bg = palette[i % len(palette)]
        bd = borders[i % len(borders)]
        parts.append(
            f'<div class="step" style="--step-bg:{bg};--step-border:{bd}">'
            f"<b>{esc(ar)}</b>" + (f"<small>{esc(en)}</small>" if en else "") + "</div>"
        )
        if i < len(steps) - 1:
            parts.append(f'<div class="arrow">{arrow}</div>')
    if loop:
        parts.append('<div class="arrow" title="loop">↻</div>')
    cls = "flow" + (" vertical" if vertical else "") + (" loop" if loop else "")
    cap = f'<div class="flow-caption">{esc(caption)}</div>' if caption else ""
    return f'<div class="{cls}">{"".join(parts)}</div>{cap}'


def flow(steps, **kw) -> None:
    st.html(flow_html(steps, **kw))


def footer() -> None:
    c = load_course()
    st.html(
        f"""<div class="footer">
        <b>{esc(c['title'])}</b> · <span class="en">{esc(c['title_en'])}</span><br>
        {esc(c['tagline'])}<br>
        إعداد وتصميم: <b>{esc(c['author_ar'])}</b> · <span class="en">{esc(c['author_en'])}</span><br>
        <span class="footer-links">
          <a href="{esc(c['app_url'])}" target="_blank" rel="noopener">المنصة على الإنترنت</a> ·
          <a href="{esc(c['repo_url'])}" target="_blank" rel="noopener">الشفرة المصدرية</a>
        </span><br>
        <span style="font-size:0.82rem">آخر تحديث للمحتوى: {esc(c['last_update'])}</span>
        </div>"""
    )
