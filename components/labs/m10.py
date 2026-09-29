"""Module 10 labs (offline, numpy only): an omitted-variable / regularisation bias simulator
that shows why naive ML coefficients are not causal and how partialling out fixes it; a
time-series split lab showing what random splitting hides; a text-index builder showing that
the number depends on the dictionary, the normalisation and the negation handling as much as
on the text; and a leakage-hunting exercise."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from components.diagrams import PALETTE, show
from components.labs import register

# ------------------------------------------------------------------ 10.3 regularisation bias


def _ols(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    X = np.column_stack([np.ones(len(X)), X])
    return np.linalg.lstsq(X, y, rcond=None)[0]


def _ridge(X: np.ndarray, y: np.ndarray, lam: float) -> np.ndarray:
    X = np.column_stack([np.ones(len(X)), X])
    p = X.shape[1]
    pen = lam * np.eye(p)
    pen[0, 0] = 0.0  # never shrink the intercept
    return np.linalg.solve(X.T @ X + pen, X.T @ y)


@register("m10_reg_bias", "مختبر: لماذا لا يكون معامل التعلّم الآلي سببيًا؟", "Regularisation bias lab", module=10)
def reg_bias() -> None:
    st.markdown(
        "نولّد بيانات **نعرف حقيقتها**: الأثر السببي الحقيقي لـ D على Y محدد سلفًا. ثم نقدّره بثلاث طرق "
        "ونقارن. وهذا أوضح ما يبيّن لماذا لا تُقرأ معاملات نموذج تنبؤي على أنها آثار."
    )
    c1, c2, c3 = st.columns(3)
    true_effect = c1.slider("الأثر السببي الحقيقي θ", 0.0, 2.0, 1.0, 0.1, key="m10-rb-theta")
    confound = c2.slider("قوة المتغيرات المُربِكة على D و Y", 0.0, 3.0, 2.0, 0.1, key="m10-rb-conf")
    lam = c3.slider("قوة الانتظام λ (في نموذج التنبؤ)", 0.0, 200.0, 60.0, 5.0, key="m10-rb-lam")
    n = st.select_slider("حجم العينة", [200, 500, 1000, 3000], value=1000, key="m10-rb-n")
    reps = 200

    rng = np.random.default_rng(11)
    naive, partialled = [], []
    for _ in range(reps):
        # X: 10 confounders. D depends on them; Y depends on D and on them.
        X = rng.normal(0, 1, (n, 10))
        g = confound * (X[:, 0] + 0.7 * X[:, 1] - 0.5 * X[:, 2])
        D = g + rng.normal(0, 1, n)
        Y = true_effect * D + g + rng.normal(0, 1, n)

        # (a) naive: a regularised predictive model of Y on [D, X]; read its D coefficient.
        b = _ridge(np.column_stack([D, X]), Y, lam)
        naive.append(b[1])

        # (b) partialling out (the DML idea): predict Y from X, predict D from X, then
        # regress the residuals on each other. Cross-fitting on two folds.
        half = n // 2
        res_y = np.empty(n)
        res_d = np.empty(n)
        for a, bidx in ((slice(0, half), slice(half, n)), (slice(half, n), slice(0, half))):
            by = _ols(X[a], Y[a])
            bd = _ols(X[a], D[a])
            Xb = np.column_stack([np.ones(X[bidx].shape[0]), X[bidx]])
            res_y[bidx] = Y[bidx] - Xb @ by
            res_d[bidx] = D[bidx] - Xb @ bd
        partialled.append(float(np.sum(res_d * res_y) / np.sum(res_d * res_d)))

    naive_arr, part_arr = np.array(naive), np.array(partialled)
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=naive_arr, name="معامل نموذج التنبؤ المنتظم", opacity=0.65,
                               marker_color=PALETTE[0], nbinsx=40))
    fig.add_trace(go.Histogram(x=part_arr, name="تقدير بعد تنقية المتغيرات", opacity=0.65,
                               marker_color=PALETTE[4], nbinsx=40))
    fig.add_vline(x=true_effect, line=dict(color="#5E8C61", width=3, dash="dash"),
                  annotation_text="الأثر الحقيقي", annotation_position="top")
    fig.update_layout(barmode="overlay", xaxis_title="التقدير", yaxis_title="التكرار")
    show(fig, 380, key="m10-rb-hist")

    a, b = st.columns(2)
    a.metric("متوسط معامل نموذج التنبؤ", f"{naive_arr.mean():.3f}",
             f"{naive_arr.mean() - true_effect:+.3f} عن الحقيقة")
    b.metric("متوسط التقدير بعد التنقية", f"{part_arr.mean():.3f}",
             f"{part_arr.mean() - true_effect:+.3f} عن الحقيقة")

    with st.expander("ماذا ترى بالضبط؟ وما الذي تبسّطه هذه المحاكاة؟"):
        st.markdown(
            "**ما تراه:** ارفع λ وسترى توزيع معامل نموذج التنبؤ **ينزاح** بعيدًا عن الأثر الحقيقي، "
            "بينما يبقى التقدير بعد التنقية متمركزًا حوله. والسبب أن الانتظام يقلّص معاملات المتغيرات "
            "الضابطة، فتتسرب آثارها إلى معامل D — وهذا هو **تحيّز الانتظام**. "
            "وارفع قوة المُربِك وسترى الأثر يشتد.\n\n"
            "**ولاحظ النقطة الجوهرية:** نموذج التنبؤ ليس «سيئًا». فهو قد يتنبأ بـ Y تنبؤًا ممتازًا. "
            "لكن **معاملاته ليست آثارًا**، والدقة التنبؤية لا تصحّحها ولا تدل عليها.\n\n"
            "**ما تبسّطه المحاكاة:** نستعمل انحدارًا خطيًا في خطوتي التنقية، بينما يستعمل التعلّم الآلي "
            "المزدوج نماذج تعلّم آلي مرنة. كما أننا نفترض أن X **يحتوي كل المُربِكات**؛ وفي الواقع "
            "لا تضمن أي طريقة ذلك — والافتراض يأتي من **تصميم البحث** لا من الخوارزمية."
        )


# ------------------------------------------------------------------ 10.4 time-series split


@register("m10_ts_split", "مختبر: ماذا يخفيه التقسيم العشوائي؟", "Time-series split lab", module=10)
def ts_split() -> None:
    st.markdown(
        "أشهر خطأ في تطبيق التعلّم الآلي على بيانات اقتصادية: **تقسيم عشوائي لسلسلة زمنية**. "
        "هنا نقيس كم يبالغ ذلك في تقدير الأداء."
    )
    c1, c2 = st.columns(2)
    persist = c1.slider("درجة الارتباط الذاتي في السلسلة", 0.0, 0.98, 0.9, 0.02, key="m10-ts-rho")
    drift = c2.slider("قوة التغيّر البنيوي في منتصف الفترة", 0.0, 3.0, 1.0, 0.1, key="m10-ts-drift")
    n = 400

    rng = np.random.default_rng(5)
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = persist * x[t - 1] + rng.normal(0, 1)
    shift = np.where(np.arange(n) > n // 2, drift, 0.0)
    y = 0.8 * x + shift + rng.normal(0, 0.5, n)
    lag = np.concatenate([[0], y[:-1]])
    X = np.column_stack([x, lag])

    idx = np.arange(n)
    rnd = rng.permutation(idx)
    r_tr, r_te = rnd[: int(0.7 * n)], rnd[int(0.7 * n):]
    t_tr, t_te = idx[: int(0.7 * n)], idx[int(0.7 * n):]

    def rmse(tr, te):
        b = _ols(X[tr], y[tr])
        pred = np.column_stack([np.ones(len(te)), X[te]]) @ b
        return float(np.sqrt(np.mean((y[te] - pred) ** 2)))

    r_rmse, t_rmse = rmse(r_tr, r_te), rmse(t_tr, t_te)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=idx, y=y, mode="lines", name="السلسلة",
                             line=dict(color=PALETTE[0], width=2)))
    fig.add_vrect(x0=int(0.7 * n), x1=n, fillcolor=PALETTE[4], opacity=0.13, line_width=0,
                  annotation_text="فترة الاختبار الزمني", annotation_position="top left")
    fig.update_xaxes(title="الزمن")
    fig.update_yaxes(title="y")
    show(fig, 320, key="m10-ts-series")

    a, b = st.columns(2)
    a.metric("خطأ التقسيم العشوائي (RMSE)", f"{r_rmse:.3f}")
    b.metric("خطأ التقسيم الزمني (RMSE)", f"{t_rmse:.3f}",
             f"{(t_rmse / max(r_rmse, 1e-9) - 1) * 100:+.0f}% عن العشوائي")

    if t_rmse > r_rmse * 1.15:
        st.error("**التقسيم العشوائي يبالغ في الأداء بوضوح.** وهذا ما ستنشره لو لم تنتبه.")
    else:
        st.info("الفرق صغير عند هذه الإعدادات. **ارفع الارتباط الذاتي أو التغيّر البنيوي** وستراه يتسع.")

    st.markdown(
        "**لماذا يحدث هذا؟** سببان مستقلان يتراكمان:\n"
        "1. **الارتباط الذاتي**: المشاهدة المجاورة تشبه جارتها. فالتقسيم العشوائي يضع لحظة `t` في "
        "التدريب و`t+1` في الاختبار، فيصير النموذج قد «رأى» جواب الاختبار تقريبًا.\n"
        "2. **التغيّر البنيوي**: التقسيم العشوائي يوزّع فترتي ما قبل التغيّر وما بعده على التدريب "
        "والاختبار معًا، فيتعلم النموذج كليهما. أما في الواقع فأنت تتنبأ بمستقبل **لم تره**.\n\n"
        "**والقاعدة:** في أي بيانات لها ترتيب زمني، **قسّم زمنيًا دائمًا**: تدريب على الماضي واختبار "
        "على المستقبل، بلا استثناء."
    )


# ------------------------------------------------------------------ 10.5 text index

# Six short, deliberately constructed Arabic snippets. They are illustrative teaching material,
# not excerpts from any real publication — the lab says so in a caption.
_DOCS = [
    ("نص 1", "سجل الاقتصاد الوطني نموًا في الفصل الأخير، مع ارتفاع الاستثمار وتحسن مؤشرات التشغيل، "
              "رغم بقاء التكاليف مرتفعة وارتفاع الالتزامات الضريبية على المؤسسات."),
    ("نص 2", "أعلنت الشركة عن خسارة في نتائجها، وتراجع رقم أعمالها، مع ارتفاع ديونها قصيرة الأجل "
              "وزيادة المخصصات المسجلة في ميزانيتها."),
    ("نص 3", "لا توجد مخاطر تُذكر على استقرار القطاع، ولم يسجل أي تراجع في الودائع، "
              "ولا مؤشرات على أزمة سيولة وشيكة."),
    ("نص 4", "بيّنت الميزانية بنود الالتزامات والضرائب والديون طويلة الأجل والتكاليف الثابتة، "
              "وهي بنود واردة في كل ميزانية سليمة، إلى جانب تسجيل ربح صافٍ وارتفاع في الأرباح الموزعة."),
    ("نص 5", "تشير المعطيات إلى أزمة في سلاسل التوريد، مع تراجع الإنتاج وارتفاع التكاليف "
              "وتزايد المخاطر على فرص التشغيل في القطاع الصناعي."),
    ("نص 6", "استقرار في أسعار الصرف وتحسن في الميزان التجاري وارتفاع في الصادرات، "
              "مع فرص نمو جديدة في قطاع الخدمات."),
]

_POS = ["نمو", "ارتفاع", "تحسن", "ربح", "أرباح", "فرص", "استقرار", "صادرات", "زيادة"]
# A general-purpose sentiment list treats accounting vocabulary as negative.
_NEG_GENERAL = ["خسارة", "تراجع", "أزمة", "مخاطر", "ديون", "التزامات", "ضرائب",
                "تكاليف", "مخصصات", "ضريبية", "ديونها"]
# A finance-specific list drops the terms that are neutral accounting line items.
_NEG_DOMAIN = ["خسارة", "تراجع", "أزمة", "مخاطر"]
_NEGATORS = {"لا", "لم", "ولا", "ولم", "دون", "غير", "بدون"}


def _tokens(text: str) -> list[str]:
    out = []
    for w in text.replace("،", " ").replace(".", " ").replace("«", " ").replace("»", " ").split():
        for prefix in ("وال", "بال", "لل", "فال", "ال", "و"):
            if w.startswith(prefix) and len(w) > len(prefix) + 2:
                w = w[len(prefix):]
                break
        out.append(w)
    return out


def _score(text: str, neg_list: list[str], normalise: bool, handle_negation: bool) -> float:
    toks = _tokens(text)
    pos = neg = 0
    for i, w in enumerate(toks):
        hit_pos = any(w.startswith(p) for p in _POS)
        hit_neg = any(w.startswith(p) for p in neg_list)
        if not (hit_pos or hit_neg):
            continue
        flipped = handle_negation and any(t in _NEGATORS for t in toks[max(0, i - 2):i])
        if hit_pos != flipped:
            pos += 1
        else:
            neg += 1
    raw = pos - neg
    return (raw / len(toks) * 100) if normalise and toks else float(raw)


@register("m10_text_index", "مختبر: ابنِ مؤشرًا نصيًا وغيّر قراراتك", "Text index builder", module=10)
def text_index() -> None:
    st.markdown(
        "ستة نصوص **ثابتة لا تتغير**. وكل ما ستغيّره هو **قرارات القياس**: أي قاموس، وهل تطبّع، "
        "وهل تعالج النفي. وراقب ماذا يحدث للأرقام — وللترتيب."
    )
    c1, c2, c3 = st.columns(3)
    dict_choice = c1.radio("القاموس", ["قاموس عام", "قاموس مخصص للسياق المالي"], key="m10-ti-dict")
    normalise = c2.toggle("تطبيع بعدد الكلمات", value=False, key="m10-ti-norm")
    handle_negation = c3.toggle("معالجة النفي", value=False, key="m10-ti-neg")
    neg_list = _NEG_GENERAL if dict_choice == "قاموس عام" else _NEG_DOMAIN

    labels = [d[0] for d in _DOCS]
    current = [_score(t, neg_list, normalise, handle_negation) for _, t in _DOCS]
    general = [_score(t, _NEG_GENERAL, normalise, handle_negation) for _, t in _DOCS]
    domain = [_score(t, _NEG_DOMAIN, normalise, handle_negation) for _, t in _DOCS]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=labels, y=current, marker_color=[
        PALETTE[0] if v < 0 else PALETTE[4] for v in current], name="المؤشر"))
    fig.add_hline(y=0, line=dict(color="#C7B8AE", width=1))
    fig.update_yaxes(title="المؤشر" + (" (لكل 100 كلمة)" if normalise else " (عدّ مطلق)"))
    fig.update_layout(showlegend=False)
    show(fig, 340, key="m10-ti-bars")

    rank_g = {lab: r for r, lab in enumerate(sorted(labels, key=lambda l: -general[labels.index(l)]), 1)}
    rank_d = {lab: r for r, lab in enumerate(sorted(labels, key=lambda l: -domain[labels.index(l)]), 1)}
    moved = [lab for lab in labels if rank_g[lab] != rank_d[lab]]

    st.markdown("**ترتيب النصوص من الأكثر إيجابية إلى الأقل، تحت القاموسين:**")
    rows = ["| النص | قاموس عام | قاموس مخصص | تغيّر الترتيب |", "|---|---|---|---|"]
    for lab in labels:
        arrow = "—" if rank_g[lab] == rank_d[lab] else f"{rank_g[lab]} ← {rank_d[lab]}"
        rows.append(f"| {lab} | {general[labels.index(lab)]:.1f} | {domain[labels.index(lab)]:.1f} | {arrow} |")
    st.markdown("\n".join(rows))

    if moved:
        st.warning(
            f"**تغيّر ترتيب {len(moved)} نصوص** بتغيير القاموس وحده، والنصوص لم تتغير حرفًا واحدًا. "
            "فالرقم ليس خاصية للنص، بل خاصية لـ «النص + أداة القياس»."
        )
    else:
        st.info("الترتيب متطابق عند هذه الإعدادات. **غيّر التطبيع أو معالجة النفي** وراقب متى ينكسر.")

    with st.expander("ماذا تفحص بالضبط؟ وما الذي تبسّطه هذه المحاكاة؟"):
        st.markdown(
            "**النص 4 هو الاختبار الأهم.** فهو نص عن **ميزانية سليمة** تحقق ربحًا، لكنه مليء ببنود "
            "محاسبية محايدة (التزامات، وضرائب، وديون، وتكاليف). وبالقاموس العام يخرج **سلبيًا**، "
            "وبالقاموس المخصص يخرج **إيجابيًا**. وهذا هو بالضبط ما وثّقته أدبيات النبرة المالية.\n\n"
            "**والنص 3 يختبر النفي.** كل جمله طمأنة مصوغة بالنفي: «لا توجد مخاطر»، و«لم يسجل أي تراجع». "
            "فبلا معالجة النفي يخرج **أشد النصوص سلبية**، وهو في الحقيقة أكثرها طمأنة. شغّل «معالجة "
            "النفي» وسترى سلبيته تزول — ولن ينقلب إيجابيًا، لأن العدّ لا يرى في النفي إثباتًا للعكس.\n\n"
            "**والنص 2 يكشف حدًا لا تعالجه أي من هذه المفاتيح:** كلمتا «ارتفاع» و«زيادة» محسوبتان "
            "إيجابيتين، وهما هنا تصفان **ارتفاع الديون وزيادة المخصصات**. فطريقة عدّ الكلمات "
            "**لا ترى ما تتعلق به الكلمة**، ولهذا تتوقف السلاسل الجادة عن الاكتفاء بالعدّ حين يكون "
            "هذا النمط شائعًا في مجموعتها.\n\n"
            "**والتطبيع يكشف أثر الطول:** فالنص الأطول يجمع كلمات أكثر بحكم طوله لا بحكم نبرته.\n\n"
            "**ما تبسّطه المحاكاة:** التجذيع هنا بدائي (حذف سوابق شائعة فقط)، ومعالجة النفي تقتصر على "
            "نافذة كلمتين قبل الكلمة، والقاموسان قصيران جدًا. والمؤشرات الجادة تستعمل قوائم من مئات "
            "الكلمات مبنية على السياق ومحقّقة بتصنيف بشري. **والدرس لا يتغير بتكبير القوائم**: قرارات "
            "القياس جزء من النتيجة، ويجب أن تُعلن معها."
        )
    st.caption(
        "النصوص الستة **مصوغة لأغراض التدريس** ولا تمثل اقتباسات من أي منشور حقيقي، "
        "والقاموسان مختصران عمدًا ليظهر الأثر في ستة نصوص."
    )


# ------------------------------------------------------------------ 10.7 leakage hunt

_LEAKS = [
    {
        "title": "التنبؤ بالتعثر الائتماني",
        "design": "بيانات قروض 2015–2024. المتغيرات تشمل: الدخل، والعمر، ومدة القرض، "
                  "و**عدد مكالمات قسم التحصيل**. قُسّمت البيانات عشوائيًا 70/30. الدقة: 96%.",
        "leaks": ["متغير وكيل: مكالمات التحصيل تقع **بعد** التعثر",
                  "تسرّب زمني: تقسيم عشوائي لبيانات مرتبة زمنيًا"],
        "fix": "احذف كل متغير لا يتوفر **لحظة اتخاذ القرار**، واسأل عن كل متغير: متى يُسجَّل بالضبط؟ "
               "ثم قسّم زمنيًا: درّب على 2015–2021 واختبر على 2022–2024.",
    },
    {
        "title": "التنبؤ بالتضخم الشهري",
        "design": "سلسلة شهرية 1990–2024. طُبّع كل المتغيرات (بطرح المتوسط والقسمة على الانحراف "
                  "المعياري) على **كامل العينة**، ثم قُسّمت زمنيًا. الأداء ممتاز.",
        "leaks": ["تسرّب المعالجة: التطبيع على كامل العينة يسرّب إحصاءات فترة الاختبار إلى التدريب"],
        "fix": "احسب معاملات التطبيع على **فترة التدريب وحدها**، ثم طبّقها على الاختبار. "
               "والقاعدة العامة: كل خطوة معالجة تتعلم شيئًا من البيانات يجب أن تتعلمه من التدريب فقط.",
    },
    {
        "title": "تقييم أثر برنامج تدريبي على الأجور",
        "design": "عيّنة من المشاركين في البرنامج **الذين أكملوه**، مقارنةً بغير المشاركين. "
                  "نموذج تعلّم آلي بدقة تنبؤ عالية. الاستنتاج: البرنامج يرفع الأجر بنسبة كبيرة.",
        "leaks": ["اختيار بعد النظر: من أكمل البرنامج فئة منتقاة",
                  "خلط بين التنبؤ والسببية: الدقة العالية لا تسند ادعاءً سببيًا"],
        "fix": "الادعاء **سببي**، فيحتاج تصميمًا: تخصيصًا عشوائيًا، أو فروق الفروق، أو متغيرًا مساعدًا. "
               "وأدرج **المنقطعين** في تحليل نية المعالجة. ودقة النموذج لا تعوّض غياب التصميم.",
    },
    {
        "title": "تصنيف الشركات المتعثرة من تقاريرها",
        "design": "تقارير سنوية لشركات، ونموذج نصي يتنبأ بالتعثر. بعض الشركات لها **عدة تقارير** "
                  "وزّعت عشوائيًا بين التدريب والاختبار. الدقة: 93%.",
        "leaks": ["تكرار السجلات: تقارير الشركة نفسها في التدريب والاختبار",
                  "تسرّب زمني محتمل: تقارير لاحقة في التدريب وسابقة في الاختبار"],
        "fix": "قسّم **على مستوى الشركة** لا التقرير (كل تقارير الشركة في جانب واحد)، وقسّم زمنيًا "
               "كذلك. فما يُقاس هنا ذاكرة لأسلوب الشركة لا قدرة على التعميم.",
    },
]


@register("m10_leakage_hunt", "صيد التسرّب: شخّص وصحّح", "Leakage hunt", module=10)
def leakage_hunt() -> None:
    st.markdown(
        "أربعة تصاميم تحليلية، كلها تعطي **أرقام أداء ممتازة**، وكلها معطوبة. "
        "شخّص المشكلة في كل واحد قبل أن تكشف التحليل."
    )
    score = 0
    for i, case in enumerate(_LEAKS):
        with st.container(border=True, key=f"m10-lk-{i}"):
            st.markdown(f"**التصميم {i + 1}: {case['title']}**")
            st.caption(case["design"])
            guess = st.text_area("ما المشكلة في رأيك؟", key=f"m10-lk-g{i}", height=80,
                                 placeholder="اكتب تشخيصك قبل الكشف — فالكتابة قبل الكشف هي التمرين.")
            if st.toggle("اكشف التحليل", key=f"m10-lk-r{i}"):
                if guess.strip():
                    score += 1
                for lk in case["leaks"]:
                    st.error(f"**{lk}**")
                st.success(f"**التصحيح:** {case['fix']}")
    if score:
        st.caption(f"كتبتَ تشخيصًا قبل الكشف في **{score}** من {len(_LEAKS)} تصاميم. "
                   "والكتابة قبل الكشف هي ما يبني المهارة، لا قراءة الجواب.")
    st.divider()
    st.markdown(
        "**السؤال الواحد الذي يكشف أغلب التسرّب:** لكل متغير في نموذجك، اسأل: "
        "**«متى يُسجَّل هذا فعلًا، وهل كان متاحًا لحظة اتخاذ القرار؟»** "
        "فأي متغير يُسجَّل بعد الحدث المتنبَّأ به — أو يحمل أثره — هو تسرّب مهما بدا منطقيًا."
    )
