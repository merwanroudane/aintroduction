"""Module 13 labs (offline, numpy only): a vigilance lab quantifying the automation paradox — how a
better system leaves the reviewer fewer chances to practise, so a larger SHARE of errors slips
through; and a rubber-stamp detector that turns "is this review real?" into four measurable
indicators with thresholds the student has to set."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from components.diagrams import PALETTE, show
from components.labs import register

# ------------------------------------------------------------------ 13.2 vigilance / paradox


@register("m13_vigilance", "مختبر: مفارقة الأتمتة بالأرقام", "Vigilance and the automation paradox", module=13)
def vigilance() -> None:
    st.markdown(
        "نظام يقترح قرارات، وإنسان يراجع. **ونقيس شيئًا واحدًا:** كم خطأً يمرّ دون كشف؟ "
        "ثم نحسّن النظام — ونرى ما يحدث للمراجعة."
    )
    c1, c2, c3 = st.columns(3)
    err_rate = c1.select_slider("معدل خطأ النظام", [0.30, 0.20, 0.10, 0.05, 0.02, 0.01, 0.005],
                                value=0.10, key="m13-v-err")
    n_cases = c2.select_slider("عدد الحالات في الفترة", [200, 500, 1000, 5000], value=1000,
                               key="m13-v-n")
    base_skill = c3.slider("قدرة المراجع الأساسية على كشف خطأ يفحصه", 0.30, 0.95, 0.70, 0.05,
                           key="m13-v-skill")

    # Detection probability falls as the reviewer meets fewer real errors: practice sustains vigilance.
    # Modelled as a saturating function of errors-per-period; stated as illustrative, not measured.
    reps = 400
    rng = np.random.default_rng(13)
    errors_seen = err_rate * n_cases
    practice_factor = errors_seen / (errors_seen + 12.0)      # 0 → no practice, →1 with many errors
    detect_p = base_skill * (0.35 + 0.65 * practice_factor)

    caught, missed = [], []
    for _ in range(reps):
        n_err = rng.binomial(n_cases, err_rate)
        c = rng.binomial(n_err, detect_p)
        caught.append(c)
        missed.append(n_err - c)
    caught_m, missed_m = float(np.mean(caught)), float(np.mean(missed))

    a, b, c = st.columns(3)
    a.metric("احتمال كشف خطأ يفحصه", f"{detect_p:.0%}",
             f"{(detect_p - base_skill) * 100:+.0f} نقطة عن قدرته الأساسية")
    b.metric("أخطاء مكشوفة (متوسط)", f"{caught_m:.1f}")
    c.metric("أخطاء مرّت دون كشف", f"{missed_m:.1f}")

    # Sweep across error rates to draw the paradox.
    rates = np.array([0.30, 0.20, 0.10, 0.05, 0.02, 0.01, 0.005])
    miss_share, miss_count = [], []
    for r in rates:
        e = r * n_cases
        pf = e / (e + 12.0)
        dp = base_skill * (0.35 + 0.65 * pf)
        miss_share.append(1 - dp)
        miss_count.append(e * (1 - dp))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=rates, y=miss_share, mode="lines+markers",
                             name="نسبة الأخطاء التي تمرّ",
                             line=dict(color=PALETTE[0], width=3), marker=dict(size=9)))
    fig.add_trace(go.Scatter(x=rates, y=np.array(miss_count) / max(max(miss_count), 1e-9),
                             mode="lines+markers", name="عدد الأخطاء التي تمرّ (منسوب)",
                             line=dict(color=PALETTE[4], width=3, dash="dash"), marker=dict(size=9)))
    fig.add_vline(x=err_rate, line=dict(color="#5E8C61", width=2, dash="dot"),
                  annotation_text="إعدادك", annotation_position="top")
    fig.update_xaxes(title="معدل خطأ النظام", type="log", autorange="reversed",
                     tickvals=[0.005, 0.01, 0.05, 0.1, 0.3],
                     ticktext=["0.5٪", "1٪", "5٪", "10٪", "30٪"])
    fig.update_yaxes(title="", tickformat=".0%")
    fig.update_layout(legend=dict(orientation="h", y=1.16))
    show(fig, 380, key="m13-v-fig")

    st.markdown(
        f"**عند معدل خطأ {err_rate:.1%}:** يصادف المراجع نحو **{errors_seen:.0f}** خطأً في الفترة، "
        f"فتنخفض قدرته على الكشف إلى **{detect_p:.0%}**، ويمرّ **{(1 - detect_p):.0%}** من الأخطاء."
    )
    if err_rate <= 0.01:
        st.error(
            "**هذا هو قلب المفارقة.** فالنظام صار ممتازًا، **ونسبة** الأخطاء التي تمرّ صارت **أعلى** — "
            "لأن المراجع لم يعد يتدرب. وقد ينخفض **عدد** الأخطاء المارّة (فهي قليلة أصلًا)، "
            "لكن **كل خطأ يمرّ الآن يقع في نظام يثق به الجميع** — فلا يُشكَّك فيه ولا يُكتشف لاحقًا."
        )
    elif err_rate >= 0.20:
        st.info("**نظام سيئ ومراجعة يقظة.** المراجع يتدرب كثيرًا فيكشف كثيرًا — "
                "لكن العبء عليه ضخم، وهذا ليس حلًّا مستدامًا.")

    with st.expander("ما تقوله المحاكاة وما لا تقوله"):
        st.markdown(
            "**الآلية المنمذجة:** أن القدرة على كشف خطأ تعتمد على **التدرب** — وعدد الأخطاء الحقيقية "
            "التي يصادفها المراجع هو تدرّبه. وهذه الآلية موثّقة في أدبيات العوامل البشرية تحت اسم "
            "**الرضا الزائف** و**تآكل المهارة**، وهي ما سمّاه Bainbridge (1983) «مفارقات الأتمتة».\n\n"
            "**ثلاث نتائج عملية:**\n"
            "1. **لا تفترض أن تحسين النظام يحسّن المراجعة.** فالعلاقة معاكسة، وهذا يخالف الحدس تمامًا.\n"
            "2. **حافظ على التدرب صناعيًا**: أدخل حالات اختبار معروفة الجواب في تدفق العمل وقِس كشفها. "
            "وهذا أهم إجراء عملي في المحاضرة كلها، وكلفته منخفضة.\n"
            "3. **ولا تقس المراجعة بوجودها**: قِسها بمعدل الرفض وبكشف الحالات المزروعة.\n\n"
            "**ما لا تقوله المحاكاة:** الأرقام **ليست مقيسة** من نظام حقيقي، ودالّة التدرب مفترضة "
            "لتوضيح الاتجاه. **والاتجاه هو المثبَت في الأدبيات**، لا القيم. ولا تعمّم هذه الأرقام على "
            "أي نظام بعينه."
        )


# ------------------------------------------------------------------ 13.2 rubber-stamp detector

_SCENARIOS = [
    {
        "name": "لجنة منح دراسية",
        "cases": 1200, "reviewers": 2, "minutes": 240, "override": 3, "reasons": 0,
        "authority": True,
    },
    {
        "name": "مراجعة تقارير آلية في مصلحة",
        "cases": 90, "reviewers": 1, "minutes": 300, "override": 14, "reasons": 12,
        "authority": True,
    },
    {
        "name": "تصديق قرارات نظام تصنيف",
        "cases": 500, "reviewers": 1, "minutes": 60, "override": 0, "reasons": 0,
        "authority": False,
    },
]


@register("m13_rubber_stamp", "مختبر: هل هذه مراجعة حقيقية؟", "Rubber-stamp detector", module=13)
def rubber_stamp() -> None:
    st.markdown(
        "«توجد مراجعة بشرية» ادعاء غير قابل للفحص. **وهذه أربعة مؤشرات تحوّله إلى قياس.** "
        "اختر حالة أو أدخل أرقامك."
    )
    names = [s["name"] for s in _SCENARIOS] + ["أرقامي الخاصة"]
    pick = st.selectbox("الحالة", names, key="m13-rs-pick")
    if pick == "أرقامي الخاصة":
        c1, c2 = st.columns(2)
        cases = c1.number_input("عدد الحالات في الفترة", 1, 100000, 300, key="m13-rs-cases")
        reviewers = c1.number_input("عدد المراجعين", 1, 100, 1, key="m13-rs-rev")
        minutes = c2.number_input("إجمالي دقائق المراجعة المتاحة", 1, 100000, 120, key="m13-rs-min")
        override = c2.number_input("عدد الحالات التي خُولف فيها اقتراح النظام", 0, 100000, 2,
                                   key="m13-rs-ovr")
        reasons = st.number_input("عدد المخالفات المسجَّل سببها كتابةً", 0, 100000, 1,
                                  key="m13-rs-rsn")
        authority = st.toggle("للمراجع سلطة مخالفة النظام بلا موافقة أعلى", value=True,
                              key="m13-rs-auth")
    else:
        s = [x for x in _SCENARIOS if x["name"] == pick][0]
        cases, reviewers, minutes = s["cases"], s["reviewers"], s["minutes"]
        override, reasons, authority = s["override"], s["reasons"], s["authority"]
        st.caption(f"{cases} حالة · {reviewers} مراجع · {minutes} دقيقة إجمالًا · "
                   f"{override} مخالفة · {reasons} منها مسجّل سببها")

    sec_per_case = (minutes * 60) / max(cases, 1)
    override_rate = override / max(cases, 1)
    reason_share = reasons / max(override, 1) if override else 0.0

    a, b, c = st.columns(3)
    a.metric("الزمن المتاح لكل حالة", f"{sec_per_case:.0f} ثانية")
    b.metric("معدل مخالفة النظام", f"{override_rate:.1%}")
    c.metric("المخالفات المبرَّرة كتابةً", f"{reason_share:.0%}" if override else "—")

    flags = []
    if sec_per_case < 30:
        flags.append(f"**الوقت غير كافٍ**: {sec_per_case:.0f} ثانية لكل حالة لا تكفي لفحص فعلي.")
    if override_rate < 0.01:
        flags.append(f"**معدل المخالفة {override_rate:.2%}**: قريب من الصفر. فإما أن النظام معصوم "
                     f"— وهذا لا يُفترض — أو أن المراجعة لا تفحص.")
    if override and reason_share < 0.5:
        flags.append("**المخالفات غير موثّقة**: فلا يمكن التعلّم منها ولا تدقيقها.")
    if not authority:
        flags.append("**لا سلطة فعلية**: المخالفة تحتاج موافقة أعلى، فتكلّف المراجع أكثر مما تكلّفه الموافقة.")

    fig = go.Figure()
    labels = ["زمن لكل حالة (ثانية)", "معدل المخالفة (٪)", "التوثيق (٪)"]
    vals = [min(sec_per_case, 300), override_rate * 100, reason_share * 100]
    thresholds = [30, 1, 50]
    fig.add_trace(go.Bar(x=labels, y=vals, marker_color=[
        PALETTE[0] if v < t else PALETTE[4] for v, t in zip(vals, thresholds)],
        text=[f"{v:.0f}" for v in vals], textposition="outside"))
    fig.update_yaxes(title="القيمة (والحد الأدنى المقترح مرسوم نقطيًا)")
    for i, t in enumerate(thresholds):
        fig.add_shape(type="line", x0=i - 0.4, x1=i + 0.4, y0=t, y1=t,
                      line=dict(color="#5E8C61", width=2, dash="dot"))
    fig.update_layout(showlegend=False)
    show(fig, 340, key="m13-rs-fig")

    if flags:
        st.error("**مؤشرات مراجعة شكلية:**\n\n" + "\n\n".join(f"- {f}" for f in flags))
    else:
        st.success("**المؤشرات الأربعة سليمة.** ويبقى فحص الشرط الخامس: هل الحوافز تكافئ الرفض المبرَّر "
                   "أم تعاقبه؟ وهذا لا يُقاس بالأرقام بل يُعرَف من الممارسة.")

    with st.expander("عن العتبات ومن أين تأتي"):
        st.markdown(
            "**العتبات المرسومة (30 ثانية، و1٪، و50٪) مقترحة للتدريس لا معايير رسمية.** والمقصود "
            "منها أن تُجبرك على **تحديد عتبتك أنت** وكتابتها في السياسة (المحاضرة 11.6): فبلا رقم "
            "مكتوب لا يُتخذ أي إجراء أبدًا.\n\n"
            "**ولماذا معدل المخالفة هو أقوى المؤشرات؟** لأنه **مخرج** لا **مدخل**: فهو يقيس ما فعلته "
            "المراجعة لا ما وُعِد به. **ومعدل رفض صفر ليس شهادة جودة للنظام بل فرضية عطب في المراجعة** — "
            "وهذا ما قلناه في المحاضرة 6.5 بصيغة أبسط.\n\n"
            "**وتنبيه على القياس نفسه:** معدل مخالفة **مرتفع جدًا** ليس جيدًا بالضرورة أيضًا — فقد يعني "
            "أن النظام سيئ ولا ينبغي استعماله، أو أن المراجعين يخالفون بلا فحص. **فالمؤشر يُقرأ مع "
            "التوثيق**: مخالفات مبرَّرة كتابةً هي الدليل على فحص فعلي."
        )
