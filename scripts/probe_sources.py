"""Probe candidate sources before citing them. One item per line in a text file:
    yt:<youtube url>   arxiv:<id>   doi:<doi>   url:<url>
Prints the real title/authors/year so the citation can be checked.

    python scripts/probe_sources.py candidates.txt
"""
import json
import re
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = {"User-Agent": "Mozilla/5.0 (academic course link checker)"}


def get(url, timeout=25):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", "replace"), r.geturl()


def probe(item):
    kind, val = item.split(":", 1)
    try:
        if kind == "yt":
            s, body, _ = get("https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(val, safe=""))
            d = json.loads(body)
            return f"OK  yt  {val} | {d['title']} | {d.get('author_name')}"
        if kind == "arxiv":
            s, body, _ = get(f"http://export.arxiv.org/api/query?id_list={val}")
            titles = re.findall(r"<title>(.*?)</title>", body, re.S)
            authors = re.findall(r"<name>(.*?)</name>", body)
            pub = re.findall(r"<published>(.*?)</published>", body)
            t = " ".join(titles[1].split()) if len(titles) > 1 else "??"
            return f"OK  arx {val} | {t} | {', '.join(authors[:3])} | {pub[0][:10] if pub else ''}"
        if kind == "doi":
            s, body, _ = get("https://api.crossref.org/works/" + urllib.parse.quote(val))
            m = json.loads(body)["message"]
            au = ", ".join(a.get("family", "") for a in m.get("author", [])[:3])
            yr = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
            return f"OK  doi {val} | {m.get('title', ['?'])[0]} | {au} | {yr} | {(m.get('container-title') or [''])[0]}"
        if kind == "url":
            s, body, final = get(val)
            t = re.search(r"<title[^>]*>(.*?)</title>", body, re.S | re.I)
            return f"OK  url {s} {val} | {(' '.join(t.group(1).split()) if t else '')[:110]}"
    except Exception as e:  # noqa: BLE001
        return f"BAD {kind} {val} | {type(e).__name__}: {str(e)[:80]}"


items = [ln.strip() for ln in open(sys.argv[1], encoding="utf-8") if ln.strip() and not ln.startswith("#")]
with ThreadPoolExecutor(max_workers=10) as ex:
    for line in ex.map(probe, items):
        print(line)
