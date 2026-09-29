# Brief for module writers

You write one module of the Streamlit course «مقدمة في الذكاء الاصطناعي» (Dr. Marwan Roudane).
The platform code is finished. Your job is **content**: YAML and Markdown files, plus the Python
diagrams and labs for your module.

## Read first, fully
1. `CONTENT_GUIDE.md`: the binding file format and quality bar.
2. **Module 1 is the worked example. Match its structure, depth and tone exactly:**
   `content/module_01/*` (metadata, 5 lectures, quiz, references, glossary),
   `components/diagrams/m01.py`, `components/labs/m01.py`.
3. `..\MASTER_PROMPT_Introduction_to_AI_Streamlit_Platform.md`: §0–§22, your module's section,
   and §16–19, §39, §42–46, §59–64, §74, §83.
4. `content/course.yml`: the official course card (verbatim axis titles; entry / learning / exit
   systems). Also look at the photos `..\1.jpeg` and `..\2.jpeg`.

## Rules
- Write only your module's files: `content/module_XX/`, `components/diagrams/mXX.py`,
  `components/labs/mXX.py`, `research/logs/mXX.md`. Never edit shared code or other modules.
  If shared code blocks you, say so in your final message.
- 4–6 lectures of 2,500–4,500 words each (Arabic, academic, professor's voice).
  Every lecture has at least one `:::exercise` with a model solution, `:::instructor` notes,
  a `:::deep` Technical Deep Dive where useful, tables, `[[diagram:…]]`, a `summary`,
  `builds_on`, `self_study` (with at least one verified video) and references.
- Sources: verify **before** citing. Use `python scripts/probe_sources.py file.txt`, which checks
  YouTube (oEmbed), arXiv (API), DOIs (Crossref) and URLs and prints the real
  title/authors/year. Use WebSearch/WebFetch for official product docs. Never invent a URL,
  DOI, author, date, statistic or product feature. Vendor facts come only from fetched official
  pages and carry `verified: "2026-09-26"`. Put anything unverifiable in `research/logs/mXX.md`
  under "To verify".
- Bidi: never glue «و» or «بـ» to a Latin word. Write «Russell و Norvig».
- Never write `<` inside CSS. Prefix lab widget keys with the lab name.
- `research/logs/mXX.md` sections: Research log (topic → sources → findings →
  disagreements → date), Source map, Topic gaps, Modern extensions, To verify.

## Self-check before finishing (fix everything except warnings about links to unwritten modules)
```
cd "C:\Users\HP\Documents\xtpmg\AI introduction\ai_intro_platform"
set PYTHONIOENCODING=utf-8
python scripts/validate_content.py --module N
python scripts/render_check.py --module N
python scripts/check_links.py --module N
```

## Final message
A short report: the files written, lecture titles, diagrams and labs, the reference count, the
three check results, and any shared-code issues.
