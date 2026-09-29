"""Module 5 diagrams: concept map, prompt anatomy, how context shifts the distribution,
zero/one/few-shot, the iterative improvement loop, and the weak→improved→structured ladder."""

import plotly.graph_objects as go
import streamlit as st

from components.diagrams import PALETTE, SOFT, flow, grid_cards, network, register, show
from components.layout import esc

COMPONENTS = [
    ("الدور", "Role", "من يتكلم؟ يضبط النبرة والمنظور، ولا يضيف معرفة."),
    ("المهمة", "Task", "ما المطلوب بالضبط؟ فعل واضح ومحدد."),
    ("السياق", "Context", "الخلفية والغرض ومن سيقرأ النتيجة ولماذا."),
    ("المدخل", "Input", "النص أو البيانات موضوع المعالجة، مفصولة بوضوح."),
    ("القيود", "Constraints", "ما يجب تجنبه: الطول، والمصادر المسموح بها، وما لا يُفترض."),
    ("الأمثلة", "Examples", "نماذج مدخل ومخرج تبيّن الشكل المطلوب."),
    ("شكل المخرج", "Output format", "جدول، أو قائمة، أو JSON، أو فقرات بعناوين."),
    ("الجمهور", "Audience", "لمن النص؟ يحدد المستوى والمصطلحات."),
    ("معيار النجاح", "Success criteria", "متى نعدّ الإجابة جيدة؟ وهو أكثر المكونات إهمالًا."),
]


@register("m05_concept_map")
def concept_map() -> None:
    nodes = [
        {"id": "p", "label": "الأمر (Prompt)", "x": 0, "y": 0, "group": 0},
        {"id": "comp", "label": "المكونات التسعة", "x": -2.0, "y": 1.1, "group": 1, "hover": "دور، مهمة، سياق، مدخل، قيود، أمثلة، شكل، جمهور، معيار"},
        {"id": "tech", "label": "التقنيات", "x": 2.0, "y": 1.1, "group": 2, "hover": "بلا أمثلة، بأمثلة قليلة، دور، فواصل، بنية"},
        {"id": "struct", "label": "البنية والفواصل", "x": 2.3, "y": -0.4, "group": 2},
        {"id": "iter", "label": "التحسين التكراري", "x": 1.2, "y": -1.7, "group": 3, "hover": "معيار → مجموعة اختبار → تغيير واحد → قياس"},
        {"id": "tmpl", "label": "قوالب الأوامر", "x": -1.2, "y": -1.7, "group": 3},
        {"id": "lim", "label": "الحدود", "x": -2.3, "y": -0.4, "group": 4, "hover": "لا يضيف معرفة، ولا يمنع الهلوسة، ولا يصلح مهمة سيئة التحديد"},
        {"id": "mech", "label": "لماذا تعمل؟ أثر السياق", "x": 0, "y": 2.0, "group": 5, "hover": "الأمر يزيح توزيع احتمالات الرمز التالي"},
    ]
    edges = [("p", "comp"), ("p", "tech"), ("tech", "struct"), ("p", "iter"), ("iter", "tmpl"),
             ("p", "lim"), ("comp", "mech"), ("tech", "mech"), ("comp", "tmpl")]
    network(nodes, edges, height=480, key="m05-concept")


@register("m05_prompt_anatomy")
def prompt_anatomy() -> None:
    st.caption("تشريح الأمر: تسعة مكونات. لا يلزم وجودها كلها في كل أمر، لكن **غياب المكوّن سبب فشل قابل للتشخيص**.")
    tiles = "".join(
        f'<div class="tile" style="background:{SOFT[i % len(SOFT)]};'
        f'border-top:5px solid {PALETTE[i % len(PALETTE)]}">'
        f"<b>{i + 1}. {esc(ar)}</b><small>{esc(en)}</small><p>{esc(desc)}</p></div>"
        for i, (ar, en, desc) in enumerate(COMPONENTS)
    )
    st.html(f'<div class="tiles" style="--cols:3">{tiles}</div>')


@register("m05_context_shift")
def context_shift() -> None:
    st.caption("لماذا يعمل الأمر؟ لأنه يزيح **توزيع احتمالات** ما سيكتبه النموذج. "
               "الأرقام أدناه توضيحية لشرح الفكرة، وليست مخرجات نموذج حقيقي.")
    words = ["ملخص عام", "قائمة نقاط", "جدول", "مقال طويل", "سؤال توضيحي"]
    bare = [0.42, 0.18, 0.05, 0.27, 0.08]
    structured = [0.06, 0.12, 0.71, 0.04, 0.07]
    fig = go.Figure()
    fig.add_trace(go.Bar(y=words, x=bare, orientation="h", name="أمر مقتضب: «لخّص هذا»",
                         marker_color="#E9B99A"))
    fig.add_trace(go.Bar(y=words, x=structured, orientation="h",
                         name="أمر منظم يطلب جدولًا بأعمدة محددة", marker_color="#C8553D"))
    fig.update_xaxes(title="احتمال أن يأخذ المخرج هذا الشكل (توضيحي)", range=[0, 0.8])
    fig.update_yaxes(side="right")
    fig.update_layout(barmode="group", legend=dict(orientation="h", y=1.16))
    show(fig, 380, key="m05-shift")


@register("m05_shot_types")
def shot_types() -> None:
    grid_cards([
        ("بلا أمثلة", "Zero-shot", "تعليمات فقط دون أمثلة. مناسب للمهام الشائعة والمعروفة، وأقصر وأرخص."),
        ("بمثال واحد", "One-shot", "مثال واحد يوضح الشكل المطلوب. مفيد حين يكون الشكل غير مألوف."),
        ("بأمثلة قليلة", "Few-shot", "3–5 أمثلة متنوعة. الأقوى في ضبط الشكل والنبرة والحالات الحدية."),
    ], cols=3)
    st.caption("توصي الأدلة الرسمية للمزودين (تم الاطلاع عليها في 2026-09-28) باستعمال أمثلة **متنوعة "
               "وممثلة للحالة الفعلية**، وتنبه إلى أن أمثلة متشابهة قد تجعل النموذج يلتقط نمطًا غير مقصود.")


@register("m05_iteration_loop")
def iteration_loop() -> None:
    flow([("حدد معيار النجاح", "Success criteria"), ("جهّز مجموعة اختبار ثابتة", "Test set"),
          ("اكتب النسخة الأولى", "Draft"), ("شغّل على كل الحالات", "Run"),
          ("صنّف الأخطاء", "Diagnose"), ("غيّر عنصرًا واحدًا", "One change"),
          ("قِس وقارن", "Measure")],
         loop=True,
         caption="دورة التحسين المنضبطة: تغيير **عنصر واحد** في كل دورة، وإلا استحال معرفة سبب التحسن.")


@register("m05_prompt_ladder")
def prompt_ladder() -> None:
    rows = [
        ("ضعيف", "Weak", "«لخص هذا المقال»",
         "لا جمهور، ولا طول، ولا شكل، ولا قيود، ولا معيار نجاح. النتيجة عشوائية الشكل.", "#C8553D"),
        ("محسَّن", "Improved", "«لخص المقال التالي في خمس نقاط لطلبة السنة الأولى، بلغة بسيطة»",
         "أضيف الجمهور والطول والشكل. بقي بلا قيود على المصدر ولا معيار نجاح.", "#F2A541"),
        ("منظم", "Structured", "أمر متعدد الأقسام: دور، ومهمة، ومدخل مفصول بفواصل، وقيود، وشكل مخرج، ومعيار نجاح",
         "كل مكوّن صريح، والمدخل مفصول عن التعليمات، والنتيجة قابلة للتقييم والتكرار.", "#5E8C61"),
    ]
    html = ""
    for ar, en, example, why, color in rows:
        html += (
            f'<div class="tile" style="background:#FFFDF9;border-top:5px solid {color}">'
            f"<b>{esc(ar)}</b><small>{esc(en)}</small>"
            f'<p style="direction:rtl"><code style="background:#FBF3EA;padding:0.1rem 0.3rem">{esc(example)}</code></p>'
            f"<p>{esc(why)}</p></div>"
        )
    st.html(f'<div class="tiles" style="--cols:3">{html}</div>')


@register("m05_limits")
def limits() -> None:
    grid_cards([
        ("لا يضيف معرفة", "No new knowledge", "إن لم يكن في النموذج معلومة صحيحة، فلن تخلقها الصياغة. الحل: استرجاع من مصدر (المحور 7)."),
        ("لا يمنع الهلوسة", "No guarantee", "يقلل احتمالها ولا يلغيها. الحل: تقييد بالمصدر + تحقق بشري (المحور 8)."),
        ("لا يصلح مهمة غامضة", "Ill-defined task", "إن لم تعرف ما تريد، لن يعرفه النموذج. الحل: حدد معيار النجاح أولًا."),
        ("لا يضمن الثبات", "Not deterministic", "المخرج قد يتغير بين تشغيلين. الحل: خفض الحرارة، ومخرجات منظمة، واختبار متكرر."),
        ("لا يتجاوز نافذة السياق", "Context limits", "السياق محدود؛ الأمر الطويل جدًا قد يُضعف التركيز. الحل: تفكيك المهمة (المحور 6)."),
        ("لا يحل محل البيانات", "Not a data fix", "بيانات ناقصة أو خاطئة في المدخل تنتج مخرجًا خاطئًا مهما حسّنت الأمر."),
    ], cols=3)
