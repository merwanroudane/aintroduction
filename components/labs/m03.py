"""Module 3 labs: decompose a claim into precise concepts, and place systems on the
scope/autonomy plane."""

import plotly.graph_objects as go
import streamlit as st

from components.diagrams import show
from components.labs import register

CONCEPTS = ["قدرة", "ذكاء", "استقلالية", "وكالة", "تكيف", "تعميم"]

CLAIMS = [
    ("«هذا النظام يحل مسائل الرياضيات الثانوية بدقة 92%».", "قدرة",
     "وصف لأداء في **مهمة محددة** بمقياس واضح: هذه قدرة، ولا يقول شيئًا عن التنوع أو الاستقلالية."),
    ("«النظام ينفذ عملية الشراء ويرسل التأكيد دون أن يراجعه أحد».", "استقلالية",
     "المسألة هنا مقدار ما يُنفَّذ دون موافقة بشرية، وهو خيار تصميمي لا صفة ذكاء."),
    ("«النظام نجح في نوع من المسائل لم يظهر إطلاقًا في بيانات تدريبه».", "تعميم",
     "النجاح خارج توزيع التدريب هو تعريف التعميم، وهو جوهر النقاش حول الذكاء العام."),
    ("«النظام يبادر باقتراح خطوات ويستدعي أدوات لتحقيق هدف كُلّف به».", "وكالة",
     "المبادرة بالفعل في البيئة سعيًا إلى هدف هي الوكالة، وتختلف عن مجرد الاستجابة لسؤال."),
    ("«يعدّل النظام سياسة التسعير تلقائيًا كلما تغير سلوك السوق بعد نشره».", "تكيف",
     "تغيير السلوك استجابة لتغير البيئة بعد النشر هو التكيف، وهو أيضًا مصدر مخاطر رقابية."),
    ("«يحقق النظام نتائج جيدة في الترجمة والبرمجة والتلخيص والتحليل القانوني».", "ذكاء",
     "الادعاء هنا عن **التنوع** عبر مجالات، وهو أقرب ما يُناقش تحت عنوان الذكاء؛ ومع ذلك يبقى الاتساع محدودًا ولا يعني ذكاءً عامًا."),
    ("«يواصل الروبوت تنفيذ مهمته ساعات دون أي تدخل من المشغّل».", "استقلالية",
     "مدة العمل دون تدخل مؤشر استقلالية، وقد يكون النظام بسيطًا جدًا في الوقت نفسه."),
    ("«يصنّف النموذج صور الأشعة بدقة تعادل أداء الأخصائيين».", "قدرة",
     "أداء في مهمة واحدة مقيس بمقياس محدد: قدرة، لا ذكاء عام."),
    ("«يطبق النظام ما تعلمه في تشخيص الأعطال الميكانيكية على أعطال كهربائية لم يرها من قبل».", "تعميم",
     "نقل ما تُعلّم إلى مجال جديد هو التعميم بمعناه القوي."),
    ("«يغيّر المساعد أسلوب شرحه تلقائيًا حين يلاحظ أن المستخدم لم يفهم».", "تكيف",
     "تعديل السلوك وفق التغذية الراجعة من البيئة أثناء الاستعمال: تكيف."),
]


@register("m03_concept_decomposer", "فكّك العبارة إلى مفهومها الدقيق", "Decompose the claim", module=3)
def concept_decomposer() -> None:
    st.caption("لكل عبارة، حدد المفهوم الذي تتحدث عنه فعلًا. الهدف كسر عادة قول «هذا النظام ذكي» "
               "حين يكون المقصود قدرة أو استقلالية أو تكيفًا.")
    with st.form("m03_concept_decomposer-form"):
        answers = [st.selectbox(f"{i + 1}. {text}", CONCEPTS, index=None, placeholder="اختر المفهوم",
                                key=f"m03_concept_decomposer-{i}")
                   for i, (text, _, _) in enumerate(CLAIMS)]
        done = st.form_submit_button("صحّح", icon=":material/task_alt:")
    if not done:
        return
    score = sum(a == c for a, (_, c, _) in zip(answers, CLAIMS))
    st.metric("النتيجة", f"{score} / {len(CLAIMS)}")
    for i, (a, (text, c, why)) in enumerate(zip(answers, CLAIMS), 1):
        if a != c:
            st.markdown(f"- **{i}.** المفهوم: **{c}** — {why}" + (f" (اخترت: {a})" if a else ""))
    if score >= 8:
        st.success("تمييز دقيق بين المفاهيم. هذه هي الكفاءة الأساسية في هذا المحور.")
    else:
        st.info("راجع جدول المفاهيم الستة في المحاضرة 3.4، ثم أعد المحاولة: الهدف 8 من 10.")


PLACEMENTS = [
    ("منظم حرارة ذكي يشغّل التدفئة تلقائيًا", 1, 4),
    ("مساعد حواري عام يجيب عن أسئلة في مجالات كثيرة", 4, 1),
    ("نظام يقترح تشخيصًا لطبيب يقرر بنفسه", 1, 2),
    ("وكيل يحجز موعدًا ويرسل بريدًا نيابة عنك", 3, 4),
    ("مرشح رسائل ينقل الرسائل المزعجة تلقائيًا", 1, 4),
]


@register("m03_scope_autonomy_lab", "ضع النظام على مستوى النطاق والاستقلالية", "Scope vs autonomy", module=3)
def scope_autonomy_lab() -> None:
    st.caption("قدّر لكل نظام: اتساع نطاقه (عدد المهام التي يجيدها) ومستوى استقلاليته (ما ينفذه دون موافقة). "
               "ثم قارن تقديرك بالتقدير المرجعي، وناقش الفروق: الاختلاف المعلّل مقبول هنا.")
    with st.form("m03_scope_autonomy_lab-form"):
        xs, ys = [], []
        for i, (label, _, _) in enumerate(PLACEMENTS):
            c1, c2 = st.columns(2)
            xs.append(c1.slider(f"{label} — النطاق", 1, 5, 3, key=f"m03_scope_autonomy_lab-x{i}"))
            ys.append(c2.slider(f"{label} — الاستقلالية", 1, 5, 3, key=f"m03_scope_autonomy_lab-y{i}"))
        done = st.form_submit_button("قارن بالتقدير المرجعي", icon=":material/insights:")
    if not done:
        return
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="markers+text", name="تقديرك",
                             text=[p[0][:18] for p in PLACEMENTS], textposition="top center",
                             marker=dict(size=16, color="#E07A5F")))
    fig.add_trace(go.Scatter(x=[p[1] for p in PLACEMENTS], y=[p[2] for p in PLACEMENTS],
                             mode="markers", name="تقدير مرجعي",
                             marker=dict(size=16, color="#5B9BD5", symbol="diamond-open",
                                         line=dict(width=3))))
    fig.update_xaxes(title="اتساع النطاق", range=[0.5, 5.5], dtick=1)
    fig.update_yaxes(title="مستوى الاستقلالية", range=[0.5, 5.5], dtick=1)
    show(fig, 430, key="m03-lab-scope")
    gaps = [(p[0], abs(x - p[1]) + abs(y - p[2])) for p, x, y in zip(PLACEMENTS, xs, ys)]
    worst = max(gaps, key=lambda g: g[1])
    st.markdown(f"**أكبر فارق بين تقديرك والتقدير المرجعي:** {worst[0]}.")
    st.info("الدرس الأهم أن البعدين **مستقلان**: منظم الحرارة ضيق النطاق جدًا لكنه عالي الاستقلالية، "
            "والمساعد الحواري واسع النطاق لكنه منخفض الاستقلالية لأنه لا ينفذ شيئًا في العالم دون طلبك.")
