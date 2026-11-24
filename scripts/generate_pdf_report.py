"""
Generates an IEEE/ACM-styled PDF Report from TECHNICAL_REPORT.md
using Headless Chrome.
"""

import os
import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
MD_PATH = ROOT_DIR / "TECHNICAL_REPORT.md"
HTML_PATH = ROOT_DIR / "TECHNICAL_REPORT.html"
PDF_PATH = ROOT_DIR / "TECHNICAL_REPORT.pdf"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Bharat AI-SoC 2026 Technical Report - CropShield AI</title>
  <style>
    @page {
      size: A4;
      margin: 20mm 15mm 20mm 15mm;
    }
    body {
      font-family: 'Helvetica Neue', Arial, sans-serif;
      color: #1e293b;
      line-height: 1.5;
      font-size: 10.5pt;
      margin: 0;
      padding: 0;
    }
    h1 {
      font-size: 20pt;
      font-weight: 900;
      color: #0f172a;
      border-bottom: 3px solid #059669;
      padding-bottom: 6px;
      margin-top: 0;
      margin-bottom: 4px;
    }
    h2 {
      font-size: 13pt;
      font-weight: 800;
      color: #059669;
      margin-top: 2px;
      margin-bottom: 12px;
    }
    h3 {
      font-size: 11.5pt;
      font-weight: 700;
      color: #0f172a;
      margin-top: 14px;
      margin-bottom: 6px;
      border-left: 3px solid #10b981;
      padding-left: 6px;
    }
    p, li {
      color: #334155;
      margin-bottom: 6px;
      text-align: justify;
    }
    .meta-box {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 10px 14px;
      font-size: 9.5pt;
      margin-bottom: 18px;
    }
    .meta-box strong {
      color: #0f172a;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 12px 0 16px 0;
      font-size: 9pt;
      page-break-inside: avoid;
    }
    th, td {
      border: 1px solid #cbd5e1;
      padding: 6px 8px;
      text-align: left;
    }
    th {
      background-color: #f1f5f9;
      font-weight: 700;
      color: #0f172a;
    }
    tr:nth-child(even) td {
      background-color: #f8fafc;
    }
    code, pre {
      font-family: 'Consolas', 'Courier New', monospace;
      font-size: 8.5pt;
    }
    pre {
      background: #0f172a;
      color: #38bdf8;
      padding: 10px 12px;
      border-radius: 6px;
      overflow-x: auto;
      white-space: pre-wrap;
      word-wrap: break-word;
      margin: 10px 0;
      page-break-inside: avoid;
    }
    blockquote {
      border-left: 3px solid #059669;
      background: #ecfdf5;
      margin: 10px 0;
      padding: 8px 12px;
      font-style: italic;
      color: #065f46;
    }
    hr {
      border: none;
      border-top: 1px solid #e2e8f0;
      margin: 16px 0;
    }
    .page-break {
      page-break-before: always;
    }
  </style>
</head>
<body>
  __BODY__
</body>
</html>
"""

def md_to_html(md_text: str) -> str:
    import re
    # Simple markdown parser for technical report
    lines = md_text.splitlines()
    html_lines = []
    in_table = False
    in_code = False
    code_block = []

    for line in lines:
        if line.startswith("```"):
            if in_code:
                in_code = False
                html_lines.append(f"<pre>{'<br>'.join(code_block)}</pre>")
                code_block = []
            else:
                in_code = True
            continue

        if in_code:
            code_block.append(line.replace("<", "&lt;").replace(">", "&gt;"))
            continue

        if line.startswith("|") and line.endswith("|"):
            if not in_table:
                in_table = True
                html_lines.append("<table>")
            
            # Skip separator line like | :--- | :--- |
            if re.match(r"^\|(\s*:?-+:?\s*\|)+$", line):
                continue

            cells = [c.strip() for c in line.strip("|").split("|")]
            tag = "th" if "Dataset" in line or "Metric" in line or "Hardware Parameter" in line or "Constraint" in line or "#" in line else "td"
            cell_html = "".join(f"<{tag}>{c}</{tag}>" for c in cells)
            html_lines.append(f"<tr>{cell_html}</tr>")
            continue
        elif in_table:
            in_table = False
            html_lines.append("</table>")

        if line.startswith("# "):
            html_lines.append(f"<h1>{line[2:].strip()}</h1>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{line[3:].strip()}</h2>")
        elif line.startswith("### "):
            html_lines.append(f"<h3>{line[4:].strip()}</h3>")
        elif line.startswith("- "):
            html_lines.append(f"<li>{line[2:].strip()}</li>")
        elif line.startswith("---"):
            html_lines.append("<hr>")
        elif line.strip():
            # Check bold formatting
            formatted = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", line)
            formatted = re.sub(r"\*(.*?)\*", r"<em>\1</em>", formatted)
            html_lines.append(f"<p>{formatted}</p>")

    if in_table:
        html_lines.append("</table>")

    return "\n".join(html_lines)


def main():
    print(f"Reading markdown from {MD_PATH}...")
    with open(MD_PATH, "r", encoding="utf-8") as f:
        md_content = f.read()

    body_html = md_to_html(md_content)
    full_html = HTML_TEMPLATE.replace("__BODY__", body_html)

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Saved intermediate HTML to {HTML_PATH}")

    if not os.path.exists(CHROME_PATH):
        print(f"Error: Chrome not found at {CHROME_PATH}")
        sys.exit(1)

    print("Compiling PDF with Headless Chrome...")
    cmd = [
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={PDF_PATH}",
        str(HTML_PATH)
    ]
    subprocess.run(cmd, check=True)

    if PDF_PATH.exists():
        size_kb = os.path.getsize(PDF_PATH) / 1024
        print(f"Successfully generated: {PDF_PATH} ({size_kb:.1f} KB)")
    else:
        print("Failed to generate PDF.")


if __name__ == "__main__":
    main()
