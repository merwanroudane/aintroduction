"""Verify every DOI, reference URL and self-study link in the course.

    python scripts/check_links.py            # all modules
    python scripts/check_links.py --module 4

DOIs are resolved through the Crossref API (publishers often answer 403 to scripts, which
says nothing about the DOI); YouTube links through YouTube's
oEmbed endpoint (a removed or invalid video returns 404 there, whereas the
watch page itself always answers 200). Results are appended to
research/link_check.md with the date, so the verification is documented.
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
import urllib.error
import urllib.parse
import urllib.request
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from utils.content import load_modules, load_references  # noqa: E402

UA = {"User-Agent": "Mozilla/5.0 (course link checker; academic use)"}


def _status(url: str, method: str = "HEAD", retries: int = 3) -> int:
    req = urllib.request.Request(url, headers=UA, method=method)
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status
    except urllib.error.HTTPError as e:
        if e.code == 429 and retries:          # Crossref throttles: back off and retry
            time.sleep(4)
            return _status(url, method, retries - 1)
        # Some servers (e.g. Google Support) answer 404/403 to HEAD but 200 to GET.
        if method == "HEAD" and e.code in (403, 404, 405, 400):
            return _status(url, "GET")
        return e.code
    except Exception:  # noqa: BLE001 — network errors are reported, not raised
        # A timeout or dropped connection says nothing about the link: some hosts (UNESCO,
        # for one) simply stall under load. Retry before calling it broken, otherwise the
        # report cries wolf and people stop reading it.
        if retries:
            time.sleep(3)
            return _status(url, method, retries - 1)
        return -1


def check(url: str) -> tuple[str, int]:
    if url.startswith("https://doi.org/"):
        # Resolve through the Crossref API: publishers (Science, ACM, OUP, OECD...) answer
        # 403 to non-browser clients, which says nothing about whether the DOI is valid.
        return url, _status("https://api.crossref.org/works/" + urllib.parse.quote(url[16:]), "GET")
    if "youtube.com/watch" in url or "youtu.be/" in url:
        o = "https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(url, safe="")
        return url, _status(o, "GET")
    return url, _status(url)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--module", type=int)
    args = ap.parse_args()
    targets: dict[str, str] = {}
    refs = load_references()
    used_refs = set()
    for m in load_modules():
        if args.module and m.number != args.module:
            continue
        for lec in m.lectures:
            for it in lec.meta.get("self_study", []):
                targets[it["url"]] = f"{lec.id} self_study: {it['title']}"
            for it in lec.meta.get("references", []):
                used_refs.add(it["id"] if isinstance(it, dict) else it)
        used_refs.update(m.meta.get("exit", {}).get("suggested_reading", []))
    # Some publishers answer 403 to any scripted request no matter the headers, so a live
    # page looks broken. Such a reference is marked bot_blocked in references.yml, and the
    # skip is only honoured when there is another way to stand behind it: a doi we can
    # resolve, or a browser_verified date recording that a human opened the page. Without
    # one of those the url is checked normally and the failure is real.
    skipped: list[str] = []
    unproven: list[str] = []
    for rid in sorted(used_refs if args.module else refs):
        ref = refs.get(rid)
        if not ref:
            continue
        if ref.get("doi"):
            targets["https://doi.org/" + ref["doi"]] = f"ref {rid} (doi)"
        if ref.get("url"):
            proof = ref.get("doi") or ref.get("browser_verified")
            if ref.get("bot_blocked") and proof:
                how = "doi" if ref.get("doi") else f"read in browser {ref['browser_verified']}"
                skipped.append(f"ref {rid} (url, bot_blocked; {how}) — {ref['url']}")
            else:
                if ref.get("bot_blocked"):
                    unproven.append(rid)
                targets[ref["url"]] = f"ref {rid} (url)"

    # A self-study item may point at the same bot-blocked page as a reference does. It is
    # the same URL and the same evidence, so skip it for the same reason instead of
    # reporting one live page as two failures.
    blocked_urls = {r["url"].rstrip("/") for r in refs.values()
                    if r.get("bot_blocked") and (r.get("doi") or r.get("browser_verified"))
                    and r.get("url")}
    for url in [u for u in targets if u.rstrip("/") in blocked_urls]:
        skipped.append(f"{targets.pop(url)} (bot_blocked, same page as a reference) — {url}")
    with ThreadPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(check, targets))
    bad = [(u, s) for u, s in results if not (200 <= s < 400)]
    for u, s in sorted(results, key=lambda r: targets[r[0]]):
        flag = "ok " if 200 <= s < 400 else "BAD"
        print(f"{flag} {s:>4}  {targets[u]}  {u}")
    today = dt.date.today().isoformat()
    log = ROOT / "research" / "link_check.md"
    with open(log, "a", encoding="utf-8") as fh:
        scope = f"module {args.module}" if args.module else "all"
        fh.write(f"\n## {today} — {scope}: {len(results)} links, {len(bad)} failing\n")
        for u, s in bad:
            fh.write(f"- {s} {targets[u]} — {u}\n")
    for s in skipped:
        print(f"skip   —  {s}")
    for rid in unproven:
        print(f"note   —  ref {rid} is marked bot_blocked but has neither a doi nor a "
              f"browser_verified date, so its url was checked anyway")
    print(f"\n{len(results)} links checked, {len(bad)} failing, {len(skipped)} skipped (bot_blocked)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
