import streamlit as st

from components.layout import breadcrumbs, footer, page_header
from utils.nav import link_to_lecture, link_to_module, page
from utils.search import build_index, search

KIND_AR = {"module": "محور", "lecture": "محاضرة", "section": "قسم من محاضرة", "glossary": "مصطلح",
           "reference": "مرجع", "case": "حالة دراسية"}
# One colour per result kind, so a scan of the result list separates them by eye.
KIND_COLOR = {"module": "blue", "lecture": "green", "section": "orange",
              "glossary": "violet", "reference": "gray", "case": "red"}
KIND_ICON = {"module": ":material/view_module:", "lecture": ":material/menu_book:",
             "section": ":material/segment:", "glossary": ":material/translate:",
             "reference": ":material/library_books:", "case": ":material/cases:"}


@st.cache_data(show_spinner=False, max_entries=1)
def _index():
    return build_index()


breadcrumbs("المقرر", "البحث")
page_header("البحث في المقرر", "Search",
            "يبحث في المحاور والمحاضرات وأقسامها والمصطلحات العربية والإنجليزية والقاموس والمراجع "
            "والحالات الدراسية. البحث محلي بالكامل ويتسامح مع اختلاف الهمزات والتاء المربوطة.")

query = st.text_input("اكتب كلمة أو مصطلحًا", placeholder="مثال: الانتباه، Attention، التحيز، RAG",
                      key="q", bind="query-params")
kinds = st.pills("نوع النتائج", list(KIND_AR), format_func=KIND_AR.get, selection_mode="multi",
                 default=list(KIND_AR), key="search_kinds")

if query.strip():
    results = [r for r in search(query, _index()) if r[1].kind in (kinds or KIND_AR)]
    st.caption(f"{len(results)} نتيجة")
    if not results:
        st.info("لا توجد نتائج. جرّب مرادفًا بالعربية أو بالإنجليزية، أو كلمة أقصر.",
                icon=":material/search_off:")
    for score, doc, snippet in results:
        with st.container(border=True, key=f"res-{abs(hash((doc.kind, doc.title, doc.lecture_id))) % 10**9}"):
            st.markdown(f"{KIND_ICON[doc.kind]} :{KIND_COLOR[doc.kind]}-badge[{KIND_AR[doc.kind]}] **{doc.title}**")
            if snippet:
                st.caption(snippet)
            if doc.lecture_id and doc.kind in ("lecture", "section", "case", "glossary"):
                link_to_lecture(doc.lecture_id, label="انتقل إلى المحاضرة", icon=":material/arrow_back:")
            elif doc.kind == "module" and doc.module:
                link_to_module(doc.module, label="انتقل إلى المحور")
            elif doc.kind == "reference":
                st.page_link(page("references"), label="صفحة المراجع", icon=":material/arrow_back:")
            elif doc.kind == "glossary":
                st.page_link(page("glossary"), label="القاموس", icon=":material/arrow_back:")
else:
    st.info("ابدأ بكتابة مصطلح. أمثلة مقترحة: «هندسة الأوامر»، «Transformer»، «الخصوصية»، «Double Machine Learning».",
            icon=":material/lightbulb:")

footer()
