"""Render parsed lecture segments: Markdown, headings, educational cards, sticky notes,
diagrams and interactive labs."""

from __future__ import annotations

import itertools

import streamlit as st

from components import diagrams, labs
from utils.content import CARD_TYPES, STICKY_TYPES, Lecture, Segment, format_reference, load_references
from utils.state import is_instructor

CARD_ICONS = {
    "definition": ":material/menu_book:", "key": ":material/lightbulb:",
    "example": ":material/emoji_objects:", "applied": ":material/work:",
    "deep": ":material/science:", "method": ":material/rule:",
    "instructor": ":material/school:", "misconception": ":material/report:",
    "warning": ":material/warning:", "didyouknow": ":material/auto_awesome:",
    "discussion": ":material/forum:", "activity": ":material/groups:",
    "case": ":material/cases:", "recap": ":material/summarize:",
    "check": ":material/quiz:", "modern": ":material/new_releases:",
    "verify": ":material/fact_check:", "crosslink": ":material/link:",
    "exercise": ":material/edit_square:", "selfstudy": ":material/local_library:",
}

_uid = itertools.count()


def _key(prefix: str) -> str:
    return f"{prefix}-{next(_uid)}"


def card(block_type: str, title: str, body: str) -> None:
    """Educational card. Colour + label come from the block type (see style.css)."""
    ar, en = CARD_TYPES.get(block_type, ("ملاحظة", "Note"))
    icon = CARD_ICONS.get(block_type, ":material/info:")
    with st.container(key=_key(f"card-{block_type}")):
        head = f"{icon} **{ar}** · <span class='term-en' style='font-weight:500'>{en}</span>"
        if title:
            head += f"  \n##### {title}"
        st.markdown(head, unsafe_allow_html=True)
        if block_type in ("check", "exercise"):
            question, _, answer = body.partition("???")
            st.markdown(question.strip())
            if answer.strip():
                label = "اعرض الحل النموذجي" if block_type == "exercise" else "اعرض الإجابة النموذجية"
                with st.expander(label, icon=":material/visibility:"):
                    st.markdown(answer.strip())
        else:
            st.markdown(body)


def sticky(block_type: str, title: str, body: str) -> None:
    with st.container(key=_key(block_type)):
        if title:
            st.markdown(f"**📌 {title}**")
        st.markdown(body)


def render_segment(seg: Segment) -> None:
    if seg.kind == "md":
        st.markdown(seg.text, unsafe_allow_html=True)
    elif seg.kind == "heading":
        st.header(seg.text, anchor=seg.anchor)
    elif seg.kind == "diagram":
        diagrams.render(seg.text)
    elif seg.kind == "widget":
        labs.render(seg.text)
    elif seg.kind == "link":
        from utils.nav import link_to_lecture

        link_to_lecture(seg.text, icon=":material/arrow_back:")
    elif seg.kind == "block":
        bt = seg.block_type
        if bt == "instructor":
            if is_instructor():
                card("instructor", seg.title, seg.text)
        elif bt == "deep":
            label = f"تعمق تقني · Technical Deep Dive — {seg.title}" if seg.title else "تعمق تقني · Technical Deep Dive"
            with st.expander(label, icon=":material/science:"):
                with st.container(key=_key("card-deep")):
                    st.markdown(seg.text, unsafe_allow_html=True)
        elif bt in STICKY_TYPES:
            sticky(bt, seg.title, seg.text)
        elif bt == "ltr":
            st.html(f'<div class="ltr">{seg.text}</div>')
        else:
            card(bt, seg.title, seg.text)


def render_lecture_body(lec: Lecture) -> None:
    for seg in lec.segments:
        render_segment(seg)


def lecture_references(lec: Lecture) -> None:
    refs = load_references()
    items = lec.meta.get("references", [])
    if not items:
        return
    with st.expander("المصادر المستخدمة في هذه المحاضرة", icon=":material/library_books:"):
        for item in items:
            rid = item["id"] if isinstance(item, dict) else item
            used_for = item.get("for", "") if isinstance(item, dict) else ""
            ref = refs.get(rid)
            if ref is None:
                st.warning(f"مرجع غير معرّف: {rid}")
                continue
            line = f"- {format_reference(ref)}"
            if used_for:
                line += f"  \n  ↳ **استُخدم في:** {used_for}"
            st.markdown(line)
