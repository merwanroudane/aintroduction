"""Module 11 labs (offline, numpy only): a fairness-criteria simulator where the student tries —
and fails — to satisfy demographic parity, equalised error rates and calibration at once; a proxy
lab showing that deleting the sensitive attribute does not remove the disparity; and an
explanation-instability lab showing that a post-hoc local explanation depends on how it is built."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from components.diagrams import PALETTE, show
from components.labs import register

# ------------------------------------------------------------------ 11.3 fairness criteria


def _group_stats(a: float, b: float, t: float, n: int = 20001) -> dict:
    """Confusion-matrix rates for a PERFECTLY calibrated score at threshold t.

    The score s has density Beta(a, b) and P(Y=1 | s) = s by construction, so calibration holds
    for every group no matter what a and b are. Every rate below is then *derived*, not chosen.
    """
    s = np.linspace(1e-6, 1 - 1e-6, n)
    f = s ** (a - 1) * (1 - s) ** (b - 1)
    f /= np.trapezoid(f, s)
    sel = s > t
    pos, neg = f * s, f * (1 - s)
    base = float(np.trapezoid(pos, s))
    tp = float(np.trapezoid(pos[sel], s[sel]))
    fp = float(np.trapezoid(neg[sel], s[sel]))
    fn = base - tp
    tn = (1 - base) - fp
    return {
        "base": base,
        "accept": tp + fp,                                     # selection rate
        "tpr": tp / base if base else 0.0,
        "fpr": fp / (1 - base) if base < 1 else 0.0,
        "fnr": fn / base if base else 0.0,
        "ppv": tp / (tp + fp) if (tp + fp) else float("nan"),  # precision
    }


@register("m11_fairness_tradeoff", "مختبر: حقّق معايير الإنصاف الثلاثة معًا", "Fairness criteria lab", module=11)
def fairness_tradeoff() -> None:
    st.markdown(
        "فئتان، ودرجة **معايَرة تمامًا** لكلتيهما بالبناء. ومهمتك بسيطة في الظاهر: "
        "**حرّك العتبتين حتى تتحقق المعايير الثلاثة معًا.** جرّب بجدية قبل أن تقرأ التحليل."
    )
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**الفئة أ**")
        base_a = st.slider("المعدل القاعدي للفئة أ", 0.10, 0.60, 0.25, 0.05, key="m11-ft-ba")
        t_a = st.slider("عتبة القرار للفئة أ", 0.05, 0.95, 0.40, 0.05, key="m11-ft-ta")
    with c2:
        st.markdown("**الفئة ب**")
        base_b = st.slider("المعدل القاعدي للفئة ب", 0.10, 0.60, 0.40, 0.05, key="m11-ft-bb")
        t_b = st.slider("عتبة القرار للفئة ب", 0.05, 0.95, 0.40, 0.05, key="m11-ft-tb")

    # Beta(2, b) has mean 2/(2+b); solve b for the requested base rate so the slider is honest.
    A = _group_stats(2.0, 2.0 * (1 - base_a) / base_a, t_a)
    B = _group_stats(2.0, 2.0 * (1 - base_b) / base_b, t_b)

    tol = 0.02
    checks = [
        ("التكافؤ الديموغرافي", "نسبة القبول متساوية", abs(A["accept"] - B["accept"]),
         f"{A['accept']:.0%} مقابل {B['accept']:.0%}"),
        ("تكافؤ الأخطاء", "الإيجابي الكاذب والسلبي الكاذب متساويان",
         max(abs(A["fpr"] - B["fpr"]), abs(A["fnr"] - B["fnr"])),
         f"إيجابي كاذب {A['fpr']:.0%}/{B['fpr']:.0%} · سلبي كاذب {A['fnr']:.0%}/{B['fnr']:.0%}"),
        ("تكافؤ القيمة التنبؤية", "الدرجة تعني الشيء نفسه بعد القبول",
         abs(A["ppv"] - B["ppv"]), f"{A['ppv']:.0%} مقابل {B['ppv']:.0%}"),
    ]

    fig = go.Figure()
    metrics = ["نسبة القبول", "إيجابي كاذب", "سلبي كاذب", "القيمة التنبؤية"]
    va = [A["accept"], A["fpr"], A["fnr"], A["ppv"]]
    vb = [B["accept"], B["fpr"], B["fnr"], B["ppv"]]
    fig.add_trace(go.Bar(name="الفئة أ", x=metrics, y=va, marker_color=PALETTE[0],
                         text=[f"{v:.0%}" for v in va], textposition="outside"))
    fig.add_trace(go.Bar(name="الفئة ب", x=metrics, y=vb, marker_color=PALETTE[4],
                         text=[f"{v:.0%}" for v in vb], textposition="outside"))
    fig.update_yaxes(title="", range=[0, 1.12], tickformat=".0%")
    fig.update_layout(barmode="group", legend=dict(orientation="h", y=1.14))
    show(fig, 380, key="m11-ft-bars")

    met = 0
    for name, what, gap, detail in checks:
        if gap <= tol:
            st.success(f"**{name}** محقَّق — {what}. ({detail})")
            met += 1
        else:
            st.error(f"**{name}** غير محقَّق — الفجوة {gap:.0%}. ({detail})")

    same_base = abs(base_a - base_b) < 1e-9
    if met == 3 and not same_base:
        st.warning(
            "**تحقّقت الثلاثة مع اختلاف المعدلات القاعدية؟** راجع الفجوات: النتيجة هنا تقريبية "
            "بهامش تسامح 2٪، والبرهان يمنع التحقق **التام** لا التقريبي عند فجوة صغيرة جدًا."
        )
    elif same_base:
        st.info(
            "**جعلتَ المعدلين القاعديين متساويين.** وهذه هي الحالة الوحيدة التي يسمح فيها البرهان "
            "باجتماع المعايير — ولهذا هي الحالة التي **لا توجد** في البيانات الاجتماعية الحقيقية."
        )

    with st.expander("لماذا لا تجتمع؟ وماذا يعني هذا عمليًا؟"):
        st.markdown(
            "**جرّب هذه الثلاث بالترتيب:**\n"
            "1. **ساوِ نسبتي القبول** (بتحريك العتبتين). سترى الأخطاء تتباعد.\n"
            "2. **ساوِ معدلات الخطأ**. سترى القيمة التنبؤية تتباعد.\n"
            "3. **وحّد العتبة** (وهو ما يحقق المعايرة والقيمة التنبؤية). سترى نسب القبول والأخطاء تتباعد.\n\n"
            "**والسبب واحد:** مع معدلين قاعديين مختلفين، تربط هوية جبرية بين معدل الخطأ والقيمة "
            "التنبؤية والمعدل القاعدي. فتثبيت اثنين **يحدد** الثالث، ولا يبقى لك فيه اختيار. "
            "وهذا ما برهنه Chouldechova (2017) وKleinberg وMullainathan وRaghavan (2016) "
            "كلٌّ بصياغته.\n\n"
            "**والنتيجة العملية — وهي المقصودة من المختبر كله:** السؤال ليس «كيف أجعل النظام عادلًا؟» "
            "بل **«أي معيار أختار، ولماذا، ومن يتحمّل كلفة ما تنازلت عنه؟»** وهذا سؤال **قِيَمي** "
            "يجب أن يُطرح صراحةً ويُوثَّق، لا أن يُحسَم ضمنيًا في اختيار عتبة.\n\n"
            "**وتنبيه على الأداة نفسها:** استعمال **عتبتين مختلفتين** لفئتين هو تفرقة صريحة على أساس "
            "الانتماء، وقد يكون **ممنوعًا قانونًا** في كثير من السياقات مهما كان مبرَّرًا إحصائيًا. "
            "فالمختبر يبيّن لك ما تستطيع الرياضيات فعله، لا ما يُسمح لك بفعله."
        )
    st.caption(
        "المحاكاة تفترض درجة معايَرة تمامًا وتوزيعات درجات من عائلة Beta، وهي تبسيط: في الواقع "
        "تكون الدرجة غير معايَرة أصلًا، فتُضاف مشكلة المعايرة إلى مشكلة التعارض لا تحلّها."
    )


# ------------------------------------------------------------------ 11.2 proxy bias


@register("m11_proxy_bias", "مختبر: احذف المتغير الحسّاس وراقب ما يبقى", "Proxy bias lab", module=11)
def proxy_bias() -> None:
    st.markdown(
        "الاعتقاد الشائع: «لا نستعمل الانتماء في النموذج، فالنموذج محايد». "
        "هنا نحذف الانتماء فعلًا — ونقيس ما يبقى من الفجوة."
    )
    c1, c2, c3 = st.columns(3)
    corr = c1.slider("ارتباط المتغير الوكيل بالانتماء", 0.0, 0.98, 0.85, 0.02, key="m11-pb-corr")
    gap = c2.slider("الفجوة الحقيقية في الفرص بين الفئتين", 0.0, 1.5, 0.8, 0.1, key="m11-pb-gap")
    drop = c3.radio("المتغيرات الداخلة في النموذج",
                    ["الانتماء + الوكيل + مهارة", "الوكيل + مهارة (حُذف الانتماء)", "مهارة فقط"],
                    key="m11-pb-drop")
    n = 4000
    rng = np.random.default_rng(7)

    g = rng.integers(0, 2, n)                       # group membership
    # A "neutral-looking" variable (e.g. neighbourhood, school, postcode) tied to the group.
    proxy = corr * (g - 0.5) * 2 + np.sqrt(max(1 - corr ** 2, 1e-9)) * rng.normal(0, 1, n)
    skill = rng.normal(0, 1, n)                     # genuinely job-relevant, group-independent
    # The LABEL carries the historical gap: equal skill, unequal recorded outcome.
    logit = 1.2 * skill + gap * (g - 0.5) * 2 - 0.3
    y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)

    cols = {"الانتماء + الوكيل + مهارة": [g, proxy, skill],
            "الوكيل + مهارة (حُذف الانتماء)": [proxy, skill],
            "مهارة فقط": [skill]}[drop]
    X = np.column_stack([np.ones(n)] + [np.asarray(c, dtype=float) for c in cols])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    pred = X @ beta
    t = float(np.quantile(pred, 0.6))               # accept the top 40%
    acc = pred > t

    r0 = float(acc[g == 0].mean())
    r1 = float(acc[g == 1].mean())
    fig = go.Figure()
    fig.add_trace(go.Bar(x=["الفئة أ", "الفئة ب"], y=[r0, r1],
                         marker_color=[PALETTE[0], PALETTE[4]],
                         text=[f"{r0:.0%}", f"{r1:.0%}"], textposition="outside"))
    fig.update_yaxes(title="نسبة القبول", range=[0, 1.05], tickformat=".0%")
    fig.update_layout(showlegend=False)
    show(fig, 330, key="m11-pb-bars")

    st.metric("الفجوة في نسبة القبول بين الفئتين", f"{abs(r1 - r0):.1%}")
    if drop == "الوكيل + مهارة (حُذف الانتماء)" and abs(r1 - r0) > 0.05:
        st.error(
            "**حُذف الانتماء، وبقيت الفجوة.** فالمتغير الوكيل ينقلها كاملةً تقريبًا — والنموذج "
            "«لا يعرف» الانتماء، لكنه **يستنتجه** ويعمل به."
        )
    elif drop == "مهارة فقط" and abs(r1 - r0) > 0.05:
        st.warning(
            "**حتى بالمهارة وحدها تبقى فجوة.** والسبب هنا ليس الوكيل بل **الوسم نفسه**: البيانات "
            "التاريخية سجّلت نتائج غير متساوية عند مهارة متساوية، فالنموذج يتعلّم الفجوة من `y` "
            "لا من `x`. وهذا **تحيّز الوسم**، ولا يعالجه حذف أي متغير."
        )
    elif abs(r1 - r0) <= 0.05:
        st.success("الفجوة صغيرة عند هذه الإعدادات. **ارفع الارتباط أو الفجوة التاريخية** وراقب ظهورها.")

    with st.expander("الدروس الثلاثة — والأخير هو الأهم"):
        st.markdown(
            "**1. حذف المتغير الحسّاس لا يكفي.** فأي متغير مرتبط به — الحي، أو المدرسة، أو الرمز "
            "البريدي، أو اسم الجهة المُصدِّرة للشهادة — يعيد بناءه. وفي البيانات الغنية يوجد دائمًا وكيل.\n\n"
            "**2. الحذف قد يضرّ.** فمن دون معرفة الانتماء **لا تستطيع قياس** الفجوة ولا تصحيحها ولا "
            "التدقيق عليها. ولهذا يوصي كثير من الباحثين بجمع بيانات الانتماء **للقياس** مع منعها في "
            "**القرار** — وهو تمييز دقيق بين الاستعمالين.\n\n"
            "**3. وأخطر المصادر ليس المتغيرات بل الوسم.** جرّب «مهارة فقط» مع فجوة تاريخية مرتفعة: "
            "لا وكيل ولا انتماء في النموذج، والفجوة باقية — لأنها في `y` نفسه. "
            "**ولا تُعالج مشكلة في الوسم بتعديل في المتغيرات.**"
        )
    st.caption(
        "بيانات مولّدة من عملية معروفة لأغراض التدريس: «المهارة» و«الوكيل» و«الفجوة التاريخية» "
        "مقادير مصطنعة نتحكم فيها لنعزل الأثر، ولا تمثّل قياسًا لأي نظام حقيقي."
    )


# ------------------------------------------------------------------ 11.4 explanation limits


@register("m11_explanation_limits", "مختبر: تفسيران مختلفان للقرار نفسه", "Explanation instability", module=11)
def explanation_limits() -> None:
    st.markdown(
        "التفسير اللاحق يقرّب النموذج **محليًا** حول نقطة. وهنا نثبّت النموذج والنقطة، "
        "ونغيّر **حجم الجوار** فقط — ونقرأ التفسير الناتج."
    )
    st.latex(r"f(x_1, x_2) = \sin(3x_1) + x_1 x_2 + 0.5\,x_2")
    c1, c2, c3 = st.columns(3)
    x1 = c1.slider("موضع النقطة x₁", -1.5, 1.5, 0.5, 0.1, key="m11-el-x1")
    x2 = c2.slider("موضع النقطة x₂", -1.5, 1.5, 0.8, 0.1, key="m11-el-x2")
    width = c3.select_slider("حجم الجوار المستعمل في التفسير",
                            [0.05, 0.15, 0.4, 0.8, 1.5], value=0.4, key="m11-el-w")

    def f(a, b):
        return np.sin(3 * a) + a * b + 0.5 * b

    rng = np.random.default_rng(3)
    widths = [0.05, 0.15, 0.4, 0.8, 1.5]
    rows = []
    for w in widths:
        s1 = x1 + rng.normal(0, w, 4000)
        s2 = x2 + rng.normal(0, w, 4000)
        Z = np.column_stack([np.ones(4000), s1 - x1, s2 - x2])
        coef = np.linalg.lstsq(Z, f(s1, s2), rcond=None)[0]
        rows.append((w, float(coef[1]), float(coef[2])))

    fig = go.Figure()
    fig.add_trace(go.Bar(name="أهمية x₁", x=[f"جوار {w}" for w, _, _ in rows],
                         y=[c1_ for _, c1_, _ in rows], marker_color=PALETTE[0],
                         text=[f"{c1_:+.2f}" for _, c1_, _ in rows], textposition="outside"))
    fig.add_trace(go.Bar(name="أهمية x₂", x=[f"جوار {w}" for w, _, _ in rows],
                         y=[c2_ for _, _, c2_ in rows], marker_color=PALETTE[4],
                         text=[f"{c2_:+.2f}" for _, _, c2_ in rows], textposition="outside"))
    fig.add_hline(y=0, line=dict(color="#C7B8AE", width=1))
    fig.update_yaxes(title="الوزن المنسوب للمتغير في التفسير")
    fig.update_layout(barmode="group", legend=dict(orientation="h", y=1.14))
    show(fig, 380, key="m11-el-bars")

    chosen = [r for r in rows if abs(r[0] - width) < 1e-9][0]
    st.info(
        f"**التفسير عند الجوار {chosen[0]}:** وزن x₁ يساوي {chosen[1]:+.2f}، ووزن x₂ يساوي {chosen[2]:+.2f}. "
        "والنموذج لم يتغير، والنقطة لم تتغير — **القرار التقني في بناء التفسير هو ما تغيّر.**"
    )
    signs = {np.sign(r[1]) for r in rows}
    if len(signs) > 1:
        st.error(
            "**لاحظ أن إشارة أهمية x₁ نفسها تنقلب** بين جوار وآخر. فلا يكفي أن نقول إن الأوزان "
            "«تقريبية»: فالتفسيران يقولان أمرين **متعاكسين** عن السبب."
        )

    with st.expander("ما الذي يثبته التفسير اللاحق وما لا يثبته؟"):
        st.markdown(
            "**الأسئلة الأربعة التي توجّه إلى أي تفسير:**\n\n"
            "| السؤال | ماذا يكشف |\n|---|---|\n"
            "| كيف بُني هذا التفسير؟ | جوار؟ وعيّنات؟ وبذرة؟ — وكل واحد منها يغيّر الناتج |\n"
            "| هل يستقر مع تغيير طريقة البناء؟ | تفسير غير مستقر ليس تفسيرًا |\n"
            "| هل يقول شيئًا **سببيًا**؟ | لا. هو يصف **تقريبًا محليًا للنموذج**، لا العالم |\n"
            "| هل يُمكِّن المتأثر من فعل شيء؟ | إن لم يفتح سبيلًا للطعن، فهو تفسير للمطوّر لا للمتأثر |\n\n"
            "**ما يثبته:** أن تقريبًا خطيًا للنموذج حول هذه النقطة، بهذه الطريقة، يُسند هذا الوزن.\n\n"
            "**ما لا يثبته:** (أ) أن النموذج «يفكّر» هكذا، (ب) أن تغيير المتغير سيغيّر القرار، "
            "(ج) أن النظام عادل، (د) أن المتأثر فُهِم قراره.\n\n"
            "**والاستعمال السليم:** التفسير اللاحق أداة **تشخيص للمطوّر** — كاشفة لأخطاء وتسرّب "
            "ومتغيرات وكيلة. أما في القرارات عالية الأثر، فالحجة التي قدّمتها Rudin (2019) هي أن "
            "الطريق الأسلم هو **نموذج قابل للتفسير من الأصل** لا صندوق أسود بتفسير مُلحَق."
        )
    st.caption(
        "المحاكاة تستعمل تقريبًا خطيًا محليًا بعيّنات موزّعة حول النقطة، وهي مبسّطة عن أدوات التفسير "
        "المستعملة فعلًا. والظاهرة التي تعرضها — اعتماد التفسير على طريقة بنائه — مشتركة بينها."
    )
