#!/usr/bin/env python3
"""Keep only the newest N editions in data/issues.json (default 4) and drop the older ones.

Usage: python3 scripts/prune_issues.py [N]
"""
import json
import sys
from pathlib import Path

PATH = Path(__file__).resolve().parent.parent / "data/issues.json"


def main():
    keep = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    data = json.loads(PATH.read_text())
    issues = sorted(data["issues"], key=lambda i: i["date"], reverse=True)
    dropped = [i["id"] for i in issues[keep:]]
    data["issues"] = issues[:keep]
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
    print(f"mantidas {len(data['issues'])} edições" + (f"; removidas: {', '.join(dropped)}" if dropped else ""))


if __name__ == "__main__":
    main()
