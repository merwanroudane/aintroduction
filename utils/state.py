"""Per-user state (no authentication in v1): mode + progress in st.session_state."""

from __future__ import annotations

import json

import streamlit as st

MODES = {"learner": "وضع الطالب", "instructor": "وضع الأستاذ"}


def init_state() -> None:
    ss = st.session_state
    ss.setdefault("mode", "learner")
    ss.setdefault("visited", set())       # lecture ids opened
    ss.setdefault("completed", set())     # lecture ids marked complete
    ss.setdefault("quiz_scores", {})      # quiz id -> (score, total)
    ss.setdefault("current_module", None)


def is_instructor() -> bool:
    return st.session_state.get("mode") == "instructor"


def mark_visited(lecture_id: str) -> None:
    st.session_state.visited.add(lecture_id)


def toggle_complete(lecture_id: str) -> None:
    done = st.session_state.completed
    if lecture_id in done:
        done.discard(lecture_id)
    else:
        done.add(lecture_id)


def record_quiz(quiz_id: str, score: int, total: int) -> None:
    prev = st.session_state.quiz_scores.get(quiz_id)
    if prev is None or score >= prev[0]:
        st.session_state.quiz_scores[quiz_id] = (score, total)


def export_progress() -> str:
    ss = st.session_state
    return json.dumps(
        {
            "visited": sorted(ss.visited),
            "completed": sorted(ss.completed),
            "quiz_scores": ss.quiz_scores,
        },
        ensure_ascii=False,
        indent=2,
    )


def import_progress(raw: str) -> None:
    data = json.loads(raw)
    ss = st.session_state
    ss.visited = set(data.get("visited", []))
    ss.completed = set(data.get("completed", []))
    ss.quiz_scores = {k: tuple(v) for k, v in data.get("quiz_scores", {}).items()}
