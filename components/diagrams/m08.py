"""Module 8 diagrams: concept map, the seven text-task types, the writing workflow,
the verification pipeline, a fluency-vs-correctness matrix, and the disclosure ladder."""

import plotly.graph_objects as go
import streamlit as st

from components.diagrams import PALETTE, flow, grid_cards, network, register, show


@register("m08_concept_map")
def concept_map() -> None:
    nodes = [
        {"id": "t", "label": "المهام النصية", "x": 0, "y": 0, "group": 0},
        {"id": "ext", "label": "الاستخراج", "x": -2.2, "y": 1.0, "group": 1, "hover": "نقل ما في المصدر: يُقارن بالمصدر"},
        {"id": "tra", "label": "التحويل", "x": -2.4, "y": -0.4, "group": 1, "hover": "تلخيص، ترجمة، إعادة صياغة"},
        {"id": "gen", "label": "التوليد", "x": -1.2, "y": -1.7, "group": 2, "hover": "إنشاء جديد: لا إجابة صحيحة واحدة"},
        {"id": "cls", "label": "التصنيف", "x": 1.2, "y": -1.7, "group": 2},
        {"id": "ret", "label": "الاسترجاع", "x": 2.4, "y": -0.4, "group": 3},
        {"id": "rea", "label": "الاستدلال", "x": 2.2, "y": 1.0, "group": 3},
        {"id": "ver", "label": "التحقق", "x": 0, "y": 2.0, "group": 4, "hover": "قلب المحور: المصادر والأرقام والاقتباسات"},
        {"id": "int", "label": "النزاهة والإفصاح", "x": 0, "y": -2.6, "group": 5},
    ]
    edges = [("t", "ext"), ("ext", "tra"), ("tra", "gen"), ("t", "cls"), ("t", "ret"),
             ("ret", "rea"), ("t", "ver"), ("ver", "int"), ("gen", "int"), ("rea", "ver")]
    network(nodes, edges, height=500, key="m08-concept")


@register("m08_task_types")
def task_types() -> None:
    grid_cards([
        ("الاستخراج", "Extraction", "نقل معلومة موجودة في المصدر. **التحقق:** مقارنة حرفية بالمصدر. خطره الأكبر: ملء حقل غير مذكور."),
        ("التحويل", "Transformation", "إعادة تقديم محتوى موجود (تلخيص، ترجمة، إعادة صياغة). **التحقق:** الأمانة للمصدر."),
        ("التوليد", "Generation", "إنشاء محتوى جديد. **لا إجابة صحيحة واحدة**؛ التقييم بمعايير لا بمطابقة."),
        ("التصنيف", "Classification", "إسناد فئة من مجموعة محددة. **التحقق:** مقارنة بتصنيف بشري على عينة."),
        ("الاسترجاع", "Retrieval", "إحضار معلومة من مجموعة. **التحقق:** هل المقطع المسترجَع هو الصحيح؟"),
        ("الاستدلال", "Reasoning", "استنتاج من معطيات. **التحقق:** إعادة تنفيذ الخطوات بنفسك."),
        ("التحقق", "Verification", "فحص صحة ادعاء. **لا يُوكَل للنموذج وحده**: يحتاج إلى مصدر خارجي مستقل."),
    ], cols=4)


@register("m08_writing_workflow")
def writing_workflow() -> None:
    flow([("تحديد الهدف والجمهور", "Goal"), ("جمع المصادر وقراءتها", "Sources"),
          ("مخطط تكتبه أنت", "Outline"), ("مسودة", "Draft"), ("مراجعة المضمون", "Content review"),
          ("تحقق من الوقائع", "Fact-check"), ("تحرير لغوي", "Edit"), ("إفصاح", "Disclosure")],
         caption="مسار الكتابة الأكاديمية: الأداة تساعد في خطوات محددة، والمخطط والحكم والتحقق للباحث.")
    st.caption("**القاعدة:** كلما اقتربت الخطوة من **الحكم العلمي** (اختيار المصادر، المخطط، الاستنتاج)، "
               "قلّ دور الأداة وزاد دورك. وكلما اقتربت من **الشكل** (اللغة، التنسيق)، جاز العكس.")


@register("m08_verification_pipeline")
def verification_pipeline() -> None:
    flow([("استخرج الادعاءات", "Extract claims"), ("صنّفها حسب النوع", "Classify"),
          ("حدد الأولوية بالأثر", "Prioritize"), ("ابحث عن المصدر الأولي", "Find primary source"),
          ("قارن حرفيًا", "Compare"), ("سجّل النتيجة", "Record")],
         caption="مسار التحقق: من نص كامل إلى ادعاءات مفردة قابلة للفحص واحدًا واحدًا.")


@register("m08_fluency_matrix")
def fluency_matrix() -> None:
    st.caption("العلاقة بين **طلاقة** النص و**صحته** ضعيفة. والخانة الخطرة هي أعلى اليسار: "
               "نص فصيح ومقنع وخاطئ، لأنه يمر دون أن يثير الشك.")
    fig = go.Figure()
    cells = [
        (0.25, 0.75, "فصيح وخاطئ", "**الخانة الخطرة**: يقنع القارئ ويمر بلا فحص", "#C8553D"),
        (0.75, 0.75, "فصيح وصحيح", "المطلوب — ولا يُعرف إلا بالتحقق", "#5E8C61"),
        (0.25, 0.25, "ركيك وخاطئ", "يُكتشف بسهولة", "#F2A541"),
        (0.75, 0.25, "ركيك وصحيح", "يحتاج تحريرًا لا تصحيحًا", "#5B9BD5"),
    ]
    for x, y, label, note, color in cells:
        fig.add_shape(type="rect", x0=x - 0.24, x1=x + 0.24, y0=y - 0.24, y1=y + 0.24,
                      fillcolor=color, opacity=0.18, line=dict(color=color, width=2))
        fig.add_annotation(x=x, y=y + 0.07, text=f"<b>{label}</b>", showarrow=False, font=dict(size=14))
        fig.add_annotation(x=x, y=y - 0.09, text=note, showarrow=False, font=dict(size=11, color="#5A4A45"))
    fig.update_xaxes(title="الصحة ←", range=[0, 1], showticklabels=False)
    fig.update_yaxes(title="الطلاقة ←", range=[0, 1], showticklabels=False)
    show(fig, 400, key="m08-fluency")


@register("m08_claim_types")
def claim_types() -> None:
    grid_cards([
        ("ادعاء واقعي", "Factual claim", "«صدر القانون سنة 2024». **التحقق:** المصدر الرسمي."),
        ("رقم أو إحصاء", "Statistic", "«ارتفع 12%». **التحقق:** المصدر الأولي للبيانات لا نقلًا عن نقل."),
        ("استشهاد", "Citation", "«وفق دراسة س». **التحقق:** وجود الدراسة + أنها تقول ذلك فعلًا."),
        ("اقتباس", "Quotation", "نص منسوب لشخص. **التحقق:** الصياغة الحرفية والسياق والمصدر."),
        ("تعريف أو مفهوم", "Definition", "**التحقق:** مرجع معتمد في التخصص، فالتعريفات تختلف بين المدارس."),
        ("استنتاج", "Inference", "«إذن فإن…». **التحقق:** هل يتبع من المعطيات؟ وهل قفز من تزامن إلى سببية؟"),
    ], cols=3)


@register("m08_disclosure_ladder")
def disclosure_ladder() -> None:
    rows = [
        ("تحرير لغوي فقط", "تصحيح إملاء ونحو لنص كتبته أنت", "إفصاح مختصر عادةً", "#5E8C61"),
        ("إعادة صياغة", "تحسين أسلوب فقرات كتبتها أنت", "إفصاح واضح", "#F2A541"),
        ("توليد محتوى", "فقرات أو أقسام ولّدتها الأداة", "إفصاح تفصيلي + تحقق كامل", "#E07A5F"),
        ("توليد تحليل أو استنتاج", "الحكم العلمي نفسه", "**غالبًا غير مقبول** أكاديميًا", "#C8553D"),
    ]
    html = ""
    for i, (title, what, req, color) in enumerate(rows):
        html += (f'<div class="tile" style="background:#FFFDF9;border-top:5px solid {color};'
                 f'margin-right:{i * 1.2}rem"><b>{title}</b><small>{what}</small>'
                 f'<p>{req}</p></div>')
    st.html(f'<div class="tiles" style="--cols:1">{html}</div>')
    st.caption("**سلّم إرشادي فقط.** القاعدة الملزمة هي **سياسة مؤسستك ومجلتك**، وهي تختلف وتتغير. "
               "والمبدأ المشترك في المواقف الرسمية: الأداة لا تكون مؤلفًا، والاستعمال يُفصَح عنه.")
