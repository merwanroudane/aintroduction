"""Module 7 labs (offline, numpy + plotly): an approximate tokenizer, a temperature/top-p
simulator, an attention toy, a RAG concept lab with real TF-IDF retrieval, and an agent
workflow walkthrough. Every lab states clearly where it simplifies reality."""

import math
import re

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from components.diagrams import PALETTE, show
from components.labs import register

# ------------------------------------------------------------------ 7.1 tokenizer

AR_PREFIXES = ["وال", "بال", "كال", "فال", "ال", "و", "ف", "ب", "ك", "ل", "س"]
AR_SUFFIXES = ["ونها", "اتها", "ونه", "اتهم", "ية", "ات", "ون", "ين", "ها", "هم", "كم", "نا", "ان", "ه", "ي"]


def toy_tokenize(text: str) -> list[tuple[str, str]]:
    """A deliberately simple, teaching-only splitter. Not a real tokenizer."""
    out: list[tuple[str, str]] = []
    for raw in re.findall(r"\S+|\s+", text):
        if raw.isspace():
            continue
        word = raw
        punct = ""
        while word and word[-1] in ".,!?؟،؛:()»«\"'":
            punct = word[-1] + punct
            word = word[:-1]
        if not word:
            out.append((punct, "علامة"))
            continue
        if re.fullmatch(r"[\d٠-٩.,]+", word):
            out.extend((c, "رقم") for c in word)
            if punct:
                out.append((punct, "علامة"))
            continue
        if re.search(r"[A-Za-z]", word):
            parts = re.findall(r"[A-Z][a-z]+|[a-z]+|[A-Z]+|\d+", word) or [word]
            out.extend((p, "لاتيني") for p in parts)
            if punct:
                out.append((punct, "علامة"))
            continue
        pre = ""
        for p in AR_PREFIXES:
            if word.startswith(p) and len(word) > len(p) + 2:
                pre, word = p, word[len(p):]
                break
        suf = ""
        for s in AR_SUFFIXES:
            if word.endswith(s) and len(word) > len(s) + 2:
                suf, word = s, word[: -len(s)]
                break
        if pre:
            out.append((pre, "سابقة"))
        out.append((word, "جذع"))
        if suf:
            out.append((suf, "لاحقة"))
        if punct:
            out.append((punct, "علامة"))
    return out


@register("m07_tokenizer", "مختبر التقطيع (تقريبي تعليمي)", "Tokenization lab", module=7)
def tokenizer_lab() -> None:
    st.warning("**تنبيه مهم:** هذا المقطّع **تعليمي تقريبي** كُتب لتوضيح الفكرة فقط، وليس المقطّع الحقيقي "
               "لأي نموذج. المقطّعات الحقيقية تُتعلَّم من البيانات (مثل BPE) وتختلف بين النماذج. "
               "الهدف هنا أن ترى **أن النص يُقسَّم إلى وحدات أصغر من الكلمة**، لا أن تعرف التقسيم الفعلي.",
               icon=":material/science:")
    text = st.text_area("اكتب نصًا", "البنك المركزي رفع سعر الفائدة بنسبة 2.5 بالمئة في 2026.",
                        key="m07_tokenizer-text", height=90)
    if not text.strip():
        return
    toks = toy_tokenize(text)
    colors = {"سابقة": "#F2A541", "جذع": "#5B9BD5", "لاحقة": "#B56576",
              "رقم": "#5E8C61", "لاتيني": "#8E7DBE", "علامة": "#7D6E68"}
    html = "".join(
        f'<span style="display:inline-block;margin:2px;padding:3px 8px;border-radius:8px;'
        f'background:{colors[k]}22;border:1.5px solid {colors[k]};font-size:0.95rem">'
        f'{t}<sub style="color:{colors[k]};font-size:0.7rem"> {k}</sub></span>'
        for t, k in toks)
    st.html(f'<div style="line-height:2.4;direction:rtl">{html}</div>')

    words = len([w for w in text.split() if w.strip()])
    c1, c2, c3 = st.columns(3)
    c1.metric("عدد الكلمات", words)
    c2.metric("عدد الرموز (تقريبي)", len(toks))
    c3.metric("رموز لكل كلمة", f"{len(toks) / max(words, 1):.2f}")
    st.markdown("**لماذا يهمّك هذا؟**")
    st.markdown(
        "- **نافذة السياق تُقاس بالرموز لا بالكلمات**، وحدود الطول والتكلفة تُحسب بها.\n"
        "- **الأرقام تُقسَّم** غالبًا إلى أجزاء، وهذا أحد أسباب ضعف بعض النماذج في الحساب الدقيق.\n"
        "- **اللغات والكتابات تختلف**: عدد الرموز للنص نفسه قد يختلف بين لغة وأخرى، وهذا يؤثر في الكلفة "
        "وفي الطول المتاح. والمقارنة الدقيقة بين لغات تحتاج إلى قياس بمقطّع حقيقي موثق، ولا نقدّم هنا رقمًا مؤكدًا.")


# ------------------------------------------------------------------ 7.1 temperature

PROMPT_CONTINUATIONS = {
    "«الاقتصاد الجزائري يعتمد بشكل كبير على …»": [
        ("المحروقات", 4.2), ("النفط", 3.6), ("الصادرات", 2.4), ("قطاع", 2.1),
        ("الغاز", 1.9), ("الموارد", 1.5), ("الزراعة", 0.7), ("السياحة", 0.2),
    ],
    "«أفضل طريقة لتعلّم البرمجة هي …»": [
        ("الممارسة", 3.9), ("التطبيق", 3.2), ("كتابة", 2.6), ("حل", 2.2),
        ("البدء", 1.8), ("قراءة", 1.2), ("مشاهدة", 0.6), ("الصبر", 0.3),
    ],
    "«في يوم من الأيام، خرج الثعلب من …»": [
        ("جحره", 3.4), ("الغابة", 3.1), ("مخبئه", 2.5), ("بيته", 2.0),
        ("الكهف", 1.6), ("الوادي", 1.1), ("القرية", 0.5), ("السحاب", 0.05),
    ],
}


@register("m07_temperature", "محاكاة درجة الحرارة وأخذ العينات", "Temperature simulation", module=7)
def temperature_lab() -> None:
    st.warning("**تنبيه:** الدرجات (logits) أدناه **موضوعة يدويًا** لأغراض التدريس. "
               "الرياضيات المطبقة عليها (Softmax مع الحرارة، وtop-p) **حقيقية تمامًا**، "
               "لكن الأرقام الأولية ليست مخرج نموذج فعلي.", icon=":material/science:")
    prompt = st.selectbox("السياق", list(PROMPT_CONTINUATIONS), key="m07_temperature-prompt")
    c1, c2 = st.columns(2)
    temp = c1.slider("درجة الحرارة (Temperature)", 0.1, 2.0, 1.0, 0.1, key="m07_temperature-t")
    top_p = c2.slider("top-p (أخذ النواة)", 0.1, 1.0, 1.0, 0.05, key="m07_temperature-p")

    items = PROMPT_CONTINUATIONS[prompt]
    words = [w for w, _ in items]
    logits = np.array([s for _, s in items], dtype=float)

    scaled = logits / temp
    exp = np.exp(scaled - scaled.max())
    probs = exp / exp.sum()

    order = np.argsort(-probs)
    cum = np.cumsum(probs[order])
    keep = order[: max(1, int(np.searchsorted(cum, top_p) + 1))]
    mask = np.zeros_like(probs, dtype=bool)
    mask[keep] = True
    final = np.where(mask, probs, 0.0)
    final = final / final.sum()

    fig = go.Figure()
    fig.add_trace(go.Bar(x=words, y=probs, name="بعد الحرارة", marker_color="#E9B99A"))
    fig.add_trace(go.Bar(x=words, y=final, name="بعد top-p", marker_color="#C8553D"))
    fig.update_yaxes(title="الاحتمال", range=[0, max(0.05, float(final.max()) * 1.15)])
    fig.update_layout(barmode="overlay", legend=dict(orientation="h", y=1.15))
    show(fig, 380, key="m07-temp")

    entropy = float(-(probs * np.log(probs + 1e-12)).sum())
    c1, c2, c3 = st.columns(3)
    c1.metric("أعلى احتمال", f"{probs.max():.1%}")
    c2.metric("عدد الكلمات المتاحة بعد top-p", int(mask.sum()))
    c3.metric("العشوائية (الإنتروبيا)", f"{entropy:.2f}")

    rng = np.random.default_rng(int(temp * 100) + int(top_p * 100))
    samples = rng.choice(words, size=8, p=final)
    st.markdown("**ثماني عينات بهذه الإعدادات:** " + "، ".join(f"`{s}`" for s in samples))

    if temp <= 0.3:
        st.info("**حرارة منخفضة:** التوزيع حاد، والمخرج شبه حتمي ومتكرر. مناسب للاستخراج والتصنيف "
                "والمهام التي نريد فيها ثباتًا.")
    elif temp >= 1.5:
        st.warning("**حرارة مرتفعة:** التوزيع مسطّح، وترتفع احتمالات كلمات بعيدة. "
                   "تزيد التنوع وتزيد أيضًا احتمال الخروج عن الموضوع. "
                   "**التنوع ليس إبداعًا، والعشوائية ليست صحة.**")
    if top_p < 1.0:
        st.caption(f"top-p يقتطع الذيل: أبقينا أصغر مجموعة كلمات يبلغ مجموع احتمالاتها {top_p:.2f}، "
                   "ثم أعدنا التوزيع عليها. وهو يحدّ من الاختيارات الشاذة حتى مع حرارة مرتفعة.")


# ------------------------------------------------------------------ 7.2 attention

ATT_SENTENCES = {
    "البنك المركزي رفع سعر الفائدة": {
        "الفائدة": {"البنك": 0.10, "المركزي": 0.05, "رفع": 0.10, "سعر": 0.35, "الفائدة": 0.40},
        "رفع": {"البنك": 0.25, "المركزي": 0.10, "رفع": 0.45, "سعر": 0.10, "الفائدة": 0.10},
        "المركزي": {"البنك": 0.35, "المركزي": 0.50, "رفع": 0.05, "سعر": 0.05, "الفائدة": 0.05},
    },
    "الطالب قرأ الكتاب لأنه كان مفيدًا": {
        "لأنه": {"الطالب": 0.15, "قرأ": 0.10, "الكتاب": 0.45, "لأنه": 0.20, "كان": 0.05, "مفيدًا": 0.05},
        "مفيدًا": {"الطالب": 0.10, "قرأ": 0.05, "الكتاب": 0.50, "لأنه": 0.10, "كان": 0.10, "مفيدًا": 0.15},
        "قرأ": {"الطالب": 0.40, "قرأ": 0.35, "الكتاب": 0.15, "لأنه": 0.05, "كان": 0.03, "مفيدًا": 0.02},
    },
}


@register("m07_attention", "مختبر الانتباه (توضيحي)", "Attention toy", module=7)
def attention_lab() -> None:
    st.warning("**تنبيه:** الأوزان أدناه **موضوعة يدويًا** لتوضيح فكرة الانتباه، وليست أوزانًا "
               "مستخرجة من نموذج. الغرض أن ترى **ما معنى أن ينتبه رمز إلى رمز آخر**.",
               icon=":material/science:")
    sent = st.selectbox("الجملة", list(ATT_SENTENCES), key="m07_attention-sent")
    data = ATT_SENTENCES[sent]
    focus = st.segmented_control("اختر الرمز الذي ينتبه", list(data), default=list(data)[0],
                                 key="m07_attention-focus", required=True)
    weights = data[focus]
    words = list(weights)
    vals = [weights[w] for w in words]

    html = ""
    for w, v in zip(words, vals):
        alpha = 0.12 + 0.88 * (v / max(vals))
        bold = "font-weight:800;" if w == focus else ""
        html += (f'<span style="display:inline-block;margin:3px;padding:6px 12px;border-radius:10px;'
                 f'background:rgba(200,85,61,{alpha:.2f});{bold}">{w}'
                 f'<sub style="font-size:0.7rem;color:#5A4A45"> {v:.2f}</sub></span>')
    st.html(f'<div style="line-height:2.6;direction:rtl;font-size:1.1rem">{html}</div>')

    fig = go.Figure(go.Bar(x=words, y=vals, marker_color=PALETTE[: len(words)]))
    fig.update_yaxes(title="وزن الانتباه", range=[0, 0.6])
    show(fig, 320, key="m07-attn-lab")
    top = words[int(np.argmax(vals))]
    st.info(f"الرمز **«{focus}»** يعطي أعلى وزن لـ**«{top}»**. "
            "هكذا يبني النموذج تمثيلًا **يراعي السياق**: معنى الرمز يتحدد بما حوله لا بذاته فقط.")
    st.caption("في النماذج الحقيقية توجد **رؤوس انتباه متعددة** في كل طبقة، ولكل رأس نمط مختلف، "
               "وتتكرر العملية عبر عشرات الطبقات.")


# ------------------------------------------------------------------ 7.4 RAG

DOCS = [
    ("لائحة الامتحانات — المادة 12",
     "يحق للطالب تقديم طعن في نتيجة الامتحان خلال ثلاثة أيام عمل من تاريخ إعلان النتائج. "
     "يُقدَّم الطعن كتابيًا إلى مصلحة الامتحانات."),
    ("لائحة الامتحانات — المادة 15",
     "يُعتبر الطالب راسبًا في المقياس إذا تحصل على علامة أقل من 10 من 20، "
     "ويُسمح له بالاستدراك في الدورة الثانية."),
    ("لائحة التسجيل — المادة 4",
     "تُفتح التسجيلات في شهر سبتمبر، ويجب على الطالب تقديم شهادة البكالوريا وبطاقة التعريف "
     "ووثيقة إثبات الإقامة."),
    ("دليل المكتبة",
     "يمكن للطالب استعارة ثلاثة كتب في وقت واحد لمدة أسبوعين قابلة للتجديد مرة واحدة. "
     "التأخير يعرّض الطالب لغرامة يومية."),
    ("لائحة المنح — المادة 7",
     "تُمنح المنحة الدراسية للطلبة المسجلين بصفة منتظمة، وتُصرف شهريًا، "
     "وتُوقف في حالة الانقطاع عن الدراسة لأكثر من شهر."),
    ("لائحة الامتحانات — المادة 20",
     "الغياب عن الامتحان بعذر مقبول يخوّل الطالب اجتياز امتحان استدراكي، "
     "شريطة تقديم مبرر خلال 48 ساعة."),
]


def _tokens(t: str) -> list[str]:
    t = re.sub("[إأآٱ]", "ا", t).replace("ى", "ي").replace("ة", "ه")
    return [w for w in re.findall(r"[\w]+", t) if len(w) > 2]


def _tfidf_scores(query: str, docs: list[tuple[str, str]]) -> list[float]:
    """Real (if simple) TF-IDF cosine scoring in numpy — no external library."""
    doc_toks = [_tokens(t + " " + b) for t, b in docs]
    q_toks = _tokens(query)
    vocab = sorted({w for d in doc_toks for w in d} | set(q_toks))
    idx = {w: i for i, w in enumerate(vocab)}
    n = len(docs)
    df = np.zeros(len(vocab))
    for d in doc_toks:
        for w in set(d):
            df[idx[w]] += 1
    idf = np.log((1 + n) / (1 + df)) + 1.0

    def vec(toks):
        v = np.zeros(len(vocab))
        for w in toks:
            v[idx[w]] += 1
        if v.sum():
            v = v / v.sum()
        return v * idf

    qv = vec(q_toks)
    scores = []
    for d in doc_toks:
        dv = vec(d)
        denom = (np.linalg.norm(qv) * np.linalg.norm(dv)) or 1e-9
        scores.append(float(qv @ dv / denom))
    return scores


@register("m07_rag", "مختبر الاسترجاع المعزز (RAG)", "RAG concept lab", module=7)
def rag_lab() -> None:
    st.caption("مجموعة وثائق صغيرة مدمجة في المختبر. **الاسترجاع حقيقي** (TF-IDF بتشابه جيب التمام "
               "منفَّذ بـnumpy)، أما **الإجابة فمولَّدة بقالب** لا بنموذج لغوي، لأن المنصة تعمل دون "
               "أي واجهة برمجية. الهدف رؤية **أثر جودة الاسترجاع على الإجابة**.")
    q = st.text_input("سؤالك", "كم يومًا لتقديم طعن في نتيجة الامتحان؟", key="m07_rag-q")
    k = st.slider("عدد المقاطع المسترجَعة (k)", 1, 4, 2, key="m07_rag-k")
    sabotage = st.checkbox("جرّب استرجاعًا سيئًا (اختيار مقاطع عشوائية)", key="m07_rag-bad")
    if not q.strip():
        return

    scores = _tfidf_scores(q, DOCS)
    if sabotage:
        rng = np.random.default_rng(len(q))
        order = rng.permutation(len(DOCS))[:k]
    else:
        order = np.argsort(-np.array(scores))[:k]

    st.markdown("#### 1) الاسترجاع")
    fig = go.Figure(go.Bar(y=[d[0] for d in DOCS], x=scores, orientation="h",
                           marker_color=["#C8553D" if i in order else "#E9D5C6"
                                         for i in range(len(DOCS))]))
    fig.update_xaxes(title="درجة التشابه مع السؤال")
    fig.update_yaxes(side="right", autorange="reversed")
    show(fig, 340, key="m07-rag-scores")

    st.markdown("#### 2) السياق المُركَّب")
    context = "\n\n".join(f"[{i + 1}] {DOCS[j][0]}\n{DOCS[j][1]}" for i, j in enumerate(order))
    st.code(context, language="text")

    st.markdown("#### 3) الإجابة المؤسَّسة (بقالب)")
    best = int(order[0])
    if sabotage or scores[best] < 0.08:
        st.error("**لا توجد إجابة في المقاطع المسترجَعة.**  \n"
                 "وهذا هو السلوك **الصحيح** حين يفشل الاسترجاع: التصريح بعدم وجود الإجابة "
                 "بدل تأليفها من المقاطع غير ذات الصلة.")
        st.info("**الدرس الأهم في المختبر:** جودة إجابة RAG **محدودة بجودة الاسترجاع**. "
                "إن لم يجد النظام المقطع الصحيح، فلا يستطيع النموذج تعويضه، وإن حاول فقد يهلوس.")
    else:
        st.success(f"**الإجابة:** استنادًا إلى «{DOCS[best][0]}»: {DOCS[best][1]}\n\n"
                   f"**المصدر:** [{list(order).index(best) + 1}] {DOCS[best][0]}")
        st.caption("لاحظ **الإسناد**: كل إجابة مقرونة بالمقطع الذي جاءت منه، فيمكن التحقق في ثوانٍ (المحاضرة 6.3).")

    with st.expander("أين يمكن أن يفشل هذا المسار؟", icon=":material/warning:"):
        st.markdown(
            "1. **سؤال غامض** لا يطابق مفردات الوثائق.\n"
            "2. **استرجاع ضعيف**: المقطع الصحيح موجود ولا يظهر ضمن أعلى k.\n"
            "3. **مصادر قديمة أو خاطئة**: الإجابة مسندة تمامًا وخاطئة تمامًا.\n"
            "4. **سياق مزدحم**: k كبير جدًا يُغرق المعلومة المهمة.\n"
            "5. **سوء استعمال السياق**: النموذج يخلط مقطعين أو ينسب إلى مقطع ما لا يقوله.\n\n"
            "**الخلاصة:** RAG يقلل الهلوسة ولا يلغيها، ويحوّل المشكلة جزئيًا من «معرفة النموذج» "
            "إلى **جودة مصادرك وجودة استرجاعك**.")


# ------------------------------------------------------------------ 7.5 agent

AGENT_STEPS = [
    ("الهدف", "احجز موعدًا مع الأستاذ لمناقشة مذكرة التخرج هذا الأسبوع.",
     "—", "الحالة: لا شيء بعد.", False),
    ("تخطيط", "أحتاج إلى: (1) معرفة أوقات الأستاذ المتاحة، (2) معرفة أوقات الطالب، (3) اقتراح موعد، (4) تثبيته.",
     "لا أداة", "الحالة: خطة من أربع خطوات.", False),
    ("فعل", "استدعاء أداة: قراءة تقويم الأستاذ (صلاحية قراءة فقط).",
     "calendar.read()", "الحالة: متاح الثلاثاء 10:00 والخميس 14:00.", False),
    ("ملاحظة", "الطالب ذكر في رسالته أنه غير متاح صباحًا.",
     "—", "الحالة: يبقى الخميس 14:00.", False),
    ("فعل", "استدعاء أداة: إنشاء موعد في التقويم.",
     "calendar.write()", "⚠ يتطلب **موافقة بشرية**: فعل يعدّل بيانات ويؤثر في الأستاذ.", True),
    ("فعل", "استدعاء أداة: إرسال تأكيد بالبريد إلى الطالب.",
     "mail.send()", "⚠ يتطلب **موافقة بشرية**: فعل غير قابل للعكس عمليًا.", True),
    ("توقف", "تحقق الهدف. إنهاء الحلقة وتسجيل ما جرى في سجل التدقيق.",
     "—", "الحالة: منتهية.", False),
]


@register("m07_agent", "مختبر حلقة الوكيل", "Agent workflow lab", module=7)
def agent_lab() -> None:
    st.caption("تنفيذ خطوة بخطوة لحلقة وكيل. لاحظ أين تتوقف الحلقة لطلب **موافقة بشرية**، "
               "وربط ذلك بقاعدة قابلية العكس (المحاضرتان 3.4 و6.5).")
    n = st.slider("الخطوة", 1, len(AGENT_STEPS), 1, key="m07_agent-step")
    for i, (kind, what, tool, state, needs_ok) in enumerate(AGENT_STEPS[:n], 1):
        color = {"الهدف": "#5E8C61", "تخطيط": "#5B9BD5", "فعل": "#E07A5F",
                 "ملاحظة": "#F2A541", "توقف": "#8E7DBE"}[kind]
        with st.container(border=True, key=f"m07-agent-{i}"):
            st.markdown(f"**{i}. :{'red' if needs_ok else 'gray'}[{kind}]** — {what}")
            c1, c2 = st.columns([1, 2])
            c1.caption(f"الأداة: `{tool}`")
            c2.caption(state)
            if needs_ok and i == n:
                a, b = st.columns(2)
                a.button("موافقة", key=f"m07_agent-ok-{i}", icon=":material/check:", type="primary")
                b.button("رفض", key=f"m07_agent-no-{i}", icon=":material/close:")
    if n == len(AGENT_STEPS):
        st.success("**اكتملت الحلقة.** لاحظ أن الوكيل عمل كله **داخل أدوات وصلاحيات منحها له البشر**: "
                   "قرأ التقويم بصلاحية قراءة، وتوقف قبل الكتابة وقبل الإرسال.")
        st.info("**الوكيل الذكي ≠ الذكاء العام:** ما رأيته حلقة تخطيط واستدعاء أدوات ضمن نطاق محدد. "
                "خارج هذا النطاق لا يملك الوكيل شيئًا، ولا يدرك أنه خارجه (المحاضرة 3.4).")
