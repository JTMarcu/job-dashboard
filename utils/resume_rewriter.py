# utils/resume_rewriter.py

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

def run_ollama(prompt):
    res = requests.post(OLLAMA_URL, json={
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    })
    res.raise_for_status()
    return res.json().get("response", "").strip()

def pad_bullets(lines, limit):
    lines = [l.strip() for l in lines if l.strip()]
    lines = [f"• {l}" if not l.startswith("•") else l for l in lines]
    sample_phrases = [
        "Demonstrated adaptability in fast-paced environments",
        "Improved operational efficiency through data insights",
        "Collaborated across departments to meet objectives",
        "Utilized analytical tools to guide business strategy",
        "Supported project deliverables through targeted research"
    ]
    while len(lines) < limit:
        lines.append(f"• {sample_phrases[len(lines) % len(sample_phrases)]}")
    return lines[:limit]

def format_resume_rows(rows):
    return [
        {
            "section": row.get("section", "").strip(),
            "subsection": row.get("subsection", "").strip(),
            "content": row.get("content", "").strip()
        }
        for row in rows if row.get("section") and row.get("content")
    ]

def sanitize_resume_blocks(blocks, master_blocks):
    # Build a lookup for personal_info from master (except target_roles)
    master_personal = {
        b["subsection"]: b["content"]
        for b in master_blocks
        if b.get("section") == "personal_info" and b.get("subsection") != "target_roles"
    }

    # Only allow LLM to change target_roles; restore all other personal_info from master
    cleaned = []
    for b in blocks:
        section = b.get("section", "")
        subsection = b.get("subsection", "")
        content = b.get("content", "")

        if section == "personal_info" and subsection != "target_roles":
            # Force content from master resume
            content = master_personal.get(subsection, "")
        cleaned.append({
            "section": section,
            "subsection": subsection,
            "content": content
        })

    # Remove duplicates (keep first occurrence)
    seen = set()
    unique = []
    for b in cleaned:
        k = (b["section"], b["subsection"])
        if k in seen:
            continue
        seen.add(k)
        unique.append(b)

    # -- Project section logic: just enforce 4 max, 2 bullets each
    filtered = []
    proj_count = 0
    for b in unique:
        if b["section"] == "projects":
            if proj_count >= 4:
                continue
            # Ensure max 2 bullets
            lines = [l for l in b["content"].split("\n") if l.strip()]
            header = lines[0] if lines else ""
            bullets = pad_bullets(lines[1:], 2)
            b["content"] = "\n".join([header] + bullets)
            proj_count += 1
        filtered.append(b)

    # --- Professional Experience bullets logic ---
    # 1st and 2nd jobs: 4 bullets. 3rd job: 2 bullets. All others: 2 bullets.
    final = []
    exp_count = 0
    for b in filtered:
        if b["section"] == "professional_experience":
            exp_count += 1
            lines = [l for l in b["content"].split("\n") if l.strip()]
            header = lines[0] if lines else ""
            bullets = lines[1:]
            if exp_count == 3:
                bullets = pad_bullets(bullets, 2)
            elif exp_count in [1, 2]:
                bullets = pad_bullets(bullets, 4)
            else:
                bullets = pad_bullets(bullets, 2)
            b["content"] = "\n".join([header] + bullets)
        final.append(b)

    # Trim to 40 lines (keep all personal_info rows)
    pers_info = [b for b in final if b["section"] == "personal_info"]
    not_pers = [b for b in final if b["section"] != "personal_info"]
    if len(pers_info) + len(not_pers) > 40:
        not_pers = not_pers[:(40 - len(pers_info))]
    final = pers_info + not_pers

    return final

def parse_and_sanitize_output(raw_response, master_blocks):
    try:
        start = raw_response.find("[")
        end = raw_response.rfind("]") + 1
        clean_json = raw_response[start:end].strip()
        parsed = json.loads(clean_json)
        return sanitize_resume_blocks(parsed, master_blocks)
    except Exception as e:
        return [{"section": "error", "subsection": "parse_fail", "content": str(e)}]

def full_resume_rewriter(job_description, resume_rows):
    resume_blocks = format_resume_rows(resume_rows)
    resume_str = json.dumps(resume_blocks, indent=2)

    prompt = f"""
You are an expert resume editor. Rewrite the following resume to better match the job description.

Return ONLY valid JSON in this format:

[
  {{
    "section": "professional_summary",
    "subsection": "summary",
    "content": "..."
  }},
  ...
]

Guidelines:
- Skills can be a list of strings
- Experience can include nested objects with title, company, dates, and responsibilities
- DO NOT include markdown, commentary, or extra text
- DO NOT wrap the response in quotes or say "Here's your updated resume"
- Output raw JSON only

Job Description:
{job_description}

Resume Blocks:
{resume_str}
""".strip()

    response = run_ollama(prompt)

    with open("ollama_raw_output.txt", "w", encoding="utf-8") as f:
        f.write(response)

    print("=== RAW OLLAMA RESPONSE START ===")
    print(response)
    print("=== RAW OLLAMA RESPONSE END ===")

    parsed_blocks = parse_and_sanitize_output(response, resume_blocks)
    return {"rewritten_blocks": parsed_blocks}