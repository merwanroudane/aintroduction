<div align="center">

<img src="assets/banner.svg" alt="مقدمة في الذكاء الاصطناعي — Introduction to Artificial Intelligence" width="100%">

### منصة تعليمية جامعية تفاعلية باللغة العربية لتدريس الذكاء الاصطناعي

**إعداد وتصميم: الدكتور مروان رودان** · **Dr Merwan Roudane**

<br>

[![Modules](https://img.shields.io/badge/المحاور-13-E4695A?style=for-the-badge&labelColor=2F2C33)](#what-is-in-the-course)
[![Lectures](https://img.shields.io/badge/المحاضرات-72-D97D2E?style=for-the-badge&labelColor=2F2C33)](#what-is-in-the-course)
[![Questions](https://img.shields.io/badge/أسئلة%20التقييم-286-46AB68?style=for-the-badge&labelColor=2F2C33)](#what-is-in-the-course)
[![Labs](https://img.shields.io/badge/مختبرات%20تفاعلية-41-2E9FB8?style=for-the-badge&labelColor=2F2C33)](#what-is-in-the-course)
[![Sources](https://img.shields.io/badge/مصادر%20موثّقة-192-7B5FD6?style=for-the-badge&labelColor=2F2C33)](SOURCES.md)
[![TD topics](https://img.shields.io/badge/مواضيع%20بحوث%20TD-65-C455A6?style=for-the-badge&labelColor=2F2C33)](#for-the-tutorial-hour-td)

[![Python](https://img.shields.io/badge/Python-3.11+-3E8FD0?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.63-E4695A?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-6.5-7B5FD6?logo=plotly&logoColor=white)](https://plotly.com/python/)
[![Tests](https://img.shields.io/badge/tests-96%20passing-46AB68?logo=pytest&logoColor=white)](#checks)
[![RTL](https://img.shields.io/badge/RTL-العربية-2FA391)](#)
[![Offline](https://img.shields.io/badge/يعمل%20بلا%20إنترنت-100%25-7F9C2B)](#quick-start)
[![No API key](https://img.shields.io/badge/بلا%20مفاتيح%20API-مجاني-B98A0E)](#quick-start)

</div>

---

An interactive **Arabic-language (RTL)** teaching platform built with Streamlit. It delivers a
complete university course on artificial intelligence: **13 modules, 72 lectures, 286 assessment
questions, 120 diagrams and 41 offline interactive labs** — with an **Instructor Mode** layered
over every page, and a separate guide for the tutorial (TD) hour.

It runs **entirely offline**. No API key, no paid service, no network call at runtime — so it
works in a lecture hall with no internet and costs the university nothing.

---

## Quick start

```bash
pip install -r requirements.txt
```

To run the test suite as well:

```bash
pip install -r requirements-dev.txt
```

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`. It runs **fully offline**: no API key, no paid
service, no network call at runtime. Every simulation in every lab is computed locally with
numpy.

Requires Python 3.11+. Verified on Python 3.11 with Streamlit 1.63.

---

## What is in the course

| # | المحور | Lectures |
|---|---|---|
| 1 | مقدمة في الذكاء الاصطناعي: المفهوم، الأهمية، والمجالات | 5 |
| 2 | تاريخ الذكاء الاصطناعي: مراحل التطور | 5 |
| 3 | أنواع الذكاء الاصطناعي: الضيق، العام، والفائق | 4 |
| 4 | مقارنة بين الذكاء الاصطناعي، التعلم الآلي، والتعلم العميق | 6 |
| 5 | المفاهيم الأساسية في هندسة الأوامر (Prompt Engineering) | 5 |
| 6 | تقنيات بناء الأوامر للنماذج اللغوية الكبيرة | 5 |
| 7 | تطبيقات النماذج اللغوية (ChatGPT، Google Gemini، Claude...) | 6 |
| 8 | التفاعل مع نماذج الذكاء الاصطناعي لتوليد النصوص | 6 |
| 9 | النماذج التوليدية للصور والصوت (DALL·E، Midjourney، Suno...) | 6 |
| 10 | استخدام الذكاء الاصطناعي في الاقتصاد | 7 |
| 11 | أخلاقيات الذكاء الاصطناعي: الإنصاف، الشفافية، والتحيز | 6 |
| 12 | قضايا الخصوصية والأمان في أدوات الذكاء الاصطناعي | 6 |
| 13 | دور الإنسان في الرقابة على الذكاء الاصطناعي | 5 |

The 13 module titles are the 13 axis titles of the official course card, **verbatim** — a
test enforces this, so an accidental edit fails the build rather than drifting quietly.

**Totals:** 72 lectures · 286 questions (65 module-entry + 168 module-post + 18 pre-test +
35 post-test) · 192 verified references · 300 glossary terms · 120 diagrams · 41 labs ·
a 6-track capstone project · a 65-topic TD research bank.

## For the tutorial hour (TD)

A separate guide for whoever runs the *travaux dirigés* session, which in Algerian
universities is often a different person from the lecturer:

- **65 research topics** in 7 axes following the course order, each mapped to the modules
  that cover it and each carrying **a concrete applied task** — a comparison, a measurement,
  a verification trail — because collecting information about a tool teaches nothing about
  the tool. Filterable by axis, level, kind and discipline.
- **A 14-week distribution** that keeps advanced topics (AI agents, explainable AI,
  deepfakes) out of the opening weeks.
- **Eight session formats** beyond the presentation: prompt duels, hallucination hunts,
  putting a system on trial, three-minute verification races.
- **An assessment rubric** that weights understanding, the applied part and the discussion
  of limits — not slide design, which is the easiest thing to generate.

## A colour system, not a colour scheme

The thirteen modules walk once around the colour wheel — 337° of it, no gap under 16°,
every accent mid-tone and light. Colour is **information** here: module 5 is green in its
banner, its cards, its chart series, its node on the knowledge map and its chip in the labs
filter. Card types carry their own fixed hues (teal defines, amber states the key point,
red warns, violet is the instructor), and Bloom levels climb the spectrum from grey to red.

The canvas behind all of it is deliberately near-neutral. A tinted page would pull thirteen
hues toward itself and the whole app would read as one colour.

Every accent was validated numerically: none dark, none washed out, and every "deep" text
weight clears 7:1 contrast against its own tint. The palette lives in one place —
`MODULE_COLORS` in `components/layout.py` — and the CSS, the Plotly theme and
`.streamlit/config.toml` all draw from it.

## Two modes

A switch in the sidebar toggles the whole app between:

- **وضع الطالب (Learner)** — lectures, exercises with hidden solutions, self-checks, labs.
- **وضع الأستاذ (Instructor)** — everything above **plus** teaching notes, session timing,
  discussion prompts, assessment ideas, and full answer keys.

## Every module follows the course card

Each module mirrors the card's own structure: a mind-map concept diagram, Bloom-tagged
objectives, an **entry system** (prior knowledge + diagnostic questions + entry quiz), a
**learning system** (lectures, self-study, exercises), and an **exit system** (competencies,
common mistakes, remediation, suggested reading, and a bridge to the next module).

---

## Project layout

```
app.py                      entry point: navigation, mode switch, progress
app_pages/
  home.py course_map.py …   static pages (glossary, search, references, labs, tests…)
  module_view.py            the generic module renderer — every module uses it
  td_guide.py               the tutorial-hour guide and topic bank
  modules/module_XX.py      thin wrappers, ~6 lines each
components/
  layout.py                 CSS injection, cards, flow HTML
  quiz.py                   the four question types and the answer key
  diagrams/mXX.py           120 diagrams, registered with @register("mXX_name")
  labs/mXX.py               41 offline labs, registered with @register(name, ar, en, module)
content/
  course.yml                the official course card, transcribed
  module_XX/
    metadata.yml            header + entry system + exit system + instructor panel
    lecture_01.md …         the lectures themselves
    quiz.yml                entry questions + module post-test
    references.yml          every source cited by this module
    glossary.yml            terms this module introduces
data/                       pre-test, post-test, capstone, TD topics, shared references
utils/                      content loading, navigation, session state
scripts/                    validation and verification tooling
research/logs/mXX.md        how each module's sources were verified, and what was
                            deliberately *not* claimed
tests/                      pytest suite
assets/css/                 the stylesheet
```

**Lectures are Markdown, not Python** (spec §54). A lecture is content, and content belongs
in a file an editor can open without reading code. `utils/content.py` parses it and
`app_pages/module_view.py` renders it, so one renderer serves all 72 lectures and a fix to
the renderer fixes every lecture at once.

### The lecture format

Front matter carries the metadata (id, objectives, keywords, references, self-study,
summary). The body is Markdown plus a small block syntax:

```markdown
:::key اسم البطاقة          a teaching card — key, warning, definition, example,
...                          deep, case, misconception, activity, instructor,
:::                          exercise, check, recap, and others

:::check تحقق من فهمك        a self-check: the question, then ??? , then the answer
سؤال
???
الجواب
:::

[[diagram:m09_diffusion_loop]]   embed a registered diagram
[[widget:m10_reg_bias]]          embed a registered lab
[[link:m08-l05]]                 cross-link to another lecture
```

`CONTENT_GUIDE.md` is the binding authoring spec: file layout, metadata schema, depth
rules, research rules, and two Arabic-specific traps (a `: ` inside an unquoted YAML
scalar, and a waw glued to a Latin word, which renders reversed).

---

## Checks

Four tools, from fastest to slowest:

```bash
python -m pytest tests/ -q
```
96 tests, about a minute. Structure, cross-links, every one of the 286 answer keys, the
registries, project files, and a boot smoke test that opens the app and twelve static pages.
Includes regression tests for bugs that already happened once: a `<` in the stylesheet that
made the sanitizer drop all CSS, and a query-param binding that wrote the Arabic label into
the URL and broke deep links.

```bash
python scripts/validate_content.py
```
Content against `CONTENT_GUIDE.md`: required front matter, depth (Arabic-aware: words
**and** teaching blocks **and** a table), reference ids, self-study dating.

```bash
python scripts/render_check.py
```
Opens **every** module view in **both** modes plus every static page through Streamlit's
`AppTest`, and reports exceptions and unregistered names. A few minutes. Use `--module 9`
for one module.

```bash
python scripts/check_links.py
```
Probes every source link: DOIs through the Crossref API, arXiv through its API, YouTube
through oEmbed, everything else by HTTP. Publishers that answer 403 to any script are marked
`bot_blocked` in `references.yml`; the skip is only honoured when the entry also carries a
resolvable DOI or a `browser_verified` date, so a broken link can never hide behind the flag.

### Authoring helpers

```bash
python scripts/probe_sources.py candidates.txt   # check a source BEFORE citing it
python scripts/build_sources.py                  # regenerate SOURCES.md
python scripts/fix_yaml_colons.py content/module_09
```

- **`probe_sources.py`** takes a list of `doi:` / `arxiv:` / `yt:` / `url:` lines and prints
  the real title, authors and year, so a citation is checked before it is written rather
  than after it is published.
- **`build_sources.py`** regenerates `SOURCES.md` from every `references.yml`. Run it after
  adding a source — a test fails if the file is stale. `--check` verifies without writing.
- **`fix_yaml_colons.py`** quotes YAML scalars containing `: `. Arabic titles and summaries
  hit this constantly, and the silent form of the bug (a list item parsed as a dict) is
  worse than the loud one.

`probe_sources.py`, `build_sources.py --check` and `check_links.py` are the only tools that
use the network. The app itself never does.

## Deploying

The repository is laid out so a host can run it unchanged: `app.py` at the root,
`requirements.txt` beside it, and no runtime secrets.

**Streamlit Community Cloud** — point a new app at this repository, branch `main`,
main file `app.py`. Nothing else to configure: there is no API key to set, because the
app never calls one.

**Anywhere else** — any host that can run Python:

```bash
pip install -r requirements.txt
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

The theme lives in `.streamlit/config.toml` and is committed, so a deployment looks the
same as a local run. `.streamlit/secrets.toml` is git-ignored; the app does not read it.

## Sourcing discipline

Every reference was probed before being cited, and `research/logs/mXX.md` records for each
module what was checked, what was found, and — importantly — **what the module deliberately
does not claim**: no detector accuracy figures, no legal conclusions on copyright, no
capability claims tied to one model generation, no product rankings. Vendor-documented
behaviour is dated, because it changes.

---

## Licence and attribution

Course content and platform by **Dr Merwan Roudane**.
