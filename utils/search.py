"""Local, offline full-text search over lectures, glossary, references and case studies."""

from __future__ import annotations

import re
from dataclasses import dataclass

from utils.content import (
    CARD_TYPES,
    load_glossary,
    load_modules,
    load_references,
)

_DIACRITICS = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭـ]")
_MD = re.compile(r"[*_`#>|\[\]()]")


def normalize(text: str) -> str:
    """Normalise Arabic spelling variants and case so queries match loosely."""
    text = _DIACRITICS.sub("", text)
    text = re.sub("[إأآٱ]", "ا", text)
    text = text.replace("ى", "ي").replace("ة", "ه").replace("ؤ", "و").replace("ئ", "ي")
    return text.lower()


def strip_md(text: str) -> str:
    return re.sub(r"\s+", " ", _MD.sub(" ", text)).strip()


@dataclass
class Doc:
    kind: str          # lecture | section | glossary | reference | case
    title: str
    text: str
    module: int | None = None
    lecture_id: str | None = None
    anchor: str | None = None


def build_index() -> list[Doc]:
    docs: list[Doc] = []
    for m in load_modules():
        docs.append(Doc("module", f"المحور {m.number}: {m.title}",
                        strip_md(m.meta.get("description", "")), m.number))
        for lec in m.lectures:
            kw = " ".join(lec.meta.get("keywords", []))
            docs.append(Doc("lecture", f"المحاضرة {m.number}.{lec.number}: {lec.title}",
                            f"{lec.subtitle} {kw}", m.number, lec.id))
            current_title, current_anchor, buf = lec.title, None, []
            for seg in lec.segments:
                if seg.kind == "heading":
                    if buf:
                        docs.append(Doc("section", current_title, strip_md(" ".join(buf)),
                                        m.number, lec.id, current_anchor))
                    current_title, current_anchor, buf = seg.text, seg.anchor, []
                elif seg.kind == "md":
                    buf.append(seg.text)
                elif seg.kind == "block":
                    if seg.block_type == "case":
                        docs.append(Doc("case", seg.title, strip_md(seg.text), m.number, lec.id))
                    elif seg.block_type != "instructor":
                        label = CARD_TYPES.get(seg.block_type, ("", ""))[0]
                        buf.append(f"{label} {seg.title} {seg.text}")
            if buf:
                docs.append(Doc("section", current_title, strip_md(" ".join(buf)),
                                m.number, lec.id, current_anchor))
    for term in load_glossary():
        docs.append(Doc("glossary", f"{term['ar']} — {term['en']}",
                        f"{term.get('acronym', '')} {term['definition']}",
                        term.get("module"), term.get("lecture")))
    for ref in load_references().values():
        docs.append(Doc("reference", ref["title"],
                        f"{ref['authors']} {ref['year']} {ref.get('topic', '')} {ref.get('venue', '')}"))
    return docs


def search(query: str, docs: list[Doc], limit: int = 40) -> list[tuple[float, Doc, str]]:
    q = normalize(query.strip())
    terms = [t for t in re.split(r"\s+", q) if len(t) > 1]
    if not terms:
        return []
    results = []
    for d in docs:
        title_n, text_n = normalize(d.title), normalize(d.text)
        score = 0.0
        for t in terms:
            if t in title_n:
                score += 5
            hits = text_n.count(t)
            score += min(hits, 6)
        if q in title_n:
            score += 6
        if score and all(t in title_n or t in text_n for t in terms):
            score *= 1.5
        if score:
            results.append((score, d, _snippet(d.text, terms)))
    results.sort(key=lambda r: -r[0])
    return results[:limit]


def _snippet(text: str, terms: list[str], width: int = 180) -> str:
    norm = normalize(text)
    pos = min((norm.find(t) for t in terms if norm.find(t) >= 0), default=0)
    start = max(0, pos - width // 3)
    snippet = text[start:start + width]
    return ("… " if start else "") + snippet + (" …" if start + width < len(text) else "")
