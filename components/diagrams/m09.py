"""Module 9 diagrams: concept map, text-vs-image generation, the diffusion loop,
the latent-diffusion pipeline, GAN vs diffusion, prompt anatomy, the media map,
and the provenance chain."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from components.diagrams import PALETTE, flow, grid_cards, network, register, show


@register("m09_concept_map")
def concept_map() -> None:
    nodes = [
        {"id": "g", "label": "الوسائط المولَّدة", "x": 0, "y": 0, "group": 0},
        {"id": "dif", "label": "نماذج الانتشار", "x": -2.2, "y": 1.1, "group": 1,
         "hover": "تدريب على إزالة الضجيج، ثم توليد بعكس العملية"},
        {"id": "gan", "label": "الشبكات التنافسية", "x": -2.5, "y": -0.3, "group": 1,
         "hover": "مولّد ومميّز يتنافسان — سبقت الانتشار"},
        {"id": "lat", "label": "الفضاء الكامن", "x": -1.3, "y": -1.6, "group": 2,
         "hover": "الانتشار في تمثيل مضغوط لا في البكسل مباشرة"},
        {"id": "clip", "label": "الربط نص–صورة", "x": 1.3, "y": -1.6, "group": 2,
         "hover": "فضاء مشترك يجعل الأمر النصي يوجّه الصورة"},
        {"id": "aud", "label": "الصوت والموسيقى", "x": 2.5, "y": -0.3, "group": 3},
        {"id": "vid", "label": "الفيديو", "x": 2.2, "y": 1.1, "group": 3},
        {"id": "bias", "label": "التحيّز والتمثيل", "x": 0, "y": 2.1, "group": 4,
         "hover": "موثق بحثيًا: التوليد يضخّم الصور النمطية"},
        {"id": "prov", "label": "الأصالة وإثبات المنشأ", "x": 0, "y": -2.7, "group": 5},
    ]
    edges = [("g", "dif"), ("dif", "gan"), ("dif", "lat"), ("g", "clip"), ("clip", "lat"),
             ("g", "aud"), ("aud", "vid"), ("g", "bias"), ("g", "prov"), ("vid", "prov")]
    network(nodes, edges, height=500, key="m09-concept")


@register("m09_text_vs_image")
def text_vs_image() -> None:
    st.caption("الفارق **البنيوي** بين توليد النص وتوليد الصورة — وهو أصل كل ما يليه من فروق في المخاطر وطرق التحقق.")
    grid_cards([
        ("النص: متسلسل ومنفصل", "Sequential, discrete",
         "يُبنى **رمزًا رمزًا** من اليمين إلى اليسار، وكل رمز مشروط بما سبقه. ويمكن إيقافه في أي نقطة فيبقى ما كُتب مفهومًا."),
        ("الصورة: كتلة متصلة", "Holistic, continuous",
         "تُبنى **كاملةً في وقت واحد** عبر خطوات تصفية متتابعة. ولا معنى لـ«نصف صورة»: الخطوة الوسطى ضجيج لا جزء."),
        ("التحقق من النص", "Verifying text",
         "الادعاء **قابل للفصل والفحص**: تستخرج الجملة وتقارنها بمصدر."),
        ("التحقق من الصورة", "Verifying an image",
         "لا توجد «ادعاءات» منفصلة تفحصها. التحقق ينتقل إلى **مصدر الصورة وتاريخها** لا إلى محتواها."),
    ], cols=2)


@register("m09_diffusion_loop")
def diffusion_loop() -> None:
    flow([("صورة أصلية", "Data"), ("أضف ضجيجًا تدريجيًا", "Forward: add noise"),
          ("ضجيج خالص", "Pure noise"), ("درّب شبكة على التنبؤ بالضجيج", "Train denoiser"),
          ("ابدأ من ضجيج جديد", "Sample noise"), ("أزل الضجيج خطوة خطوة", "Reverse: denoise"),
          ("صورة جديدة", "New image")],
         caption="الفكرة كلها: إفساد الصورة عملية معروفة وسهلة؛ والتعلّم يكون على **عكسها**.")
    st.caption("**لماذا هذا ذكي؟** لأن بناء صورة من العدم مسألة مستحيلة التأطير، بينما «أزل قليلًا من الضجيج» "
               "مسألة محددة وقابلة للتدريب — ويكفي تكرارها.")


@register("m09_latent_pipeline")
def latent_pipeline() -> None:
    flow([("الأمر النصي", "Prompt"), ("مُرمِّز نصي", "Text encoder"),
          ("توجيه الانتشار", "Conditioning"), ("انتشار في الفضاء الكامن", "Latent diffusion"),
          ("فك الترميز إلى بكسل", "Decoder"), ("الصورة", "Image")],
         caption="مسار نموذج انتشار كامن: الحساب الثقيل يجري في تمثيل مضغوط، لا على البكسل مباشرة.")
    st.caption("**لماذا كان الانتقال إلى الفضاء الكامن مفصليًا؟** لأن صورة 512×512 فيها ما يفوق 786 ألف قيمة، "
               "بينما تمثيلها الكامن أصغر بعشرات المرات. وهذا ما جعل التوليد ممكنًا على عتاد عادي، "
               "فانتقلت التقنية من المختبرات إلى أيدي الناس.")


@register("m09_gan_vs_diffusion")
def gan_vs_diffusion() -> None:
    grid_cards([
        ("الشبكات التنافسية (GAN)", "2014",
         "**مولّد** ينتج صورًا و**مميّز** يحاول كشفها، ويتحسنان بالتنافس. سريعة في التوليد، لكن تدريبها **غير مستقر** وتميل إلى **انهيار النمط**: تنتج تنويعات قليلة."),
        ("نماذج الانتشار", "2020 →",
         "تدريب **مستقر** على مسألة واحدة واضحة (تنبأ بالضجيج)، وتنوّع أوسع، وجودة أعلى. ثمنها: التوليد يحتاج **عشرات الخطوات** لا خطوة واحدة."),
        ("ما الذي حسم المقارنة؟", "2021",
         "دراسات مقارنة منشورة أظهرت تفوق الانتشار على الشبكات التنافسية في تركيب الصور. ومنذ ذلك الحين صار الانتشار الأساس في أغلب أدوات الصورة."),
    ], cols=3)


@register("m09_noise_schedule")
def noise_schedule() -> None:
    st.caption("كيف تتغير نسبة الإشارة إلى الضجيج عبر خطوات الانتشار. لاحظ أن **أول الخطوات العكسية** "
               "تحدد البنية العامة للصورة، و**آخرها** يحدد التفاصيل الدقيقة.")
    t = np.linspace(0, 1, 200)
    signal = np.cos(t * np.pi / 2) ** 2
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=signal, mode="lines", name="الإشارة (الصورة)",
                             line=dict(color=PALETTE[0], width=3)))
    fig.add_trace(go.Scatter(x=t, y=1 - signal, mode="lines", name="الضجيج",
                             line=dict(color=PALETTE[4], width=3, dash="dash")))
    fig.add_vrect(x0=0.0, x1=0.3, fillcolor=PALETTE[1], opacity=0.12, line_width=0,
                  annotation_text="تفاصيل", annotation_position="top left")
    fig.add_vrect(x0=0.7, x1=1.0, fillcolor=PALETTE[2], opacity=0.12, line_width=0,
                  annotation_text="بنية عامة", annotation_position="top right")
    fig.update_xaxes(title="خطوة الانتشار (0 = صورة، 1 = ضجيج خالص)")
    fig.update_yaxes(title="النسبة", range=[0, 1.05])
    show(fig, 380, key="m09-schedule")


@register("m09_prompt_anatomy")
def prompt_anatomy() -> None:
    grid_cards([
        ("الموضوع", "Subject", "ما الذي في الصورة؟ **أول ما يُحدَّد وأهمه**: «امرأة تقرأ كتابًا»، لا «شيء جميل»."),
        ("السياق والمشهد", "Scene", "أين؟ ومتى؟ وما المحيط؟ «في مكتبة قديمة، عند الغروب»."),
        ("التركيب", "Composition", "زاوية الكاميرا، والمسافة، والإطار: «لقطة متوسطة من مستوى العين»."),
        ("الإضاءة", "Lighting", "أقوى عنصر أثرًا في الانطباع: «إضاءة جانبية دافئة»."),
        ("الأسلوب", "Style", "رسم؟ تصوير؟ أسلوب مدرسة فنية؟ **تجنّب أسماء فنانين أحياء** (المحاضرة 9.6)."),
        ("التفاصيل التقنية", "Technical", "نسبة الأبعاد، والدقة، وعمق الميدان. وتُترك للنهاية."),
        ("الاستبعاد", "Negative", "ما لا تريده. ليست كل الأدوات تدعمه، وحين يُدعم فهو **قوي جدًا**."),
        ("البذرة والمعاملات", "Seed & params", "البذرة تثبّت العشوائية فتصير المقارنة عادلة — وهي **شرط الضبط المنهجي**."),
    ], cols=4)


@register("m09_media_map")
def media_map() -> None:
    grid_cards([
        ("نص ← صورة", "Text-to-image", "الأنضج والأوسع انتشارًا. جودة عالية، ومخاطر تمثيل وأصالة."),
        ("نص ← كلام", "Text-to-speech", "طبيعية عالية. **استنساخ الصوت** يطرح مسألة الهوية والاحتيال."),
        ("كلام ← نص", "Speech-to-text", "الأكثر نفعًا أكاديميًا: تفريغ المقابلات والمحاضرات. **يخطئ في الأسماء والمصطلحات**."),
        ("نص ← موسيقى", "Text-to-music", "توليد مقطوعات من وصف نصي. مسائل الحقوق فيه شائكة."),
        ("نص ← فيديو", "Text-to-video", "الأحدث والأصعب: يضيف بُعد **الاتساق الزمني** بين الإطارات."),
        ("صورة ← نص", "Image captioning", "وصف الصور. أساس البحث البصري وإتاحة المحتوى لذوي الإعاقة البصرية."),
    ], cols=3)


@register("m09_provenance_chain")
def provenance_chain() -> None:
    flow([("إنشاء المحتوى", "Creation"), ("توقيع بيانات المنشأ", "Sign manifest"),
          ("تحرير", "Edit"), ("تحديث السجل", "Append"), ("نشر", "Publish"),
          ("فحص المتلقي", "Verify")],
         caption="سلسلة إثبات المنشأ: سجل موقَّع يرافق الملف ويدوّن ما جرى عليه، بدل محاولة كشف التزييف بعد وقوعه.")
    st.caption("**ما تثبته هذه السلسلة:** أن هذا الملف خرج من هذه الأداة وجرى عليه هذا التحرير. "
               "**وما لا تثبته:** أن الملف الذي **لا يحمل** سجلًا مزيّف — فغياب البيانات ليس دليلًا، "
               "والسجل يُنزع بلقطة شاشة واحدة.")


@register("m09_authenticity_matrix")
def authenticity_matrix() -> None:
    st.caption("أربع حالات يخلط بينها النقاش العام. والخانتان السفليتان هما مصدر أغلب الأخطاء.")
    fig = go.Figure()
    cells = [
        (0.25, 0.75, "مولَّد وموسوم", "الحالة المثالية — ولا تلزم إلا المنتجين الملتزمين", "#5E8C61"),
        (0.75, 0.75, "حقيقي وموثّق", "سلسلة منشأ كاملة — نادرة عمليًا", "#5B9BD5"),
        (0.25, 0.25, "مولَّد بلا وسم", "**الخطر الأول**: تزييف يمر بلا إشارة", "#C8553D"),
        (0.75, 0.25, "حقيقي بلا توثيق", "**الخطر الثاني**: حقيقي يُتّهم بأنه مزيّف", "#F2A541"),
    ]
    for x, y, label, note, color in cells:
        fig.add_shape(type="rect", x0=x - 0.24, x1=x + 0.24, y0=y - 0.24, y1=y + 0.24,
                      fillcolor=color, opacity=0.18, line=dict(color=color, width=2))
        fig.add_annotation(x=x, y=y + 0.07, text=f"<b>{label}</b>", showarrow=False, font=dict(size=14))
        fig.add_annotation(x=x, y=y - 0.09, text=note, showarrow=False, font=dict(size=11, color="#5A4A45"))
    fig.update_xaxes(title="أصالة المحتوى ←", range=[0, 1], showticklabels=False)
    fig.update_yaxes(title="وجود بيانات منشأ ←", range=[0, 1], showticklabels=False)
    show(fig, 400, key="m09-auth")
