"""Module 10 diagrams: concept map, prediction vs causation, the question-to-tool map,
double machine learning, the nowcasting timeline, text-as-data pipeline, the productivity
J-curve, the task framework, and the leakage taxonomy."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from components.diagrams import PALETTE, flow, grid_cards, network, register, show


@register("m10_concept_map")
def concept_map() -> None:
    nodes = [
        {"id": "e", "label": "الاقتصاد والتعلّم الآلي", "x": 0, "y": 0, "group": 0},
        {"id": "pred", "label": "التنبؤ", "x": -2.3, "y": 1.0, "group": 1,
         "hover": "ŷ: ما القيمة المتوقعة؟ — التعلّم الآلي قوي هنا"},
        {"id": "caus", "label": "الاستدلال السببي", "x": -2.4, "y": -0.5, "group": 1,
         "hover": "β̂: ما أثر التدخل؟ — يحتاج تصميمًا لا دقة"},
        {"id": "dml", "label": "التعلّم المزدوج", "x": -1.2, "y": -1.8, "group": 2,
         "hover": "جسر بين الاثنين: تنبؤ في الخطوة الأولى، تقدير في الثانية"},
        {"id": "now", "label": "التنبؤ الآني", "x": 1.2, "y": -1.8, "group": 2},
        {"id": "text", "label": "النص بوصفه بيانات", "x": 2.4, "y": -0.5, "group": 3},
        {"id": "prod", "label": "الإنتاجية والعمل", "x": 2.3, "y": 1.0, "group": 3},
        {"id": "pit", "label": "المزالق المنهجية", "x": 0, "y": 2.0, "group": 4,
         "hover": "التسرّب، وفرط الملاءمة، وإعادة الإنتاج"},
        {"id": "ev", "label": "مستويات الأدلة", "x": 0, "y": -2.8, "group": 5},
    ]
    edges = [("e", "pred"), ("pred", "caus"), ("caus", "dml"), ("e", "now"), ("now", "text"),
             ("text", "prod"), ("e", "pit"), ("pit", "ev"), ("prod", "ev"), ("dml", "pit")]
    network(nodes, edges, height=500, key="m10-concept")


@register("m10_prediction_vs_causation")
def prediction_vs_causation() -> None:
    st.caption("التمييز الذي يحكم المحور كله — ويحكم استعمالك للتعلّم الآلي طول حياتك المهنية.")
    grid_cards([
        ("التنبؤ", "Prediction — ŷ",
         "**السؤال:** ما القيمة المتوقعة؟ **المعيار:** دقة على بيانات لم يرها النموذج. "
         "**لا يهم** لماذا صحّ التنبؤ. **الأداة:** التعلّم الآلي بامتياز."),
        ("الاستدلال السببي", "Causal inference — β̂",
         "**السؤال:** ماذا يحدث لو تدخّلنا؟ **المعيار:** صحة التصميم وقابلية التعرّف. "
         "**الدقة لا تكفي ولا تدل.** **الأداة:** تصميم البحث، والتعلّم الآلي مساعد."),
        ("مثال تنبؤي", "Which one?",
         "«أي المقترضين سيتعثّر؟» — قرار **فرز** لا يتطلب معرفة السبب. (مسائل سياسة التنبؤ)"),
        ("مثال سببي", "What if?",
         "«ما أثر خفض سعر الفائدة على التعثّر؟» — قرار **تدخّل** لا يجيب عنه أي نموذج تنبؤي."),
    ], cols=2)


@register("m10_question_to_tool")
def question_to_tool() -> None:
    flow([("ما سؤالك؟", "Question"), ("تنبؤي أم سببي؟", "Type"),
          ("ما البيانات المتاحة؟", "Data"), ("ما التصميم الممكن؟", "Design"),
          ("اختر الأداة", "Tool"), ("حدد معيار التقييم", "Metric")],
         caption="الترتيب الصحيح: السؤال أولًا والأداة أخيرًا. وعكسه هو أشهر أخطاء التطبيق.")
    st.caption("**القاعدة:** لا تبدأ من «أريد استعمال التعلّم العميق» ثم تبحث عن سؤال. "
               "فاختيار الأداة قبل السؤال يجعلك تعيد صياغة السؤال ليناسب الأداة — وهو انحراف منهجي كامل.")


@register("m10_double_ml")
def double_ml() -> None:
    flow([("Y و D و X", "Data"), ("تنبأ بـ Y من X", "ML #1"), ("تنبأ بـ D من X", "ML #2"),
          ("احسب البواقي", "Residualize"), ("قدّر الأثر من البواقي", "Estimate"),
          ("تقسيم العينة المتقاطع", "Cross-fitting")],
         caption="التعلّم الآلي المزدوج: التعلّم الآلي للتنبؤ بالمزعجات، والتقدير على ما تبقّى بعدها.")
    st.caption("**الفكرة:** استعمل قوة التعلّم الآلي حيث ينفع (التنبؤ بالمتغيرات الضابطة)، "
               "واحتفظ بالتقدير الإحصائي حيث يلزم (معامل الأثر). و**تقسيم العينة المتقاطع** هو ما يمنع "
               "تحيّز فرط الملاءمة من التسرّب إلى التقدير.")


@register("m10_nowcast_timeline")
def nowcast_timeline() -> None:
    st.caption("لماذا يوجد التنبؤ الآني أصلًا: المؤشرات الرسمية تصدر **متأخرة** وتُراجَع، "
               "بينما تصدر مؤشرات أخرى **يوميًا**. والفجوة هي ما يملؤه التنبؤ الآني.")
    fig = go.Figure()
    rows = [
        ("بيانات عالية التواتر (مبيعات، وبحث، ونقل)", 0, 1, PALETTE[0]),
        ("مسوح شهرية", 30, 45, PALETTE[1]),
        ("الناتج المحلي (تقدير أولي)", 0, 75, PALETTE[2]),
        ("الناتج المحلي (مراجَع)", 0, 165, PALETTE[3]),
    ]
    for i, (label, start, end, color) in enumerate(rows):
        fig.add_trace(go.Scatter(x=[start, end], y=[i, i], mode="lines+markers",
                                 line=dict(color=color, width=12), marker=dict(size=12),
                                 name=label, hovertext=f"{label}: يصدر بعد ~{end} يومًا",
                                 hoverinfo="text"))
        fig.add_annotation(x=end, y=i, text=f"  {label}", showarrow=False, xanchor="left",
                           font=dict(size=11))
    fig.update_xaxes(title="أيام بعد نهاية الفترة المرجعية", range=[-10, 260])
    fig.update_yaxes(visible=False, range=[-0.6, 3.8])
    fig.update_layout(showlegend=False)
    show(fig, 340, key="m10-nowcast")


@register("m10_text_as_data")
def text_as_data() -> None:
    flow([("مجموعة نصوص محددة", "Corpus"), ("قرار الاشتمال", "Selection"),
          ("المعالجة والتمثيل", "Representation"), ("قياس أو تصنيف", "Measurement"),
          ("مؤشر عددي", "Index"), ("تحقق خارجي", "Validation")],
         caption="النص بوصفه بيانات: المؤشر لا يكتسب معناه من طريقة الحساب بل من **التحقق الخارجي** منه.")
    st.caption("**أخطر خطوة هي الثانية:** ما الذي أدخلته في المجموعة وما الذي استبعدته؟ "
               "فقرار الاشتمال يحدد ما يقيسه مؤشرك فعلًا — وهو قرار **بحثي** لا تقني.")


@register("m10_j_curve")
def j_curve() -> None:
    st.caption("منحنى الإنتاجية على شكل J: الاستثمار في الأصول غير الملموسة (المهارات، وإعادة تنظيم "
               "العمليات، والبيانات) يُنفَق مبكرًا ويظهر عائده متأخرًا — فتبدو الإنتاجية المقيسة منخفضة أولًا.")
    t = np.linspace(0, 10, 200)
    measured = -0.35 * t * np.exp(-0.45 * t) * 3 + 0.16 * t
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=measured, mode="lines", name="الإنتاجية المقيسة",
                             line=dict(color=PALETTE[0], width=3)))
    fig.add_trace(go.Scatter(x=t, y=0.16 * t, mode="lines", name="الإنتاجية الحقيقية (تقديرًا)",
                             line=dict(color=PALETTE[4], width=3, dash="dash")))
    fig.add_hline(y=0, line=dict(color="#C7B8AE", width=1))
    fig.add_annotation(x=1.7, y=-0.55, text="مرحلة الاستثمار:<br>كلفة ظاهرة وعائد غير مقيس",
                       showarrow=True, arrowhead=2, ax=70, ay=-40, font=dict(size=11))
    fig.add_annotation(x=8.2, y=1.35, text="مرحلة الحصاد", showarrow=True, arrowhead=2,
                       ax=-60, ay=30, font=dict(size=11))
    fig.update_xaxes(title="الزمن منذ تبنّي التقنية")
    fig.update_yaxes(title="الإنتاجية")
    show(fig, 380, key="m10-jcurve")


@register("m10_task_framework")
def task_framework() -> None:
    grid_cards([
        ("أثر الإزاحة", "Displacement", "الآلة تحل محل العمل في مهام كان يؤديها البشر ← ينخفض الطلب على العمل."),
        ("أثر الإنتاجية", "Productivity", "انخفاض الكلفة يرفع الإنتاج والطلب ← قد يرتفع الطلب على العمل."),
        ("المهام الجديدة", "Reinstatement", "تظهر مهام جديدة يتفوق فيها البشر ← يعود الطلب على العمل ويتغير محتواه."),
        ("المحصلة", "Net effect", "**تجريبية لا نظرية**: تعتمد على أي الآثار يغلب، وهذا يختلف بالقطاع والفترة والسياسة."),
    ], cols=4)
    st.caption("إطار المهام: الأتمتة ليست «فقدان وظائف» ولا «خلق وظائف»، بل **ثلاثة آثار متزامنة** "
               "محصّلتها مسألة قياس لا مسألة رأي.")


@register("m10_leakage_types")
def leakage_types() -> None:
    grid_cards([
        ("تسرّب زمني", "Temporal leakage", "تدريب على بيانات لاحقة للفترة المتنبَّأ بها. **الأشيع في الاقتصاد**، وسببه التقسيم العشوائي لسلسلة زمنية."),
        ("تسرّب المعالجة", "Preprocessing", "تطبيع أو ملء قيم ناقصة **قبل** التقسيم، فتتسرب معلومات الاختبار إلى التدريب."),
        ("متغير وكيل", "Proxy leakage", "متغير يحمل المخرج نفسه بصورة أخرى (رقم الملف، وتاريخ التسجيل)."),
        ("تكرار السجلات", "Duplicates", "سجل واحد في التدريب والاختبار معًا، فتُقاس ذاكرة لا تعميمًا."),
        ("اختيار بعد النظر", "Selection", "اختيار العينة بشرط يعتمد على المستقبل (مثل الشركات الباقية)."),
        ("ضبط على الاختبار", "Test-set tuning", "تكرار الضبط حتى تتحسن نتيجة الاختبار — فيصير الاختبار جزءًا من التدريب."),
    ], cols=3)
