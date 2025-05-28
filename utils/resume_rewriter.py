# utils/resume_rewriter.py

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# Dynamic profile loader from Streamlit-created JSON
try:
    with open("users/active_profile.json", "r") as f:
        ACTIVE_PROFILE = json.load(f).get("active_profile", "user_profile")
except Exception:
    ACTIVE_PROFILE = "user_profile"

USER_PROFILE_PATH = f"users/{ACTIVE_PROFILE}.json"

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
    lines = [f"\u2022 {l}" if not l.startswith("\u2022") else l for l in lines]
    sample_phrases = [
        "Demonstrated adaptability in fast-paced environments",
        "Improved operational efficiency through data insights",
        "Collaborated across departments to meet objectives",
        "Utilized analytical tools to guide business strategy",
        "Supported project deliverables through targeted research"
    ]
    while len(lines) < limit:
        lines.append(f"\u2022 {sample_phrases[len(lines) % len(sample_phrases)]}")
    return lines[:limit]

def sanitize_resume_blocks(blocks):
    job_counter = 0
    proj_counter = 0
    final_blocks = []
    seen = set()
    tech_skills_fields = [
        "programming_languages", "libraries_frameworks", "tools_platforms", "other_skills"
    ]
    skill_blocks = {key: None for key in tech_skills_fields}
    cert_blocks = []
    cert_seen = set()

    for block in blocks:
        section = block.get("section", "").strip()
        subsection = block.get("subsection", "").strip()
        raw_content = block.get("content", "")

        # Normalize content to string
        if isinstance(raw_content, list):
            if all(isinstance(item, str) for item in raw_content):
                content = " | ".join(raw_content) if section == "technical_skills" else "\n".join(raw_content)
            elif all(isinstance(item, dict) for item in raw_content):
                formatted = []
                for item in raw_content:
                    bullets = item.get("responsibilities") or item.get("bullets") or []
                    date_str = item.get("dates", "") if isinstance(item.get("dates"), str) else " ".join(item.get("dates", []))
                    header_parts = [item.get("title", ""), item.get("company", ""), date_str]
                    header = " | ".join([p for p in header_parts if p])
                    formatted.append(header + "\n" + "\n".join([f"• {b}" for b in bullets]))
                content = "\n\n".join(formatted)
            else:
                content = str(raw_content)
        else:
            content = str(raw_content).strip()

        key = (section, subsection)
        if key in seen:
            continue
        seen.add(key)

        block["content"] = content

        if section == "personal_info" and subsection == "target_roles":
            roles = [r.strip() for r in content.split("|") if r.strip()]
            if len(roles) < 4:
                roles += ["(Other Relevant Role)"] * (4 - len(roles))
            block["content"] = " | ".join(roles[:4])
            final_blocks.append(block)

        elif section == "professional_experience":
            job_counter += 1
            lines = [l for l in content.split("\n") if l.strip()]
            header = lines[0] if lines else ""
            bullets = pad_bullets(lines[1:], 4 if job_counter in [1, 2] else 2)
            block["subsection"] = f"job_{job_counter}"
            block["content"] = "\n".join([header] + bullets)
            final_blocks.append(block)

        elif section == "projects":
            if proj_counter >= 4:
                continue
            lines = [l for l in content.split("\n") if l.strip()]
            if not lines:
                continue
            header = lines[0]
            bullets = pad_bullets(lines[1:], 2)
            proj_counter += 1
            block["subsection"] = f"proj_{proj_counter}"
            block["content"] = "\n".join([header] + bullets)
            final_blocks.append(block)

        elif section == "technical_skills" and subsection in tech_skills_fields:
            items = [x.strip() for x in content.split("|") if x.strip()]
            items = (items + ["..."] * 5)[:5]
            skill_blocks[subsection] = {
                "section": section,
                "subsection": subsection,
                "content": " | ".join(items)
            }

        elif section == "certifications":
            if content in cert_seen:
                continue
            cert_seen.add(content)
            cert_blocks.append(block)

        elif section != "personal_info":
            final_blocks.append(block)

    try:
        with open(USER_PROFILE_PATH, "r") as f:
            profile = json.load(f)
        personal_fields = ["name", "location", "email", "phone", "linkedin", "github", "portfolio"]
        final_blocks = [
            b for b in final_blocks
            if not (b["section"] == "personal_info" and b["subsection"] in personal_fields)
        ]
        for field in reversed(personal_fields):
            final_blocks.insert(0, {
                "section": "personal_info",
                "subsection": field,
                "content": profile.get(field, "")
            })
    except Exception as e:
        final_blocks.insert(0, {
            "section": "error",
            "subsection": "profile_load_fail",
            "content": f"Could not load profile: {e}"
        })

    for sub, b in skill_blocks.items():
        final_blocks.append(b if b else {
            "section": "technical_skills", "subsection": sub, "content": ""
        })

    final_blocks += cert_blocks
    return final_blocks

def parse_and_sanitize_output(raw_response):
    try:
        start = raw_response.find("[")
        end = raw_response.rfind("]") + 1
        clean_json = raw_response[start:end].strip()
        parsed = json.loads(clean_json)
        return sanitize_resume_blocks(parsed)
    except Exception as e:
        return [{"section": "error", "subsection": "parse_fail", "content": str(e)}]

def format_resume_rows(rows):
    return [
        {
            "section": row.get("section", "").strip(),
            "subsection": row.get("subsection", "").strip(),
            "content": row.get("content", "").strip()
        }
        for row in rows if row.get("section") and row.get("content")
    ]

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

    parsed_blocks = parse_and_sanitize_output(response)
    return {"rewritten_blocks": str(parsed_blocks)}