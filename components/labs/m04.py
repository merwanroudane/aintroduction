"""Module 4 labs, all offline (numpy + plotly): paradigm sorter, perceptron, gradient descent,
model complexity (over/underfitting) and a confusion-matrix threshold explorer."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from components.diagrams import show
from components.labs import register

# ----------------------------------------------------------------- 4.2 paradigms

PARADIGMS = ["موجَّه", "غير موجَّه", "ذاتي الإشراف", "معزز"]
PROBLEMS = [
    ("لديك 50 ألف رسالة صنّفها موظفون إلى «شكوى» و«استفسار»، وتريد تصنيف الرسائل الجديدة.", "موجَّه",
     "أمثلة مع الإجابة الصحيحة (وسم) = تعلم موجَّه."),
    ("لديك بيانات مشتريات 100 ألف عميل بلا أي تصنيف، وتريد اكتشاف مجموعات متشابهة السلوك.", "غير موجَّه",
     "لا توجد أوسمة، والهدف اكتشاف بنية = تجميع (تعلم غير موجَّه)."),
    ("تريد تدريب نموذج لغوي على مليارات الجمل بإخفاء كلمة وطلب التنبؤ بها.", "ذاتي الإشراف",
     "الهدف مشتق من البيانات نفسها دون وسم بشري = تعلم ذاتي الإشراف."),
    ("روبوت يتعلم السير بالتجربة: يحصل على مكافأة حين يتقدم وعقوبة حين يسقط.", "معزز",
     "تعلم بالتفاعل مع بيئة عبر مكافأة = تعلم معزز."),
    ("لديك 500 صورة أشعة موسومة بأطباء، ومليون صورة غير موسومة، وتريد الاستفادة من الاثنين.", "ذاتي الإشراف",
     "التدريب المسبق الذاتي الإشراف على غير الموسومة ثم الضبط على الموسومة هو الحل المعتاد "
     "(ويسمى أحيانًا شبه موجَّه حسب التفصيل)."),
    ("تريد التنبؤ بسعر شقة انطلاقًا من مساحتها وموقعها، ولديك أسعار 8000 صفقة سابقة.", "موجَّه",
     "مخرج عددي معروف في البيانات = انحدار ضمن التعلم الموجَّه."),
    ("تريد ضغط بيانات ذات 200 متغير إلى بعدين لرسمها وفهم بنيتها.", "غير موجَّه",
     "تقليل الأبعاد بلا أوسمة = تعلم غير موجَّه."),
    ("نظام يتعلم استراتيجية تسعير بتجريب أسعار ومراقبة الأرباح الناتجة عبر الزمن.", "معزز",
     "أفعال متتابعة ومكافأة مؤجلة = تعلم معزز."),
    ("تريد كشف المعاملات الشاذة دون أن يكون لديك أمثلة موسومة للاحتيال.", "غير موجَّه",
     "كشف الشذوذ بلا أوسمة = تعلم غير موجَّه."),
    ("تدرّب نموذجًا ليتنبأ بالجزء المخفي من صورة انطلاقًا من بقيتها.", "ذاتي الإشراف",
     "الإشارة التعليمية مستخرجة من البيانات نفسها = ذاتي الإشراف."),
]


@register("m04_paradigm_sorter", "أي نمط تعلم يناسب هذه المسألة؟", "Learning paradigm sorter", module=4)
def paradigm_sorter() -> None:
    st.caption("لكل مسألة، حدد نمط التعلم المناسب. السؤال الحاسم دائمًا: **هل توجد إجابة صحيحة في البيانات؟ "
               "ومن أين تأتي؟**")
    with st.form("m04_paradigm_sorter-form"):
        answers = [st.selectbox(f"{i + 1}. {t}", PARADIGMS, index=None, placeholder="اختر النمط",
                                key=f"m04_paradigm_sorter-{i}")
                   for i, (t, _, _) in enumerate(PROBLEMS)]
        done = st.form_submit_button("صحّح", icon=":material/task_alt:")
    if not done:
        return
    score = sum(a == c for a, (_, c, _) in zip(answers, PROBLEMS))
    st.metric("النتيجة", f"{score} / {len(PROBLEMS)}")
    for i, (a, (t, c, why)) in enumerate(zip(answers, PROBLEMS), 1):
        if a != c:
            st.markdown(f"- **{i}.** النمط: **{c}** — {why}" + (f" (اخترت: {a})" if a else ""))
    (st.success if score >= 8 else st.info)(
        "تمييز جيد بين الأنماط." if score >= 8 else "راجع جدول الأنماط في المحاضرة 4.2؛ الهدف 8 من 10.")


# ----------------------------------------------------------------- 4.4 perceptron

@register("m04_perceptron", "البيرسبترون: الأوزان والحد الفاصل", "Perceptron playground", module=4)
def perceptron() -> None:
    st.caption("النيورون يحسب $z = w_1x_1 + w_2x_2 + b$ ثم يطبق دالة تنشيط. "
               "حرّك الأوزان وراقب كيف يتحرك الحد الفاصل ويتغير التصنيف.")
    c1, c2, c3 = st.columns(3)
    w1 = c1.slider("الوزن w₁", -3.0, 3.0, 1.0, 0.1, key="m04_perceptron-w1")
    w2 = c2.slider("الوزن w₂", -3.0, 3.0, 1.0, 0.1, key="m04_perceptron-w2")
    b = c3.slider("الانحياز b", -3.0, 3.0, -0.5, 0.1, key="m04_perceptron-b")
    act = st.segmented_control("دالة التنشيط", ["عتبة (Step)", "سيجمويد (Sigmoid)", "ReLU"],
                               default="عتبة (Step)", key="m04_perceptron-act", required=True)
    problem = st.segmented_control("المسألة", ["AND", "OR", "XOR"], default="AND",
                                   key="m04_perceptron-prob", required=True)

    pts = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    targets = {"AND": [0, 0, 0, 1], "OR": [0, 1, 1, 1], "XOR": [0, 1, 1, 0]}[problem]

    def activate(z):
        if act.startswith("عتبة"):
            return (z >= 0).astype(float)
        if act.startswith("سيجمويد"):
            return 1 / (1 + np.exp(-z))
        return np.maximum(0, z)

    z = pts @ np.array([w1, w2]) + b
    out = activate(z)
    pred = (out >= 0.5).astype(int) if not act.startswith("عتبة") else out.astype(int)
    correct = int((pred == np.array(targets)).sum())

    gx = np.linspace(-0.4, 1.4, 120)
    fig = go.Figure()
    if abs(w2) > 1e-6:
        fig.add_trace(go.Scatter(x=gx, y=-(w1 * gx + b) / w2, mode="lines", name="الحد الفاصل",
                                 line=dict(color="#5E8C61", width=3)))
    for cls, color, sym in [(1, "#C8553D", "circle"), (0, "#5B9BD5", "square")]:
        idx = [i for i, t in enumerate(targets) if t == cls]
        fig.add_trace(go.Scatter(
            x=pts[idx, 0], y=pts[idx, 1], mode="markers+text",
            text=[f"({int(pts[i,0])},{int(pts[i,1])})→{targets[i]}" for i in idx],
            textposition="top center", name=f"الفئة {cls}",
            marker=dict(size=18, color=color, symbol=sym, line=dict(color="#FFFFFF", width=2))))
    fig.update_xaxes(title="x₁", range=[-0.4, 1.5])
    fig.update_yaxes(title="x₂", range=[-0.4, 1.5])
    fig.update_layout(legend=dict(orientation="h", y=1.14))
    show(fig, 430, key="m04-perceptron")

    st.metric("نقاط مصنّفة تصنيفًا صحيحًا", f"{correct} / 4")
    st.dataframe([{"x₁": int(p[0]), "x₂": int(p[1]), "z": round(float(zz), 2),
                   "المخرج": round(float(o), 3), "التنبؤ": int(pr), "المطلوب": t}
                  for p, zz, o, pr, t in zip(pts, z, out, pred, targets)], hide_index=True)
    if problem == "XOR" and correct < 4:
        st.warning("لن تبلغ 4/4 في XOR مهما جرّبت: نقطتا الفئة 1 تقعان على قطرين متقابلين، "
                   "ولا يفصلهما مستقيم واحد. هذا بالضبط ما بيّنه Minsky و Papert سنة 1969 (المحاضرة 2.2)، "
                   "والحل هو إضافة طبقة خفية.", icon=":material/lightbulb:")
    elif correct == 4:
        st.success("أحسنت: هذه المسألة قابلة للفصل خطيًا، فوجد النيورون الواحد حدًا يفصل الفئتين.")


# ----------------------------------------------------------------- 4.5 gradient descent

@register("m04_gradient_descent", "النزول التدريجي خطوة بخطوة", "Gradient descent", module=4)
def gradient_descent() -> None:
    st.caption("نبحث عن الوزن الذي يقلل الخسارة. النزول التدريجي يتحرك عكس اتجاه الميل بخطوة يحددها "
               "**معدل التعلم**. جرّب معدلات مختلفة ولاحظ متى يتقارب ومتى ينفجر.")
    c1, c2, c3 = st.columns(3)
    lr = c1.select_slider("معدل التعلم η", [0.01, 0.05, 0.1, 0.3, 0.6, 0.9, 1.05],
                          value=0.1, key="m04_gradient_descent-lr")
    steps = c2.slider("عدد الخطوات", 1, 40, 12, key="m04_gradient_descent-steps")
    w0 = c3.slider("نقطة البداية", -4.0, 4.0, -3.5, 0.5, key="m04_gradient_descent-w0")

    def loss(w):
        return 0.5 * w ** 2 + 0.6 * np.sin(3 * w) + 1.2

    def grad(w):
        return w + 1.8 * np.cos(3 * w)

    ws, w = [w0], w0
    for _ in range(steps):
        w = w - lr * grad(w)
        w = float(np.clip(w, -6, 6))
        ws.append(w)

    grid = np.linspace(-4.5, 4.5, 300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=grid, y=loss(grid), mode="lines", name="دالة الخسارة",
                             line=dict(color="#E9B99A", width=3)))
    fig.add_trace(go.Scatter(x=ws, y=[loss(x) for x in ws], mode="lines+markers", name="مسار النزول",
                             line=dict(color="#C8553D", width=2),
                             marker=dict(size=[13] + [7] * (len(ws) - 2) + [15],
                                         color=["#5E8C61"] + ["#C8553D"] * (len(ws) - 2) + ["#3A2E2B"])))
    fig.update_xaxes(title="الوزن w")
    fig.update_yaxes(title="الخسارة L(w)")
    fig.update_layout(legend=dict(orientation="h", y=1.14))
    show(fig, 430, key="m04-gd")

    c1, c2, c3 = st.columns(3)
    c1.metric("الخسارة الابتدائية", f"{loss(w0):.3f}")
    c2.metric("الخسارة النهائية", f"{loss(ws[-1]):.3f}")
    c3.metric("الوزن النهائي", f"{ws[-1]:.3f}")
    if lr >= 0.9:
        st.warning("معدل تعلم كبير جدًا: الخطوات تتجاوز القاع فتتذبذب أو تتباعد. "
                   "هذا سبب شائع لفشل التدريب.", icon=":material/warning:")
    elif lr <= 0.01:
        st.info("معدل تعلم صغير جدًا: التقارب صحيح لكنه بطيء، وقد يحتاج إلى خطوات كثيرة جدًا.")
    st.caption("لاحظ أيضًا أثر نقطة البداية: هذه الدالة لها أكثر من قاع محلي، وقد ينتهي النزول إلى قاع "
               "غير الأعمق. هذا تبسيط لسطح حقيقي في ملايين الأبعاد.")


# ----------------------------------------------------------------- 4.5 complexity

@register("m04_complexity", "تعقيد النموذج: نقص التوافق والإفراط فيه", "Model complexity", module=4)
def complexity() -> None:
    st.caption("نولّد بيانات من علاقة حقيقية + ضجيج، ونلائمها بكثير حدود من درجة متغيرة. "
               "راقب خطأ التدريب وخطأ الاختبار معًا: الفرق بينهما هو القصة كلها.")
    c1, c2, c3 = st.columns(3)
    deg = c1.slider("درجة كثير الحدود (التعقيد)", 1, 15, 3, key="m04_complexity-deg")
    noise = c2.slider("مستوى الضجيج", 0.0, 2.5, 1.0, 0.1, key="m04_complexity-noise")
    n = c3.slider("حجم بيانات التدريب", 8, 60, 20, key="m04_complexity-n")

    rng = np.random.default_rng(3)
    def truth(x):
        return 0.6 * x ** 2 - 0.5 * x + 1
    x_tr = np.sort(rng.uniform(-3, 3, n))
    y_tr = truth(x_tr) + rng.normal(0, noise, n)
    x_te = np.sort(rng.uniform(-3, 3, 200))
    y_te = truth(x_te) + rng.normal(0, noise, 200)

    coef = np.polyfit(x_tr, y_tr, deg)
    err_tr = float(np.mean((np.polyval(coef, x_tr) - y_tr) ** 2))
    err_te = float(np.mean((np.polyval(coef, x_te) - y_te) ** 2))

    grid = np.linspace(-3.2, 3.2, 300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_tr, y=y_tr, mode="markers", name="بيانات التدريب",
                             marker=dict(size=9, color="#7D6E68")))
    fig.add_trace(go.Scatter(x=grid, y=truth(grid), mode="lines", name="العلاقة الحقيقية",
                             line=dict(color="#5E8C61", width=3, dash="dash")))
    fig.add_trace(go.Scatter(x=grid, y=np.polyval(coef, grid), mode="lines", name=f"النموذج (درجة {deg})",
                             line=dict(color="#C8553D", width=3)))
    fig.update_yaxes(range=[float(min(y_tr)) - 4, float(max(y_tr)) + 4])
    fig.update_layout(legend=dict(orientation="h", y=1.14))
    show(fig, 430, key="m04-complexity")

    c1, c2, c3 = st.columns(3)
    c1.metric("خطأ التدريب (MSE)", f"{err_tr:.2f}")
    c2.metric("خطأ الاختبار (MSE)", f"{err_te:.2f}")
    c3.metric("الفجوة", f"{err_te - err_tr:.2f}")
    if err_te > 2.2 * max(err_tr, 1e-6) and deg >= 6:
        st.error("**إفراط في التوافق:** خطأ التدريب صغير والاختبار كبير. النموذج حفظ الضجيج. "
                 "العلاج: تقليل التعقيد، أو زيادة البيانات، أو التنظيم (Regularization).",
                 icon=":material/warning:")
    elif err_tr > 1.4 * noise ** 2 + 0.6 and deg <= 2:
        st.warning("**نقص في التوافق:** النموذج أبسط من أن يلتقط البنية الحقيقية. "
                   "العلاج: زيادة التعقيد أو إضافة سمات أفضل.", icon=":material/trending_down:")
    else:
        st.success("توازن معقول بين البساطة والقدرة على التقاط البنية.")
    st.caption("جرّب: ثبّت الدرجة على 15 وارفع حجم البيانات تدريجيًا. ستلاحظ أن **زيادة البيانات** "
               "تخفف الإفراط في التوافق دون تغيير النموذج. هذا مبدأ عملي مهم.")


# ----------------------------------------------------------------- 4.6 threshold

@register("m04_threshold", "مصفوفة الارتباك وعتبة القرار", "Confusion matrix & threshold", module=4)
def threshold_lab() -> None:
    st.caption("نموذج يعطي **احتمالًا** لا قرارًا. القرار يأتي من **عتبة** نختارها نحن، وهذا الاختيار "
               "قرار قيمي لا تقني: من نفضل أن نخطئ في حقه؟")
    c1, c2 = st.columns(2)
    prevalence = c1.slider("نسبة انتشار الحالة في العينة %", 1, 50, 5, key="m04_threshold-prev")
    thr = c2.slider("عتبة القرار", 0.05, 0.95, 0.50, 0.05, key="m04_threshold-thr")
    sep = st.slider("جودة النموذج (فصل الفئتين)", 0.5, 3.5, 1.8, 0.1, key="m04_threshold-sep")

    rng = np.random.default_rng(11)
    n = 1000
    n_pos = max(int(n * prevalence / 100), 5)
    scores_pos = 1 / (1 + np.exp(-rng.normal(sep, 1.0, n_pos)))
    scores_neg = 1 / (1 + np.exp(-rng.normal(-sep, 1.0, n - n_pos)))
    tp = int((scores_pos >= thr).sum())
    fn = n_pos - tp
    fp = int((scores_neg >= thr).sum())
    tn = (n - n_pos) - fp

    acc = (tp + tn) / n
    recall = tp / max(tp + fn, 1)
    precision = tp / max(tp + fp, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-9)

    fig = go.Figure(go.Heatmap(
        z=[[tp, fn], [fp, tn]], x=["تنبؤ: إيجابي", "تنبؤ: سلبي"], y=["الواقع: إيجابي", "الواقع: سلبي"],
        text=[[f"إيجابي صحيح<br>{tp}", f"سلبي كاذب<br>{fn}"], [f"إيجابي كاذب<br>{fp}", f"سلبي صحيح<br>{tn}"]],
        texttemplate="%{text}", colorscale=[[0, "#FFF4E6"], [1, "#E07A5F"]], showscale=False))
    fig.update_yaxes(autorange="reversed", side="right")
    show(fig, 320, key="m04-threshold")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("الدقة الإجمالية", f"{acc:.1%}")
    c2.metric("الاستدعاء (Recall)", f"{recall:.1%}", help="من بين المصابين فعلًا، كم اكتشف النظام؟")
    c3.metric("الدقة الإيجابية (Precision)", f"{precision:.1%}", help="من بين من قال إنهم مصابون، كم كان محقًا؟")
    c4.metric("F1", f"{f1:.1%}")

    naive = (n - n_pos) / n
    st.info(f"**خط الأساس الساذج:** نموذج يقول «سلبي» للجميع يحقق دقة إجمالية {naive:.1%} "
            f"واستدعاء 0%. قارن بها دائمًا قبل الاحتفال بالدقة.", icon=":material/balance:")
    if thr <= 0.25:
        st.warning("عتبة منخفضة: يرتفع الاستدعاء (نفوّت حالات أقل) وتنخفض الدقة الإيجابية "
                   "(إنذارات كاذبة أكثر). مناسب حين تكون كلفة تفويت الحالة عالية، كفحص أولي لمرض خطير.")
    elif thr >= 0.75:
        st.warning("عتبة مرتفعة: ترتفع الدقة الإيجابية وينخفض الاستدعاء. مناسب حين تكون كلفة "
                   "الإنذار الكاذب عالية، كاتهام شخص بالاحتيال.")
    st.caption("لا توجد عتبة «صحيحة» رياضيًا: الاختيار يوازن بين نوعي الخطأ وفق كلفتهما في السياق الواقعي.")
