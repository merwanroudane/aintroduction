"""Interactive lab registry.

Lectures embed a lab with ``[[widget:name]]``. Each module keeps its labs in
``components/labs/mXX.py`` and registers them with ``@register(name, title, en)``.
Labs run fully offline (no paid API): they are teaching simulations, and each
one says so when it simplifies reality.

Widget keys inside a lab must be prefixed with the lab name so two labs never
collide on one page.
"""

from __future__ import annotations

import importlib
import pkgutil
from dataclasses import dataclass
from typing import Callable

import streamlit as st


@dataclass
class Lab:
    name: str
    title: str
    title_en: str
    module: int
    fn: Callable[[], None]


REGISTRY: dict[str, Lab] = {}
_loaded = False


def register(name: str, title: str, title_en: str, module: int):
    def deco(fn: Callable[[], None]):
        REGISTRY[name] = Lab(name, title, title_en, module, fn)
        return fn

    return deco


def _load_all() -> None:
    global _loaded
    if _loaded:
        return
    for info in pkgutil.iter_modules(__path__):
        importlib.import_module(f"{__name__}.{info.name}")
    _loaded = True


def all_labs() -> list[Lab]:
    _load_all()
    return sorted(REGISTRY.values(), key=lambda lab: (lab.module, lab.name))


def render(name: str) -> None:
    _load_all()
    lab = REGISTRY.get(name)
    if lab is None:
        st.warning(f"مختبر غير معرّف: {name}")
        return
    with st.container(border=True, key=f"lab-{name}"):
        st.markdown(f"#### :material/science: مختبر تفاعلي: {lab.title}")
        st.caption(lab.title_en)
        lab.fn()
