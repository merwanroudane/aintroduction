"""Module 4 diagrams: concept map, nested AI/ML/DL sets, learning paradigms, the ML workflow,
a layered neural network, the loss landscape, and over/underfitting curves."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from components.diagrams import PALETTE, flow, grid_cards, nested, network, register, show


@register("m04_concept_map")
def concept_map() -> None:
    nodes = [
        {"id": "ml", "label": "التعلم الآلي", "x": 0, "y": 0, "group": 0},
        {"id": "par", "label": "أنماط التعلم", "x": -2.0, "y": 1.1, "group": 1, "hover": "موجَّه، غير موجَّه، ذاتي الإشراف، معزز"},
        {"id": "data", "label": "البيانات والسمات", "x": -2.3, "y": -0.4, "group": 2, "hover": "بيانات، سمة، وسم، تقسيم"},
        {"id": "model", "label": "النموذج والمعاملات", "x": -1.0, "y": -1.6, "group": 2},
        {"id": "loss", "label": "الخسارة", "x": 0.6, "y": -1.8, "group": 3, "hover": "ما يقيس الخطأ ويوجّه التعلم"},
        {"id": "opt", "label": "النزول التدريجي", "x": 2.0, "y": -0.9, "group": 3},
        {"id": "gen", "label": "التعميم", "x": 2.3, "y": 0.6, "group": 4, "hover": "الإفراط في التوافق ونقصه"},
        {"id": "eval", "label": "التقييم", "x": 1.2, "y": 1.7, "group": 4, "hover": "دقة، استدعاء، F1، RMSE"},
        {"id": "dl", "label": "التعلم العميق", "x": -0.6, "y": 1.9, "group": 5, "hover": "شبكات متعددة الطبقات تتعلم التمثيلات"},
    ]
    edges = [("ml", "par"), ("ml", "data"), ("data", "model"), ("model", "loss"), ("loss", "opt"),
             ("opt", "gen"), ("gen", "eval"), ("ml", "dl"), ("dl", "model"), ("eval", "par")]
    network(nodes, edges, height=500, key="m04-concept")


@register("m04_nested")
def nested_sets() -> None:
    nested([
        ("الذكاء الاصطناعي", "Artificial Intelligence",
         "كل ما يجعل الآلة تؤدي مهامًا تتطلب ذكاءً: بحث، منطق، قواعد، تخطيط، وتعلم."),
        ("التعلم الآلي", "Machine Learning",
         "المناهج التي تستنتج القواعد من البيانات بدل أن يكتبها الخبير."),
        ("التعلم العميق", "Deep Learning",
         "شبكات عصبية متعددة الطبقات تتعلم التمثيلات بنفسها."),
        ("النماذج التوليدية والتأسيسية", "Generative / Foundation Models",
         "نماذج كبيرة تتعلم توزيع البيانات فتولّد محتوى جديدًا، وتُكيَّف لمهام كثيرة (ومنها النماذج اللغوية الكبيرة)."),
    ], caption="علاقة تضمين لا تواز: كل تعلم عميق تعلم آلي، وكل تعلم آلي ذكاء اصطناعي، والعكس غير صحيح.")


@register("m04_paradigms")
def paradigms() -> None:
    grid_cards([
        ("التعلم الموجَّه", "Supervised", "أمثلة مع الإجابة الصحيحة (وسم). الهدف: تعلّم دالة من المدخل إلى الوسم. مثال: تصنيف رسائل."),
        ("التعلم غير الموجَّه", "Unsupervised", "بيانات بلا أوسمة. الهدف: اكتشاف بنية. مثال: تجميع العملاء، تقليل الأبعاد."),
        ("شبه الموجَّه", "Semi-supervised", "أوسمة قليلة وبيانات كثيرة بلا أوسمة؛ يستفيد من الاثنين معًا."),
        ("الذاتي الإشراف", "Self-supervised", "الهدف يُشتق من البيانات نفسها (أخفِ كلمة وتنبأ بها). أساس النماذج اللغوية."),
        ("المعزز", "Reinforcement", "وكيل يتعلم بالتجربة من المكافأة والعقوبة في بيئة. مثال: الألعاب، التحكم."),
        ("التعلم من التغذية الراجعة البشرية", "RLHF — امتداد حديث", "تعلم معزز من تفضيلات بشرية لمواءمة سلوك النموذج (Ouyang et al., 2022)."),
    ], cols=3)


@register("m04_workflow")
def workflow() -> None:
    flow([("تحديد المهمة والمقياس", "Task & metric"), ("جمع البيانات وتنظيفها", "Data"),
          ("التقسيم: تدريب/تحقق/اختبار", "Split"), ("التدريب", "Train"),
          ("الضبط على التحقق", "Validate & tune"), ("التقييم النهائي على الاختبار", "Test"),
          ("النشر", "Deploy"), ("المراقبة", "Monitor")],
         loop=True,
         caption="مخطط العمل: مجموعة الاختبار تُفتح مرة واحدة في النهاية، والمراقبة تعيدنا إلى البداية عند انحراف الأداء.")


@register("m04_neural_net")
def neural_net() -> None:
    layers = [(4, "المدخلات", "Input"), (5, "طبقة خفية", "Hidden"), (5, "طبقة خفية", "Hidden"), (2, "المخرج", "Output")]
    fig = go.Figure()
    pos = {}
    for li, (n, _, _) in enumerate(layers):
        for i in range(n):
            pos[(li, i)] = (li * 1.6, (n - 1) / 2 - i)
    for li in range(len(layers) - 1):
        for i in range(layers[li][0]):
            for j in range(layers[li + 1][0]):
                x0, y0 = pos[(li, i)]
                x1, y1 = pos[(li + 1, j)]
                fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode="lines",
                                         line=dict(color="rgba(224,122,95,0.28)", width=1),
                                         hoverinfo="skip", showlegend=False))
    for li, (n, ar, en) in enumerate(layers):
        fig.add_trace(go.Scatter(
            x=[pos[(li, i)][0] for i in range(n)], y=[pos[(li, i)][1] for i in range(n)],
            mode="markers", marker=dict(size=26, color=PALETTE[li % len(PALETTE)],
                                        line=dict(color="#FFFFFF", width=2)),
            hovertext=[f"{ar} · {en}"] * n, hoverinfo="text", showlegend=False))
        fig.add_annotation(x=li * 1.6, y=3.0, text=f"<b>{ar}</b><br>{en}", showarrow=False,
                           font=dict(size=12))
    fig.update_xaxes(visible=False, range=[-0.8, (len(layers) - 1) * 1.6 + 0.8])
    fig.update_yaxes(visible=False, range=[-3.0, 3.6])
    show(fig, 420, key="m04-net")
    st.caption("كل خط وزن يُتعلَّم، وكل عقدة تحسب مجموعًا موزونًا ثم تطبق دالة تنشيط. "
               "الطبقات الخفية هي التي تكتشف السمات الوسيطة (المحاضرة 2.3).")


@register("m04_loss_landscape")
def loss_landscape() -> None:
    x = np.linspace(-3, 3, 60)
    y = np.linspace(-3, 3, 60)
    X, Y = np.meshgrid(x, y)
    Z = (X ** 2 + Y ** 2) / 6 + 0.55 * np.sin(2 * X) * np.cos(2 * Y) + 1.1
    fig = go.Figure(go.Surface(z=Z, x=x, y=y, showscale=False,
                               colorscale=[[0, "#FFF4E6"], [0.5, "#FFC59E"], [1, "#A8483A"]]))
    path_x = [-2.6, -2.0, -1.4, -0.9, -0.5, -0.25, -0.1]
    path_y = [2.4, 1.8, 1.2, 0.7, 0.35, 0.15, 0.05]
    path_z = [(px ** 2 + py ** 2) / 6 + 0.55 * np.sin(2 * px) * np.cos(2 * py) + 1.16
              for px, py in zip(path_x, path_y)]
    fig.add_trace(go.Scatter3d(x=path_x, y=path_y, z=path_z, mode="lines+markers",
                               line=dict(color="#3A2E2B", width=5),
                               marker=dict(size=4, color="#3A2E2B"), name="مسار النزول"))
    fig.update_layout(scene=dict(xaxis_title="الوزن 1", yaxis_title="الوزن 2", zaxis_title="الخسارة"),
                      showlegend=False)
    show(fig, 480, key="m04-landscape")
    st.caption("سطح الخسارة بوزنين اثنين فقط للتوضيح؛ النماذج الحقيقية لها ملايين أو مليارات الأوزان، "
               "أي سطح في فضاء لا يمكن تصوره. الكرة تنزل في اتجاه أشد انحدار.")


@register("m04_fitting")
def fitting() -> None:
    rng = np.random.default_rng(7)
    n = 22
    x = np.sort(rng.uniform(-3, 3, n))
    y_true = 0.6 * x ** 2 - 0.5 * x + 1
    y = y_true + rng.normal(0, 1.1, n)
    grid = np.linspace(-3.2, 3.2, 200)
    fits = [(1, "نقص التوافق", "#5B9BD5"), (2, "توافق مناسب", "#5E8C61"), (15, "إفراط في التوافق", "#C8553D")]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", name="بيانات التدريب",
                             marker=dict(size=10, color="#7D6E68")))
    for deg, label, color in fits:
        coef = np.polyfit(x, y, deg)
        fig.add_trace(go.Scatter(x=grid, y=np.polyval(coef, grid), mode="lines", name=label,
                                 line=dict(color=color, width=3)))
    fig.update_yaxes(range=[min(y) - 3, max(y) + 3])
    fig.update_layout(legend=dict(orientation="h", y=1.12))
    show(fig, 420, key="m04-fitting")
    st.caption("درجة 1 بسيطة جدًا فتفوت البنية (نقص توافق)، ودرجة 15 تمر بكل نقطة فتحفظ الضجيج (إفراط)، "
               "ودرجة 2 تلتقط البنية الحقيقية. البيانات هنا مولَّدة لأغراض التوضيح.")


@register("m04_bias_variance")
def bias_variance() -> None:
    c = np.linspace(1, 12, 60)
    train = 2.6 * np.exp(-0.32 * c) + 0.10
    gap = 0.030 * (c ** 1.85) / 6
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=c, y=train, mode="lines", name="خطأ التدريب",
                             line=dict(color="#5B9BD5", width=3)))
    fig.add_trace(go.Scatter(x=c, y=train + gap, mode="lines", name="خطأ الاختبار",
                             line=dict(color="#C8553D", width=3)))
    best = int(np.argmin(train + gap))
    fig.add_vline(x=c[best], line_dash="dash", line_color="#5E8C61",
                  annotation_text="أفضل تعقيد", annotation_position="top")
    fig.add_annotation(x=2.0, y=2.2, text="نقص التوافق", showarrow=False, font=dict(color="#5B9BD5"))
    fig.add_annotation(x=10.5, y=2.2, text="إفراط في التوافق", showarrow=False, font=dict(color="#C8553D"))
    fig.update_xaxes(title="تعقيد النموذج", showticklabels=False)
    fig.update_yaxes(title="الخطأ", showticklabels=False)
    fig.update_layout(legend=dict(orientation="h", y=1.12))
    show(fig, 400, key="m04-biasvar")
    st.caption("منحنى تخطيطي: خطأ التدريب ينخفض دائمًا مع التعقيد، وخطأ الاختبار ينخفض ثم يرتفع. "
               "والفجوة بينهما هي مؤشر الإفراط في التوافق.")


@register("m04_confusion")
def confusion() -> None:
    z = [[45, 5], [12, 938]]
    labels_x = ["تنبؤ: مصاب", "تنبؤ: سليم"]
    labels_y = ["الواقع: مصاب", "الواقع: سليم"]
    text = [["إيجابي صحيح<br>45", "سلبي كاذب<br>5"], ["إيجابي كاذب<br>12", "سلبي صحيح<br>938"]]
    fig = go.Figure(go.Heatmap(z=z, x=labels_x, y=labels_y, text=text, texttemplate="%{text}",
                               colorscale=[[0, "#FFF4E6"], [1, "#E07A5F"]], showscale=False))
    fig.update_yaxes(autorange="reversed", side="right")
    show(fig, 320, key="m04-confusion")
    st.caption("مثال لمرض يصيب 5% من عينة 1000 شخص. الدقة الإجمالية هنا 98.3%، "
               "لكن الاستدعاء 90% والدقة الإيجابية 79%: ثلاثة أرقام تروي ثلاث قصص مختلفة.")


@register("m04_rl_loop")
def rl_loop() -> None:
    flow([("الوكيل", "Agent"), ("الفعل", "Action"), ("البيئة", "Environment"),
          ("الحالة الجديدة + المكافأة", "State + Reward")],
         loop=True,
         caption="حلقة التعلم المعزز: الوكيل يفعل، والبيئة تردّ بحالة ومكافأة، والسياسة تتحسن بالتكرار.")


@register("m04_data_split")
def data_split() -> None:
    fig = go.Figure()
    parts = [("التدريب", 70, "#E07A5F", "يضبط النموذج معاملاته"),
             ("التحقق", 15, "#F2A541", "نختار المعاملات الفائقة ونقارن النماذج"),
             ("الاختبار", 15, "#5B9BD5", "يُفتح مرة واحدة في النهاية")]
    start = 0
    for name, size, color, role in parts:
        fig.add_trace(go.Bar(x=[size], y=["البيانات"], orientation="h", name=name,
                             marker_color=color, text=f"{name}<br>{size}%", textposition="inside",
                             hovertemplate=f"<b>{name}</b> ({size}%)<br>{role}<extra></extra>"))
        start += size
    fig.update_layout(barmode="stack", showlegend=False, xaxis=dict(showticklabels=False),
                      yaxis=dict(showticklabels=False))
    show(fig, 220, key="m04-split")
    st.caption("النسب توضيحية وتتغير حسب حجم البيانات. القاعدة الثابتة: **مجموعة الاختبار لا تُلمس** "
               "أثناء التطوير، وإلا فقدت معناها.")
