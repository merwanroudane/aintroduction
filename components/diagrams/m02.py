"""Module 2 diagrams: concept map, interactive AI history timeline, winters schematic,
paradigm shifts, the five-question frame, and the three factors of the deep learning revolution."""

import plotly.graph_objects as go
import streamlit as st

from components.diagrams import PALETTE, flow, grid_cards, network, register, show

# (year, label, approach, description). Every date is verified — see content/module_02/references.yml.
MILESTONES = [
    (1943, "نموذج McCulloch و Pitts العصبي", "اتصالية", "أول نموذج رياضي لخلية عصبية اصطناعية: عتبة على مجموع موزون."),
    (1950, "مقال تورينغ ولعبة المحاكاة", "رمزية", "«Computing Machinery and Intelligence»: استبدال سؤال «هل تفكر الآلة؟» بمعيار سلوكي."),
    (1955, "مقترح ورشة Dartmouth", "رمزية", "صياغة مصطلح «Artificial Intelligence» في مقترح McCarthy و Minsky و Rochester و Shannon (الورشة صيف 1956)."),
    (1958, "البيرسبترون (Rosenblatt)", "اتصالية", "نموذج احتمالي للتعلم من الأمثلة بتعديل الأوزان."),
    (1959, "برنامج الداما (Samuel)", "رمزية", "برنامج يتحسن بالخبرة؛ من أوائل تجارب التعلم الآلي."),
    (1966, "ELIZA", "رمزية", "برنامج محادثة بقواعد بسيطة كشف ميل المستخدمين إلى نسبة الفهم إلى الآلة."),
    (1969, "Minsky و Papert: Perceptrons", "اتصالية", "بيان حدود البيرسبترون أحادي الطبقة؛ أسهم في تراجع الاهتمام بالشبكات."),
    (1972, "DENDRAL و بدايات الأنظمة الخبيرة", "رمزية", "تمثيل معرفة الخبراء في قواعد لتوليد فرضيات كيميائية."),
    (1973, "تقرير Lighthill", "رمزية", "تقييم نقدي بريطاني أدى إلى خفض التمويل: بداية الشتاء الأول."),
    (1980, "حجة الغرفة الصينية (Searle)", "رمزية", "نقد فلسفي: معالجة الرموز لا تعني الفهم."),
    (1986, "الانتشار العكسي (Rumelhart, Hinton, Williams)", "اتصالية", "طريقة عملية لتدريب الشبكات متعددة الطبقات: إحياء المقاربة الاتصالية."),
    (1987, "انهيار سوق آلات LISP", "رمزية", "بداية الشتاء الثاني مع تراجع الأنظمة الخبيرة."),
    (1995, "آلات الأشعة الداعمة (SVM)", "إحصائية", "طرق إحصائية متينة بأسس نظرية قوية سيطرت على التسعينيات."),
    (1997, "Deep Blue يهزم Kasparov", "رمزية", "قوة البحث والعتاد المتخصص في مجال ضيق محدد القواعد."),
    (1998, "LeNet-5 للتعرف على الأرقام", "اتصالية", "شبكة التفافية عملية لقراءة الشيكات: نجاح مبكر للتعلم العميق."),
    (2009, "قاعدة ImageNet", "إحصائية", "ملايين الصور الموسومة: البنية التحتية التي جعلت التعلم العميق قابلًا للتقييم."),
    (2012, "AlexNet", "عميقة", "قفزة في دقة تصنيف الصور بالشبكات العميقة على وحدات المعالجة الرسومية."),
    (2014, "آلية الانتباه (Bahdanau et al.)", "عميقة", "حل مشكلة الاختناق في الترجمة الآلية العصبية بالانتباه على المدخل."),
    (2015, "DQN يتعلم ألعاب أتاري", "عميقة", "التعلم المعزز العميق من البكسلات مباشرة."),
    (2017, "المحوّل Transformer", "عميقة", "«Attention Is All You Need»: البنية التي قامت عليها النماذج اللغوية الكبيرة."),
    (2018, "AlphaZero", "عميقة", "إتقان الشطرنج و Go و Shogi بالتعلم الذاتي دون بيانات بشرية."),
    (2021, "مصطلح «النماذج التأسيسية»", "توليدية", "تقرير Stanford CRFM يسمي النماذج الكبيرة القابلة للتكييف على مهام كثيرة."),
]
APPROACH_COLORS = {"رمزية": "#E07A5F", "اتصالية": "#8E7DBE", "إحصائية": "#F2A541",
                   "عميقة": "#5B9BD5", "توليدية": "#B56576"}


@register("m02_concept_map")
def concept_map() -> None:
    nodes = [
        {"id": "h", "label": "تاريخ الذكاء الاصطناعي", "x": 0, "y": 0, "group": 0},
        {"id": "f", "label": "التأسيس 1943–1956", "x": -2.1, "y": 1.0, "group": 1, "hover": "المنطق، الحوسبة، تورينغ، Dartmouth"},
        {"id": "s", "label": "العصر الرمزي", "x": -2.4, "y": -0.4, "group": 1, "hover": "البحث، المنطق، القواعد"},
        {"id": "w1", "label": "الشتاء الأول 1974", "x": -1.2, "y": -1.6, "group": 2, "hover": "تقرير Lighthill وخفض التمويل"},
        {"id": "e", "label": "الأنظمة الخبيرة", "x": 0.2, "y": 1.7, "group": 3, "hover": "DENDRAL، MYCIN، XCON"},
        {"id": "w2", "label": "الشتاء الثاني 1987", "x": 1.2, "y": -1.6, "group": 2, "hover": "انهيار سوق آلات LISP"},
        {"id": "st", "label": "التحول الإحصائي", "x": 2.4, "y": -0.4, "group": 4, "hover": "SVM، النماذج الاحتمالية، البيانات"},
        {"id": "d", "label": "التعلم العميق", "x": 2.1, "y": 1.0, "group": 5, "hover": "ImageNet، AlexNet، GPU"},
        {"id": "t", "label": "المحوّل والنماذج التأسيسية", "x": 0, "y": 2.4, "group": 5, "hover": "Attention 2017 ← LLMs"},
    ]
    edges = [("f", "s"), ("s", "w1"), ("w1", "e"), ("e", "w2"), ("w2", "st"), ("st", "d"), ("d", "t"),
             ("h", "f"), ("h", "st"), ("h", "t")]
    network(nodes, edges, height=500, key="m02-concept")


@register("m02_timeline")
def timeline() -> None:
    st.caption("خط زمني تفاعلي: صفِّ المحطات حسب المقاربة، ومرّر المؤشر على كل نقطة لقراءة تفاصيلها.")
    chosen = st.pills("المقاربة", list(APPROACH_COLORS), selection_mode="multi",
                      default=list(APPROACH_COLORS), key="m02-tl-approach")
    chosen = chosen or list(APPROACH_COLORS)
    fig = go.Figure()
    for approach in chosen:
        pts = [m for m in MILESTONES if m[2] == approach]
        if not pts:
            continue
        fig.add_trace(go.Scatter(
            x=[p[0] for p in pts],
            y=[list(APPROACH_COLORS).index(approach)] * len(pts),
            mode="markers+text",
            text=[f"{p[0]}" for p in pts],
            textposition="top center", textfont=dict(size=10),
            hovertext=[f"<b>{p[1]}</b><br>{p[0]} · مقاربة {p[2]}<br>{p[3]}" for p in pts],
            hoverinfo="text", name=approach,
            marker=dict(size=17, color=APPROACH_COLORS[approach], line=dict(color="#FFFFFF", width=2)),
        ))
    for y0, y1, label, color in [(1974, 1980, "الشتاء الأول", "#F4D3C4"), (1987, 1993, "الشتاء الثاني", "#F4D3C4")]:
        fig.add_vrect(x0=y0, x1=y1, fillcolor=color, opacity=0.45, line_width=0,
                      annotation_text=label, annotation_position="bottom left")
    fig.update_xaxes(title="السنة", range=[1938, 2026], dtick=10)
    fig.update_yaxes(tickvals=list(range(len(APPROACH_COLORS))), ticktext=list(APPROACH_COLORS),
                     side="right", range=[-0.8, len(APPROACH_COLORS) - 0.2])
    fig.update_layout(legend=dict(orientation="h", y=1.12))
    show(fig, 470, key="m02-timeline")


@register("m02_winters")
def winters() -> None:
    years = list(range(1950, 2026))
    # Schematic curve of attention/funding — illustrative, not measured data.
    def level(y):
        if y < 1956: return 0.15 + 0.02 * (y - 1950)
        if y < 1974: return 0.30 + 0.030 * (y - 1956)
        if y < 1980: return 0.84 - 0.095 * (y - 1974)
        if y < 1987: return 0.27 + 0.055 * (y - 1980)
        if y < 1993: return 0.66 - 0.075 * (y - 1987)
        if y < 2012: return 0.21 + 0.016 * (y - 1993)
        return min(0.52 + 0.036 * (y - 2012), 1.0)
    fig = go.Figure(go.Scatter(x=years, y=[level(y) for y in years], mode="lines",
                               line=dict(color="#C8553D", width=3, shape="spline"),
                               hovertemplate="%{x}<extra></extra>"))
    for x0, x1 in [(1974, 1980), (1987, 1993)]:
        fig.add_vrect(x0=x0, x1=x1, fillcolor="#D9E7F2", opacity=0.6, line_width=0)
    for x, label in [(1956, "Dartmouth"), (1977, "الشتاء الأول"), (1990, "الشتاء الثاني"),
                     (2012, "AlexNet"), (2017, "Transformer")]:
        fig.add_annotation(x=x, y=level(x), text=label, showarrow=True, arrowhead=2,
                           ay=-38, font=dict(size=12))
    fig.update_xaxes(title="السنة")
    fig.update_yaxes(title="مستوى الاهتمام والتمويل (تخطيطي)", showticklabels=False, range=[0, 1.15])
    show(fig, 380, key="m02-winters")
    st.caption("منحنى **تخطيطي توضيحي** لدورات التفاؤل والتراجع، وليس قياسًا كميًا لتمويل فعلي. "
               "الهدف منه إبراز النمط الدوري لا الأرقام.")


@register("m02_five_questions")
def five_questions() -> None:
    flow([("ما المشكلة السائدة؟", "Problem"), ("ما المنهج؟", "Method"), ("لماذا نجح؟", "Success"),
          ("ما حدوده؟", "Limits"), ("لماذا الانتقال؟", "Transition")],
         caption="الإطار الخماسي الذي نحلل به كل مرحلة من مراحل الحقل.")


@register("m02_paradigms")
def paradigms() -> None:
    grid_cards([
        ("المقاربة الرمزية", "Symbolic AI", "المعرفة رموز وقواعد صريحة؛ الذكاء استدلال منطقي وبحث في فضاء الحالات."),
        ("المقاربة الاتصالية", "Connectionism", "المعرفة موزعة في أوزان شبكة؛ الذكاء يُتعلَّم من الأمثلة."),
        ("المقاربة الإحصائية", "Statistical ML", "النمذجة الاحتمالية والتعميم من عينة، بأسس نظرية في التعلم."),
        ("التعلم العميق", "Deep Learning", "شبكات متعددة الطبقات تتعلم التمثيلات بنفسها من بيانات ضخمة."),
        ("النماذج التأسيسية والتوليدية", "Foundation & Generative", "نماذج ضخمة عامة الغرض تُكيَّف لمهام كثيرة وتولّد محتوى."),
    ], cols=3)


@register("m02_three_factors")
def three_factors() -> None:
    grid_cards([
        ("البيانات", "Data", "ImageNet (2009) وملايين الصور الموسومة، ثم نصوص الويب الضخمة: مادة التعلم."),
        ("العتاد", "Compute / GPU", "وحدات المعالجة الرسومية جعلت تدريب الشبكات العميقة ممكنًا عمليًا."),
        ("الخوارزميات", "Algorithms", "الانتشار العكسي، ودوال تنشيط أفضل، وتقنيات تنظيم وتدريب أكثر استقرارًا."),
    ], cols=3)
    st.caption("لم يكن أي عامل من الثلاثة كافيًا وحده: اجتماعها هو ما فسّر الانفجار بعد 2012.")


@register("m02_expert_system")
def expert_system() -> None:
    flow([("الوقائع من المستخدم", "Facts"), ("محرك الاستدلال", "Inference engine"),
          ("قاعدة المعرفة: قواعد إذا… فإن…", "Knowledge base"),
          ("الاستنتاج", "Conclusion"), ("واجهة الشرح: لماذا؟", "Explanation")],
         caption="بنية النظام الخبير: المعرفة مفصولة عن آلية الاستدلال، وكل استنتاج قابل للتتبع.")


@register("m02_data_vs_rules")
def data_vs_rules() -> None:
    grid_cards([
        ("النظام الخبير", "Expert system", "يسأل: ما القواعد التي يستعملها الخبير؟ — يحتاج إلى خبير ووقت طويل لاستخراج المعرفة."),
        ("التعلم الإحصائي", "Statistical learning", "يسأل: ما الدالة التي تربط المدخلات بالمخرجات؟ — يحتاج إلى بيانات ممثلة وكافية."),
        ("التعلم العميق", "Deep learning", "يسأل: هل يمكن تعلّم السمات نفسها آليًا؟ — يحتاج إلى بيانات ضخمة وعتاد قوي."),
    ], cols=3)


@register("m02_attention_vs_rnn")
def attention_vs_rnn() -> None:
    st.html(
        '<div class="tiles" style="--cols:2">'
        '<div class="tile" style="background:#FFF1E4;border-top:5px solid #E07A5F">'
        '<b>الشبكة التكرارية</b><small>RNN · sequential</small>'
        '<p>تعالج الرموز واحدًا بعد آخر، وتضغط ما سبق في حالة واحدة. '
        'التبعيات البعيدة تضعف، والتدريب لا يستفيد من التوازي.</p></div>'
        '<div class="tile" style="background:#EAF5FE;border-top:5px solid #5B9BD5">'
        '<b>المحوّل</b><small>Transformer · parallel self-attention</small>'
        '<p>يعالج كل الرموز معًا، ويحسب علاقة كل رمز بكل رمز مباشرة. '
        'التدريب متوازٍ، ومن ثم قابل للتوسع إلى نماذج ضخمة.</p></div></div>'
    )
    flow([("المدخل: كل الرموز", "All tokens"), ("الانتباه الذاتي", "Self-attention"),
          ("طبقات تغذية أمامية", "Feed-forward"), ("تمثيل يراعي السياق", "Contextual representation")],
         caption="مسار مبسط داخل طبقة المحوّل؛ التفصيل الرياضي في المحور 7.")
