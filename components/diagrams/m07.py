"""Module 7 diagrams: concept map, tokenization, embedding space, next-token loop,
Transformer block, attention heatmap, LLM lifecycle, RAG pipeline, agent loop,
and the prompting/RAG/fine-tuning comparison."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from components.diagrams import PALETTE, flow, grid_cards, network, register, show


@register("m07_concept_map")
def concept_map() -> None:
    nodes = [
        {"id": "llm", "label": "النموذج اللغوي الكبير", "x": 0, "y": 0, "group": 0},
        {"id": "tok", "label": "الرموز والتقطيع", "x": -2.2, "y": 1.1, "group": 1},
        {"id": "emb", "label": "التضمينات", "x": -2.4, "y": -0.3, "group": 1},
        {"id": "next", "label": "التنبؤ بالرمز التالي", "x": -1.2, "y": -1.6, "group": 1, "hover": "Softmax + أخذ عينة"},
        {"id": "trf", "label": "المحوّل والانتباه", "x": 0, "y": 2.0, "group": 2},
        {"id": "life", "label": "دورة الحياة", "x": 2.2, "y": 1.1, "group": 3, "hover": "بيانات ← تدريب مسبق ← تعليمات ← مواءمة ← تقييم ← استدلال"},
        {"id": "hal", "label": "الهلوسة", "x": 2.4, "y": -0.3, "group": 4},
        {"id": "rag", "label": "الاسترجاع المعزز", "x": 1.2, "y": -1.6, "group": 5},
        {"id": "agent", "label": "الوكلاء والأدوات", "x": 0, "y": -2.3, "group": 5},
    ]
    edges = [("llm", "tok"), ("tok", "emb"), ("emb", "next"), ("llm", "trf"), ("llm", "life"),
             ("life", "hal"), ("hal", "rag"), ("rag", "agent"), ("next", "agent"), ("trf", "life")]
    network(nodes, edges, height=520, key="m07-concept")


@register("m07_tokenization")
def tokenization() -> None:
    st.caption("التقطيع: النموذج لا يرى كلمات بل **رموزًا (tokens)**، وقد يُقسَّم الرمز الواحد إلى أجزاء. "
               "العرض أدناه **تعليمي تقريبي** لتوضيح الفكرة، وليس مخرج مقطّع حقيقي.")
    flow([("النص الخام", "Raw text"), ("التقطيع", "Tokenization"), ("معرّفات عددية", "Token IDs"),
          ("التضمينات", "Embeddings"), ("طبقات المحوّل", "Transformer layers")],
         caption="لا يرى النموذج حروفًا ولا كلمات، بل متجهات أعداد.")


@register("m07_embedding_space")
def embedding_space() -> None:
    st.caption("فضاء التضمينات: الكلمات المتقاربة في المعنى تقع في مواضع متقاربة. "
               "**المواضع أدناه موضوعة يدويًا للتوضيح** وليست تضمينات نموذج حقيقي.")
    groups = {
        "مهن": [("طبيب", 0.8, 2.1), ("مهندس", 1.1, 2.4), ("أستاذ", 0.6, 2.5), ("محامٍ", 1.3, 2.0)],
        "حيوانات": [("قط", -2.1, 1.2), ("كلب", -1.8, 1.5), ("حصان", -2.4, 0.9), ("أسد", -1.6, 0.8)],
        "اقتصاد": [("تضخم", 1.9, -1.4), ("فائدة", 2.2, -1.1), ("ناتج", 1.6, -1.8), ("سوق", 2.4, -1.7)],
        "مدن": [("الجزائر", -1.9, -1.6), ("وهران", -1.6, -1.9), ("قسنطينة", -2.2, -1.3)],
    }
    fig = go.Figure()
    for i, (name, pts) in enumerate(groups.items()):
        fig.add_trace(go.Scatter(
            x=[p[1] for p in pts], y=[p[2] for p in pts], mode="markers+text",
            text=[p[0] for p in pts], textposition="top center", name=name,
            marker=dict(size=14, color=PALETTE[i], line=dict(color="#FFFFFF", width=2))))
    fig.update_xaxes(visible=False, range=[-3.2, 3.2])
    fig.update_yaxes(visible=False, range=[-2.8, 3.2])
    fig.update_layout(legend=dict(orientation="h", y=1.12))
    show(fig, 420, key="m07-emb")


@register("m07_next_token")
def next_token() -> None:
    flow([("السياق كله", "Context"), ("طبقات المحوّل", "Layers"), ("درجات لكل رمز", "Logits"),
          ("Softmax", "Probabilities"), ("أخذ عينة", "Sampling"), ("الرمز التالي", "Next token")],
         loop=True,
         caption="الحلقة تتكرر لكل رمز: الرمز المولَّد يُضاف إلى السياق ثم تُعاد العملية كلها.")


@register("m07_transformer_block")
def transformer_block() -> None:
    grid_cards([
        ("التضمين والموضع", "Embedding + Position", "تحويل كل رمز إلى متجه، مع إضافة معلومة عن موقعه في التسلسل."),
        ("الانتباه الذاتي", "Self-attention", "كل رمز ينظر إلى بقية الرموز ويرجّحها حسب صلتها به."),
        ("التغذية الأمامية", "Feed-forward", "معالجة كل موضع على حدة بطبقات كثيفة."),
        ("الوصلات المتخطية", "Residual connections", "تمرير المدخل مع المخرج لتسهيل تدريب الشبكات العميقة."),
        ("التسوية", "Layer normalization", "استقرار التدريب بضبط توزيع القيم داخل الطبقة."),
        ("التكرار", "N layers", "تُكرَّر الكتلة عشرات المرات، وتبني كل طبقة تمثيلًا أعمق."),
    ], cols=3)


@register("m07_attention_heatmap")
def attention_heatmap() -> None:
    st.caption("خريطة انتباه **توضيحية**: الأرقام موضوعة يدويًا لشرح الفكرة، وليست أوزانًا من نموذج حقيقي.")
    words = ["البنك", "المركزي", "رفع", "سعر", "الفائدة"]
    w = np.array([
        [0.55, 0.30, 0.05, 0.05, 0.05],
        [0.35, 0.50, 0.05, 0.05, 0.05],
        [0.25, 0.10, 0.45, 0.10, 0.10],
        [0.05, 0.05, 0.15, 0.40, 0.35],
        [0.10, 0.05, 0.10, 0.35, 0.40],
    ])
    fig = go.Figure(go.Heatmap(z=w, x=words, y=words, colorscale=[[0, "#FFF9F3"], [1, "#C8553D"]],
                               texttemplate="%{z:.2f}", showscale=False,
                               hovertemplate="الرمز %{y} ينتبه إلى %{x}: %{z:.2f}<extra></extra>"))
    fig.update_yaxes(autorange="reversed", side="right", title="الرمز الذي ينتبه")
    fig.update_xaxes(title="الرمز المنتبَه إليه")
    show(fig, 420, key="m07-attn")
    st.caption("لاحظ أن «الفائدة» تنتبه بقوة إلى «سعر»، وأن «المركزي» تنتبه إلى «البنك»: "
               "الانتباه يبني تمثيلًا **يراعي السياق** لكل رمز.")


@register("m07_lifecycle")
def lifecycle() -> None:
    flow([("البيانات", "Data"), ("التدريب المسبق", "Pretraining"), ("ضبط التعليمات", "Instruction tuning"),
          ("المواءمة", "Alignment"), ("التقييم", "Evaluation"), ("الاستدلال", "Inference")],
         caption="دورة حياة النموذج اللغوي: ثلاث مراحل تدريب، ثم تقييم، ثم الاستعمال.")
    grid_cards([
        ("التدريب المسبق", "Pretraining", "تعلم ذاتي الإشراف على نصوص ضخمة: التنبؤ بالرمز التالي. هنا تتكون «المعرفة»."),
        ("ضبط التعليمات", "Instruction tuning", "تعلم موجَّه على أمثلة (تعليمة ← استجابة) ليتبع النموذج الطلبات."),
        ("المواءمة", "Alignment", "تعلم من تفضيلات بشرية (RLHF وغيره) ليكون مفيدًا ومهذبًا وأقل ضررًا."),
    ], cols=3)


@register("m07_hallucination_types")
def hallucination_types() -> None:
    grid_cards([
        ("اختلاق", "Fabrication", "معلومة لا وجود لها: مرجع، أو اقتباس، أو رقم مخترع."),
        ("تعارض مع المصدر", "Source conflict", "يخالف النص المرفق أو ينسب إليه ما لا يقوله."),
        ("معلومة قديمة", "Outdated", "كانت صحيحة ولم تعد كذلك. ليست هلوسة بالمعنى الدقيق لكنها خطأ."),
        ("خطأ استدلالي", "Reasoning error", "خطوات حساب أو استنتاج خاطئة رغم صحة المعطيات."),
        ("إجابة غامضة", "Vague answer", "صحيحة شكليًا وبلا مضمون قابل للفحص."),
        ("ثقة زائدة", "Overconfidence", "صياغة جازمة في موضع الشك؛ تضاعف ضرر كل ما سبق."),
    ], cols=3)


@register("m07_rag_pipeline")
def rag_pipeline() -> None:
    flow([("سؤال المستخدم", "User query"), ("تمثيل السؤال", "Query representation"),
          ("البحث والاسترجاع", "Search / Retrieval"), ("الوثائق ذات الصلة", "Relevant documents"),
          ("تركيب السياق", "Context assembly"), ("النموذج اللغوي", "LLM"),
          ("إجابة مؤسَّسة بالمصدر", "Grounded response")],
         caption="مسار الاسترجاع المعزز بالتوليد (RAG) كما في مواصفات المقرر §40.")
    st.caption("**نقاط الفشل:** سؤال غامض، أو استرجاع لا يجد المقطع الصحيح، أو مصادر قديمة أو خاطئة، "
               "أو سياق مزدحم يُغرق المعلومة المهمة، أو نموذج يسيء استعمال ما استُرجع.")


@register("m07_agent_loop")
def agent_loop() -> None:
    flow([("الهدف", "Goal"), ("التخطيط", "Reason / Plan"), ("اختيار الأداة", "Choose tool"),
          ("التنفيذ", "Act"), ("الملاحظة", "Observe"), ("تحديث الحالة", "Update state"),
          ("متابعة أم توقف", "Continue / Stop")],
         loop=True, caption="حلقة الوكيل كما في مواصفات المقرر §41. الوكيل الذكي ≠ الذكاء العام.")


@register("m07_approach_comparison")
def approach_comparison() -> None:
    st.html(
        '<div class="tiles" style="--cols:3">'
        '<div class="tile" style="background:#FFF4D6;border-top:5px solid #F2A541">'
        '<b>هندسة الأوامر</b><small>Prompt Engineering</small>'
        '<p>توجيه النموذج بالسياق والتعليمات.<br>'
        '<b>النموذج:</b> لا يتغير · <b>البيانات:</b> لا شيء إضافي · <b>الكلفة:</b> منخفضة جدًا · '
        '<b>التحديث:</b> فوري · <b>الحد:</b> لا يضيف معرفة.</p></div>'
        '<div class="tile" style="background:#EAF5FE;border-top:5px solid #5B9BD5">'
        '<b>الاسترجاع المعزز</b><small>RAG</small>'
        '<p>إحضار مقاطع من مصادرك ووضعها في السياق.<br>'
        '<b>النموذج:</b> لا يتغير · <b>البيانات:</b> وثائقك · <b>الكلفة:</b> متوسطة (بنية تحتية) · '
        '<b>التحديث:</b> بتحديث الوثائق · <b>الميزة:</b> إسناد قابل للتحقق.</p></div>'
        '<div class="tile" style="background:#F3EEFF;border-top:5px solid #8E7DBE">'
        '<b>الضبط الدقيق</b><small>Fine-tuning</small>'
        '<p>تعديل معاملات النموذج على أمثلتك.<br>'
        '<b>النموذج:</b> <b>يتغير</b> · <b>البيانات:</b> آلاف الأمثلة · <b>الكلفة:</b> عالية · '
        '<b>التحديث:</b> بإعادة التدريب · <b>الأنسب لـ:</b> الأسلوب والصيغة لا الوقائع.</p></div></div>'
    )
