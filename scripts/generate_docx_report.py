"""
Generates a styled Microsoft Word document (.docx) from TECHNICAL_REPORT.md.
"""

import os
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

ROOT_DIR = Path(__file__).parent.parent
MD_PATH = ROOT_DIR / "TECHNICAL_REPORT.md"
DOCX_PATH = ROOT_DIR / "TECHNICAL_REPORT.docx"


def build_docx():
    doc = Document()

    # Page Margins (0.75 in)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    with open(MD_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_table = False
    table_lines = []

    for line in lines:
        stripped = line.strip()

        # Handle Tables
        if stripped.startswith("|") and stripped.endswith("|"):
            if "---" in stripped:
                continue
            table_lines.append([c.strip() for c in stripped.strip("|").split("|")])
            continue
        elif table_lines:
            # Create Table in Word with max columns across rows
            max_cols = max(len(row) for row in table_lines)
            table = doc.add_table(rows=len(table_lines), cols=max_cols)
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            table.style = 'Table Grid'

            for r_idx, row in enumerate(table_lines):
                for c_idx in range(max_cols):
                    cell = table.cell(r_idx, c_idx)
                    cell.text = row[c_idx] if c_idx < len(row) else ""
                    # Header styling
                    if r_idx == 0:
                        for p in cell.paragraphs:
                            for run in p.runs:
                                run.bold = True
                                run.font.size = Pt(9.5)
                    else:
                        for p in cell.paragraphs:
                            for run in p.runs:
                                run.font.size = Pt(9)
            doc.add_paragraph()  # Spacing
            table_lines = []

        if stripped.startswith("# "):
            p = doc.add_heading(stripped[2:], level=1)
            p.runs[0].font.color.rgb = RGBColor(15, 23, 42)
        elif stripped.startswith("## "):
            p = doc.add_heading(stripped[3:], level=2)
            p.runs[0].font.color.rgb = RGBColor(5, 150, 105)
        elif stripped.startswith("### "):
            p = doc.add_heading(stripped[4:], level=3)
            p.runs[0].font.color.rgb = RGBColor(30, 41, 59)
        elif stripped.startswith("- "):
            p = doc.add_paragraph(stripped[2:], style='List Bullet')
            p.paragraph_format.space_after = Pt(2)
        elif stripped.startswith("```"):
            continue
        elif stripped.startswith("---"):
            continue
        elif stripped:
            p = doc.add_paragraph(stripped)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15

    doc.save(DOCX_PATH)
    print(f"Successfully generated: {DOCX_PATH}")


if __name__ == "__main__":
    build_docx()
