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

def enforce_all_guidelines(normalized_blocks, master_blocks):
    """
    normalized_blocks: flat, normalized blocks from LLM
    master_blocks: flat blocks from master resume
    Returns: 40-line, 3-column list of dicts
    """
    def block_dict(blocks):
        return {(b["section"], b["subsection"]): b["content"] for b in blocks}

    master_lookup = block_dict(master_blocks)
    llm_lookup = block_dict(normalized_blocks)

    # Personal Info (fields, order, always from master except target_roles)
    personal_info_order = ["name", "location", "email", "phone", "linkedin", "github", "portfolio", "target_roles"]
    personal_info_blocks = []
    for sub in personal_info_order:
        if sub == "target_roles" and ("personal_info", "target_roles") in llm_lookup:
            content = llm_lookup[("personal_info", "target_roles")]
        else:
            content = master_lookup.get(("personal_info", sub), "")
        personal_info_blocks.append({
            "section": "personal_info",
            "subsection": sub,
            "content": content
        })

    # Professional Summary
    summary = llm_lookup.get(("professional_summary", "summary"), master_lookup.get(("professional_summary", "summary"), ""))
    summary_block = [{"section": "professional_summary", "subsection": "summary", "content": summary}]

    # Technical Skills
    skill_subsections = ["programming_languages", "libraries_frameworks", "tools_platforms", "other_skills"]
    skill_blocks = []
    for sub in skill_subsections:
        content = llm_lookup.get(("technical_skills", sub), master_lookup.get(("technical_skills", sub), ""))
        skill_blocks.append({"section": "technical_skills", "subsection": sub, "content": content})

    # Professional Experience (always 3 jobs, 4/4/2 bullets)
    llm_jobs = [b for b in normalized_blocks if b["section"] == "professional_experience"]
    master_jobs = [b for b in master_blocks if b["section"] == "professional_experience"]
    jobs = []
    idx = 0
    for b in llm_jobs + master_jobs:
        if idx >= 3:
            break
        if b in jobs:
            continue
        lines = [l for l in b["content"].split("\n") if l.strip()]
        header = lines[0] if lines else ""
        bullets = lines[1:]
        if idx in [0,1]:
            bullets = pad_bullets(bullets, 4)
        else:
            bullets = pad_bullets(bullets, 2)
        jobs.append({
            "section": "professional_experience",
            "subsection": f"job_{idx+1}",
            "content": "\n".join([header] + bullets)
        })
        idx += 1
    while len(jobs) < 3:
        jobs.append({
            "section": "professional_experience",
            "subsection": f"job_{len(jobs)+1}",
            "content": ""
        })

    # Education (1 entry, LLM or master or blank)
    llm_edus = [b for b in normalized_blocks if b["section"] == "education"]
    master_edus = [b for b in master_blocks if b["section"] == "education"]
    edu_blocks = []
    if llm_edus:
        edu_blocks.append(llm_edus[0])
    elif master_edus:
        edu_blocks.append(master_edus[0])
    else:
        edu_blocks.append({"section": "education", "subsection": "edu_1", "content": ""})

    # Certifications (up to 3, fill or pad)
    llm_certs = [b for b in normalized_blocks if b["section"] == "certifications"]
    master_certs = [b for b in master_blocks if b["section"] == "certifications"]
    cert_blocks = []
    for b in (llm_certs or master_certs)[:3]:
        cert_blocks.append(b)
    while len(cert_blocks) < 3:
        cert_blocks.append({"section": "certifications", "subsection": f"cert_{len(cert_blocks)+1}", "content": ""})

    # Projects (4, 2 bullets each)
    llm_projects = [b for b in normalized_blocks if b["section"] == "projects"]
    master_projects = [b for b in master_blocks if b["section"] == "projects"]
    proj_blocks = []
    idx = 0
    for b in llm_projects + master_projects:
        if idx >= 4:
            break
        lines = [l for l in b["content"].split("\n") if l.strip()]
        header = lines[0] if lines else ""
        bullets = lines[1:]
        bullets = pad_bullets(bullets, 2)
        proj_blocks.append({
            "section": "projects",
            "subsection": f"proj_{idx+1}",
            "content": "\n".join([header] + bullets)
        })
        idx += 1
    while len(proj_blocks) < 4:
        proj_blocks.append({"section": "projects", "subsection": f"proj_{len(proj_blocks)+1}", "content": ""})

    # Strict order and 40 lines
    output_blocks = (
        personal_info_blocks +
        summary_block +
        skill_blocks +
        jobs +
        edu_blocks +
        cert_blocks +
        proj_blocks
    )
    while len(output_blocks) < 40:
        output_blocks.append({"section": "", "subsection": "", "content": ""})
    output_blocks = output_blocks[:40]

    return output_blocks

def parse_and_sanitize_output(raw_response, master_blocks):
    try:
        start = raw_response.find("[")
        end = raw_response.rfind("]") + 1
        clean_json = raw_response[start:end].strip()
        parsed = json.loads(clean_json)
        normalized = normalize_ollama_blocks(parsed)
        return enforce_all_guidelines(normalized, master_blocks)
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