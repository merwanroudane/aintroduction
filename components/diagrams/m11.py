"""Module 11 diagrams: concept map, the harm taxonomy, where bias enters the pipeline, the
three families of fairness definitions, a numeric illustration of the impossibility result,
the layers of transparency, the documentation stack, and the governance map."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from components.diagrams import PALETTE, flow, grid_cards, nested, network, register, show


@register("m11_concept_map")
def concept_map() -> None:
    nodes = [
        {"id": "eth", "label": "أخلاقيات الذكاء الاصطناعي", "x": 0, "y": 0, "group": 0},
        {"id": "bias", "label": "التحيّز", "x": -2.4, "y": 1.1, "group": 1,
         "hover": "من أين يأتي؟ من كل مرحلة في مسار البيانات — لا من متغير واحد"},
        {"id": "proxy", "label": "المتغير الوكيل", "x": -2.6, "y": -0.4, "group": 1,
         "hover": "متغير يبدو محايدًا وينقل التحيّز كاملًا"},
        {"id": "fair", "label": "تعريفات الإنصاف", "x": 0, "y": 2.1, "group": 2,
         "hover": "ثلاث عائلات: التكافؤ الديموغرافي، وتكافؤ الأخطاء، والمعايرة"},
        {"id": "imp", "label": "التعارض المُثبَت", "x": 0, "y": -2.2, "group": 2,
         "hover": "لا يمكن تحقيق المعايير الرئيسية معًا إذا اختلفت المعدلات القاعدية"},
        {"id": "trans", "label": "الشفافية", "x": 2.4, "y": 1.1, "group": 3,
         "hover": "قابلية التفسير بالتصميم ≠ تفسير لاحق مُلحَق بصندوق أسود"},
        {"id": "doc", "label": "التوثيق والتدقيق", "x": 2.6, "y": -0.4, "group": 3,
         "hover": "بطاقة النموذج، وصحيفة البيانات، والتدقيق الخارجي"},
        {"id": "gov", "label": "الحكامة", "x": 0, "y": -3.4, "group": 4,
         "hover": "من يقرر المعيار؟ ومن يتحمّل الكلفة؟ ومن يُلزِم؟"},
    ]
    edges = [("eth", "bias"), ("bias", "proxy"), ("eth", "fair"), ("fair", "imp"),
             ("imp", "gov"), ("eth", "trans"), ("trans", "doc"), ("doc", "gov"),
             ("proxy", "imp")]
    network(nodes, edges, height=520, key="m11-concept")


@register("m11_harm_types")
def harm_types() -> None:
    st.caption("قبل الحديث عن العدالة، يلزم تحديد **نوع الضرر**: فلكل نوع مقياس مختلف وعلاج مختلف، "
               "وجمعها كلها تحت كلمة «تحيّز» هو ما يجعل النقاش يدور بلا نتيجة.")
    grid_cards([
        ("ضرر التخصيص", "Allocative harm",
         "النظام يحجب موردًا أو فرصة: قرضًا، أو وظيفة، أو منحة، أو علاجًا. **قابل للقياس** بمقارنة "
         "معدلات القبول والأخطاء بين الفئات."),
        ("ضرر التمثيل", "Representational harm",
         "النظام يثبّت صورة نمطية أو يُغيّب فئة، دون أن يحجب موردًا مباشرة. **أصعب في القياس** وأطول أثرًا."),
        ("ضرر الجودة", "Quality-of-service harm",
         "النظام يعمل، لكنه **يعمل أسوأ** لفئة بعينها: تعرّف صوتي أدق في لغة، وتشخيص أدق في لون بشرة."),
        ("ضرر الحرمان", "Denial of self-identity",
         "النظام يصنّف الشخص تصنيفًا يرفضه أو لا يعترف به، فيفرض عليه فئة ليست فئته."),
    ], cols=2)


@register("m11_bias_pipeline")
def bias_pipeline() -> None:
    flow([("الظاهرة في المجتمع", "World"), ("ما الذي قِيس؟", "Measurement"),
          ("من دخل العينة؟", "Sampling"), ("كيف وُسِمت البيانات؟", "Labels"),
          ("ما المتغير الهدف؟", "Target choice"), ("كيف تعلّم النموذج؟", "Learning"),
          ("كيف استُعمل القرار؟", "Deployment")],
         caption="التحيّز لا يدخل من باب واحد: لكل خطوة بابها، ومعالجة واحدة لا تكفي.")
    st.caption("**والخطوة الخامسة هي الأخطر وأقلها انتباهًا:** اختيار المتغير الهدف قرار **قِيَمي** "
               "لا تقني — فمن يقرر أن «التكلفة» تمثّل «الحاجة» قد حسم سؤالًا أخلاقيًا في سطر رمز.")


@register("m11_fairness_definitions")
def fairness_definitions() -> None:
    st.caption("ثلاث عائلات من التعريفات، كلها مبنية من مصفوفة الالتباس نفسها، وكلها معقولة أخلاقيًا — "
               "ومع ذلك **لا تجتمع** عند اختلاف المعدلات القاعدية.")
    grid_cards([
        ("التكافؤ الديموغرافي", "Demographic parity",
         "**الشرط:** نسبة القبول متساوية بين الفئات. **الحدس:** النتائج يجب أن تُوزَّع بالتساوي. "
         "**الاعتراض:** يتجاهل الاستحقاق تمامًا، وقد يفرض قبول من لا يستوفي الشرط."),
        ("تكافؤ الأخطاء", "Equalized odds / Equal opportunity",
         "**الشرط:** معدل الخطأ متساوٍ بين الفئات — إيجابي كاذب وسلبي كاذب (أو السلبي وحده). "
         "**الحدس:** لا فئة تتحمّل أخطاء أكثر. **الاعتراض:** قد يُلزِم بعتبات مختلفة لكل فئة."),
        ("المعايرة", "Calibration / Predictive parity",
         "**الشرط:** الدرجة تعني الشيء نفسه لكل فئة — من أُعطي 0.7 يتحقق فيه الحدث بنسبة 70٪ في كل فئة. "
         "**الحدس:** الرقم يجب أن يكون صادقًا. **الاعتراض:** متوافق مع فجوات كبيرة في الأخطاء."),
        ("الإنصاف الفردي", "Individual fairness",
         "**الشرط:** المتشابهان في ما يخص القرار يُعامَلان معاملة متشابهة. **الحدس:** الأقرب إلى العدل "
         "الحدسي. **الاعتراض:** يحتاج تعريف «التشابه»، وهو نفسه قرار قِيَمي مُربِك."),
    ], cols=2)


def _calibrated_errors(a: float, b: float, t: float = 0.5, n: int = 20001):
    """Error rates for a PERFECTLY calibrated score.

    The score s has density Beta(a, b) and, by construction, P(Y=1 | s) = s — so the score is
    calibrated by definition, for any group. Everything below is then forced, not chosen:
        base rate = E[s]
        FPR = P(s > t | Y = 0) = ∫_t^1 f(s)(1-s) ds / ∫_0^1 f(s)(1-s) ds
        FNR = P(s ≤ t | Y = 1) = ∫_0^t f(s) s   ds / ∫_0^1 f(s) s   ds
    Integrals are evaluated on a grid, so the figure reports derived numbers, not assumed ones.
    """
    s = np.linspace(1e-6, 1 - 1e-6, n)
    f = s ** (a - 1) * (1 - s) ** (b - 1)
    f /= np.trapezoid(f, s)
    above = s > t
    neg, pos = f * (1 - s), f * s
    base = float(np.trapezoid(pos, s))
    fpr = float(np.trapezoid(neg[above], s[above]) / np.trapezoid(neg, s))
    fnr = float(np.trapezoid(pos[~above], s[~above]) / np.trapezoid(pos, s))
    return base, fpr, fnr


@register("m11_impossibility")
def impossibility() -> None:
    st.caption("التعارض المُثبَت، مرسومًا: نظام **معايَر تمامًا** لفئتين تختلف معدلاتهما القاعدية. "
               "المعايرة محقَّقة بالبناء — وانظر ماذا يحدث لمعدلات الخطأ.")
    # Two groups sharing one threshold. The score is calibrated for BOTH by construction; the
    # only difference is the score distribution, hence the base rate. The errors are then derived.
    (base_a, fpr_a, fnr_a) = _calibrated_errors(2.0, 6.0, t=0.4)
    (base_b, fpr_b, fnr_b) = _calibrated_errors(2.0, 3.0, t=0.4)
    labels = [f"الفئة أ (المعدل القاعدي {base_a:.0%})", f"الفئة ب (المعدل القاعدي {base_b:.0%})"]
    fpr, fnr = [fpr_a, fpr_b], [fnr_a, fnr_b]
    fig = go.Figure()
    fig.add_trace(go.Bar(name="معدل الإيجابي الكاذب", x=labels, y=fpr,
                         marker_color=PALETTE[0], text=[f"{v:.0%}" for v in fpr],
                         textposition="outside"))
    fig.add_trace(go.Bar(name="معدل السلبي الكاذب", x=labels, y=fnr,
                         marker_color=PALETTE[4], text=[f"{v:.0%}" for v in fnr],
                         textposition="outside"))
    fig.update_yaxes(title="معدل الخطأ", range=[0, 0.85], tickformat=".0%")
    fig.update_layout(barmode="group", legend=dict(orientation="h", y=1.12))
    show(fig, 380, key="m11-impossibility")
    st.caption(
        "**النتيجة:** المعايرة محقَّقة للفئتين بالبناء، والعتبة **واحدة** لا عتبتين، ومع ذلك الأخطاء "
        "**غير متكافئة** — بل تنقلب جهتها: الفئة الأقل معدلًا قاعديًا تتحمّل **سلبيات كاذبة** أكثر، "
        "والفئة الأعلى تتحمّل **إيجابيات كاذبة** أكثر. ولو أجبرتَ الأخطاء على التكافؤ لانكسرت المعايرة. "
        "وهذا ليس عطبًا في النظام ولا نقصًا في الخوارزمية: **هو نتيجة رياضية** تلزم كلما اختلفت المعدلات "
        "القاعدية. والأرقام محسوبة من توزيعي درجات محددين عند عتبة 0.4، والبنية عامة لا تتعلق بهما."
    )


@register("m11_transparency_layers")
def transparency_layers() -> None:
    nested([
        ("الحكامة والمساءلة", "Accountability", "من المسؤول؟ وما سبيل الطعن والتصحيح؟ — الطبقة التي تجعل البقية ذات أثر."),
        ("التوثيق", "Documentation", "بطاقة نموذج وصحيفة بيانات: ما بُني، وعلى ماذا، ولأي استعمال، وما حدوده."),
        ("قابلية التفسير بالتصميم", "Interpretability", "نموذج يمكن لإنسان تتبّع منطقه: شجرة قصيرة، أو نظام نقاط، أو انحدار خطي."),
        ("التفسير اللاحق", "Post-hoc explanation", "تقريب يُلحَق بصندوق أسود بعد بنائه: يفيد التشخيص، ولا يثبت أن النموذج يعمل كما يقول التفسير."),
    ], caption="الشفافية طبقات لا خاصية واحدة. ونشر الرمز وحده ليس أيًّا من هذه الطبقات.")


@register("m11_documentation_stack")
def documentation_stack() -> None:
    grid_cards([
        ("صحيفة البيانات", "Datasheet for a dataset",
         "من جمع البيانات؟ ولماذا؟ ومن يظهر فيها ومن يغيب؟ وكيف وُسِمت، وبأي تعليمات، ومن وسّمها؟ "
         "وما الاستعمالات غير الملائمة لها؟"),
        ("بطاقة النموذج", "Model card",
         "ما الاستعمال المقصود وما غير المقصود؟ وما الأداء **مُفصّلًا بحسب الفئات** لا في المتوسط؟ "
         "وبأي بيانات قُيِّم؟ وما الحدود والاعتبارات الأخلاقية؟"),
        ("التدقيق الخارجي", "External audit",
         "فحص مستقل بمعايير معلنة على بيانات اختبار مصمّمة للكشف. **الاستقلال شرط**: التدقيق الذاتي "
         "يفحص ما تعرف أن تبحث عنه."),
        ("سبيل الطعن", "Recourse",
         "كيف يعرف المتأثر أن قرارًا آليًا مسّه؟ وكيف يطلب مراجعته؟ **ودون هذا يبقى التوثيق ورقًا**."),
    ], cols=2)
    st.caption("**الخانة الأصعب في كل بطاقة نموذج هي «الحدود».** فمن لا يستطيع كتابتها كتابة محددة "
               "لا يعرف نظامه بعد.")


@register("m11_governance_map")
def governance_map() -> None:
    st.caption("من المبادئ إلى الإلزام: أربع طبقات تختلف في **قوة الإلزام** لا في نبل المبادئ.")
    grid_cards([
        ("مبادئ دولية", "Principles",
         "توصيات ومبادئ متعددة الأطراف: مرجع قِيَمي مشترك وأساس للسياسات الوطنية. "
         "**قوة الإلزام: أدبية وسياسية.**"),
        ("أطر إدارة المخاطر", "Risk frameworks",
         "إطار عملي يحوّل المبادئ إلى وظائف متكررة — الحكم، والتخطيط، والقياس، والإدارة. "
         "**قوة الإلزام: طوعية، إلا إذا فُرضت تعاقديًا.**"),
        ("تشريع ملزم", "Binding law",
         "تصنيف بحسب مستوى المخاطر مع التزامات مقابلة وعقوبات. "
         "**قوة الإلزام: قانونية، في نطاقها الجغرافي.**"),
        ("سياسة المؤسسة", "Institutional policy",
         "ما يُطبَّق فعلًا في جامعة أو بنك أو وزارة: إجراءات، وأدوار، ومراجعة. "
         "**قوة الإلزام: هي الطبقة التي تمسّ عملك مباشرة.**"),
    ], cols=2)
