"""Module 1 diagrams: concept map, capabilities, four approaches, agent, OECD system,
functions, automation vs augmentation, fields map."""

import plotly.graph_objects as go
import streamlit as st

from components.diagrams import PALETTE, SOFT, flow, grid_cards, network, register, show
from components.layout import esc


@register("m01_concept_map")
def concept_map() -> None:
    nodes = [
        {"id": "ai", "label": "الذكاء الاصطناعي", "x": 0, "y": 0, "group": 0,
         "hover": "Artificial Intelligence: حقل علمي وهندسي"},
        {"id": "def", "label": "التعريفات", "x": -1.6, "y": 1.0, "group": 1, "hover": "المحاضرة 1.1: أربع مقاربات + تعريف OECD"},
        {"id": "cap", "label": "قدرات الذكاء", "x": -2.4, "y": 0.1, "group": 1, "hover": "إدراك، استدلال، تعلم، تخطيط، لغة، قرار"},
        {"id": "fun", "label": "الوظائف", "x": 1.6, "y": 1.0, "group": 2, "hover": "المحاضرة 1.2: تنبؤ، تصنيف، توليد، تحسين…"},
        {"id": "aug", "label": "أتمتة / تعزيز", "x": 2.4, "y": 0.1, "group": 2, "hover": "خيار تصميمي له آثار اقتصادية"},
        {"id": "fld", "label": "الفروع", "x": -1.3, "y": -1.1, "group": 3, "hover": "المحاضرة 1.3: NLP، رؤية، روبوتات، تعلم آلي…"},
        {"id": "app", "label": "التطبيقات", "x": 1.3, "y": -1.1, "group": 4, "hover": "المحاضرة 1.4: تعليم، طب، اقتصاد، مالية…"},
        {"id": "mis", "label": "المفاهيم الخاطئة", "x": 0, "y": -1.9, "group": 5, "hover": "المحاضرة 1.5: AI ≠ روبوت، AI ≠ ML…"},
        {"id": "sys", "label": "نظام / نموذج", "x": 0, "y": 1.6, "group": 6, "hover": "امتداد حديث: AI system ≠ AI model"},
    ]
    edges = [("ai", "def"), ("def", "cap"), ("ai", "fun"), ("fun", "aug"), ("ai", "fld"),
             ("fld", "app"), ("fun", "app"), ("ai", "mis"), ("def", "sys"), ("app", "mis")]
    network(nodes, edges, height=470, key="m01-concept")


@register("m01_capabilities")
def capabilities() -> None:
    grid_cards([
        ("الإدراك", "Perception", "تحويل الصور والأصوات والإشارات إلى تمثيل ذي معنى."),
        ("الاستدلال", "Reasoning", "استخلاص نتائج جديدة من معارف وقواعد قائمة."),
        ("التعلم", "Learning", "تحسين الأداء بالخبرة والبيانات."),
        ("التخطيط", "Planning", "اختيار سلسلة أفعال توصل إلى هدف."),
        ("اللغة", "Language", "فهم اللغة الطبيعية وإنتاجها."),
        ("اتخاذ القرار", "Decision making", "الاختيار بين بدائل في ظل عدم اليقين."),
        ("حل المشكلات", "Problem solving", "البحث عن حل في فضاء واسع من الاحتمالات."),
        ("التكيف", "Adaptation", "تعديل السلوك عند تغير البيئة."),
        ("التعميم", "Generalization", "النجاح في حالات جديدة لم تُرَ أثناء التعلم."),
    ], cols=3)


@register("m01_four_approaches")
def four_approaches() -> None:
    cells = [
        ("التفكير كالإنسان", "Thinking humanly", "النمذجة المعرفية: هل يفكر كما نفكر؟", 0),
        ("التفكير العقلاني", "Thinking rationally", "قوانين الفكر: هل يستدل استدلالًا صحيحًا؟", 2),
        ("الفعل كالإنسان", "Acting humanly", "اختبار تورينغ: هل نميّزه عن الإنسان؟", 3),
        ("الفعل العقلاني", "Acting rationally", "الوكيل العقلاني: هل يختار أفضل فعل؟ (مقاربة AIMA)", 1),
    ]
    tiles = "".join(
        f'<div class="tile" style="background:{SOFT[c]};border-top:5px solid {PALETTE[c]};'
        f'{"outline:3px solid " + PALETTE[c] + ";" if i == 3 else ""}">'
        f"<b>{esc(ar)}</b><small>{esc(en)}</small><p>{esc(t)}</p></div>"
        for i, (ar, en, t, c) in enumerate(cells)
    )
    st.html(
        '<div class="tiles" style="--cols:2">' + tiles + "</div>"
        '<div class="flow-caption">الصف الأول: التفكير · الصف الثاني: الفعل — العمود الأيمن: المعيار البشري · '
        "العمود الأيسر: المعيار العقلاني. الخانة المؤطرة هي المقاربة التي يتبناها Russell وNorvig.</div>"
    )


@register("m01_agent")
def agent() -> None:
    flow([("البيئة", "Environment"), ("الحساسات: الإدراك", "Sensors · percepts"),
          ("الوكيل: الاختيار وفق مقياس الأداء", "Agent function"), ("المشغلات: الفعل", "Actuators · actions")],
         loop=True, caption="الوكيل يدرك البيئة ويفعل فيها، ثم يدرك أثر فعله: حلقة مستمرة.")


@register("m01_oecd_system")
def oecd_system() -> None:
    flow([("أهداف صريحة أو ضمنية", "Objectives"), ("المدخلات", "Input"),
          ("الاستنتاج", "Infers how to generate outputs"),
          ("المخرجات: تنبؤات · محتوى · توصيات · قرارات", "Outputs"),
          ("التأثير في بيئة مادية أو افتراضية", "Environment")],
         caption="تعريف OECD (2024) لنظام الذكاء الاصطناعي، مع درجات متفاوتة من الاستقلالية والتكيف بعد النشر.")


@register("m01_functions")
def functions() -> None:
    grid_cards([
        ("التنبؤ", "Prediction", "تقدير قيمة غير معروفة: الطلب غدًا، احتمال الاحتيال."),
        ("التصنيف", "Classification", "تنبؤ بفئة: مزعجة / عادية، مقبول / مرفوض."),
        ("التوليد", "Generation", "إنتاج محتوى جديد: نص، صورة، صوت، شيفرة."),
        ("التحسين", "Optimization", "أفضل حل ضمن قيود: مسار، جدول، تكلفة."),
        ("التعرف على الأنماط", "Pattern recognition", "اكتشاف بنى منتظمة: وجوه، كلمات، شذوذ."),
        ("دعم القرار", "Decision support", "معلومات وتوصيات، والقرار للإنسان."),
        ("الأتمتة", "Automation", "النظام يؤدي المهمة بدل الإنسان."),
        ("التعزيز", "Augmentation", "النظام يوسّع قدرة الإنسان ويبقيه في المركز."),
    ], cols=4)


@register("m01_automation_augmentation")
def automation_augmentation() -> None:
    tasks = [("فرز الطرود", 0.95, 0.15), ("تفريغ التسجيلات الصوتية", 0.8, 0.45), ("ترجمة مسودة", 0.55, 0.75),
             ("تشخيص طبي بالصور", 0.3, 0.9), ("كتابة تقرير بحثي", 0.2, 0.8), ("منح قرض صغير", 0.75, 0.5),
             ("تصحيح مقالات", 0.45, 0.7), ("خدمة عملاء بسيطة", 0.7, 0.35)]
    fig = go.Figure(go.Scatter(
        x=[t[1] for t in tasks], y=[t[2] for t in tasks], mode="markers+text",
        text=[t[0] for t in tasks], textposition="top center",
        marker=dict(size=18, color=PALETTE[: len(tasks)], line=dict(color="#FFFFFF", width=2)),
        hovertemplate="%{text}<extra></extra>"))
    fig.add_annotation(x=0.9, y=0.03, text="منطقة الأتمتة", showarrow=False, font=dict(color="#C8553D", size=14))
    fig.add_annotation(x=0.12, y=1.0, text="منطقة التعزيز", showarrow=False, font=dict(color="#7A5AA6", size=14))
    fig.update_xaxes(title="قابلية الأتمتة التقنية للمهمة", range=[0, 1.05], showticklabels=False)
    fig.update_yaxes(title="أهمية الحكم البشري وكلفة الخطأ", range=[0, 1.08], showticklabels=False)
    show(fig, 430, key="m01-autoaug")
    st.caption("رسم توضيحي مفاهيمي: المواقع تقديرية لأغراض النقاش، وليست قياسًا تجريبيًا.")


@register("m01_fields_map")
def fields_map() -> None:
    nodes = [
        {"id": "ai", "label": "الذكاء الاصطناعي", "x": 0, "y": 0, "group": 0},
        {"id": "ml", "label": "التعلم الآلي", "x": 0, "y": -1.1, "group": 1, "hover": "Machine Learning: منهج أفقي يخدم كل الفروع"},
        {"id": "dl", "label": "التعلم العميق", "x": 0, "y": -2.0, "group": 1},
        {"id": "gen", "label": "الذكاء التوليدي", "x": 1.2, "y": -2.2, "group": 1},
        {"id": "nlp", "label": "معالجة اللغة", "x": -2.0, "y": 0.9, "group": 2, "hover": "NLP"},
        {"id": "cv", "label": "الرؤية الحاسوبية", "x": -0.7, "y": 1.5, "group": 2, "hover": "Computer Vision"},
        {"id": "sp", "label": "الكلام", "x": -2.4, "y": -0.3, "group": 2, "hover": "Speech"},
        {"id": "rob", "label": "الروبوتات", "x": 0.8, "y": 1.5, "group": 3, "hover": "Robotics"},
        {"id": "plan", "label": "التخطيط والبحث", "x": 2.1, "y": 0.9, "group": 3, "hover": "Planning & Search"},
        {"id": "es", "label": "الأنظمة الخبيرة", "x": 2.4, "y": -0.3, "group": 4, "hover": "Expert Systems"},
        {"id": "rec", "label": "أنظمة التوصية", "x": -1.3, "y": -2.0, "group": 4, "hover": "Recommender Systems"},
    ]
    edges = [("ai", x) for x in ("nlp", "cv", "sp", "rob", "plan", "es", "ml")] + [
        ("ml", "dl"), ("dl", "gen"), ("ml", "rec"), ("ml", "nlp"), ("ml", "cv"), ("ml", "sp")]
    network(nodes, edges, height=520, key="m01-fields")
    st.caption("الفروع الموجهة بالمهمة (اللغة، الرؤية، الروبوتات…) تستعمل التعلم الآلي منهجًا مشتركًا؛ "
               "لذلك يظهر التعلم الآلي مرتبطًا بعدة فروع وليس فرعًا معزولًا.")


@register("m01_voice_assistant")
def voice_assistant() -> None:
    flow([("الكلام → نص", "ASR · Speech"), ("فهم القصد والكيانات", "NLP · understanding"),
          ("استدعاء خدمة الطقس", "Retrieval · API"), ("صياغة الجواب", "NLP · generation"),
          ("نص → كلام", "TTS · Speech")],
         caption="المساعد الصوتي: خمس حلقات من فروع مختلفة، وخطأ أي حلقة ينتقل إلى ما بعدها.")


@register("m01_case_frame")
def case_frame() -> None:
    flow([("السياق", "Context"), ("دور الذكاء الاصطناعي", "AI role"), ("البيانات", "Data"),
          ("الفوائد", "Benefits"), ("المخاطر", "Risks"), ("التحقق", "Verification"),
          ("الرقابة البشرية", "Human oversight")],
         caption="الإطار السباعي لتحليل أي تطبيق أو حالة دراسية في المقرر.")


@register("m01_app_questions")
def app_questions() -> None:
    levels = ["إعلان تجاري", "عرض تجريبي", "تقييم معياري", "دراسة محكّمة", "تجربة ميدانية"]
    fig = go.Figure(go.Bar(x=list(range(1, 6)), y=levels, orientation="h",
                           marker_color=["#F4D3C4", "#F2B89E", "#EC9C7C", "#DB7B5C", "#C45A44"],
                           hovertemplate="%{y}: المستوى %{x}<extra></extra>"))
    fig.update_xaxes(title="قوة الدليل (ترتيب تقريبي)", tickvals=[1, 2, 3, 4, 5])
    fig.update_yaxes(side="right")
    show(fig, 300, key="m01-evidence")
    st.caption("سلّم تقريبي لقوة الأدلة على أثر تطبيق ما. الترتيب توجيهي لأغراض القراءة النقدية، وليس تصنيفًا صارمًا.")


@register("m01_misconceptions_map")
def misconceptions_map() -> None:
    nodes = [
        {"id": "c", "label": "إسقاط صفات بشرية أو سحرية", "x": 0, "y": 0, "group": 0},
        {"id": "1", "label": "AI = روبوت", "x": -1.8, "y": 0.9, "group": 1, "hover": "← المحاضرة 1.3"},
        {"id": "2", "label": "AI = ML", "x": 0, "y": 1.4, "group": 1, "hover": "← المحور 4"},
        {"id": "3", "label": "يفهم كالإنسان", "x": 1.8, "y": 0.9, "group": 2, "hover": "← المحور 7"},
        {"id": "4", "label": "صحيح دائمًا", "x": 1.8, "y": -0.9, "group": 2, "hover": "← المحور 8"},
        {"id": "5", "label": "مستقل دائمًا", "x": 0, "y": -1.4, "group": 3, "hover": "← المحور 13"},
        {"id": "6", "label": "الأكبر أفضل", "x": -1.8, "y": -0.9, "group": 3, "hover": "← المحور 7"},
    ]
    network(nodes, [("c", k) for k in "123456"], height=420, key="m01-misc")
