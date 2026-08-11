#!/usr/bin/env python3
"""
Generate REAL evidence images for every finding:
  - code-evidence images: the actual source lines (Pygments), the buggy line highlighted,
    with a file:line caption bar — rendered to PNG via headless Chrome.
  - terminal images: the real console errors / live API responses, terminal-styled.

These are NOT mockups — every code image is read straight from the cloned project source,
and every terminal image is real captured output.

Usage: python3 scripts/make_evidence_images.py
Output: docs/evidence/*.png
"""
import html
import os
import subprocess
import tempfile

from pygments import highlight
from pygments.lexers import get_lexer_for_filename, get_lexer_by_name
from pygments.formatters import HtmlFormatter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "docs", "evidence")
os.makedirs(OUT, exist_ok=True)

APP = "/home/user/food-delivery-multivendor/enatega-multivendor-app"
WEB = "/home/user/food-delivery-multivendor/enatega-multivendor-web"
CHROME = "google-chrome"

# id, title, absolute file, start_line, end_line, [highlight lines], caption
CODE_FINDINGS = [
    ("WEB-1", "Apollo `connectToDevTools` deprecated",
     f"{WEB}/lib/hooks/useSetApollo.tsx", 213, 221, [218],
     "enatega-multivendor-web/lib/hooks/useSetApollo.tsx:218"),
    ("WEB-2", "useLazyQuery deprecated options (onCompleted/onError/variables)",
     f"{WEB}/lib/hooks/useLazyQueryQL.tsx", 33, 47, [35, 37, 38, 41],
     "enatega-multivendor-web/lib/hooks/useLazyQueryQL.tsx:35-41"),
    ("WEB-3", "next-intl webpack dynamic-import warning",
     f"{WEB}/next.config.mjs", 1, 6, [1],
     "enatega-multivendor-web/next.config.mjs:1"),
    ("MOB-1", "Login email regex rejects modern TLDs (.store/.info)",
     f"{APP}/src/screens/Login/useLogin.js", 76, 91, [80, 81],
     "enatega-multivendor-app/src/screens/Login/useLogin.js:80"),
    ("MOB-2", "Password eye icon inverted (showPassword=true + secureTextEntry)",
     f"{APP}/src/screens/Login/Login.js", 86, 90, [88, 89],
     "enatega-multivendor-app/src/screens/Login/Login.js:88-89 (+ useLogin.js:33)"),
    ("MOB-3", "Login controls have no testID / accessibilityLabel",
     f"{APP}/src/screens/Login/Login.js", 67, 90, [69, 88],
     "enatega-multivendor-app/src/screens/Login/Login.js:69,88,117"),
    ("MOB-4", "Demo password hard-coded in client",
     f"{APP}/src/screens/Login/useLogin.js", 60, 69, [63, 64],
     "enatega-multivendor-app/src/screens/Login/useLogin.js:63-64"),
    ("MOB-5", "Cart addQuantity has no upper cap",
     f"{APP}/src/context/User.js", 114, 121, [114, 117],
     "enatega-multivendor-app/src/context/User.js:114"),
    ("MOB-6", "deleteItem mutates cart state in place (splice)",
     f"{APP}/src/context/User.js", 123, 132, [126],
     "enatega-multivendor-app/src/context/User.js:126"),
    ("MOB-7", "Offer filters read flags the backend never sets",
     f"{APP}/src/screens/Menu/Menu.js", 678, 685, [680, 683],
     "enatega-multivendor-app/src/screens/Menu/Menu.js:680,683"),
]


def read_lines(path, start, end):
    with open(path, encoding="utf-8", errors="ignore") as fh:
        lines = fh.readlines()
    return "".join(lines[start - 1:end]), start


def render_html_to_png(html_str, png_path, width, height):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
        tf.write(html_str)
        html_path = tf.name
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
         f"--window-size={width},{height}", "--default-background-color=00000000",
         "--virtual-time-budget=4000", f"--screenshot={png_path}", f"file://{html_path}"],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    os.remove(html_path)


CODE_CSS = HtmlFormatter(style="monokai").get_style_defs(".highlight")


def code_image(fid, title, file, start, end, hl, caption):
    code, first = read_lines(file, start, end)
    ext = os.path.splitext(file)[1].lower()
    lexer_name = {".tsx": "tsx", ".ts": "typescript", ".jsx": "jsx",
                  ".js": "javascript", ".mjs": "javascript"}.get(ext, "text")
    try:
        lexer = get_lexer_by_name(lexer_name, stripnl=False)
    except Exception:
        lexer = get_lexer_by_name("javascript", stripnl=False)
    formatter = HtmlFormatter(style="monokai", linenos="table", linenostart=first,
                              hl_lines=[l - first + 1 for l in hl], cssclass="highlight")
    body = highlight(code, lexer, formatter)
    n = end - start + 1
    height = 150 + n * 21
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><style>
      body{{margin:0;background:#1e2127;font-family:'DejaVu Sans',Arial,sans-serif}}
      .win{{margin:14px;border-radius:10px;overflow:hidden;border:1px solid #333;
            box-shadow:0 8px 24px rgba(0,0,0,.4)}}
      .bar{{background:#2b2f3a;color:#e6e6e6;padding:9px 14px;font-size:13px;font-weight:bold;
            display:flex;align-items:center;gap:8px}}
      .dot{{width:11px;height:11px;border-radius:50%;display:inline-block}}
      .r{{background:#ff5f56}}.y{{background:#ffbd2e}}.g{{background:#27c93f}}
      .tag{{margin-left:auto;background:#e67e22;color:#fff;padding:2px 9px;border-radius:5px;font-size:11px}}
      .cap{{background:#161922;color:#8fd6ff;padding:6px 14px;font-family:monospace;font-size:12px}}
      .highlight{{margin:0;font-size:13px;line-height:1.55}}
      .highlight pre{{margin:0;padding:10px 6px}}
      .highlight .hll{{background:#4a3b12;display:block}}
      td.linenos{{color:#666;padding-right:10px;text-align:right;user-select:none}}
      {CODE_CSS}
    </style></head><body><div class="win">
      <div class="bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>
        {html.escape(fid)} — {html.escape(title)}<span class="tag">BUG</span></div>
      <div class="cap">📍 {html.escape(caption)}</div>
      {body}
    </div></body></html>"""
    png = os.path.join(OUT, f"{fid}-code.png")
    render_html_to_png(doc, png, 1080, height)
    print("  ✓", os.path.relpath(png, ROOT))


def terminal_image(name, title, text, subtitle=""):
    esc = html.escape(text)
    n = text.count("\n") + 1
    height = 150 + n * 19
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><style>
      body{{margin:0;background:#0d1117;font-family:'DejaVu Sans',Arial,sans-serif}}
      .win{{margin:14px;border-radius:10px;overflow:hidden;border:1px solid #30363d}}
      .bar{{background:#161b22;color:#e6e6e6;padding:9px 14px;font-size:13px;font-weight:bold;
            display:flex;gap:8px;align-items:center}}
      .dot{{width:11px;height:11px;border-radius:50%}}
      .r{{background:#ff5f56}}.y{{background:#ffbd2e}}.g{{background:#27c93f}}
      .tag{{margin-left:auto;background:#238636;color:#fff;padding:2px 9px;border-radius:5px;font-size:11px}}
      .sub{{background:#0d1117;color:#7d8590;padding:5px 14px;font-family:monospace;font-size:12px}}
      pre{{margin:0;padding:12px 14px;color:#c9d1d9;font-family:'DejaVu Sans Mono',monospace;
           font-size:12.5px;line-height:1.5;white-space:pre-wrap}}
      .err{{color:#ff7b72}}
    </style></head><body><div class="win">
      <div class="bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>
        {html.escape(title)}<span class="tag">LIVE</span></div>
      {f'<div class="sub">{html.escape(subtitle)}</div>' if subtitle else ''}
      <pre>{esc}</pre></div></body></html>"""
    png = os.path.join(OUT, f"{name}.png")
    render_html_to_png(doc, png, 1080, height)
    print("  ✓", os.path.relpath(png, ROOT))


if __name__ == "__main__":
    print("Code-evidence images (real source):")
    for f in CODE_FINDINGS:
        code_image(*f)

    print("Terminal images (real captured output):")
    console = os.path.join(ROOT, "01-manual-testing", "web-run-screenshots", "CONSOLE-ERRORS-live.txt")
    if os.path.exists(console):
        txt = open(console, encoding="utf-8").read()
        terminal_image("WEB-console-errors", "npm run dev — real console output (enatega-multivendor-web)",
                       txt, "http://localhost:3000  →  errors repeat on every render")
    print("done")
