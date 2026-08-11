#!/usr/bin/env python3
"""
Render the Markdown deliverables to colour-coded PDFs.

- Markdown -> HTML (tables, fenced code, toc)
- Severity / Priority / test-type cells are tinted by keyword so the PDF tables are
  genuinely COLOUR-CODED (not just black & white).
- Relative screenshots are embedded via a <base href> so images appear in the PDF.
- Chrome headless prints the HTML to PDF.

Usage: python3 scripts/build_pdfs.py
"""
import os
import re
import subprocess
import sys

import markdown

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "docs", "pdf")
os.makedirs(OUT, exist_ok=True)

# md file -> output pdf name
JOBS = [
    ("01-manual-testing/bug-reports.md", "bug-reports.pdf"),
    ("01-manual-testing/test-cases.md", "test-cases.pdf"),
    ("03-api-testing/api-testing.md", "api-testing.pdf"),
    ("04-answers/answers.md", "answers.pdf"),
    ("BUG-LOCATION-MAP.md", "BUG-LOCATION-MAP.pdf"),
    ("REPRODUCE-AND-SCREENSHOT-GUIDE.md", "REPRODUCE-AND-SCREENSHOT-GUIDE.pdf"),
    ("README.md", "README.pdf"),
]

# keyword -> (background, text colour)
CELL_COLORS = {
    r"\bCritical\b": ("#f8d0d0", "#7a0000"),
    r"🔴|\bMajor\b|\bHigh\b": ("#ffe0c2", "#8a3b00"),
    r"🟠": ("#ffe0c2", "#8a3b00"),
    r"🟡|\bMinor\b|\bMedium\b": ("#fff3c4", "#7a5b00"),
    r"⚪|\bTrivial\b|\bLow\b": ("#e6e8ea", "#41484d"),
    r"✅|\bPositive\b": ("#d9f2d9", "#0f5c2e"),
    r"⛔|\bNegative\b": ("#fbdcdc", "#7a0000"),
    r"🔶|\bEdge\b": ("#dce8fb", "#123a7a"),
}

CSS = """
<style>
  @page { size: A4; margin: 16mm 14mm; }
  * { box-sizing: border-box; }
  body { font-family: 'DejaVu Sans','Noto Sans','Liberation Sans',Arial,sans-serif;
         color:#212529; font-size:12px; line-height:1.5; }
  h1 { color:#2f7d1a; border-bottom:3px solid #5ec12f; padding-bottom:6px; font-size:22px; }
  h2 { color:#1f5c12; margin-top:26px; font-size:16px;
       border-left:5px solid #5ec12f; padding-left:8px; }
  h3 { color:#333; font-size:13px; }
  code, pre { font-family:'DejaVu Sans Mono',monospace; background:#f4f6f8;
              border-radius:4px; }
  code { padding:1px 4px; font-size:11px; }
  pre { padding:10px; overflow:auto; border:1px solid #e2e6ea; }
  pre code { background:none; padding:0; }
  table { border-collapse:collapse; width:100%; margin:12px 0; font-size:11px; }
  th, td { border:1px solid #cfd6dc; padding:6px 8px; text-align:left;
           vertical-align:top; }
  th { background:#2f7d1a; color:#fff; font-weight:bold; }
  tr:nth-child(even) td { background:#f7faf6; }
  img { max-width:100%; border:1px solid #e2e6ea; border-radius:6px; margin:8px 0; }
  blockquote { border-left:4px solid #ffce54; background:#fffdf3; margin:10px 0;
               padding:6px 12px; color:#5a4b00; }
  a { color:#2f7d1a; text-decoration:none; }
  hr { border:0; border-top:1px solid #e2e6ea; margin:18px 0; }
</style>
"""


def colorize_cells(html):
    """Tint <td> cells whose text matches a severity/priority/type keyword."""
    def repl(m):
        attrs, inner = m.group(1), m.group(2)
        if "style=" in attrs:  # header or already-styled
            return m.group(0)
        for pattern, (bg, fg) in CELL_COLORS.items():
            if re.search(pattern, inner):
                return f'<td{attrs} style="background:{bg};color:{fg};font-weight:600">{inner}</td>'
        return m.group(0)

    return re.sub(r"<td([^>]*)>(.*?)</td>", repl, html, flags=re.DOTALL)


def build(md_rel, pdf_name):
    md_path = os.path.join(ROOT, md_rel)
    base_dir = os.path.dirname(md_path)
    with open(md_path, encoding="utf-8") as fh:
        text = fh.read()

    body = markdown.markdown(
        text, extensions=["tables", "fenced_code", "sane_lists", "attr_list"]
    )
    body = colorize_cells(body)

    html = (
        f'<!doctype html><html><head><meta charset="utf-8">'
        f'<base href="file://{base_dir}/">{CSS}</head><body>{body}</body></html>'
    )
    html_path = os.path.join(OUT, pdf_name.replace(".pdf", ".html"))
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(html)

    pdf_path = os.path.join(OUT, pdf_name)
    subprocess.run(
        [
            "google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox",
            "--no-pdf-header-footer", "--virtual-time-budget=6000",
            f"--print-to-pdf={pdf_path}", f"file://{html_path}",
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    os.remove(html_path)  # keep only the PDF
    print(f"  ✓ {pdf_name}  ({os.path.getsize(pdf_path)//1024} KB)")


if __name__ == "__main__":
    print("Building PDFs ->", os.path.relpath(OUT, ROOT))
    for md_rel, pdf_name in JOBS:
        if os.path.exists(os.path.join(ROOT, md_rel)):
            build(md_rel, pdf_name)
        else:
            print(f"  (skip, not found: {md_rel})", file=sys.stderr)
    print("done")
