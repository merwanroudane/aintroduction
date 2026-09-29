"""Module 13 diagrams: concept map, the three oversight roles, the automation paradox curve, the
failure modes of review, levels of autonomy, the risk-proportionality matrix, the four conditions of
a review that works, and the closing synthesis of the whole course."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from components.diagrams import PALETTE, flow, grid_cards, nested, network, register, show


@register("m13_concept_map")
def concept_map() -> None:
    nodes = [
        {"id": "ov", "label": "الرقابة البشرية", "x": 0, "y": 0, "group": 0},
        {"id": "roles", "label": "الأدوار الثلاثة", "x": -2.4, "y": 1.1, "group": 1,
         "hover": "في الحلقة، وعلى الحلقة، وآمِر — ولكل دور شروطه ومخاطره"},
        {"id": "auth", "label": "سلطة التجاوز", "x": -2.6, "y": -0.4, "group": 1,
         "hover": "الصلاحية النظرية لا تكفي: تلزم القدرة الفعلية"},
        {"id": "bias", "label": "تحيّز الأتمتة", "x": 0, "y": 2.1, "group": 2,
         "hover": "قبول اقتراح النظام حتى مع وجود دليل يخالفه"},
        {"id": "para", "label": "مفارقة الأتمتة", "x": 0, "y": -2.2, "group": 2,
         "hover": "كلما تحسّن النظام صارت مهمة المراجع أصعب لا أسهل"},
        {"id": "lvl", "label": "مستويات الاستقلالية", "x": 2.4, "y": 1.1, "group": 3,
         "hover": "من الاقتراح إلى التنفيذ الكامل — والمستوى يتناسب مع المخاطر"},
        {"id": "des", "label": "تصميم المراجعة", "x": 2.6, "y": -0.4, "group": 3,
         "hover": "معلومات، ووقت، وسلطة، وحوافز — أربعة شروط لا نصائح"},
        {"id": "meas", "label": "قياس المراجعة", "x": 0, "y": -3.4, "group": 4,
         "hover": "معدل الرفض، وزمن المراجعة، ونصيب الحالات الحدّية"},
    ]
    edges = [("ov", "roles"), ("roles", "auth"), ("ov", "bias"), ("bias", "para"),
             ("para", "meas"), ("ov", "lvl"), ("lvl", "des"), ("des", "meas"),
             ("auth", "des")]
    network(nodes, edges, height=520, key="m13-concept")


@register("m13_oversight_roles")
def oversight_roles() -> None:
    st.caption("ثلاثة أدوار يُخلط بينها دائمًا، وتُسمّى كلها «رقابة بشرية» — ومخاطر كل واحد مختلفة.")
    grid_cards([
        ("إنسان في الحلقة", "Human in the loop",
         "**لا يُنفَّذ القرار بلا موافقته** في كل حالة. **أقوى حماية وأغلى كلفة.** "
         "**وخطره:** يتحول إلى موافقة آلية إذا كثُر الحجم أو ضاق الوقت."),
        ("إنسان على الحلقة", "Human on the loop",
         "النظام ينفّذ، والإنسان **يراقب ويتدخل** عند الحاجة، ويراجع عيّنة. "
         "**وخطره:** لا يلاحظ الخطأ لأنه لا يفحص كل حالة، ويفقد اليقظة بطول المراقبة."),
        ("إنسان آمِر", "Human in command",
         "النظام يعمل باستقلالية، والإنسان يحدد **الغرض والحدود** ويملك **سلطة الإيقاف** ويحاسب. "
         "**وخطره:** يصير إشرافًا اسميًا إذا لم يملك معلومات ولا سلطة فعلية."),
        ("لا رقابة", "No oversight",
         "قرار آلي بلا مراجعة ولا سبيل طعن. **مقبول** في مسائل ضئيلة الأثر وقابلة للتراجع، "
         "**وغير مقبول** فيما يمسّ أشخاصًا (المحور 11)."),
    ], cols=2)
    st.caption("**القاعدة:** لا تسأل «هل توجد رقابة بشرية؟» بل **«أي دور، وبأي شروط، وكيف نقيس أثره؟»**")


@register("m13_automation_paradox")
def automation_paradox() -> None:
    st.caption("مفارقة الأتمتة، مرسومةً: كلما قلّ معدل خطأ النظام، **قلّت** فرص المراجع للتدرب على كشف "
               "الخطأ، فتضعف قدرته على كشفه حين يقع — ويرتفع **أثر** الخطأ الواحد الذي يمرّ.")
    err = np.array([0.30, 0.20, 0.10, 0.05, 0.02, 0.01, 0.005, 0.001])
    # Detection skill proxy: how many genuine errors a reviewer meets per 1000 cases, i.e. practice.
    practice = err * 1000
    # Consequence proxy: an undetected error in a system trusted this much is costlier.
    trust = 1 - err
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=err, y=practice, mode="lines+markers", name="فرص التدرب لكل 1000 حالة",
                             line=dict(color=PALETTE[0], width=3), marker=dict(size=9)))
    fig.add_trace(go.Scatter(x=err, y=trust * 100, mode="lines+markers", name="درجة الثقة المكتسبة (٪)",
                             line=dict(color=PALETTE[4], width=3, dash="dash"), marker=dict(size=9),
                             yaxis="y2"))
    fig.update_layout(
        xaxis=dict(title="معدل خطأ النظام", type="log", autorange="reversed",
                   tickvals=[0.001, 0.01, 0.1, 0.3], ticktext=["0.1٪", "1٪", "10٪", "30٪"]),
        yaxis=dict(title="عدد الأخطاء التي يصادفها المراجع", type="log"),
        yaxis2=dict(title="الثقة (٪)", overlaying="y", side="right", range=[60, 101]),
        legend=dict(orientation="h", y=1.16),
    )
    show(fig, 400, key="m13-paradox")
    st.caption("**اقرأ الاتجاهين معًا:** فالتحرك نحو اليمين (نظام أفضل) يخفض التدرب ويرفع الثقة — "
               "**وهذا أسوأ تركيب ممكن لليقظة**. والرسم توضيحي لعلاقة بنيوية، لا قياس لنظام بعينه.")


@register("m13_failure_modes")
def failure_modes() -> None:
    grid_cards([
        ("تحيّز الأتمتة", "Automation bias",
         "قبول اقتراح النظام **حتى مع وجود دليل يخالفه**. وموثّق تجريبيًا في مهام مراقبة، "
         "وبصورتين: **أخطاء إغفال** (لا ينتبه لما فات النظام) و**أخطاء إذعان** (يتبع اقتراحًا خاطئًا)."),
        ("الرضا الزائف", "Complacency",
         "انخفاض اليقظة مع طول التعامل مع نظام موثوق. **ليس تقصيرًا أخلاقيًا** بل نتيجة توزيع الانتباه "
         "على مهام متعددة، ولهذا لا يُعالَج بالتوصية بل بالتصميم."),
        ("تآكل المهارة", "Skill degradation",
         "ضعف المهارة التي لم تُمارَس لأن النظام يؤديها — **وهي المهارة نفسها اللازمة للمراجعة**. "
         "فالأتمتة تُضعف شرط نجاحها."),
        ("المراجعة الشكلية", "Rubber-stamping",
         "موافقة بلا فحص فعلي. **وأخطر من غياب المراجعة**، لأنها توزّع المسؤولية على من لم يفحص "
         "وتمنح النظام غطاءً."),
        ("إجهاد التنبيهات", "Alert fatigue",
         "كثرة طلبات التأكيد تحوّلها إلى ضغطات آلية. **فزيادة التأكيدات قد تخفض الرقابة** لا ترفعها."),
        ("سلطة بلا قدرة", "Authority without ability",
         "للمراجع صلاحية الرفض نظريًا، ولا يملك **معلومات** ولا **وقتًا** ولا **غطاءً** لاستعمالها. "
         "وهذا أشيع فشل في المؤسسات."),
    ], cols=3)


@register("m13_autonomy_levels")
def autonomy_levels() -> None:
    nested([
        ("المستوى 0 — لا مساعدة", "Manual", "الإنسان يقرر وينفّذ. النظام يعرض بيانات خامًا فقط."),
        ("المستوى 1 — اقتراح", "Suggest", "النظام يقترح خيارًا واحدًا أو أكثر، والإنسان يقرر من الصفر إن شاء."),
        ("المستوى 2 — توصية مرتّبة", "Recommend", "النظام يرتّب الخيارات ويبرّر، والإنسان يختار. **أكثر المستويات خطرًا على الحياد**: الترتيب نفسه يوجّه القرار."),
        ("المستوى 3 — تنفيذ بموافقة", "Execute on approval", "النظام يجهّز الفعل وينفّذه **بعد** موافقة صريحة لكل حالة."),
        ("المستوى 4 — تنفيذ بمهلة اعتراض", "Execute unless vetoed", "النظام ينفّذ بعد مهلة إن لم يعترض الإنسان. **ويعتمد كليًا على أن المهلة كافية وأن الإشعار يُقرأ.**"),
        ("المستوى 5 — تنفيذ كامل", "Full autonomy", "النظام ينفّذ ويُبلّغ لاحقًا، أو لا يُبلّغ. **لا يُستعمل فيما يمسّ أشخاصًا.**"),
    ], caption="مستويات الاستقلالية: الانتقال من مستوى إلى أعلى منه قرار يحتاج مبررًا مكتوبًا وتناسبًا مع المخاطر.")


@register("m13_proportionality")
def proportionality() -> None:
    st.caption("مصفوفة التناسب: **المستوى المسموح يحدده الأثر وقابلية التراجع**، لا قدرة النظام ولا دقته.")
    rows = ["قابل للتراجع بسهولة", "قابل للتراجع بكلفة", "غير قابل للتراجع"]
    cols = ["أثر ضئيل", "أثر متوسط", "يمسّ أشخاصًا"]
    # Allowed maximum autonomy level per cell (see m13_autonomy_levels).
    z = [[5, 4, 3],
         [4, 3, 2],
         [3, 2, 1]]
    text = [[f"حتى المستوى {v}" for v in row] for row in z]
    fig = go.Figure(data=go.Heatmap(
        z=z, x=cols, y=rows, text=text, texttemplate="%{text}",
        colorscale=[[0, "#F6E3D7"], [0.5, "#F2A541"], [1, "#E07A5F"]],
        reversescale=True, showscale=False, xgap=4, ygap=4,
        hovertemplate="%{y} × %{x}: %{text}<extra></extra>"))
    fig.update_xaxes(side="top")
    show(fig, 320, key="m13-prop")
    st.caption("**والقاعدة المستخلصة:** ما كان **غير قابل للتراجع ويمسّ أشخاصًا** لا يتجاوز **الاقتراح** — "
               "ويبقى القرار والتنفيذ بشريين. (وهذا يوافق التزامات عالي المخاطر، المحاضرة 11.6.)")


@register("m13_review_conditions")
def review_conditions() -> None:
    flow([("معلومات كافية", "Information"), ("وقت كافٍ", "Time"),
          ("سلطة فعلية", "Authority"), ("حوافز سليمة", "Incentives"),
          ("قياس الأثر", "Measurement")],
         caption="أربعة شروط لمراجعة تعمل، وخامس يثبت أنها تعمل. وغياب واحد يُبطل البقية.")
    st.caption("**اختبار سريع لأي إجراء مراجعة:** اسأل عن الشروط الأربعة بالترتيب. "
               "وستجد أن أكثر ما يغيب هو **الوقت** ثم **الحوافز** — وهما الأقل ذكرًا في أي سياسة مكتوبة.")


@register("m13_course_synthesis")
def course_synthesis() -> None:
    st.caption("خلاصة المقرر كله في أربع عادات تبقى بعد أن تتغير كل الأدوات.")
    grid_cards([
        ("حدّد نوع سؤالك", "Frame the question",
         "تنبؤي أم سببي؟ (المحور 10) وصفي أم تقييمي؟ **فاختيار الأداة قبل السؤال انحراف منهجي كامل.**"),
        ("تحقّق من كل مخرج", "Verify",
         "بالمصدر الأولي لا بالثقة ولا بالإقناع (المحاور 7 و8). **والإتقان ليس دقة، والتفسير المقنع ليس صحيحًا.**"),
        ("وثّق قراراتك", "Document",
         "سجل قرارات، وبطاقة نموذج، وصحيفة بيانات، وسجل معالجة (المحاور 10 و11 و12). "
         "**فما لا يُوثَّق لا يُفحَص، وما لا يُفحَص لا يستحق الثقة.**"),
        ("اعرف حدودك وحدودها", "State the limits",
         "ما لا يسنده تصميمك، وما لا تصلح له أداتك، ومن يتحمّل كلفة الخطأ (المحاور 11 و12 و13). "
         "**والإفصاح عن الحد يحوّله من مفاجأة إلى شرط استعمال.**"),
    ], cols=2)
