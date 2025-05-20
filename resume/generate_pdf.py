# job-dashboard/resume/generate_pdf.py

import pandas as pd
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import csv

# Layout constants
LEFT_MARGIN = 50
TOP_MARGIN = 50
LINE_HEIGHT = 13.5
PAGE_WIDTH, PAGE_HEIGHT = LETTER

# Font settings
HEADER_FONT = ("Helvetica-Bold", 12)
SUBHEADER_FONT = ("Helvetica-Bold", 10)
NORMAL_FONT = ("Helvetica", 8)
ITALIC_FONT = ("Helvetica-Oblique", 8)

def check_page_break(c, y_position):
    if y_position < LINE_HEIGHT * 2:
        c.showPage()
        c.setFont(*NORMAL_FONT)
        return PAGE_HEIGHT - TOP_MARGIN
    return y_position

def draw_text_with_bold(c, text, x, y, width):
    lines = simpleSplit(text, NORMAL_FONT[0], NORMAL_FONT[1], width - LEFT_MARGIN*2)
    for line in lines:
        x_pos = LEFT_MARGIN
        segments = line.split('**')
        bold = False
        for segment in segments:
            font = ("Helvetica-Bold", NORMAL_FONT[1]) if bold else NORMAL_FONT
            c.setFont(*font)
            c.drawString(x_pos, y, segment)
            seg_width = c.stringWidth(segment, font[0], font[1])
            x_pos += seg_width
            bold = not bold
        y -= LINE_HEIGHT
        y = check_page_break(c, y)
    return y

def create_ats_resume_pdf(csv_path, output_path):
    try:
        df = pd.read_csv(csv_path, sep=',', engine='python', quoting=csv.QUOTE_MINIMAL)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    section_order = [
        "personal_info",
        "professional_summary",
        "technical_skills",
        "professional_experience",
        "education",
        "certifications",
        "projects"
    ]

    try:
        name = df.loc[(df["section"] == "personal_info") & (df["subsection"] == "name"), "content"].values[0]
        target_roles = df.loc[(df["section"] == "personal_info") & (df["subsection"] == "target_roles"), "content"].values[0]
    except IndexError:
        print("Required personal_info fields (name/target_roles) are missing in the CSV.")
        return

    personal_info = df[(df["section"] == "personal_info") & 
                       (~df["subsection"].isin(["name", "target_roles"]))]
    personal_info_string = " | ".join(personal_info["content"].dropna().astype(str).tolist())

    portfolio = df.loc[(df["section"] == "personal_info") & (df["subsection"] == "portfolio"), "content"].values
    portfolio_link = portfolio[0] if len(portfolio) > 0 else None

    c = canvas.Canvas(output_path, pagesize=LETTER)
    y = PAGE_HEIGHT - TOP_MARGIN

    c.setFont(*HEADER_FONT)
    c.drawString(LEFT_MARGIN, y, name)
    y -= LINE_HEIGHT
    y = check_page_break(c, y)

    c.setFont(*NORMAL_FONT)
    c.drawString(LEFT_MARGIN, y, personal_info_string)
    y -= LINE_HEIGHT
    y = check_page_break(c, y)

    c.setFont(*ITALIC_FONT)
    c.drawString(LEFT_MARGIN, y, target_roles)
    y -= int(LINE_HEIGHT * 1.25)
    y = check_page_break(c, y)

    for section in section_order:
        if section == "personal_info":
            continue

        group = df[df["section"] == section]
        if group.empty:
            continue

        c.setFont(*SUBHEADER_FONT)
        section_title = section.replace("_", " ").title()
        c.drawString(LEFT_MARGIN, y, section_title)
        y -= 8
        c.line(LEFT_MARGIN, y, PAGE_WIDTH - LEFT_MARGIN, y)
        y -= int(LINE_HEIGHT * 1.1)
        y = check_page_break(c, y)

        if section == "technical_skills":
            skill_lines = []
            for _, row in group.iterrows():
                content = str(row.get("content", "")).strip()
                if content:
                    skill_lines.append(content)

            for line in skill_lines:
                y = draw_text_with_bold(c, line, LEFT_MARGIN, y, PAGE_WIDTH)
                y -= 3
                y = check_page_break(c, y)
        else:
            for _, row in group.iterrows():
                text = str(row.get("content", "")).strip()
                y = draw_text_with_bold(c, text, LEFT_MARGIN, y, PAGE_WIDTH)
                y -= 3
                y = check_page_break(c, y)

        y -= 8
        y = check_page_break(c, y)

    if portfolio_link:
        y = LINE_HEIGHT * 2
        c.setFont(*ITALIC_FONT)
        c.drawString(LEFT_MARGIN, y, f"Self-designed Portfolio: https://{portfolio_link}")

    c.save()
    print(f"ATS resume saved to {output_path}")