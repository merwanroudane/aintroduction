from collections import defaultdict

import streamlit as st

from components.layout import breadcrumbs, footer, page_header
from utils.content import all_lectures, format_reference, load_references
from utils.search import normalize

TOPICS = [
    ("AI Foundations", "أسس الذكاء الاصطناعي"), ("AI History", "تاريخ الذكاء الاصطناعي"),
    ("Machine Learning", "التعلم الآلي"), ("Deep Learning", "التعلم العميق"),
    ("LLMs", "النماذج اللغوية الكبيرة"), ("Prompt Engineering", "هندسة الأوامر"),
    ("Generative AI", "الذكاء الاصطناعي التوليدي"), ("Multimodal AI", "الذكاء الاصطناعي متعدد الوسائط"),
    ("Economics + AI", "الاقتصاد والذكاء الاصطناعي"), ("AI Ethics", "أخلاقيات الذكاء الاصطناعي"),
    ("Privacy", "الخصوصية"), ("Security", "الأمان"), ("Human Oversight", "الرقابة البشرية"),
    ("AI Governance", "حوكمة الذكاء الاصطناعي"), ("AI Education", "الذكاء الاصطناعي والتعليم"),
    ("Official Product Documentation", "الوثائق الرسمية للمنتجات"),
]
TYPE_AR = {"book": "كتاب", "article": "مقال محكّم", "report": "تقرير", "standard": "معيار / إطار",
           "documentation": "وثائق رسمية", "course": "مقرر", "web": "صفحة ويب", "preprint": "ورقة أولية",
           "law": "نص قانوني", "video": "فيديو"}

breadcrumbs("المقرر", "المصادر والمراجع")
page_header("المصادر والمراجع", "References",
            "كل مرجع في المنصة مُتحقق منه، مع تاريخ التحقق للمعلومات المتغيرة (خصائص المنتجات، "
            "الوثائق الرسمية). يظهر أسفل كل مرجع المحاضرات التي استُخدم فيها.")

refs = load_references()
used_in = defaultdict(list)
for lec in all_lectures():
    for item in lec.meta.get("references", []):
        rid = item["id"] if isinstance(item, dict) else item
        used_in[rid].append(f"{lec.module}.{lec.number}")

by_topic = defaultdict(list)
for r in refs.values():
    by_topic[r.get("topic", "AI Foundations")].append(r)

c1, c2 = st.columns([2, 1])
q = normalize(c1.text_input("ابحث في المراجع", placeholder="مؤلف، عنوان، سنة…", key="rq").strip())
types = sorted({r.get("type", "web") for r in refs.values()})
tsel = c2.multiselect("النوع", types, format_func=lambda t: TYPE_AR.get(t, t), key="rtypes")

st.metric("عدد المراجع", len(refs))
known = [t for t, _ in TOPICS]
ordered = TOPICS + [(t, t) for t in sorted(by_topic) if t not in known]
for topic, ar in ordered:
    items = [r for r in by_topic.get(topic, [])
             if (not q or q in normalize(f"{r['authors']} {r['title']} {r['year']} {r.get('venue', '')}"))
             and (not tsel or r.get("type") in tsel)]
    if not items:
        continue
    with st.expander(f"{ar} · {topic} ({len(items)})", expanded=bool(q)):
        for r in sorted(items, key=lambda r: (str(r["authors"]), str(r["year"]))):
            lecs = "، ".join(sorted(set(used_in.get(r["id"], [])), key=lambda s: tuple(map(int, s.split(".")))))
            st.markdown(f"- :gray-badge[{TYPE_AR.get(r.get('type'), r.get('type', ''))}] {format_reference(r)}"
                        + (f"  \n  :gray[استُخدم في المحاضرات: {lecs}]" if lecs else ""))

footer()
