#!/usr/bin/env python3
"""List recent arXiv candidates for the weekly digest (last N days, default 8).

Usage: python3 scripts/arxiv_candidates.py [days]
Prints one line per unique paper: id | date | categories | title.
If export.arxiv.org is unreachable from this environment, use WebFetch on the same URLs instead.
"""
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

QUERIES = [
    'all:"item response theory"',
    'all:psychometric AND (all:"language model" OR all:"machine learning")',
    'all:"adaptive testing"',
    'all:"cultural consensus"',
    'all:"annotator disagreement"',
    'all:benchmark AND all:"language models" AND all:evaluation',
    'all:"LLM-as-a-judge"',
    'all:contamination AND all:benchmark',
    'all:"efficient evaluation" AND all:"language models"',
]
NS = {"a": "http://www.w3.org/2005/Atom"}


def fetch(q):
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": q, "sortBy": "submittedDate", "sortOrder": "descending", "max_results": 50}
    )
    with urllib.request.urlopen(url, timeout=30) as r:
        return ET.fromstring(r.read())


def main():
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    seen = {}
    for q in QUERIES:
        try:
            feed = fetch(q)
        except Exception as exc:
            print(f"# falhou: {q}: {exc}", file=sys.stderr)
            continue
        for entry in feed.findall("a:entry", NS):
            pub = datetime.fromisoformat(entry.find("a:published", NS).text.replace("Z", "+00:00"))
            if pub < cutoff:
                continue
            aid = entry.find("a:id", NS).text.rsplit("/", 1)[-1].split("v")[0]
            cats = ",".join(c.get("term") for c in entry.findall("a:category", NS))[:40]
            title = " ".join(entry.find("a:title", NS).text.split())
            seen.setdefault(aid, f"{aid} | {pub:%Y-%m-%d} | {cats} | {title}")
        time.sleep(3)  # arXiv API etiquette
    print("\n".join(sorted(seen.values(), reverse=True)))


if __name__ == "__main__":
    main()
