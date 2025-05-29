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

def normalize_ollama_blocks(raw_blocks):
    """
    Accepts parsed LLM output (list of dicts, possibly nested/lists).
    Returns strict flat blocks as expected by your app (section,subsection,content).
    """
    flat_blocks = []
    for block in raw_blocks:
        section = block.get("section", "").strip().lower()
        subsection = block.get("subsection")
        content = block.get("content")

        # Normalize section name
        if section == "experience":
            section = "professional_experience"
        elif section == "certification":
            section = "certifications"
        elif section == "project":
            section = "projects"

        # --- Flatten professional_experience ---
        if section == "professional_experience":
            entries = []
            if isinstance(subsection, list):
                entries = subsection
            elif isinstance(content, list):
                entries = content
            elif isinstance(subsection, dict):
                entries = [subsection]
            elif isinstance(content, dict):
                entries = [content]
            else:
                if content and isinstance(content, str):
                    entries = [{"title": subsection, "company": "", "dates": "", "responsibilities": [content]}]
            for i, job in enumerate(entries):
                header = "**{} | {} | {}**".format(
                    job.get("title", ""),
                    job.get("company", ""),
                    " ".join(job.get("dates", [])) if isinstance(job.get("dates"), list) else job.get("dates", "")
                )
                bullets = job.get("responsibilities") or []
                if isinstance(bullets, str): bullets = [bullets]
                content_str = header
                if bullets:
                    content_str += "\n" + "\n".join(
                        f"• {b.strip()}" if not b.strip().startswith("•") else b.strip() for b in bullets if b.strip()
                    )
                flat_blocks.append({
                    "section": "professional_experience",
                    "subsection": f"job_{i+1}",
                    "content": content_str.strip()
                })

        # --- Flatten projects ---
        elif section == "projects":
            entries = []
            if isinstance(subsection, list):
                entries = subsection
            elif isinstance(content, list):
                entries = content
            elif isinstance(subsection, dict):
                entries = [subsection]
            elif isinstance(content, dict):
                entries = [content]
            else:
                if content and isinstance(content, str):
                    entries = [{"title": subsection, "description": [content]}]
            for i, proj in enumerate(entries):
                header = "**{}**".format(proj.get("title", ""))
                desc = proj.get("description", [])
                if isinstance(desc, str): desc = [desc]
                content_str = header
                if desc:
                    content_str += "\n" + "\n".join(
                        f"• {d.strip()}" if not d.strip().startswith("•") else d.strip() for d in desc if d.strip()
                    )
                flat_blocks.append({
                    "section": "projects",
                    "subsection": f"proj_{i+1}",
                    "content": content_str.strip()
                })

        # --- Flatten certifications ---
        elif section == "certifications":
            entries = []
            if isinstance(subsection, list):
                entries = subsection
            elif isinstance(content, list):
                entries = content
            elif isinstance(subsection, dict):
                entries = [subsection]
            elif isinstance(content, dict):
                entries = [content]
            else:
                if content and isinstance(content, str):
                    entries = [{"name": content}]
            for i, cert in enumerate(entries):
                name = cert.get("name", "")
                date = cert.get("date", "")
                content_str = f"{name} | {date}".strip(" |")
                flat_blocks.append({
                    "section": "certifications",
                    "subsection": f"cert_{i+1}",
                    "content": content_str
                })

        # --- Flatten education ---
        elif section == "education":
            entries = []
            if isinstance(subsection, list):
                entries = subsection
            elif isinstance(content, list):
                entries = content
            elif isinstance(subsection, dict):
                entries = [subsection]
            elif isinstance(content, dict):
                entries = [content]
            else:
                if content and isinstance(content, str):
                    entries = [{"degree": subsection, "school": "", "date": "", "highlights": [content]}]
            for i, edu in enumerate(entries):
                degree = edu.get("degree", "") or edu.get("title", "")
                school = edu.get("school", "")
                date = edu.get("date", "")
                highlights = edu.get("highlights", [])
                if isinstance(highlights, str):
                    highlights = [highlights]
                header = "**{} | {} | {}**".format(degree, school, date).strip(" |")
                content_str = header
                if highlights:
                    content_str += "\n" + "\n".join(
                        f"• {h.strip()}" if not h.strip().startswith("•") else h.strip() for h in highlights if h.strip()
                    )
                flat_blocks.append({
                    "section": "education",
                    "subsection": f"edu_{i+1}",
                    "content": content_str.strip()
                })

        # --- Flatten technical_skills ---
        elif section == "technical_skills":
            if isinstance(content, list):
                pipe = " | ".join([str(x).strip() for x in content if str(x).strip()])
                flat_blocks.append({
                    "section": "technical_skills",
                    "subsection": subsection,
                    "content": pipe
                })
            else:
                flat_blocks.append({
                    "section": "technical_skills",
                    "subsection": subsection,
                    "content": str(content).strip() if content else ""
                })

        # --- Flatten personal_info, professional_summary, etc. ---
        else:
            if subsection and isinstance(subsection, str):
                flat_blocks.append({
                    "section": section,
                    "subsection": subsection,
                    "content": str(content).strip() if content else ""
                })
    return flat_blocks

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
        # Normalize the blocks!
        normalized = normalize_ollama_blocks(parsed)
        return sanitize_resume_blocks(normalized, master_blocks)
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