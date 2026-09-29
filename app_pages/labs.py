import streamlit as st

from components import labs
from components.layout import MODULE_COLORS, breadcrumbs, footer, page_header
from utils.content import load_modules

breadcrumbs("المقرر", "المختبرات التفاعلية")
page_header("المختبرات التفاعلية", "Practical labs",
            "كل مختبرات المقرر في مكان واحد. تعمل جميعها دون اتصال بأي واجهة برمجية مدفوعة: "
            "هي محاكاة تعليمية توضح الآلية، وكل مختبر يذكر حدود التبسيط الذي يعتمده.")

all_labs = labs.all_labs()
mods = {m.number: m for m in load_modules()}
if not all_labs:
    st.info("لا توجد مختبرات مسجلة.")
else:
    options = [lab.name for lab in all_labs]
    names = {lab.name: f"المحور {lab.module} · {lab.title}" for lab in all_labs}
    # Each module keeps its own hue here too, so the spread of labs across the course is
    # readable at a glance instead of being thirteen identical badges.
    chips = "".join(
        f'<span class="modchip" style="--c:{MODULE_COLORS[n].accent};'
        f'--b:{MODULE_COLORS[n].tint};--d:{MODULE_COLORS[n].deep}">'
        f"المحور {n}<b>{count}</b></span>"
        for n in sorted(mods)
        if (count := sum(1 for lab in all_labs if lab.module == n))
    )
    st.html(f'<div class="modchips">{chips}</div>')
    choice = st.selectbox("اختر مختبرًا", options, format_func=names.get, key="lab", bind="query-params")
    labs.render(choice)

footer()
