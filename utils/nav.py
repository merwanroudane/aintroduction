"""Page registry shared by app.py (navigation) and pages that link to each other.

Each module has a thin page file (app_pages/modules/module_XX.py) that calls the
generic renderer. ``st.Page`` objects are cheap and are matched by their script,
so building them again when a page needs a link is safe.
"""

from __future__ import annotations

import streamlit as st

from utils.content import lecture_index, load_modules

MODULE_ICONS = {
    1: ":material/psychology:", 2: ":material/history_edu:", 3: ":material/category:",
    4: ":material/account_tree:", 5: ":material/edit_note:", 6: ":material/construction:",
    7: ":material/forum:", 8: ":material/article:", 9: ":material/palette:",
    10: ":material/finance:", 11: ":material/balance:", 12: ":material/shield_lock:",
    13: ":material/supervisor_account:",
}

STATIC_PAGES = {
    "home": ("app_pages/home.py", "الصفحة الرئيسية", ":material/home:"),
    "map": ("app_pages/course_map.py", "خريطة المقرر", ":material/hub:"),
    "pretest": ("app_pages/pretest.py", "الاختبار القبلي", ":material/assignment:"),
    "posttest": ("app_pages/posttest.py", "الاختبار البعدي", ":material/assignment_turned_in:"),
    "labs": ("app_pages/labs.py", "المختبرات التفاعلية", ":material/science:"),
    "capstone": ("app_pages/capstone.py", "المشروع الختامي", ":material/rocket_launch:"),
    "glossary": ("app_pages/glossary.py", "قاموس الذكاء الاصطناعي", ":material/translate:"),
    "search": ("app_pages/search.py", "البحث", ":material/search:"),
    "references": ("app_pages/references.py", "المصادر والمراجع", ":material/library_books:"),
    "toolkit": ("app_pages/instructor_toolkit.py", "أدوات الأستاذ", ":material/school:"),
    "td": ("app_pages/td_guide.py", "دليل حصص الأعمال الموجّهة", ":material/groups:"),
    "progress": ("app_pages/progress.py", "تقدمي", ":material/insights:"),
    "knowledge": ("app_pages/knowledge_map.py", "الخريطة الشاملة للمقرر", ":material/device_hub:"),
}


def page(name: str) -> st.Page:
    path, title, icon = STATIC_PAGES[name]
    return st.Page(path, title=title, icon=icon, default=(name == "home"))


def module_page(number: int) -> st.Page:
    m = next(m for m in load_modules() if m.number == number)
    return st.Page(
        f"app_pages/modules/module_{number:02d}.py",
        title=f"{number}. {m.meta.get('short_title', m.title)}",
        icon=MODULE_ICONS.get(number, ":material/menu_book:"),
        url_path=f"module-{number:02d}",
    )


def lecture_key(module_number: int) -> str:
    """Widget key (and URL query param) that selects the open lecture of a module."""
    return f"lec{module_number:02d}"


def link_to_lecture(lecture_id: str, label: str | None = None, icon: str = ":material/link:") -> None:
    lec = lecture_index().get(lecture_id)
    if lec is None:
        st.caption(f"رابط غير صالح: {lecture_id}")
        return
    st.page_link(
        module_page(lec.module),
        label=label or f"المحاضرة {lec.module}.{lec.number}: {lec.title}",
        icon=icon,
        query_params={lecture_key(lec.module): lec.id},
    )


def link_to_module(number: int, label: str | None = None) -> None:
    m = next((m for m in load_modules() if m.number == number), None)
    if m is None:
        st.caption(f"رابط غير صالح: المحور {number}")
        return
    st.page_link(module_page(number), label=label or f"المحور {number}: {m.title}",
                 icon=MODULE_ICONS.get(number))
