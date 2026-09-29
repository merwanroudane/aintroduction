"""Module 6 diagrams: concept map, task decomposition, prompt chaining, structured output
pipeline, grounding vs retrieval, instruction hierarchy, and the injection threat model."""

import streamlit as st

from components.diagrams import flow, grid_cards, network, register
from components.layout import esc


@register("m06_concept_map")
def concept_map() -> None:
    nodes = [
        {"id": "adv", "label": "بناء الأوامر المتقدم", "x": 0, "y": 0, "group": 0},
        {"id": "dec", "label": "تفكيك المهام", "x": -2.1, "y": 1.0, "group": 1, "hover": "من أمر واحد إلى خطوات"},
        {"id": "chain", "label": "سلاسل الأوامر", "x": -2.3, "y": -0.5, "group": 1, "hover": "مخرج خطوة = مدخل التالية"},
        {"id": "struct", "label": "المخرجات المنظمة", "x": 0, "y": 1.9, "group": 2, "hover": "JSON بمخطط + تحقق برمجي"},
        {"id": "ground", "label": "التقييد بالمصدر", "x": 2.1, "y": 1.0, "group": 3, "hover": "Grounding: اعتمد حصريًا على…"},
        {"id": "evid", "label": "جدول الأدلة", "x": 2.3, "y": -0.5, "group": 3, "hover": "تبرير منظم قابل للتحقق"},
        {"id": "sec", "label": "الأمان", "x": 0, "y": -1.9, "group": 4, "hover": "حقن الأوامر والتسلسل الهرمي"},
        {"id": "inj", "label": "حقن الأوامر", "x": -1.3, "y": -1.5, "group": 4},
        {"id": "tool", "label": "سوء استعمال الأدوات", "x": 1.3, "y": -1.5, "group": 4},
    ]
    edges = [("adv", "dec"), ("dec", "chain"), ("chain", "struct"), ("adv", "struct"),
             ("adv", "ground"), ("ground", "evid"), ("adv", "sec"), ("sec", "inj"), ("sec", "tool"),
             ("struct", "sec")]
    network(nodes, edges, height=500, key="m06-concept")


@register("m06_decomposition")
def decomposition() -> None:
    st.html(
        '<div class="tiles" style="--cols:2">'
        '<div class="tile" style="background:#FFE7DF;border-top:5px solid #C8553D">'
        '<b>أمر واحد كبير</b><small>Monolithic prompt</small>'
        '<p>«اقرأ هذه التقارير العشرة واستخرج الاتجاهات واكتب تقريرًا من عشر صفحات مع توصيات».<br><br>'
        '<b>ما يحدث:</b> تغطية سطحية لكل جزء، وضياع تفاصيل، ويستحيل معرفة أي مرحلة أخفقت، '
        'ولا يمكن التحقق من خطوة دون إعادة كل شيء.</p></div>'
        '<div class="tile" style="background:#EAF5FE;border-top:5px solid #5B9BD5">'
        '<b>سلسلة خطوات</b><small>Decomposed chain</small>'
        '<p>استخراج ← توحيد ← تحليل ← صياغة ← مراجعة.<br><br>'
        '<b>الفائدة:</b> كل خطوة مهمة واحدة واضحة، ومخرجها قابل للتحقق قبل الانتقال، '
        'ويمكن إصلاح خطوة واحدة دون المساس بالباقي.</p></div></div>'
    )


@register("m06_chain")
def chain() -> None:
    flow([("استخراج الوقائع", "Extract"), ("توحيد الصيغ", "Normalize"), ("تحليل ومقارنة", "Analyze"),
          ("صياغة المسودة", "Draft"), ("نقد ومراجعة", "Critique"), ("الصيغة النهائية", "Finalize")],
         caption="سلسلة أوامر: مخرج كل خطوة مدخل التالية، ونقطة تحقق بين كل خطوتين.")
    st.caption("**قاعدة السلسلة:** إن لم تستطع التحقق من مخرج خطوة، فلا تبنِ عليها خطوة أخرى. "
               "الخطأ في الخطوة الأولى يتضخم في كل ما بعدها.")


@register("m06_structured_pipeline")
def structured_pipeline() -> None:
    flow([("مخطط محدد", "Schema"), ("أمر يطلبه صراحة", "Prompt"), ("مخرج النموذج", "Output"),
          ("تحقق برمجي", "Validate"), ("إعادة المحاولة عند الفشل", "Retry"), ("استعمال آمن", "Use")],
         loop=True,
         caption="المخرج المنظم ليس طلبًا فقط بل **مسار تحقق**: الالتزام بالمخطط احتمالي لا مضمون.")


@register("m06_grounding_vs_retrieval")
def grounding_vs_retrieval() -> None:
    grid_cards([
        ("التقييد بالمصدر", "Grounding", "أنت تضع المصدر في الأمر وتلزم النموذج بالاعتماد عليه حصريًا. "
                                          "مناسب لمستند واحد أو بضعة مستندات تعرفها مسبقًا."),
        ("الاسترجاع", "Retrieval", "النظام **يبحث** عن المقاطع ذات الصلة في مجموعة كبيرة ثم يضعها في السياق. "
                                    "مناسب لآلاف الوثائق. (تفصيله في المحور 7)"),
        ("الاسترجاع المعزز بالتوليد", "RAG", "الجمع بينهما: استرجاع ثم توليد مقيّد بالمسترجَع مع الإسناد. "
                                              "لا يضمن الصحة، وجودته من جودة الاسترجاع والمصادر."),
    ], cols=3)


@register("m06_instruction_hierarchy")
def instruction_hierarchy() -> None:
    levels = [
        ("سياسات النظام والمطوّر", "System / developer", "أعلى سلطة: قواعد السلامة وحدود الاستعمال.", "#C8553D"),
        ("تعليمات المستخدم", "User", "ما تطلبه أنت، ضمن حدود ما سبق.", "#F2A541"),
        ("مخرجات الأدوات والمحتوى الخارجي", "Tool output / external", "**بيانات تُعالَج، لا تعليمات تُنفَّذ.**", "#5B9BD5"),
    ]
    html = ""
    for i, (ar, en, desc, color) in enumerate(levels):
        html += (
            f'<div class="tile" style="background:#FFFDF9;border-top:5px solid {color};'
            f'margin-right:{i * 1.4}rem">'
            f"<b>{i + 1}. {esc(ar)}</b><small>{esc(en)}</small><p>{desc}</p></div>"
        )
    st.html(f'<div class="tiles" style="--cols:1">{html}</div>')
    st.caption("**التسلسل الهرمي للتعليمات:** كلما نزلنا قلّت السلطة. والخطأ الأمني الأشهر هو منح المستوى "
               "الثالث سلطة المستوى الثاني.")


@register("m06_injection_model")
def injection_model() -> None:
    flow([("مهاجم يضع تعليمات في محتوى", "Attacker plants text"),
          ("النظام يجلب المحتوى", "System fetches"),
          ("المحتوى يدخل السياق", "Enters context"),
          ("النموذج ينفّذه بوصفه تعليمة", "Model obeys"),
          ("فعل ضار بصلاحيات المستخدم", "Harmful action")],
         caption="حقن الأوامر غير المباشر: الضحية لم تكتب التعليمة، والنظام نفّذها بصلاحياتها.")
    st.caption("المصدر المرجعي: Greshake et al. (2023) — تم التحقق في 2026-09-28.")


@register("m06_defense_layers")
def defense_layers() -> None:
    grid_cards([
        ("فصل وتوسيم", "Separation", "افصل المحتوى الخارجي بفواصل وقل صراحة إنه بيانات لا تعليمات. "
                                      "ضروري، وغير كافٍ وحده."),
        ("أقل صلاحية", "Least privilege", "امنح الأداة أضيق صلاحية ممكنة. الوكيل الذي لا يملك صلاحية الحذف لا يحذف."),
        ("موافقة على الأفعال", "Human approval", "كل فعل غير قابل للعكس يمر بموافقة بشرية صريحة."),
        ("تحقق من المخرجات", "Output validation", "لا تنفّذ مخرج النموذج مباشرة: تحقق من شكله ومن حدوده قبل الاستعمال."),
        ("عزل المحتوى غير الموثوق", "Isolation", "عالج المحتوى الخارجي في سياق منفصل بصلاحيات أقل حيثما أمكن."),
        ("سجل تدقيق", "Audit trail", "سجّل كل فعل ومصدره ليمكن كشف الخلل وتصحيحه لاحقًا."),
    ], cols=3)
    st.caption("**الدفاع في العمق:** لا ضابط واحد كافٍ؛ القوة في تراكم الطبقات وفي تقليل ما يمكن أن يحدث أصلًا.")
