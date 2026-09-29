# Content authoring guide

This is the binding format for course content. It turns two sources into files:
`MASTER_PROMPT_Introduction_to_AI_Streamlit_Platform.md` (the build specification)
and the official course card (`1.jpeg`, `2.jpeg`, transcribed in `content/course.yml`).
Anything written here must follow both.

## 1. Files per module

```
content/module_XX/
  metadata.yml        module header + entry system + exit system + instructor panel
  lecture_01.md …     3–6 lectures (as many as the topic needs; no fixed count)
  quiz.yml            entry:  test d'entrée (4–6 questions)
                      questions: module post-test (8–10 questions)
  references.yml      every source cited in this module (real, verified)
  glossary.yml        8–20 terms introduced in this module
components/diagrams/mXX.py   diagrams registered with @register("mXX_name")
components/labs/mXX.py       interactive labs registered with @register("mXX_name", ...)
```

IDs: module `m01`, lecture `m01-l03`, question `m01-q07` / entry `m01-e02`,
diagram and lab names `m01_ai_ecosystem`. References use `author_year_word`
(for example `russell_norvig_2021`, `nist_ai_rmf_2023`).

## 2. Official course card: what every module must mirror

| Card requirement | Where it lives |
|---|---|
| البطاقة المفاهيمية الذهنية (mind-map concept card) | `metadata.yml: concept_diagram:` → a network/mind-map diagram in `mXX.py` |
| موارد مختلفة: صور، جداول، معادلات، مخططات، روابط فيديو | lecture bodies (tables, `$…$` equations, `[[diagram:…]]`) + `self_study` video links |
| أهداف الدروس بأفعال بلوم | `metadata.yml: objectives` with a `bloom` level; lecture `objectives` start with a Bloom verb (يعرّف، يشرح، يطبق، يحلل، يقيّم، يصمم…) |
| أنشطة المدخلات القبلية + QUIZ بتغذية راجعة | `metadata.yml: entry.prior_knowledge`, `entry.diagnostic_questions`, `quiz.yml: entry` |
| ارتباط المكتسبات القبلية بالمحتوى | lecture front matter `builds_on` (lecture ids or plain prior-knowledge statements) |
| savoir / auto-apprentissage / savoir-faire | savoir = lecture body; auto-apprentissage = `self_study`; savoir-faire = `:::exercise` + activities + labs |
| تمرين في كل درس | **at least one `:::exercise` block in every lecture**, with a model solution after `???` |
| post-tests QUIZ | `quiz.yml: questions` |
| تقييم الكفاءات حسب الأهداف | `metadata.yml: exit.competencies` (phrased "أستطيع أن…") |
| أنشطة تقييمية مختلفة الطرح | `metadata.yml: exit.assessment_activities` (vary the format: oral, written, lab, peer review, mini-case) |
| أنشطة تدعيمية في حالة الفشل + توجيه إلى موارد | `exit.remediation` + `exit.suggested_reading` (reference ids) |

## 3. `metadata.yml`

```yaml
module_number: 1
title: "مقدمة في الذكاء الاصطناعي: المفهوم، الأهمية، والمجالات"   # official axis title, verbatim
short_title: مقدمة في الذكاء الاصطناعي                              # ≤ 32 chars, for navigation
title_en: "Introduction to AI: Concept, Importance and Fields"
subtitle: one sentence on what the module achieves
description: |
  2–4 academic paragraphs in Markdown: scope, why it matters, how it connects to the course.
estimated_duration: "3 حصص × 90 دقيقة"
difficulty: مبتدئ | متوسط | متقدم
keywords: [..]
concept_diagram: m01_concept_map
objectives:
  - {bloom: remember, text: "يعرّف …"}
  - {bloom: understand, text: "يشرح …"}
  # 5–8 objectives covering at least 4 Bloom levels
prerequisites: [..]
entry:
  prior_knowledge: [what students already know and how this module uses it]
  diagnostic_questions: [3–5 open questions]
exit:
  competencies: ["أستطيع أن …", ...]
  assessment_activities: [..]
  common_mistakes: [..]
  remediation: [concrete support activities, each naming the lecture to revisit]
  suggested_reading: [reference ids]
  bridge: paragraph linking to the next module
instructor:
  sequence: [suggested teaching order with reasoning]
  timing: ["الحصة 1 (90 د): …", ...]
  discussion: [open questions that start discussion]
  assessment_ideas: [..]
  extensions: [advanced extensions for strong groups]
```

## 4. Lecture file `lecture_NN.md`

```markdown
---
id: m01-l01
number: 1
title: ما هو الذكاء الاصطناعي؟
short_title: ما هو AI؟
title_en: What is Artificial Intelligence?
subtitle: …
duration: 90
difficulty: مبتدئ
objectives: ["يعرّف …", "يميز …", "يحلل …"]
prerequisites: [..]
builds_on: ["m01-l01", "خبرة الطالب اليومية مع أنظمة التوصية"]
keywords: [..]
related: [m04-l01, m03-l01]          # lecture ids only
summary: [4–7 takeaways]
references:
  - {id: russell_norvig_2021, for: "تصنيف التعريفات الأربعة للذكاء الاصطناعي"}
self_study:
  - type: video | reading | doc | course | tool | dataset
    title: …
    source: Organisation / channel (English)
    url: https://…
    why: one sentence on what to watch or read for
    verified: "2026-09-26"
---

Body (Markdown)…
```

### Body syntax

- `## Heading` creates a section and a table-of-contents anchor. Use `###` inside sections.
- Cards (open with `:::type Title`, close with a line `:::`):
  `definition key example applied method misconception warning didyouknow discussion
  activity case recap check exercise selfstudy modern verify crosslink`.
  `instructor` appears only in Instructor Mode. `deep` is a collapsed Technical Deep Dive.
- `check` and `exercise`: the question comes first, then a line `???`, then the model answer.
- Sticky notes: `:::sticky`, `:::sticky-rose`, `:::sticky-lavender`, `:::sticky-peach`.
- `[[diagram:m01_name]]`, `[[widget:m01_name]]` and `[[link:m04-l01]]` go on their own line.
- Math: `$w_1x_1 + b$` inline, `$$ … $$` display (KaTeX). Code: fenced blocks (rendered LTR).
- Tables: Markdown tables (horizontal scroll on small screens).
- YAML rule: any front-matter value containing «: » must be quoted ("عنوان: فرعي").
  `python scripts/fix_yaml_colons.py` quotes them automatically, and `--check` reports without
  writing (use it before finishing a module). There are **two** failure modes, and the second is
  the dangerous one:
  - `key: نص: بقية` → the parser raises and the file does not load. **Loud**, fixed immediately.
  - `- نص: بقية` inside a list of plain strings (`summary`, `objectives`, `prerequisites`,
    `keywords`, `builds_on`, `related`, and the `entry`/`exit`/`instructor` lists) → YAML silently
    parses the item as a **mapping** instead of a string. **Nothing raises**: validation passes and
    pages render, then any code joining those items (`app_pages/knowledge_map.py`) crashes with
    "sequence item N: expected str instance, dict found". Always quote a list item that contains «: ».
- Bidi rule: never glue Arabic «و» or «بـ» directly to a Latin word («Russell وNorvig» renders as
  «Norvigg Russell»). Write «Russell و Norvig» or use the Arabic form «راسل ونورفيغ».
- English terms: at first use, write the Arabic term followed by the English, e.g.
  «التعلم الآلي (Machine Learning)».

## 5. Depth and style (spec §5, §6, §10, §62, §74, §83)

- A lecture is something a professor can teach from for 90 minutes. Typical size is 1,800–3,000 Arabic
  words of Markdown plus at least 10 teaching blocks and a comparison table (Arabic prose is
  much more compact than English, so the validator measures words, blocks and tables together), with a Core explanation, **instructor** cards (Teaching Insights) and a
  **deep** block (Technical Deep Dive) wherever it helps.
- For each important concept, choose from: definition, intuition, historical motivation,
  problem solved, mechanism, components, relations, comparison, simple / academic / practical
  examples, strengths, limitations, failure modes, misconceptions, teaching notes, diagram,
  table, activity, self-check.
- Vary the rhythm. Do not stack cards one after another: mix text, tables, diagrams, stickies,
  cards and labs.
- Academic voice. Do not use filler openers such as «في عالمنا سريع التغير», «لا شك أن»,
  «كما نعلم جميعًا» or «ثورة مذهلة».
- Instructor notes are specific ("ask students to list three systems that … then classify …"),
  never generic.
- **Never** write TODO, placeholder, lorem ipsum, "coming soon", or text such as "to be completed".
- Add modern topics in a `:::modern` card (امتداد حديث | Modern Extension) and do not remove any
  official axis.

## 6. Research and verification (spec §1–3, §67)

- Cite only sources you actually verified: fetch the URL or DOI and confirm title, authors and
  year. Never invent a DOI, URL, title, author, date or product feature.
- Vendor facts (ChatGPT, Gemini, Claude, DALL·E, Midjourney, Suno, …) come **only** from
  official documentation pages that you fetched. Record the date in `verified:`. If something
  cannot be verified, describe it generically ("some assistants offer…"), not as a claim.
- Video links: only official channels or institutions (university channels, 3Blue1Brown,
  Stanford Online, MIT OpenCourseWare, Google, IBM Technology, the vendors' own channels, …).
  Confirm the video page exists before listing it.
- Put anything you could not verify in `research/sources_to_verify.md`, and log your research in
  `research/logs/mXX.md` (topic, sources, key findings, disagreements, date).

## 7. `references.yml`

```yaml
references:
  - id: russell_norvig_2021
    authors: Russell, S., & Norvig, P.
    year: 2021
    title: "Artificial Intelligence: A Modern Approach (4th ed.)"
    venue: Pearson
    type: book | article | report | standard | documentation | course | web
    url: https://aima.cs.berkeley.edu/
    doi: 10.xxxx/yyyy        # optional, only if verified
    topic: AI Foundations    # one of the References page sections
    verified: "2026-09-26"
```

Topics: AI Foundations, AI History, Machine Learning, Deep Learning, LLMs, Prompt Engineering,
Generative AI, Multimodal AI, Economics + AI, AI Ethics, Privacy, Security, Human Oversight,
AI Governance, Official Product Documentation, AI Education.

## 8. `quiz.yml`

```yaml
entry:        # test d'entrée — prior knowledge, diagnostic, instant feedback
  - {id: m01-e01, type: tf, bloom: remember, prompt: …, answer: false, explanation: …, review: m01-l01}
questions:    # post-test — mix of mcq, multi, tf, scenario; ≥ 4 Bloom levels; not memorisation only
  - id: m01-q01
    type: scenario
    bloom: analyze
    scenario: …
    prompt: …
    options: [.., .., .., ..]
    answer: 2
    explanation: …
    why_wrong: {0: …, 1: …}
    review: m01-l03
```

## 9. `glossary.yml`

```yaml
terms:
  - {ar: التعلم الآلي, en: Machine Learning, acronym: ML, definition: …, related: [Deep Learning],
     module: 4, lecture: m04-l01}
```

## 10. Diagrams and labs (Python)

```python
# components/diagrams/m01.py
import streamlit as st
from components.diagrams import flow, grid_cards, nested, network, register, show, style_fig

@register("m01_ai_fields")
def ai_fields():
    grid_cards([("معالجة اللغة الطبيعية", "NLP", "…"), …], cols=3)
```

```python
# components/labs/m07.py
import streamlit as st
from components.labs import register

@register("m07_temperature", "محاكاة درجة الحرارة", "Temperature simulation", module=7)
def temperature():
    t = st.slider("درجة الحرارة", 0.1, 2.0, 1.0, key="m07_temperature-t")
    …
```

- Use Plotly for anything quantitative (`show(fig, height)`) and `flow`, `nested`, `grid_cards`
  or `network` for concepts. Text in diagrams is Arabic, with English as a subtitle.
- Labs run offline with no API key. When a lab simplifies reality (a toy tokenizer, invented
  probabilities), it must say so in an `st.caption`.
- Prefix every widget key with the lab name.
- Colours: warm, light, multi-colour. Never a dark background, and never green as the
  dominant colour.

## 11. Self-check before finishing a module

```bash
python scripts/validate_content.py --module 1
python -m pytest -q
```
