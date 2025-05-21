import re
import pandas as pd
from typing import List

def parse_resume_questionnaire(text: str) -> pd.DataFrame:
    rows = []
    current_section = None
    current_subsection = None
    buffer = []

    def flush_buffer():
        if buffer and current_section:
            content = "\n".join(buffer).strip()
            if content:
                rows.append({
                    "section": current_section,
                    "subsection": current_subsection or "",
                    "content": content
                })
        buffer.clear()

    lines = text.splitlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Detect section header
        section_match = re.match(r"\*\*(.+?)\*\*", line)
        if section_match:
            flush_buffer()
            current_section = section_match.group(1).strip().lower().replace(" ", "_")
            current_subsection = None
            continue

        # Detect key-value field
        if '|' in line and not line.startswith('-'):
            flush_buffer()
            parts = [p.strip() for p in line.split('|', 1)]
            if len(parts) == 2:
                key, value = parts
                rows.append({
                    "section": current_section,
                    "subsection": key.lower().replace(" ", "_"),
                    "content": value
                })
            continue

        # Detect list item (project or work bullets)
        bullet_match = re.match(r"^- (.+)", line)
        if bullet_match:
            buffer.append(bullet_match.group(1).strip())
            continue

        # Detect subsection entry (e.g., Project | Title)
        if current_section in ["projects", "professional_experience", "education", "certifications"] and '|' in line:
            flush_buffer()
            key, val = [p.strip() for p in line.split('|', 1)]
            current_subsection = val
            continue

        # Default: part of a paragraph
        buffer.append(line)

    flush_buffer()
    return pd.DataFrame(rows)
