import streamlit as st

from components.layout import breadcrumbs, footer, page_header
from utils.content import load_capstone
from utils.state import is_instructor

cap = load_capstone()
breadcrumbs("المقرر", "التطبيق والتقييم", "المشروع العملي الختامي")
page_header("المشروع العملي الختامي", "Final capstone project", cap["intro"])

with st.container(key="card-key-capstone"):
    st.markdown(":material/flag: **الإطار العام للمشروع**")
    for line in cap["general"]:
        st.markdown(f"- {line}")

st.subheader("المراحل والجدول الزمني المقترح")
st.table({"المرحلة": [p["phase"] for p in cap["phases"]],
          "الأسبوع": [p["week"] for p in cap["phases"]],
          "المخرج": [p["output"] for p in cap["phases"]]})

st.subheader("المسارات الستة")
tracks = cap["tracks"]
tabs = st.tabs([f"{t['code']} · {t['title']}" for t in tracks])
for tab, t in zip(tabs, tracks):
    with tab:
        st.markdown(f"#### {t['title']}")
        st.caption(t["title_en"])
        st.markdown(f"**المشكلة.** {t['problem']}")
        c1, c2 = st.columns(2, gap="large")
        with c1:
            st.markdown("##### الأهداف")
            for x in t["objectives"]:
                st.markdown(f"- {x}")
            st.markdown("##### النطاق")
            st.markdown(t["scope"])
            st.markdown("##### المتطلبات")
            for x in t["requirements"]:
                st.markdown(f"- {x}")
        with c2:
            st.markdown("##### المهام")
            for i, x in enumerate(t["tasks"], 1):
                st.markdown(f"{i}. {x}")
            st.markdown("##### المخرجات المطلوبة")
            for x in t["deliverables"]:
                st.markdown(f"- {x}")
        with st.container(key=f"card-warning-cap-{t['code']}"):
            st.markdown("**:material/balance: الأخلاقيات والخصوصية والتحقق**")
            st.markdown(f"- **الأخلاقيات:** {t['ethics']}\n- **الخصوصية:** {t['privacy']}\n- **التحقق:** {t['verification']}")
        st.markdown(f"**متطلبات العرض.** {t['presentation']}")
        if is_instructor():
            with st.container(key=f"card-instructor-cap-{t['code']}"):
                st.markdown("**:material/school: ملاحظات للأستاذ**")
                for x in t["instructor_notes"]:
                    st.markdown(f"- {x}")

st.subheader("سلم التقييم المشترك | Evaluation rubric")
st.caption("يطبَّق على جميع المسارات. لكل معيار أربعة مستويات أداء، والدرجة النهائية من 100.")
rub = cap["rubric"]
st.dataframe(
    [{"المعيار": r["criterion"], "الوزن": r["weight"], "ممتاز": r["levels"][0], "جيد": r["levels"][1],
      "مقبول": r["levels"][2], "غير كافٍ": r["levels"][3]} for r in rub],
    hide_index=True,
)
st.subheader("تقييمي الذاتي قبل التسليم")
total = 0
for r in rub:
    lvl = st.select_slider(r["criterion"], ["غير كافٍ", "مقبول", "جيد", "ممتاز"], value="جيد",
                           key=f"rub-{r['criterion']}")
    total += r["weight"] * {"غير كافٍ": 0.25, "مقبول": 0.5, "جيد": 0.75, "ممتاز": 1.0}[lvl]
st.metric("الدرجة التقديرية", f"{total:.0f} / 100")
footer()
