"""Module 2 labs: order the milestones, and classify the approach behind a system."""

import random

import streamlit as st

from components.diagrams.m02 import MILESTONES
from components.labs import register


@register("m02_timeline_sort", "رتّب المحطات زمنيًا", "Order the milestones", module=2)
def timeline_sort() -> None:
    st.caption("اختر ثماني محطات عشوائية ورتّبها من الأقدم إلى الأحدث بإسناد رقم لكل محطة. "
               "النتيجة تقيس عدد الأزواج المرتبة ترتيبًا صحيحًا، لا المطابقة التامة فقط.")
    if st.button("محطات جديدة", key="m02_timeline_sort-new", icon=":material/casino:"):
        st.session_state.pop("m02_timeline_sort-items", None)
    items = st.session_state.get("m02_timeline_sort-items")
    if items is None:
        items = random.sample(MILESTONES, 8)
        st.session_state["m02_timeline_sort-items"] = items

    with st.form("m02_timeline_sort-form"):
        ranks = []
        for i, (_, label, _, _) in enumerate(items):
            ranks.append(st.selectbox(label, list(range(1, 9)), index=i,
                                      key=f"m02_timeline_sort-r{i}",
                                      help="1 = الأقدم، 8 = الأحدث"))
        done = st.form_submit_button("صحّح الترتيب", icon=":material/sort:")
    if not done:
        return
    if len(set(ranks)) != len(ranks):
        st.warning("استعمل كل رقم مرة واحدة فقط.")
        return
    pairs = ok = 0
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            pairs += 1
            same = (items[i][0] < items[j][0]) == (ranks[i] < ranks[j])
            ok += same
    st.metric("أزواج مرتبة ترتيبًا صحيحًا", f"{ok} / {pairs}", f"{round(100 * ok / pairs)}%",
              delta_color="off")
    st.markdown("**الترتيب الصحيح:**")
    for year, label, approach, desc in sorted(items):
        mine = ranks[items.index((year, label, approach, desc))]
        st.markdown(f"- **{year}** — {label} :gray-badge[{approach}] "
                    f"(ترتيبك: {mine})  \n  :gray[{desc}]")


SYSTEMS = [
    ("برنامج يثبت مبرهنات هندسية بتطبيق قواعد استنتاج على بديهيات.", "رمزية",
     "المعرفة رموز وقواعد صريحة، والاستدلال منطقي."),
    ("نظام يتعلم تصنيف صور الأرقام المكتوبة يدويًا من 60 ألف مثال موسوم بشبكة التفافية.", "عميقة",
     "شبكة متعددة الطبقات تتعلم التمثيلات من بيانات كثيرة."),
    ("برنامج طبي من الثمانينيات يسأل الطبيب أسئلة ويستنتج التشخيص من 500 قاعدة «إذا… فإن…».", "رمزية",
     "نظام خبير قائم على قواعد كتبها خبراء."),
    ("مصنّف يفصل بين فئتين بإيجاد المستوى الفاصل الأعظمي الهامش في فضاء السمات.", "إحصائية",
     "آلة الأشعة الداعمة (SVM): مقاربة إحصائية بأساس نظري."),
    ("نموذج يولّد فقرة نصية جديدة بالتنبؤ المتكرر بالرمز التالي بعد تدريب على نصوص الويب.", "توليدية",
     "نموذج تأسيسي توليدي قائم على بنية المحوّل."),
    ("خوارزمية تبحث في شجرة حركات الشطرنج بعمق كبير مع دالة تقييم صممها خبراء.", "رمزية",
     "بحث في فضاء الحالات مع معرفة مصممة يدويًا (مثل Deep Blue)."),
    ("شبكة من الوحدات البسيطة تعدّل أوزانها بعد كل مثال لتقليل الخطأ في التصنيف.", "اتصالية",
     "المقاربة الاتصالية: المعرفة في الأوزان والتعلم بتعديلها (البيرسبترون والانتشار العكسي)."),
    ("نظام يتعلم لعب أتاري من البكسلات والمكافأة فقط، دون قواعد مكتوبة للعبة.", "عميقة",
     "تعلم معزز عميق (DQN، 2015)."),
    ("نموذج احتمالي يقدّر توزيع الكلمات بالاعتماد على تكرارات ثنائيات وثلاثيات في مدونة نصية.", "إحصائية",
     "نمذجة لغوية إحصائية سبقت النماذج العصبية."),
    ("نموذج يحوّل وصفًا نصيًا إلى صورة بإزالة الضجيج تدريجيًا.", "توليدية",
     "نموذج انتشار توليدي (المحور 9)."),
]


@register("m02_paradigm_classifier", "أي مقاربة يمثل هذا النظام؟", "Classify the approach", module=2)
def paradigm_classifier() -> None:
    st.caption("كل وصف يمثل نظامًا من مرحلة معينة. حدد المقاربة التي ينتمي إليها.")
    options = ["رمزية", "اتصالية", "إحصائية", "عميقة", "توليدية"]
    with st.form("m02_paradigm_classifier-form"):
        answers = [st.selectbox(f"{i + 1}. {text}", options, index=None, placeholder="اختر المقاربة",
                                key=f"m02_paradigm_classifier-{i}")
                   for i, (text, _, _) in enumerate(SYSTEMS)]
        done = st.form_submit_button("صحّح", icon=":material/task_alt:")
    if not done:
        return
    score = sum(a == c for a, (_, c, _) in zip(answers, SYSTEMS))
    st.metric("النتيجة", f"{score} / {len(SYSTEMS)}")
    for i, (a, (text, c, why)) in enumerate(zip(answers, SYSTEMS), 1):
        if a != c:
            st.markdown(f"- **{i}.** المقاربة: **{c}** — {why}" + (f" (اخترت: {a})" if a else ""))
    if score >= 8:
        st.success("تمييز جيد بين المقاربات. انتقل إلى نظام الخروج.")
    else:
        st.info("راجع جدول المقاربات في المحاضرة 2.5، ثم أعد المحاولة: الهدف 8 من 10.")
