"""Module 9 labs (offline): a diffusion denoising simulator, a visual prompt builder with a
completeness check, and an image-authenticity triage exercise. Everything runs on numpy —
no image model and no network call."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from components.diagrams import show
from components.labs import register

# ------------------------------------------------------------------ 9.2 diffusion


def _target_image(kind: str, n: int = 48) -> np.ndarray:
    """A tiny synthetic 'image' so the denoising idea is visible without any model."""
    y, x = np.mgrid[0:n, 0:n] / (n - 1)
    if kind == "دائرة":
        img = np.exp(-(((x - 0.5) ** 2 + (y - 0.5) ** 2) / 0.03))
    elif kind == "تدرّج قطري":
        img = (x + y) / 2
    elif kind == "شريطان":
        img = ((np.abs(x - 0.33) < 0.08) | (np.abs(x - 0.67) < 0.08)).astype(float)
    else:  # مربع
        img = ((np.abs(x - 0.5) < 0.25) & (np.abs(y - 0.5) < 0.25)).astype(float)
    return img


def _heat(z: np.ndarray, title: str) -> go.Figure:
    fig = go.Figure(go.Heatmap(z=z, colorscale="Greys", reversescale=True,
                               showscale=False, zmin=-0.3, zmax=1.3))
    fig.update_layout(title=dict(text=title, x=0.5, font=dict(size=13)))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False, scaleanchor="x")
    return fig


@register("m09_denoise_lab", "مختبر الانتشار: أضف الضجيج ثم أزله", "Diffusion denoising lab", module=9)
def denoise_lab() -> None:
    st.markdown(
        "نماذج الانتشار تقوم على فكرة واحدة: **إفساد الصورة سهل ومعروف، فدرّب الشبكة على عكسه**. "
        "هنا نحاكي الطرفين على «صورة» صغيرة جدًا حتى ترى العملية بعينك."
    )
    c1, c2 = st.columns(2)
    kind = c1.selectbox("الشكل الأصلي", ["دائرة", "مربع", "شريطان", "تدرّج قطري"], key="m09-dn-kind")
    step = c2.slider("خطوة الانتشار t (0 = الأصل، 1 = ضجيج خالص)", 0.0, 1.0, 0.6, 0.05,
                     key="m09-dn-t")
    seed = st.number_input("البذرة (تثبّت العشوائية فتصير المقارنة عادلة)", 0, 9999, 7,
                           key="m09-dn-seed")

    rng = np.random.default_rng(int(seed))
    img = _target_image(kind)
    noise = rng.normal(0, 1, img.shape)
    # Variance-preserving forward process: x_t = sqrt(a) x_0 + sqrt(1-a) eps
    a = float(np.cos(step * np.pi / 2) ** 2)
    noisy = np.sqrt(a) * img + np.sqrt(1 - a) * noise

    st.markdown("#### المسار الأمامي: إضافة الضجيج")
    d1, d2 = st.columns(2)
    with d1:
        show(_heat(img, "الصورة الأصلية x₀"), 300, key="m09-dn-orig")
    with d2:
        show(_heat(noisy, f"بعد إضافة الضجيج (t = {step:.2f})"), 300, key="m09-dn-noisy")
    st.caption(f"نسبة الإشارة المتبقية: **{a:.0%}** — والباقي ضجيج. "
               "لاحظ أن هذه العملية **معروفة تمامًا** ولا تحتاج تعلّمًا: نحن من أضاف الضجيج.")

    st.markdown("#### المسار العكسي: إزالة الضجيج خطوة خطوة")
    n_steps = st.slider("عدد خطوات الإزالة", 1, 24, 8, key="m09-dn-steps")
    # Teaching simulation. A trained denoiser predicts the noise from the noisy image alone;
    # here we let the simulated denoiser remove a fraction of the *known* noise each step, with
    # a small residual error, so what stays visible is the thing that matters pedagogically:
    # the image emerges gradually, and more steps means a cleaner result.
    frames = [noisy.copy()]
    for i in range(n_steps):
        p = (i + 1) / n_steps
        residual = rng.normal(0, 0.12 * (1 - p) + 0.015, img.shape)
        frames.append((1 - p) * noisy + p * img + residual)

    cols = st.columns(4)
    picks = [0, max(1, n_steps // 3), max(2, 2 * n_steps // 3), n_steps]
    for col, k in zip(cols, picks):
        with col:
            show(_heat(frames[min(k, len(frames) - 1)], f"خطوة {k}"), 230, key=f"m09-dn-f{k}")

    with st.expander("ماذا يحاكي هذا بالضبط — وما الذي يبسّطه؟"):
        st.markdown(
            "**ما يحاكيه بأمانة:** (أ) أن المسار الأمامي **معروف ومحدد** ولا يحتاج تعلّمًا؛ "
            "(ب) أن الشبكة تُدرَّب على مسألة واحدة واضحة هي **التنبؤ بالضجيج المضاف**؛ "
            "(ج) أن التوليد يجري **تدريجيًا** عبر خطوات، وأن زيادة الخطوات تحسّن النتيجة إلى حد.\n\n"
            "**ما يبسّطه:** هنا نعرف الصورة الأصلية، أما النموذج الحقيقي فلا يعرفها — إنما تعلّم من "
            "ملايين الأمثلة كيف يبدو الضجيج فيتنبأ به. كما أن النموذج الحقيقي يعمل في **فضاء كامن** "
            "مضغوط لا على البكسل، ويكون **موجَّهًا بالنص**، وهما عنصران لا تمثّلهما هذه المحاكاة."
        )


# ------------------------------------------------------------------ 9.3 prompt builder

_ELEMENTS = [
    ("subject", "الموضوع", "ما الذي في الصورة؟", "امرأة مسنّة تقرأ كتابًا",
     "**العنصر الوحيد الذي لا يُستغنى عنه.** بدونه يملأ النموذج الفراغ بما شاء."),
    ("scene", "السياق والمشهد", "أين؟ ومتى؟", "في مكتبة قديمة، عند الغروب",
     "يحدد الجو العام، ويقلّل التنويعات غير المرغوبة بدرجة كبيرة."),
    ("composition", "التركيب", "زاوية الكاميرا والإطار", "لقطة متوسطة من مستوى العين",
     "أكثر عنصر يهمله المبتدئون، وأسرع ما يحسّن النتيجة."),
    ("lighting", "الإضاءة", "نوع الضوء واتجاهه", "ضوء جانبي دافئ من نافذة",
     "أقوى عنصر أثرًا في الانطباع العاطفي للصورة."),
    ("style", "الأسلوب", "تصوير؟ رسم؟ مدرسة فنية؟", "تصوير فوتوغرافي واقعي",
     "**تجنّب أسماء فنانين أحياء**؛ استعمل وصف الأسلوب لا اسم صاحبه (المحاضرة 9.6)."),
    ("technical", "تفاصيل تقنية", "الأبعاد والدقة وعمق الميدان", "نسبة 3:2، عمق ميدان ضحل",
     "تُترك للنهاية، وأثرها أقل مما يُظن."),
    ("negative", "الاستبعاد", "ما لا تريده", "بلا نص مكتوب، بلا أطراف مشوّهة",
     "قوي حين تدعمه الأداة. لا تُطل القائمة: خمسة عناصر تكفي."),
]


@register("m09_prompt_builder", "بانِ الأمر البصري", "Visual prompt builder", module=9)
def prompt_builder() -> None:
    st.markdown(
        "الأمر البصري ليس جملة، بل **قائمة عناصر**. املأ ما تحتاجه واترك الباقي فارغًا، "
        "ثم انظر إلى تقييم الاكتمال أسفل الصفحة."
    )
    vals: dict[str, str] = {}
    for key, label, hint, example, _ in _ELEMENTS:
        vals[key] = st.text_input(f"{label} — {hint}", key=f"m09-pb-{key}",
                                  placeholder=f"مثال: {example}")

    filled = [k for k in vals if vals[k].strip()]
    order = ["subject", "scene", "composition", "lighting", "style", "technical"]
    parts = [vals[k].strip() for k in order if vals[k].strip()]
    prompt = "، ".join(parts)
    if vals["negative"].strip():
        prompt += f"\n\n**استبعاد:** {vals['negative'].strip()}"

    st.markdown("#### الأمر المجمَّع")
    st.code(prompt or "(لم تملأ أي عنصر بعد)", language=None)

    st.markdown("#### تقييم الاكتمال")
    if "subject" not in filled:
        st.error("**لا موضوع.** هذا ليس أمرًا ناقصًا بل أمر بلا معنى: النموذج سيملأ الفراغ بأي شيء.")
    score = len([k for k in ("subject", "scene", "composition", "lighting", "style") if k in filled])
    st.progress(score / 5, text=f"العناصر الأساسية المكتملة: {score} من 5")
    for key, label, _h, _e, note in _ELEMENTS:
        if key not in filled and key != "technical":
            st.caption(f"**{label} — ناقص.** {note}")

    st.divider()
    st.markdown(
        "#### منهج الضبط: **غيّر عنصرًا واحدًا في كل مرة**\n"
        "وهذا هو الفرق بين تجريب عشوائي وعمل منهجي:\n"
        "1. ثبّت **البذرة (seed)** — وإلا قارنتَ صورتين اختلفتا لسبب لا تعرفه.\n"
        "2. غيّر **عنصرًا واحدًا** فقط (الإضاءة مثلًا) واحتفظ بالباقي حرفيًا.\n"
        "3. سجّل في جدول: الأمر، والبذرة، والعنصر المتغيّر، والنتيجة، والحكم.\n"
        "4. أبقِ التغيير إن تحسّنت النتيجة، وارجع عنه إن لم تتحسن. ثم انتقل إلى العنصر التالي.\n\n"
        "**لماذا؟** لو غيّرت ثلاثة عناصر دفعةً واحدة وتحسّنت الصورة، فأنت **لا تعرف أيها السبب** — "
        "ولن تستطيع تكرار النجاح. وهذا هو مبدأ التغيير المفرد نفسه الذي تعرفه من التصميم التجريبي."
    )


# ------------------------------------------------------------------ 9.6 authenticity triage

_CASES = [
    {
        "title": "صورة متداولة لحدث سياسي",
        "text": "صورة تنتشر على وسائل التواصل يُقال إنها لمظاهرة وقعت أمس في مدينة معروفة. "
                "الصورة عالية الجودة، والوجوه واضحة، والتفاصيل متقنة.",
        "best": ["ابحث عن أقدم ظهور للصورة على الشبكة (بحث عكسي)",
                 "افحص بيانات المنشأ المرفقة بالملف إن وُجدت",
                 "ابحث عن تغطية من مصادر إخبارية مستقلة للحدث نفسه"],
        "worst": ["افحص جودة الصورة ودقتها بعينك",
                  "مرّرها على أداة كشف صور مولَّدة واعتمد نتيجتها"],
        "lesson": "**جودة الصورة ليست إشارة إلى أي شيء.** الأدوات الحديثة تنتج صورًا عالية الدقة، "
                  "والصور الحقيقية قد تكون رديئة. والتحقق ينتقل من **محتوى الصورة** إلى "
                  "**تاريخها ومصدرها**: متى ظهرت أول مرة؟ ومن نشرها؟ وهل يوثّق الحدث أحد آخر؟ "
                  "وهذا هو بالضبط منهج **القراءة الجانبية** من المحاضرة 8.5، منقولًا إلى الصورة.",
    },
    {
        "title": "تسجيل صوتي منسوب إلى مسؤول",
        "text": "تسجيل صوتي قصير ينتشر، والصوت يشبه صوت شخصية عامة معروفة، ويتضمن تصريحًا مثيرًا.",
        "best": ["ابحث عن تصريح رسمي من الجهة المعنية نفيًا أو تأكيدًا",
                 "ابحث عن المصدر الأصلي للتسجيل وسياقه الكامل",
                 "افحص هل يوجد تسجيل فيديو أو محضر للمناسبة نفسها"],
        "worst": ["اعتمد على أن الصوت يشبه صوت الشخص",
                  "انشره مع عبارة «للتحقق» حتى يردّ أحد"],
        "lesson": "**التشابه الصوتي لم يعد دليلًا**: استنساخ الصوت صار متاحًا بثوانٍ قليلة من عينة. "
                  "والأخطر أن التسجيل الصوتي **يفتقر إلى السياق البصري** الذي يكشف التناقضات عادةً. "
                  "وأما نشره «للتحقق» فهو **مشاركة في الانتشار**: الانطباع الأول يبقى حتى بعد التكذيب.",
    },
    {
        "title": "صورة حقيقية يُتّهم صاحبها بالتزييف",
        "text": "صحفي ينشر صورة التقطها بنفسه، فيتهمه بعضهم بأنها مولَّدة لأن أداة كشف أعطت نسبة عالية.",
        "best": ["اطلب الملف الأصلي ببياناته الوصفية الكاملة",
                 "اطلب صورًا أخرى من التسلسل نفسه ومن الموقع نفسه",
                 "تحقق من وجود شهود أو مصادر أخرى وثّقت الحدث"],
        "worst": ["اعتمد نتيجة أداة الكشف بوصفها حاسمة",
                  "افترض التزييف لأن الصورة تبدو «مثالية أكثر من اللازم»"],
        "lesson": "**هذا هو الوجه الثاني للمشكلة، وكثيرًا ما يُنسى.** فانتشار التوليد لا يهدد الثقة "
                  "في المزيّف فحسب، بل يمنح **ذريعة جاهزة لإنكار الحقيقي** — وهو ما يسمّى «عائد الكاذب». "
                  "وأدوات الكشف غير موثوقة في الاتجاهين معًا (المحاضرة 8.6)، فلا يُبنى عليها اتهام ولا تبرئة.",
    },
]


@register("m09_authenticity_triage", "فرز الأصالة: ماذا تفعل أولًا؟", "Authenticity triage", module=9)
def authenticity_triage() -> None:
    st.markdown(
        "ثلاث حالات واقعية. اختر في كل واحدة **الإجراءات التي تبدأ بها**، ثم اكشف التحليل. "
        "المطلوب ليس الحكم على الصورة بالنظر، بل **بناء مسار تحقق**."
    )
    for i, case in enumerate(_CASES):
        with st.container(border=True, key=f"m09-auth-case-{i}"):
            st.markdown(f"**الحالة {i + 1}: {case['title']}**")
            st.caption(case["text"])
            options = case["best"] + case["worst"]
            picks = st.multiselect("ما الإجراءات التي تبدأ بها؟", options,
                                   key=f"m09-auth-pick-{i}")
            if st.toggle("اكشف التحليل", key=f"m09-auth-rev-{i}"):
                good = [p for p in picks if p in case["best"]]
                bad = [p for p in picks if p in case["worst"]]
                st.success(f"إجراءات سليمة اخترتها: **{len(good)} من {len(case['best'])}**")
                for b in case["best"]:
                    mark = "✓" if b in good else "—"
                    st.markdown(f"{mark} {b}")
                for b in bad:
                    st.warning(f"**إجراء غير موثوق:** {b}")
                st.info(case["lesson"])

    st.divider()
    st.markdown(
        "**القاعدة الجامعة للحالات الثلاث:** لا تُقيّم الوسيط بالنظر إليه. "
        "فكل ما تراه داخل الصورة أو تسمعه في التسجيل **هو بالضبط ما يستطيع المولّد صنعه**. "
        "والتحقق يخرج إلى **المصدر والتاريخ والشهادة المستقلة** — والوسيط يتغير، والمنهج واحد."
    )
