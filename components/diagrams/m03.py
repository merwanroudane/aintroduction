"""Module 3 diagrams: concept map, capability classification, the scope/autonomy plane,
the four-type taxonomy, agent vs AGI, and the six confused concepts."""

import plotly.graph_objects as go
import streamlit as st

from components.diagrams import PALETTE, SOFT, flow, grid_cards, network, register, show
from components.layout import esc


@register("m03_concept_map")
def concept_map() -> None:
    nodes = [
        {"id": "t", "label": "أنواع الذكاء الاصطناعي", "x": 0, "y": 0, "group": 0},
        {"id": "ani", "label": "الضيق ANI", "x": -1.9, "y": 1.0, "group": 1, "hover": "متحقق: قوي في نطاق محدد"},
        {"id": "agi", "label": "العام AGI", "x": 0, "y": 1.7, "group": 2, "hover": "مفهوم محل نقاش: لا تعريف ولا مقياس متفق عليهما"},
        {"id": "asi", "label": "الفائق ASI", "x": 1.9, "y": 1.0, "group": 3, "hover": "مفهوم نظري بالكامل"},
        {"id": "four", "label": "التصنيف الرباعي", "x": -2.2, "y": -0.6, "group": 4, "hover": "تفاعلية، ذاكرة محدودة، نظرية عقل، وعي ذاتي — تصنيف تعليمي"},
        {"id": "cap", "label": "القدرة", "x": -1.1, "y": -1.7, "group": 5},
        {"id": "aut", "label": "الاستقلالية", "x": 0.3, "y": -2.0, "group": 5},
        {"id": "gen", "label": "التعميم", "x": 1.6, "y": -1.5, "group": 5},
        {"id": "ag", "label": "الوكيل الذكي", "x": 2.3, "y": -0.5, "group": 6, "hover": "Agent ≠ AGI"},
    ]
    edges = [("t", "ani"), ("ani", "agi"), ("agi", "asi"), ("t", "four"), ("t", "cap"),
             ("cap", "aut"), ("aut", "gen"), ("gen", "ag"), ("ag", "agi"), ("ani", "gen")]
    network(nodes, edges, height=500, key="m03-concept")


@register("m03_capability_levels")
def capability_levels() -> None:
    rows = [
        ("الذكاء الضيق", "Artificial Narrow Intelligence — ANI",
         "أنظمة قوية داخل نطاق محدد من المهام، وتفشل خارجه. **هذا هو الواقع المتحقق اليوم كله.**",
         "#E07A5F", "#FFF1EA", "متحقق"),
        ("الذكاء العام", "Artificial General Intelligence — AGI",
         "نظام افتراضي يؤدي أي مهمة فكرية يؤديها الإنسان، وينقل خبرته بين المجالات. **مفهوم محل نقاش: لا تعريف ولا مقياس متفق عليهما.**",
         "#8E7DBE", "#F3EEFF", "محل نقاش"),
        ("الذكاء الفائق", "Artificial Superintelligence — ASI",
         "نظام افتراضي يتجاوز أفضل العقول البشرية في كل المجالات. **مفهوم نظري بالكامل يُبحث في أدبيات المخاطر.**",
         "#5B9BD5", "#EAF5FE", "نظري"),
    ]
    html = ""
    for ar, en, desc, color, bg, status in rows:
        html += (
            f'<div class="tile" style="background:{bg};border-top:5px solid {color};margin-bottom:0.6rem">'
            f'<b>{esc(ar)}</b><small>{esc(en)}</small>'
            f'<p>{desc}</p>'
            f'<span class="card-badge" style="border-color:{color}">{esc(status)}</span></div>'
        )
    st.html(f'<div class="tiles" style="--cols:3">{html}</div>')
    st.caption("تنبيه منهجي: هذه **فئات مفاهيمية**، لا مراحل زمنية حتمية. الانتقال من فئة إلى أخرى ليس مضمونًا "
               "ولا يقع على مسار متصل (راجع مغالطة الاستمرارية في المحاضرة 2.5).")


@register("m03_scope_autonomy")
def scope_autonomy() -> None:
    systems = [
        ("منظم حرارة ذكي", 0.10, 0.55), ("مرشح الرسائل المزعجة", 0.12, 0.70),
        ("نظام توصية", 0.25, 0.60), ("مترجم آلي", 0.30, 0.25),
        ("نظام تشخيص بالصور", 0.20, 0.35), ("سيارة ذاتية القيادة", 0.35, 0.85),
        ("مساعد حواري عام", 0.72, 0.20), ("وكيل ذكي يستعمل أدوات", 0.70, 0.65),
        ("ذكاء عام افتراضي", 0.97, 0.90),
    ]
    fig = go.Figure(go.Scatter(
        x=[s[1] for s in systems], y=[s[2] for s in systems], mode="markers+text",
        text=[s[0] for s in systems], textposition="top center",
        marker=dict(size=[16] * (len(systems) - 1) + [22],
                    color=PALETTE[: len(systems) - 1] + ["#B0A7A2"],
                    symbol=["circle"] * (len(systems) - 1) + ["star"],
                    line=dict(color="#FFFFFF", width=2)),
        hovertemplate="%{text}<extra></extra>"))
    fig.add_annotation(x=0.97, y=0.80, text="افتراضي: غير متحقق", showarrow=False,
                       font=dict(size=11, color="#7D6E68"))
    fig.update_xaxes(title="اتساع النطاق (عدد المهام والمجالات)", range=[0, 1.1], showticklabels=False)
    fig.update_yaxes(title="مستوى الاستقلالية في التنفيذ", range=[0, 1.05], showticklabels=False)
    show(fig, 450, key="m03-scope")
    st.caption("بعدان مستقلان: نظام قد يكون **ضيق النطاق عالي الاستقلالية** (منظم الحرارة)، أو **واسع النطاق "
               "منخفض الاستقلالية** (المساعد الحواري). المواقع تقديرية لأغراض النقاش الصفي.")


@register("m03_four_types")
def four_types() -> None:
    grid_cards([
        ("الآلات التفاعلية", "Reactive Machines", "تستجيب للمدخل الحالي دون ذاكرة للماضي؛ المثال المتداول: Deep Blue."),
        ("الذاكرة المحدودة", "Limited Memory", "تستعمل بيانات سابقة ضمن نافذة محدودة؛ أغلب الأنظمة الحالية توصف بهذه الفئة."),
        ("نظرية العقل", "Theory of Mind", "افتراضية: نمذجة معتقدات الآخرين ونواياهم؛ المصطلح مستعار من علم النفس (1978)."),
        ("الوعي الذاتي", "Self-aware AI", "افتراضية بالكامل: وعي بالذات؛ لا يوجد إجماع حتى على كيفية اختبارها."),
    ], cols=4)
    st.caption("تنبيه: هذا تصنيف **تعليمي تبسيطي** شاع في الكتابات التعريفية، وليس تصنيفًا تقنيًا رسميًا "
               "ولا معيارًا معتمدًا. الفئتان الأخيرتان افتراضيتان.")


@register("m03_agent_vs_agi")
def agent_vs_agi() -> None:
    flow([("هدف من المستخدم", "Goal"), ("تخطيط بالنموذج", "Plan"), ("اختيار أداة مصرح بها", "Tool"),
          ("تنفيذ", "Act"), ("ملاحظة النتيجة", "Observe"), ("تحديث الحالة", "State")],
         loop=True, caption="حلقة الوكيل الذكي: تعمل كلها **داخل** أدوات وصلاحيات يمنحها البشر.")
    st.html(
        '<div class="tiles" style="--cols:2">'
        '<div class="tile" style="background:#EAF5FE;border-top:5px solid #5B9BD5">'
        '<b>الوكيل الذكي</b><small>AI Agent — يوجد اليوم</small>'
        '<p>نظام ضيق النطاق نسبيًا، يخطط ضمن أدوات محددة، وقدرته مستمدة من نموذج ومن الصلاحيات الممنوحة له. '
        'يفشل خارج نطاق أدواته، ولا يعرف أنه فشل.</p></div>'
        '<div class="tile" style="background:#F3EEFF;border-top:5px solid #8E7DBE">'
        '<b>الذكاء العام</b><small>AGI — مفهوم محل نقاش</small>'
        '<p>قدرة مفترضة على أداء أي مهمة فكرية بشرية ونقل الخبرة بين المجالات المختلفة، '
        'بما فيها مجالات لم يُدرَّب عليها إطلاقًا.</p></div></div>'
    )


@register("m03_six_concepts")
def six_concepts() -> None:
    grid_cards([
        ("القدرة", "Capability", "ما يستطيع النظام فعله في مهمة محددة، ويُقاس بمقياس أداء واضح."),
        ("الذكاء", "Intelligence", "قدرة على تحقيق أهداف في بيئات **متنوعة**، ومفتاحه التنوع لا الأداء وحده."),
        ("الاستقلالية", "Autonomy", "مقدار ما ينفذه النظام دون موافقة بشرية؛ خيار تصميمي لا صفة ذاتية."),
        ("الوكالة", "Agency", "قدرة النظام على المبادرة بأفعال في بيئته لتحقيق هدف، لا مجرد الاستجابة."),
        ("التكيف", "Adaptation", "تعديل السلوك عند تغير البيئة أو بعد النشر، وقد يكون مصدر مخاطر أيضًا."),
        ("التعميم", "Generalization", "النجاح في حالات جديدة لم تُرَ في التدريب؛ وهو جوهر الخلاف حول الذكاء العام."),
    ], cols=3)


@register("m03_levels")
def levels() -> None:
    st.caption("إطار المستويات: بدل سؤال ثنائي، وصف على بعدين. المواقع توضيحية لشرح الفكرة، "
               "وليست تصنيفًا رسميًا لأنظمة بعينها.")
    points = [
        ("حاسبة", 0.9, 0.05, "أداء فائق في مهمة واحدة محددة"),
        ("برنامج شطرنج", 0.95, 0.10, "أداء يفوق البشر، عمومية شبه معدومة"),
        ("نظام تشخيص بالصور", 0.75, 0.15, "أداء عالٍ في صنف ضيق"),
        ("مساعد حواري عام", 0.55, 0.60, "أداء متفاوت، عمومية أوسع"),
        ("إنسان بالغ كفء", 0.70, 0.95, "المرجع المقارن"),
        ("ذكاء عام افتراضي", 0.95, 0.95, "غير متحقق"),
    ]
    fig = go.Figure(go.Scatter(
        x=[p[2] for p in points], y=[p[1] for p in points], mode="markers+text",
        text=[p[0] for p in points], textposition="top center",
        hovertext=[f"<b>{p[0]}</b><br>{p[3]}" for p in points], hoverinfo="text",
        marker=dict(size=[16, 16, 16, 18, 20, 22],
                    color=["#F2A541", "#E07A5F", "#B56576", "#5B9BD5", "#5E8C61", "#B0A7A2"],
                    symbol=["circle"] * 5 + ["star"], line=dict(color="#FFFFFF", width=2))))
    fig.update_xaxes(title="العمومية: اتساع نطاق المهام", range=[0, 1.1], showticklabels=False)
    fig.update_yaxes(title="الأداء مقارنة بالبشر", range=[0, 1.1], showticklabels=False)
    show(fig, 430, key="m03-levels")


@register("m03_claim_checklist")
def claim_checklist() -> None:
    flow([("ما التعريف؟", "Definition"), ("ما المقياس؟", "Benchmark"),
          ("هل استُبعد التسرب؟", "Contamination"), ("هل اختُبرت المتانة؟", "Robustness"),
          ("قدرة أم استقلالية؟", "Capability vs autonomy"), ("من الناشر؟", "Source")],
         caption="ست خطوات لقراءة أي ادعاء عن قدرات نظام قبل تصديقه أو رفضه.")
