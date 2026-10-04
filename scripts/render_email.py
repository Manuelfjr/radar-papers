#!/usr/bin/env python3
"""Render one edition of data/issues.json as an email (HTML + plain text).

Usage: python3 scripts/render_email.py [issue-id]   (default: newest edition)
Writes out/email.html, out/email.txt and prints the subject line.
Email-safe: table layout, inline styles only, no external CSS or scripts.
"""
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://manuelfjr.github.io/radar-papers/"
MONTHS = ["jan.", "fev.", "mar.", "abr.", "mai.", "jun.", "jul.", "ago.", "set.", "out.", "nov.", "dez."]
SECTIONS = [
    ("irt", "IRT e psicometria para ML", "#1E7A55", "#E2F3EA"),
    ("avaliacao", "Avaliação de LLMs", "#A86A00", "#FBF1DC"),
    ("llm", "LLMs: vale conhecer", "#7A3FC4", "#F0E8FB"),
]
INK, MUTED, LINE, BG, SURFACE, ACCENT = "#141A26", "#5B6578", "#DDE2EA", "#F2F4F7", "#FFFFFF", "#1F4FD1"
SERIF = "Georgia,'Times New Roman',serif"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "'SF Mono',Menlo,Consolas,monospace"

e = lambda s: html.escape(str(s or ""))


def fmt_date(iso):
    y, m, d = map(int, iso.split("-"))
    return f"{d} {MONTHS[m - 1]} {y}"


def dots(n, on, off):
    return "".join(
        f'<span style="display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:3px;background:{on if i < n else off}"></span>'
        for i in range(5)
    )


def tags(p, color, border):
    return " ".join(
        f'<span style="display:inline-block;font:500 11px {MONO};color:{color};border:1px solid {border};border-radius:999px;padding:1px 8px;margin:0 4px 4px 0">{e(t)}</span>'
        for t in p.get("tags", [])
    )


def featured(p):
    return f"""
<tr><td style="padding:0 0 28px">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{INK};border-radius:14px">
  <tr><td style="padding:26px 26px 22px">
    <div style="font:600 11px {SANS};letter-spacing:.14em;text-transform:uppercase;color:#9DB4FF">Destaque da semana</div>
    <a href="{e(p['url'])}" style="display:block;margin:10px 0 6px;font:600 24px/1.25 {SERIF};color:#FFFFFF;text-decoration:none">{e(p['title'])}</a>
    <div style="font:13px/1.5 {SANS};color:#AAB3C4">{e(', '.join(p.get('authors', [])))}</div>
    <p style="margin:14px 0 0;font:15px/1.6 {SANS};color:#E8ECF3">{e(p['tldr'])}</p>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:14px"><tr>
      <td style="border-left:3px solid #FFFFFF;background:#232B3B;border-radius:0 8px 8px 0;padding:10px 14px;font:14px/1.55 {SANS};color:#E8ECF3"><b style="color:#FFFFFF">Por que importa:</b> {e(p['why'])}</td>
    </tr></table>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:16px"><tr>
      <td style="vertical-align:middle">{tags(p, '#C9D1DF', '#3A4458')}</td>
      <td align="right" style="vertical-align:middle;white-space:nowrap;font:12px {SANS};color:#AAB3C4">
        {dots(p.get('novelty', 0), '#FFFFFF', '#3A4458')}&nbsp;
        <a href="{e(p['url'])}" style="display:inline-block;margin-left:8px;background:#FFFFFF;color:{INK};font:600 13px {SANS};text-decoration:none;border-radius:999px;padding:7px 14px">Ler no arXiv →</a>
      </td>
    </tr></table>
  </td></tr></table>
</td></tr>"""


def card(p, color, soft):
    pdf = f' &nbsp;·&nbsp; <a href="{e(p["pdf"])}" style="color:{ACCENT};text-decoration:none">PDF</a>' if p.get("pdf") else ""
    return f"""
<tr><td style="padding:0 0 14px">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{SURFACE};border:1px solid {LINE};border-radius:12px">
  <tr><td style="padding:18px 20px">
    <a href="{e(p['url'])}" style="display:block;font:600 18px/1.3 {SERIF};color:{INK};text-decoration:none">{e(p['title'])}</a>
    <div style="margin-top:4px;font:13px/1.5 {SANS};color:{MUTED}">{e(', '.join(p.get('authors', [])))}</div>
    <p style="margin:10px 0 0;font:15px/1.6 {SANS};color:{INK}">{e(p['tldr'])}</p>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:10px"><tr>
      <td style="border-left:3px solid {color};background:{soft};border-radius:0 8px 8px 0;padding:9px 13px;font:14px/1.55 {SANS};color:{INK}"><b style="color:{color}">Por que importa:</b> {e(p['why'])}</td>
    </tr></table>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:12px"><tr>
      <td style="vertical-align:middle">{tags(p, MUTED, LINE)}</td>
      <td align="right" style="vertical-align:middle;white-space:nowrap;font:12px {SANS};color:{MUTED}">
        {dots(p.get('novelty', 0), color, LINE)}&nbsp;
        <a href="{e(p['url'])}" style="color:{ACCENT};font-weight:600;text-decoration:none">arXiv →</a>{pdf}
      </td>
    </tr></table>
  </td></tr></table>
</td></tr>"""


def section(key, label, color, soft, papers):
    ps = [p for p in papers if p.get("section") == key]
    if not ps:
        return ""
    head = f"""
<tr><td style="padding:6px 0 12px;font:700 12px {SANS};letter-spacing:.1em;text-transform:uppercase;color:{MUTED}">
  <span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:{color};margin-right:8px;vertical-align:1px"></span>{e(label)}
</td></tr>"""
    return head + "".join(card(p, color, soft) for p in ps)


def render(issue):
    papers = issue["papers"]
    feat = next((p for p in papers if p.get("section") == "destaque"), None)
    link = f"{SITE}#/{issue['id']}"
    body = (featured(feat) if feat else "") + "".join(section(k, l, c, s, papers) for k, l, c, s in SECTIONS)
    preheader = feat["title"] if feat else issue["intro"]
    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light"><title>Leituras θ nº {issue['number']}</title></head>
<body style="margin:0;padding:0;background:{BG}">
<div style="display:none;max-height:0;overflow:hidden;opacity:0">{e(preheader)}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{BG}"><tr><td align="center" style="padding:28px 14px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:640px">
  <tr><td style="padding:0 0 18px">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
      <td style="font:700 26px/1 {SANS};letter-spacing:-.02em;color:{INK}"><span style="color:{ACCENT}">θ</span> Leituras θ</td>
      <td align="right" style="font:12px {MONO};color:{MUTED}">nº {issue['number']:02d} · {fmt_date(issue['date'])}</td>
    </tr></table>
  </td></tr>
  <tr><td style="border-top:3px solid {INK};padding:16px 0 26px">
    <div style="font:500 19px/1.45 {SERIF};color:{INK}">{e(issue['intro'])}</div>
    <div style="margin-top:8px;font:13px {SANS};color:{MUTED}">{len(papers)} papers selecionados · <a href="{link}" style="color:{ACCENT};text-decoration:none">ver no site →</a></div>
  </td></tr>
  {body}
  <tr><td align="center" style="padding:14px 0 6px">
    <a href="{link}" style="display:inline-block;background:{INK};color:#FFFFFF;font:600 14px {SANS};text-decoration:none;border-radius:999px;padding:11px 22px">Abrir a edição no site</a>
  </td></tr>
  <tr><td align="center" style="padding:18px 0 0;font:12px/1.6 {SANS};color:{MUTED}">
    Curadoria semanal feita por Claude a partir do arXiv. Os pontos indicam o grau de novidade (1 a 5).<br>
    <a href="{SITE}" style="color:{MUTED}">Todas as edições</a> · <a href="https://manuelfjr.github.io/radar-conferencias/" style="color:{MUTED}">Radar θ de Conferências</a>
  </td></tr>
</table></td></tr></table>
</body></html>"""


def render_text(issue):
    out = [f"Leituras θ nº {issue['number']} · {fmt_date(issue['date'])}", "", issue["intro"], ""]
    order = [("destaque", "DESTAQUE DA SEMANA")] + [(k, l.upper()) for k, l, _, _ in SECTIONS]
    for key, label in order:
        ps = [p for p in issue["papers"] if p.get("section") == key]
        if not ps:
            continue
        out += [label, ""]
        for p in ps:
            out += [p["title"], ", ".join(p.get("authors", [])), p["tldr"], "Por que importa: " + p["why"], p["url"], ""]
    out.append(f"Edição no site: {SITE}#/{issue['id']}")
    return "\n".join(out)


def main():
    issues = json.loads((ROOT / "data/issues.json").read_text())["issues"]
    issues.sort(key=lambda i: i["date"], reverse=True)
    issue = next(i for i in issues if i["id"] == sys.argv[1]) if len(sys.argv) > 1 else issues[0]
    out = ROOT / "out"
    out.mkdir(exist_ok=True)
    (out / "email.html").write_text(render(issue))
    (out / "email.txt").write_text(render_text(issue))
    feat = next((p for p in issue["papers"] if p.get("section") == "destaque"), None)
    hook = f": {feat['title']}" if feat else ""
    print(f"Leituras θ nº {issue['number']}{hook}")


if __name__ == "__main__":
    main()
