"""Quote unquoted YAML scalars that contain ': ' (Arabic prose very often does).

Two distinct bugs are repaired, both caused by an unquoted ': ' inside a value:

1. `key: some text: more`  → YAML raises "mapping values are not allowed here" and the file
   fails to parse at all. Loud, so it gets fixed immediately.

2. `- some text: more` inside a list of plain strings → YAML silently parses the item as a
   **mapping** `{some text: more}` instead of a string. Nothing raises: validation passes,
   pages render, and then any code doing `", ".join(items)` crashes with
   "sequence item N: expected str instance, dict found". Silent, so it survives for a long
   time. Only the keys in STRING_LIST_KEYS are touched, so block mappings inside lists
   (`- type: reading` under `self_study:`) are left alone.

Usage:  python scripts/fix_yaml_colons.py [--check]
        --check reports without writing and exits 1 if anything would change.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Keys whose value is a single scalar.
KEYS = ("title", "title_en", "short_title", "subtitle", "description", "bridge", "prompt",
        "explanation", "why", "scenario", "definition", "text")

# Keys whose value is a list of PLAIN STRINGS. A '- ' item under one of these must be a
# string, so an unquoted ': ' in it is always a bug. Keys holding lists of mappings
# (references, self_study, objectives in metadata.yml, terms, entry/questions) are absent
# on purpose.
STRING_LIST_KEYS = {
    "summary", "objectives", "keywords", "prerequisites", "builds_on", "related",
    "competencies", "assessment_activities", "common_mistakes", "remediation",
    "suggested_reading", "diagnostic_questions", "prior_knowledge", "sequence", "timing",
    "discussion", "assessment_ideas", "extensions", "axes", "general_objectives",
    "options", "related_modules",
}

scalar_pat = re.compile(r"^(\s*(?:- )?(?:" + "|".join(KEYS) + r"):\s+)(?![\"'|>\[{])(.*: .*)$")
item_pat = re.compile(r"^(\s*- )(?![\"'|>\[{])(.*: .*)$")
key_only_pat = re.compile(r"^\s*([A-Za-z_][\w]*):\s*$")
key_val_pat = re.compile(r"^\s*[A-Za-z_][\w]*:\s+\S")
# `- id: m09-e02` opens a block MAPPING, not a string: the part before the colon is a bare
# YAML identifier. Arabic prose containing ': ' never looks like that, so this tells them apart.
mapping_item_pat = re.compile(r"^[A-Za-z_][\w.-]*$")

check_only = "--check" in sys.argv
fixed_files = 0
fixed_lines = 0

targets = (list((ROOT / "content").rglob("*.md")) + list((ROOT / "content").rglob("*.yml"))
           + list((ROOT / "data").glob("*.yml")))

for p in sorted(targets):
    lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
    out, changed, in_fm = [], [], p.suffix == ".yml"
    list_key = None          # most recent "key:" that opened a block
    for i, line in enumerate(lines):
        if p.suffix == ".md" and line.strip() == "---":
            in_fm = not in_fm if i == 0 or in_fm else in_fm
            out.append(line)
            continue
        if not in_fm:
            out.append(line)
            continue

        stripped = line.rstrip("\n")
        km = key_only_pat.match(stripped)
        if km:
            list_key = km.group(1)
        elif key_val_pat.match(stripped):
            list_key = None          # a key WITH a value closes the previous list block

        m = scalar_pat.match(stripped)
        if m and '"' not in m.group(2):
            out.append(f'{m.group(1)}"{m.group(2)}"\n')
            changed.append((i + 1, m.group(2)))
            continue

        if list_key in STRING_LIST_KEYS:
            m = item_pat.match(stripped)
            if m and '"' not in m.group(2):
                before = m.group(2).split(": ", 1)[0]
                if not mapping_item_pat.match(before):
                    out.append(f'{m.group(1)}"{m.group(2)}"\n')
                    changed.append((i + 1, m.group(2)))
                    continue
                list_key = None      # this list holds mappings, not strings

        out.append(line)

    if changed:
        fixed_files += 1
        fixed_lines += len(changed)
        print(f"{'would fix' if check_only else 'fixed'} {p.relative_to(ROOT)}")
        for ln, txt in changed:
            print(f"    line {ln}: {txt[:90]}")
        if not check_only:
            p.write_text("".join(out), encoding="utf-8")

verb = "would be fixed" if check_only else "fixed"
print(f"\n{fixed_lines} line(s) in {fixed_files} file(s) {verb}")
sys.exit(1 if (check_only and fixed_lines) else 0)
