"""Content loading and parsing.

Course content lives in ``content/`` as YAML + Markdown so that lectures can be
edited without touching Python:

    content/course.yml                 course identity, objectives, outcomes
    content/module_XX/metadata.yml     module header, entry/exit systems
    content/module_XX/lecture_YY.md    front matter (YAML) + lecture body
    content/module_XX/quiz.yml         entry test ("entry") + module post-test ("questions")
    content/module_XX/references.yml   module bibliography (merged with data/references.yml)
    content/module_XX/glossary.yml     module glossary terms (merged with data/glossary.yml)
    data/references.yml                global bibliography (ids used everywhere)
    data/glossary.yml                  bilingual glossary
    data/assessments.yml               pre-test + post-test
    data/capstone.yml                  capstone tracks + rubrics

Lecture bodies use a small block syntax on top of Markdown:

    :::definition Title                educational card (see CARD_TYPES)
    body in Markdown
    :::

    :::check Question text             self-check; answer after a line "???"
    :::exercise Title                  the lesson exercise (required in every lecture); solution after "???"
    :::instructor Title                shown only in Instructor Mode
    :::deep Title                      Technical Deep Dive (collapsed expander)
    :::sticky-rose Title               sticky note (yellow, rose, lavender, peach)
    [[diagram:name]]                   registered diagram (components/diagrams/)
    [[widget:name]]                    registered interactive lab (components/labs/)
    [[link:m04-l01]]                   cross-link button to another lecture
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
DATA_DIR = ROOT / "data"

CARD_TYPES: dict[str, tuple[str, str]] = {
    # type: (Arabic label, English label)
    "definition": ("تعريف", "Definition"),
    "key": ("فكرة أساسية", "Key Idea"),
    "example": ("مثال", "Example"),
    "applied": ("مثال تطبيقي", "Applied Example"),
    "deep": ("تعمق تقني", "Technical Deep Dive"),
    "method": ("ملاحظة منهجية", "Methodological Note"),
    "instructor": ("ملاحظة للأستاذ", "Instructor Note"),
    "misconception": ("خطأ شائع", "Common Misconception"),
    "warning": ("تحذير", "Warning"),
    "didyouknow": ("هل تعلم؟", "Did You Know?"),
    "discussion": ("سؤال للنقاش", "Discussion Question"),
    "activity": ("نشاط صفي", "Classroom Activity"),
    "case": ("حالة دراسية", "Case Study"),
    "recap": ("ملخص المفهوم", "Concept Recap"),
    "check": ("اختبر نفسك", "Check Your Understanding"),
    "modern": ("امتداد حديث", "Modern Extension"),
    "verify": ("تحقق من المعلومة", "Verification Note"),
    "crosslink": ("ربط بالمحاضرات", "Cross-link"),
    "exercise": ("تمرين الدرس", "Lesson exercise"),
    "selfstudy": ("تعلم ذاتي", "Auto-apprentissage"),
}
STICKY_TYPES = {"sticky", "sticky-rose", "sticky-lavender", "sticky-peach"}

_BLOCK_START = re.compile(r"^:::([a-z\-]+)\s*(.*)$")
_TOKEN = re.compile(r"^\[\[(diagram|widget|link):([a-z0-9_\-]+)\]\]\s*$")


@dataclass
class Segment:
    kind: str  # "md" | "heading" | "block" | "diagram" | "widget" | "link"
    text: str = ""
    block_type: str = ""
    title: str = ""
    anchor: str = ""


@dataclass
class Lecture:
    id: str
    module: int
    number: int
    title: str
    subtitle: str
    meta: dict
    body: str
    path: Path
    segments: list[Segment] = field(default_factory=list)

    @property
    def headings(self) -> list[Segment]:
        return [s for s in self.segments if s.kind == "heading"]

    def blocks(self, block_type: str) -> list[Segment]:
        return [s for s in self.segments if s.kind == "block" and s.block_type == block_type]


@dataclass
class Module:
    number: int
    meta: dict
    lectures: list[Lecture]
    quiz: list[dict]          # post-test of the module (les post-tests)
    path: Path
    entry_quiz: list[dict] = field(default_factory=list)   # test d'entrée

    @property
    def id(self) -> str:
        return f"m{self.number:02d}"

    @property
    def title(self) -> str:
        return self.meta["title"]


def read_yaml(path: Path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def split_front_matter(raw: str) -> tuple[dict, str]:
    if raw.startswith("---"):
        _, fm, body = raw.split("---", 2)
        return yaml.safe_load(fm) or {}, body.lstrip("\n")
    return {}, raw


def parse_body(body: str, lecture_id: str = "") -> list[Segment]:
    """Split a lecture body into renderable segments."""
    segments: list[Segment] = []
    buf: list[str] = []
    heading_no = 0
    in_fence = False
    lines = body.splitlines()
    i = 0

    def flush():
        text = "\n".join(buf).strip("\n")
        if text.strip():
            segments.append(Segment("md", text=text))
        buf.clear()

    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            in_fence = not in_fence
            buf.append(line)
            i += 1
            continue
        if in_fence:
            buf.append(line)
            i += 1
            continue
        m = _BLOCK_START.match(line.strip())
        if m and m.group(1) != "":
            flush()
            btype, title = m.group(1), m.group(2).strip()
            inner: list[str] = []
            i += 1
            inner_fence = False
            while i < len(lines):
                cur = lines[i]
                if cur.strip().startswith("```"):
                    inner_fence = not inner_fence
                if not inner_fence and cur.strip() == ":::":
                    break
                inner.append(cur)
                i += 1
            segments.append(Segment("block", text="\n".join(inner).strip("\n"),
                                    block_type=btype, title=title))
            i += 1  # skip closing :::
            continue
        t = _TOKEN.match(line.strip())
        if t:
            flush()
            segments.append(Segment(t.group(1), text=t.group(2)))
            i += 1
            continue
        if line.startswith("## "):
            flush()
            heading_no += 1
            segments.append(Segment("heading", text=line[3:].strip(),
                                    anchor=f"{lecture_id}-s{heading_no}"))
            i += 1
            continue
        buf.append(line)
        i += 1
    flush()
    return segments


def _load_lecture(path: Path, module_no: int) -> Lecture:
    raw = path.read_text(encoding="utf-8")
    meta, body = split_front_matter(raw)
    lec = Lecture(
        id=meta["id"],
        module=module_no,
        number=int(meta["number"]),
        title=meta["title"],
        subtitle=meta.get("subtitle", ""),
        meta=meta,
        body=body,
        path=path,
    )
    lec.segments = parse_body(body, lec.id)
    return lec


@lru_cache(maxsize=1)
def load_course() -> dict:
    return read_yaml(CONTENT_DIR / "course.yml")


@lru_cache(maxsize=1)
def load_modules() -> tuple[Module, ...]:
    modules = []
    for mdir in sorted(CONTENT_DIR.glob("module_*")):
        if not (mdir / "metadata.yml").exists():
            continue
        meta = read_yaml(mdir / "metadata.yml")
        number = int(meta["module_number"])
        lectures = sorted(
            (_load_lecture(p, number) for p in mdir.glob("lecture_*.md")),
            key=lambda lec: lec.number,
        )
        quiz_path = mdir / "quiz.yml"
        qdata = read_yaml(quiz_path) if quiz_path.exists() else {}
        modules.append(Module(number, meta, lectures, qdata.get("questions") or [], mdir,
                              qdata.get("entry") or []))
    return tuple(sorted(modules, key=lambda m: m.number))


def get_module(number: int) -> Module:
    for m in load_modules():
        if m.number == number:
            return m
    raise KeyError(number)


def all_lectures() -> list[Lecture]:
    return [lec for m in load_modules() for lec in m.lectures]


def lecture_index() -> dict[str, Lecture]:
    return {lec.id: lec for lec in all_lectures()}


def _collect(filename: str, key: str) -> list[dict]:
    """Global data/<filename> first, then each content/module_XX/<filename>."""
    items: list[dict] = []
    sources = [DATA_DIR / filename, *sorted(CONTENT_DIR.glob(f"module_*/{filename}"))]
    for path in sources:
        if path.exists():
            items.extend((read_yaml(path) or {}).get(key) or [])
    return items


@lru_cache(maxsize=1)
def load_references() -> dict[str, dict]:
    """Bibliography keyed by id. Module files may reuse a global id only if identical."""
    refs: dict[str, dict] = {}
    for ref in _collect("references.yml", "references"):
        refs.setdefault(ref["id"], ref)
    return refs


@lru_cache(maxsize=1)
def load_glossary() -> list[dict]:
    terms, seen = [], set()
    for term in _collect("glossary.yml", "terms"):
        k = term["en"].strip().lower()
        if k not in seen:
            seen.add(k)
            terms.append(term)
    return sorted(terms, key=lambda t: t["en"].lower())


@lru_cache(maxsize=1)
def load_assessments() -> dict:
    return read_yaml(DATA_DIR / "assessments.yml")


@lru_cache(maxsize=1)
def load_capstone() -> dict:
    return read_yaml(DATA_DIR / "capstone.yml")


@lru_cache(maxsize=1)
def load_td_projects() -> dict:
    """The TD research-topic bank: 7 axes, 65 topics, each mapped to the modules that cover it."""
    return read_yaml(DATA_DIR / "td_projects.yml")


def format_reference(ref: dict) -> str:
    """APA-like one-line citation in Markdown (English metadata kept LTR)."""
    parts = [f"{ref['authors']} ({ref['year']}). *{ref['title']}*."]
    if ref.get("venue"):
        parts.append(f"{ref['venue']}.")
    if ref.get("doi"):
        parts.append(f"[doi:{ref['doi']}](https://doi.org/{ref['doi']})")
    elif ref.get("url"):
        parts.append(f"[{ref['url']}]({ref['url']})")
    if ref.get("verified"):
        parts.append(f"(تم التحقق: {ref['verified']})")
    return " ".join(parts)
