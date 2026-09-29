"""Validate course content against CONTENT_GUIDE.md.

    python scripts/validate_content.py            # whole course (strict: all 13 modules)
    python scripts/validate_content.py --module 7 # one module; links to unwritten modules → warnings

Exit code 1 if any error is found.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from utils.content import (  # noqa: E402
    CARD_TYPES, STICKY_TYPES, load_assessments, load_capstone, load_glossary,
    load_modules, load_references,
)

PLACEHOLDERS = re.compile(
    r"\b(TODO|TBD|FIXME|lorem ipsum|coming soon|placeholder|add text here|sample lecture|to be completed)\b"
    r"|قريبًا سيتم|سيُضاف قريبًا|سيتم استكمال|يُستكمل لاحقًا|محتوى مؤقت|نص مؤقت",
    re.IGNORECASE,
)
LECTURE_ID = re.compile(r"^m\d{2}-l\d{2}$")
BLOOM = {"remember", "understand", "apply", "analyze", "evaluate", "create"}
QTYPES = {"mcq", "multi", "tf", "scenario"}
KNOWN_BLOCKS = set(CARD_TYPES) | STICKY_TYPES | {"ltr"}


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, where, msg):
        self.errors.append(f"[ERROR] {where}: {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"[warn]  {where}: {msg}")


def check_question(r: Report, where: str, q: dict, lecture_ids: set, strict_links: bool) -> None:
    for f in ("id", "type", "prompt"):
        if not q.get(f):
            r.err(where, f"question missing '{f}'")
            return
    if q["type"] not in QTYPES:
        r.err(where, f"{q['id']}: unknown type {q['type']}")
    if q.get("bloom") and q["bloom"] not in BLOOM:
        r.err(where, f"{q['id']}: unknown bloom level {q['bloom']}")
    if not q.get("explanation"):
        r.err(where, f"{q['id']}: missing explanation (feedback)")
    if q["type"] == "tf":
        if not isinstance(q.get("answer"), bool):
            r.err(where, f"{q['id']}: tf answer must be true/false")
    else:
        opts = q.get("options") or []
        if len(opts) < 2:
            r.err(where, f"{q['id']}: needs ≥ 2 options")
        ans = q.get("answer")
        idx = ans if isinstance(ans, list) else [ans]
        if not idx or not all(isinstance(i, int) and 0 <= i < len(opts) for i in idx):
            r.err(where, f"{q['id']}: answer index out of range")
        if q["type"] == "multi" and not isinstance(ans, list):
            r.err(where, f"{q['id']}: multi answer must be a list")
        for k in (q.get("why_wrong") or {}):
            if not (0 <= int(k) < len(opts)):
                r.err(where, f"{q['id']}: why_wrong index {k} out of range")
    rv = q.get("review")
    if rv and rv not in lecture_ids:
        (r.err if strict_links else r.warn)(where, f"{q['id']}: review → unknown lecture {rv}")


def validate(only: int | None) -> Report:
    from components import diagrams, labs

    r = Report()
    modules = load_modules()
    refs = load_references()
    diagram_names = set(diagrams.names())
    lab_names = {lab.name for lab in labs.all_labs()}
    lecture_ids = {lec.id for m in modules for lec in m.lectures}
    strict = only is None
    numbers = [m.number for m in modules]
    if strict and sorted(numbers) != list(range(1, 14)):
        r.err("course", f"expected modules 1–13, found {numbers}")
    seen_ids: dict[str, str] = {}

    for m in modules:
        if only is not None and m.number != only:
            continue
        where = f"module {m.number:02d}"
        meta = m.meta
        for f in ("title", "short_title", "title_en", "subtitle", "description", "objectives",
                  "entry", "exit", "instructor", "concept_diagram", "estimated_duration"):
            if not meta.get(f):
                r.err(where, f"metadata missing '{f}'")
        levels = {o.get("bloom") for o in meta.get("objectives", []) if isinstance(o, dict)}
        if len(levels) < 4:
            r.err(where, f"objectives cover {len(levels)} Bloom levels (need ≥ 4)")
        ex = meta.get("exit", {})
        for f in ("competencies", "assessment_activities", "common_mistakes", "remediation",
                  "suggested_reading", "bridge"):
            if not ex.get(f):
                r.err(where, f"exit missing '{f}'")
        for rid in ex.get("suggested_reading", []):
            if rid not in refs:
                r.err(where, f"suggested_reading → unknown reference {rid}")
        en = meta.get("entry", {})
        for f in ("prior_knowledge", "diagnostic_questions"):
            if not en.get(f):
                r.err(where, f"entry missing '{f}'")
        if meta.get("concept_diagram") and meta["concept_diagram"] not in diagram_names:
            r.err(where, f"concept_diagram '{meta['concept_diagram']}' is not registered")
        if len(m.lectures) < 3:
            r.err(where, f"only {len(m.lectures)} lectures (need ≥ 3)")
        if len(m.entry_quiz) < 4:
            r.err(where, f"entry test has {len(m.entry_quiz)} questions (need ≥ 4)")
        if len(m.quiz) < 8:
            r.err(where, f"post-test has {len(m.quiz)} questions (need ≥ 8)")
        for q in [*m.entry_quiz, *m.quiz]:
            check_question(r, f"{where}/quiz", q, lecture_ids, strict)
            if q.get("id") in seen_ids:
                r.err(where, f"duplicate question id {q['id']}")
            seen_ids[q.get("id")] = where
        qb = {q.get("bloom") for q in m.quiz}
        if len(qb - {None}) < 4:
            r.err(where, "post-test should cover ≥ 4 Bloom levels")

        for lec in m.lectures:
            lw = f"{where}/{lec.path.name}"
            lm = lec.meta
            if not LECTURE_ID.match(lec.id) or not lec.id.startswith(m.id):
                r.err(lw, f"bad lecture id {lec.id}")
            if lec.id in seen_ids:
                r.err(lw, f"duplicate id {lec.id}")
            seen_ids[lec.id] = lw
            for f in ("title", "title_en", "objectives", "summary", "references", "keywords",
                      "self_study", "builds_on", "duration"):
                if not lm.get(f):
                    r.err(lw, f"front matter missing '{f}'")
            # Depth is measured as a composite, because Arabic prose is markedly more
            # compact than English: raw word counts under-report an equivalent lecture.
            n_words = len(re.findall(r"\S+", lec.body))
            n_blocks = len([s for s in lec.segments if s.kind == "block"])
            n_tables = len([ln for ln in lec.body.splitlines() if ln.lstrip().startswith("|")])
            # A word count alone misreads this content twice over: Arabic is compact, and a
            # lecture carries much of its teaching in blocks and tables rather than prose.
            # So the shortfall is only reported when the lecture is ALSO light on structure —
            # otherwise padding it to reach 1800 words would make it worse, not better.
            if n_words < 1500:
                r.err(lw, f"body has only {n_words} words — too shallow for a 90-minute lecture (target 1800+)")
            elif n_words < 1800 and (n_blocks < 12 or n_tables < 10):
                r.warn(lw, f"body has {n_words} words with {n_blocks} teaching blocks and "
                           f"{n_tables} table rows — thin on both counts (target 1800+ words, "
                           f"or 12+ blocks and 10+ table rows)")
            if n_blocks < 8:
                r.err(lw, f"only {n_blocks} teaching blocks (cards/exercises/notes) — target 10+")
            if n_tables < 5:
                r.warn(lw, "no comparison table found (the spec asks for tables where they clarify)")
            if PLACEHOLDERS.search(lec.body) or PLACEHOLDERS.search(str(lm)):
                r.err(lw, f"placeholder text: {PLACEHOLDERS.search(lec.body + str(lm)).group(0)!r}")
            blocks = [s for s in lec.segments if s.kind == "block"]
            kinds = {b.block_type for b in blocks}
            if "exercise" not in kinds:
                r.err(lw, "no :::exercise block (the course card requires an exercise in every lesson)")
            for b in blocks:
                if b.block_type not in KNOWN_BLOCKS:
                    r.err(lw, f"unknown block type ':::{b.block_type}'")
                if b.block_type == "exercise" and "???" not in b.text:
                    r.err(lw, "exercise without model solution after '???'")
            if "instructor" not in kinds:
                r.err(lw, "no :::instructor note")
            if not lec.headings or len(lec.headings) < 3:
                r.err(lw, "fewer than 3 '## ' sections")
            for s in lec.segments:
                if s.kind == "diagram" and s.text not in diagram_names:
                    r.err(lw, f"diagram '{s.text}' not registered")
                if s.kind == "widget" and s.text not in lab_names:
                    r.err(lw, f"lab '{s.text}' not registered")
                if s.kind == "link" and s.text not in lecture_ids:
                    (r.err if strict else r.warn)(lw, f"link → unknown lecture {s.text}")
            for rid in lm.get("related", []) + [b for b in lm.get("builds_on", []) if LECTURE_ID.match(str(b))]:
                if rid not in lecture_ids:
                    (r.err if strict else r.warn)(lw, f"related/builds_on → unknown lecture {rid}")
            for item in lm.get("references", []):
                rid = item["id"] if isinstance(item, dict) else item
                if rid not in refs:
                    r.err(lw, f"reference '{rid}' not defined in any references.yml")
            for res in lm.get("self_study", []):
                if not str(res.get("url", "")).startswith("http"):
                    r.err(lw, f"self_study item without URL: {res.get('title')}")
                if not res.get("verified"):
                    r.err(lw, f"self_study item not marked verified: {res.get('title')}")

    for ref in refs.values():
        for f in ("id", "authors", "year", "title", "type", "topic"):
            if not ref.get(f):
                r.err(f"reference {ref.get('id')}", f"missing '{f}'")
        if not (ref.get("url") or ref.get("doi")):
            r.err(f"reference {ref['id']}", "needs url or doi")
    for t in load_glossary():
        for f in ("ar", "en", "definition", "module"):
            if not t.get(f):
                r.err(f"glossary {t.get('en')}", f"missing '{f}'")

    if strict:
        a = load_assessments()
        if not 15 <= len(a["pretest"]["questions"]) <= 25:
            r.err("assessments", "pre-test should have 15–20 questions")
        if not 30 <= len(a["posttest"]["questions"]) <= 45:
            r.err("assessments", "post-test should have 30–40 questions")
        for q in a["pretest"]["questions"] + a["posttest"]["questions"]:
            check_question(r, "assessments", q, lecture_ids, True)
        tracks = load_capstone()["tracks"]
        if len(tracks) < 6:
            r.err("capstone", "expected 6 tracks (A–F)")
    return r


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--module", type=int)
    args = ap.parse_args()
    r = validate(args.module)
    for line in r.warnings + r.errors:
        print(line)
    print(f"\n{len(r.errors)} error(s), {len(r.warnings)} warning(s)")
    return 1 if r.errors else 0


if __name__ == "__main__":
    sys.exit(main())
