"""Generate SOURCES.md — the course-wide bibliography — from the references themselves.

    python scripts/build_sources.py            # write SOURCES.md
    python scripts/build_sources.py --check    # fail if SOURCES.md is out of date (CI)

Writing the bibliography by hand would guarantee drift: 192 entries live in fourteen
references.yml files and get edited module by module. This reads them and regenerates the
one list a reader or a reviewer actually wants.
"""

from __future__ import annotations

import argparse
import collections
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from utils.content import load_modules, load_references  # noqa: E402

OUT = ROOT / "SOURCES.md"

# Grouped and ordered so the list reads like a syllabus, not a dump.
TOPIC_ORDER = [
    ("AI Foundations", "أسس الذكاء الاصطناعي"),
    ("AI History", "تاريخ الذكاء الاصطناعي"),
    ("Machine Learning", "التعلّم الآلي"),
    ("Deep Learning", "التعلّم العميق"),
    ("LLMs", "النماذج اللغوية الكبيرة"),
    ("Prompt Engineering", "هندسة الأوامر"),
    ("Economics + AI", "الاقتصاد والذكاء الاصطناعي"),
    ("AI Ethics", "أخلاقيات الذكاء الاصطناعي"),
    ("Privacy", "الخصوصية"),
    ("Security", "الأمان"),
    ("AI Governance", "الحوكمة والتنظيم"),
    ("Human Oversight", "الرقابة البشرية"),
    ("AI Education", "الذكاء الاصطناعي والتعليم"),
    ("Official Product Documentation", "وثائق المنتجات الرسمية"),
]

TYPE_AR = {
    "article": "مقال محكّم", "preprint": "مسودة بحثية", "book": "كتاب",
    "standard": "معيار أو موقف رسمي", "documentation": "توثيق رسمي",
    "report": "تقرير", "law": "نص قانوني", "web": "صفحة ويب", "course": "مقرر",
}


def _link(ref: dict) -> str:
    if ref.get("doi"):
        return f"https://doi.org/{ref['doi']}"
    return ref.get("url", "")


def _entry(ref: dict, cited_by: list[int]) -> str:
    bits = [f"**{ref['authors']}** ({ref['year']}). *{ref['title']}*."]
    if ref.get("venue"):
        bits.append(f"{ref['venue']}.")
    line = " ".join(bits)
    url = _link(ref)
    if url:
        line += f" <{url}>"
    meta = [TYPE_AR.get(ref["type"], ref["type"])]
    if cited_by:
        nums = sorted(set(cited_by))
        label = "المحور" if len(nums) == 1 else "المحاور"
        meta.append(f"{label} " + "، ".join(str(n) for n in nums))
    meta.append(f"تُحقِّق منه في {ref['verified']}")
    line += f"  \n<sub>{' · '.join(meta)}</sub>"
    if ref.get("bot_blocked"):
        how = ("عبر معرّف DOI" if ref.get("doi")
               else f"بقراءة الصفحة في متصفح يوم {ref.get('browser_verified', '—')}")
        line += f"  \n<sub>⚠︎ الموقع يرفض الطلبات الآلية؛ تُحقِّق منه {how}.</sub>"
    return f"- {line}"


def build() -> str:
    refs = load_references()
    modules = load_modules()

    # Which modules cite each source.
    usage: dict[str, list[int]] = collections.defaultdict(list)
    for m in modules:
        for lec in m.lectures:
            for item in lec.meta.get("references") or []:
                usage[item["id"] if isinstance(item, dict) else item].append(m.number)
        for rid in m.meta.get("exit", {}).get("suggested_reading", []):
            usage[rid].append(m.number)

    by_topic: dict[str, list[dict]] = collections.defaultdict(list)
    for ref in refs.values():
        by_topic[ref["topic"]].append(ref)

    n_doi = sum(1 for r in refs.values() if r.get("doi"))
    n_url = sum(1 for r in refs.values() if r.get("url") and not r.get("doi"))
    types = collections.Counter(r["type"] for r in refs.values())

    out = [
        "# المصادر — Sources",
        "",
        "الببليوغرافيا الكاملة للمقرر. **هذا الملف مولَّد آليًا** من ملفات "
        "`references.yml`، فلا يُحرَّر يدويًا:",
        "",
        "```bash",
        "python scripts/build_sources.py",
        "```",
        "",
        "---",
        "",
        "## منهج التحقق",
        "",
        "لم يُذكر في هذا المقرر مصدر لم يُفحص قبل الاستشهاد به. وإجراء الفحص:",
        "",
        "| نوع المصدر | كيف تُحقِّق منه |",
        "|---|---|",
        "| مقال بمعرّف DOI | واجهة Crossref البرمجية، مع مقارنة العنوان والمجلة والسنة "
        "والمجلد والصفحات وقائمة المؤلفين بما في الملف |",
        "| مسودة على arXiv | واجهة arXiv البرمجية، مع مقارنة العنوان والمؤلفين وسنة الإيداع |",
        "| فيديو | واجهة oEmbed للتأكد من أن المقطع ما زال متاحًا |",
        "| توثيق أو معيار أو نص قانوني | جلب الصفحة وقراءتها، وتسجيل تاريخ القراءة |",
        "",
        "والمواقع التي ترفض الطلبات الآلية (403 لأي نص برمجي) موسومة بـ`bot_blocked` في "
        "`references.yml`. ولا يتخطّاها `scripts/check_links.py` إلا إذا حمل المصدر "
        "**دليلًا آخر**: معرّف DOI يمكن حلّه، أو تاريخ `browser_verified` يسجّل أن إنسانًا "
        "فتح الصفحة. وبغير ذلك يُفحص الرابط كغيره ويُعدّ فشله فشلًا حقيقيًا — حتى لا يختبئ "
        "رابط معطوب خلف الوسم.",
        "",
        "**لإعادة فحص كل الروابط:**",
        "",
        "```bash",
        "python scripts/check_links.py",
        "```",
        "",
        "## ما لا يدّعيه هذا المقرر",
        "",
        "الانضباط في التوثيق يشمل **الامتناع** عن الادعاء بقدر ما يشمل الإسناد. وسجلات "
        "`research/logs/mXX.md` تسجّل لكل محور ما فُحص وما وُجد وما امتنع المحور عن قوله. "
        "والقواعد العامة:",
        "",
        "- **لا أرقام دقة لأدوات كشف النصوص أو الصور المولَّدة** — تختلف بالأداة والإصدار "
        "ونوع المحتوى، وتتقادم فورًا. والمذكور هو الحدود **البنيوية** والنتيجة المعيارية.",
        "- **لا خلاصات قانونية في حقوق المصنفات** — الدعاوى منظورة وتختلف بين الأنظمة. "
        "والمذكور هو **الأسئلة التي تُطرح** والإحالة إلى النص الملزم وإلى المختص.",
        "- **لا ادعاءات عن قدرات جيل بعينه من النماذج** — وحين يُذكر حدّ تقني يُذكر معه "
        "**سببه البنيوي**، ويُقال صراحةً إنه يتحسن.",
        "- **لا ترتيب ولا تفضيل بين المنتجات** — المقارنة وظيفية، مبنية على وثائق رسمية "
        "مؤرَّخة، وتنبّه إلى أنها تتغير.",
        "",
        "---",
        "",
        "## إحصاء",
        "",
        f"- **{len(refs)}** مصدرًا: **{n_doi}** بمعرّف DOI، و**{n_url}** برابط مباشر.",
        "- بحسب النوع: "
        + "، ".join(f"{TYPE_AR.get(t, t)} ({n})" for t, n in types.most_common())
        + ".",
        "",
        "---",
        "",
    ]

    seen = set()
    for key, arabic in TOPIC_ORDER:
        items = by_topic.get(key, [])
        if not items:
            continue
        seen.add(key)
        out.append(f"## {arabic} — {key} ({len(items)})")
        out.append("")
        for ref in sorted(items, key=lambda r: (str(r["authors"]), str(r["year"]))):
            out.append(_entry(ref, usage.get(ref["id"], [])))
        out.append("")

    for key in sorted(set(by_topic) - seen):
        out.append(f"## {key} ({len(by_topic[key])})")
        out.append("")
        for ref in sorted(by_topic[key], key=lambda r: (str(r["authors"]), str(r["year"]))):
            out.append(_entry(ref, usage.get(ref["id"], [])))
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if SOURCES.md differs from what would be generated")
    args = ap.parse_args()

    text = build()
    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != text:
            print("SOURCES.md is out of date — run: python scripts/build_sources.py")
            return 1
        print("SOURCES.md is up to date.")
        return 0

    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(text.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
