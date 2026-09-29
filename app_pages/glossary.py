import streamlit as st

from components.layout import breadcrumbs, esc, footer, page_header
from utils.content import load_glossary, load_modules
from utils.nav import link_to_lecture
from utils.search import normalize

breadcrumbs("المقرر", "القاموس")
page_header("قاموس الذكاء الاصطناعي", "AI Glossary",
            "مصطلحات المقرر بالعربية والإنجليزية مع التعريف، والمفاهيم المرتبطة، والمحور والمحاضرة "
            "التي يُشرح فيها المصطلح.")

terms = load_glossary()
mods = {m.number: m for m in load_modules()}

c1, c2 = st.columns([2, 1])
q = c1.text_input("ابحث في القاموس", placeholder="عربي أو إنجليزي أو اختصار", key="gq")
module_filter = c2.selectbox("المحور", [0] + sorted(mods),
                             format_func=lambda n: "كل المحاور" if n == 0 else f"{n}. {mods[n].meta.get('short_title', mods[n].title)}",
                             key="gmod")

nq = normalize(q.strip())
shown = [
    t for t in terms
    if (module_filter == 0 or t.get("module") == module_filter)
    and (not nq or nq in normalize(f"{t['ar']} {t['en']} {t.get('acronym', '')} {t['definition']}"))
]
st.caption(f"{len(shown)} من {len(terms)} مصطلحًا")

view = st.segmented_control("طريقة العرض", ["بطاقات", "جدول"], default="بطاقات", key="gview",
                            required=True)
if view == "جدول":
    st.dataframe(
        [{"المصطلح": t["ar"], "English": t["en"], "الاختصار": t.get("acronym", ""),
          "التعريف": t["definition"], "المحور": t.get("module"),
          "مرتبط بـ": "، ".join(t.get("related", []) or [])} for t in shown],
        hide_index=True,
    )
else:
    for t in shown:
        with st.container(key=f"card-definition-g-{abs(hash(t['en'])) % 10**9}"):
            acr = f" · {esc(t['acronym'])}" if t.get("acronym") else ""
            st.html(f"<div><b style='font-size:1.08rem'>{esc(t['ar'])}</b> — "
                    f"<span class='term-en'>{esc(t['en'])}{acr}</span></div>")
            st.markdown(t["definition"])
            meta = []
            if t.get("related"):
                meta.append("مفاهيم مرتبطة: " + "، ".join(t["related"]))
            if t.get("see_also"):
                meta.append("انظر أيضًا: " + "، ".join(t["see_also"]))
            if t.get("module") in mods:
                meta.append(f"المحور {t['module']}: {mods[t['module']].title}")
            if meta:
                st.caption(" · ".join(meta))
            if t.get("lecture"):
                link_to_lecture(t["lecture"], label="اقرأ الشرح في المحاضرة", icon=":material/arrow_back:")

footer()
