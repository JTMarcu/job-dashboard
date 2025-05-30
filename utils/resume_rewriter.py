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
    lines = [safe_str(l).strip() for l in lines if safe_str(l).strip()]
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
            "section": safe_str(row.get("section", "")).strip(),
            "subsection": safe_str(row.get("subsection", "")).strip(),
            "content": safe_str(row.get("content", "")).strip()
        }
        for row in rows if safe_str(row.get("section")) and safe_str(row.get("content"))
    ]

def safe_str(x):
    if x is None:
        return ""
    try:
        import pandas as pd
        if isinstance(x, float) and pd.isna(x):
            return ""
    except Exception:
        pass
    return str(x)

def normalize_ollama_blocks(raw_blocks):
    flat_blocks = []
    for block in raw_blocks:
        section = safe_str(block.get("section", "")).strip().lower()
        subsection = block.get("subsection")
        content = block.get("content")

        if section == "experience":
            section = "professional_experience"
        elif section == "certification":
            section = "certifications"
        elif section == "project":
            section = "projects"

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
                    safe_str(job.get("title", "")),
                    safe_str(job.get("company", "")),
                    " ".join(job.get("dates", [])) if isinstance(job.get("dates"), list) else safe_str(job.get("dates", ""))
                )
                bullets = job.get("responsibilities") or []
                if isinstance(bullets, str): bullets = [bullets]
                content_str = header
                if bullets:
                    content_str += "\n" + "\n".join(
                        f"• {safe_str(b).strip()}" if not safe_str(b).strip().startswith("•") else safe_str(b).strip() for b in bullets if safe_str(b).strip()
                    )
                flat_blocks.append({
                    "section": "professional_experience",
                    "subsection": f"job_{i+1}",
                    "content": safe_str(content_str.strip())
                })

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
                header = "**{}**".format(safe_str(proj.get("title", "")))
                desc = proj.get("description", [])
                if isinstance(desc, str): desc = [desc]
                content_str = header
                if desc:
                    content_str += "\n" + "\n".join(
                        f"• {safe_str(d).strip()}" if not safe_str(d).strip().startswith("•") else safe_str(d).strip() for d in desc if safe_str(d).strip()
                    )
                flat_blocks.append({
                    "section": "projects",
                    "subsection": f"proj_{i+1}",
                    "content": safe_str(content_str.strip())
                })

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
                name = safe_str(cert.get("name", ""))
                date = safe_str(cert.get("date", ""))
                content_str = f"{name} | {date}".strip(" |")
                flat_blocks.append({
                    "section": "certifications",
                    "subsection": f"cert_{i+1}",
                    "content": safe_str(content_str)
                })

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
                degree = safe_str(edu.get("degree", "")) or safe_str(edu.get("title", ""))
                school = safe_str(edu.get("school", ""))
                date = safe_str(edu.get("date", ""))
                highlights = edu.get("highlights", [])
                if isinstance(highlights, str):
                    highlights = [highlights]
                header = "**{} | {} | {}**".format(degree, school, date).strip(" |")
                content_str = header
                if highlights:
                    content_str += "\n" + "\n".join(
                        f"• {safe_str(h).strip()}" if not safe_str(h).strip().startswith("•") else safe_str(h).strip() for h in highlights if safe_str(h).strip()
                    )
                flat_blocks.append({
                    "section": "education",
                    "subsection": f"edu_{i+1}",
                    "content": safe_str(content_str.strip())
                })

        elif section == "technical_skills":
            if isinstance(content, list):
                pipe = " | ".join([safe_str(x).strip() for x in content if safe_str(x).strip()])
                flat_blocks.append({
                    "section": "technical_skills",
                    "subsection": safe_str(subsection),
                    "content": safe_str(pipe)
                })
            else:
                flat_blocks.append({
                    "section": "technical_skills",
                    "subsection": safe_str(subsection),
                    "content": safe_str(content).strip() if content else ""
                })

        else:
            if subsection and isinstance(subsection, str):
                flat_blocks.append({
                    "section": safe_str(section),
                    "subsection": safe_str(subsection),
                    "content": safe_str(content).strip() if content else ""
                })
    return flat_blocks

def enforce_all_guidelines(normalized_blocks, master_blocks):
    def block_dict(blocks):
        return {(safe_str(b.get("section", "")), safe_str(b.get("subsection", ""))): safe_str(b.get("content", "")) for b in blocks}

    master_lookup = block_dict(master_blocks)
    llm_lookup = block_dict(normalized_blocks)

    personal_info_order = ["name", "location", "email", "phone", "linkedin", "github", "portfolio", "target_roles"]
    personal_info_blocks = []
    for sub in personal_info_order:
        if sub == "target_roles" and ("personal_info", "target_roles") in llm_lookup:
            content = safe_str(llm_lookup[("personal_info", "target_roles")])
        else:
            content = safe_str(master_lookup.get(("personal_info", sub), ""))
        personal_info_blocks.append({
            "section": "personal_info",
            "subsection": sub,
            "content": content
        })

    summary = safe_str(llm_lookup.get(("professional_summary", "summary"), master_lookup.get(("professional_summary", "summary"), "")))
    summary_block = [{"section": "professional_summary", "subsection": "summary", "content": summary}]

    skill_subsections = ["programming_languages", "libraries_frameworks", "tools_platforms", "other_skills"]
    skill_blocks = []
    for sub in skill_subsections:
        content = safe_str(llm_lookup.get(("technical_skills", sub), master_lookup.get(("technical_skills", sub), "")))
        skill_blocks.append({"section": "technical_skills", "subsection": sub, "content": content})

    llm_jobs = [b for b in normalized_blocks if b["section"] == "professional_experience"]
    master_jobs = [b for b in master_blocks if b["section"] == "professional_experience"]
    jobs = []
    idx = 0
    for b in llm_jobs + master_jobs:
        if idx >= 3:
            break
        if b in jobs:
            continue
        lines = [safe_str(l) for l in safe_str(b.get("content", "")).split("\n") if safe_str(l).strip()]
        header = lines[0] if lines else ""
        bullets = lines[1:]
        if idx in [0, 1]:
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

    llm_edus = [b for b in normalized_blocks if b["section"] == "education"]
    master_edus = [b for b in master_blocks if b["section"] == "education"]
    edu_blocks = []
    if llm_edus:
        edu = llm_edus[0]
        edu_blocks.append({
            "section": "education",
            "subsection": safe_str(edu.get("subsection", "edu_1")),
            "content": safe_str(edu.get("content", ""))
        })
    elif master_edus:
        edu = master_edus[0]
        edu_blocks.append({
            "section": "education",
            "subsection": safe_str(edu.get("subsection", "edu_1")),
            "content": safe_str(edu.get("content", ""))
        })
    else:
        edu_blocks.append({"section": "education", "subsection": "edu_1", "content": ""})

    llm_certs = [b for b in normalized_blocks if b["section"] == "certifications"]
    master_certs = [b for b in master_blocks if b["section"] == "certifications"]
    cert_blocks = []
    for b in (llm_certs or master_certs)[:3]:
        cert_blocks.append({
            "section": "certifications",
            "subsection": safe_str(b.get("subsection", f"cert_{len(cert_blocks)+1}")),
            "content": safe_str(b.get("content", ""))
        })
    while len(cert_blocks) < 3:
        cert_blocks.append({"section": "certifications", "subsection": f"cert_{len(cert_blocks)+1}", "content": ""})

    llm_projects = [b for b in normalized_blocks if b["section"] == "projects"]
    master_projects = [b for b in master_blocks if b["section"] == "projects"]
    proj_blocks = []
    idx = 0
    for b in llm_projects + master_projects:
        if idx >= 4:
            break
        lines = [safe_str(l) for l in safe_str(b.get("content", "")).split("\n") if safe_str(l).strip()]
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

    output_blocks = (
        personal_info_blocks +
        summary_block +
        skill_blocks +
        jobs +
        edu_blocks +
        cert_blocks +
        proj_blocks
    )

    # Remove duplicate target_roles and ensure all values are strings
    target_roles_found = False
    final_blocks = []
    for b in output_blocks[:40]:
        s = safe_str(b.get("section", ""))
        sub = safe_str(b.get("subsection", ""))
        c = safe_str(b.get("content", ""))
        if s == "personal_info" and sub == "target_roles":
            if target_roles_found:
                continue
            target_roles_found = True
        final_blocks.append({"section": s, "subsection": sub, "content": c})
    # Remove trailing lines where all fields are blank
    while final_blocks and all(v == "" for v in final_blocks[-1].values()):
        final_blocks.pop()
    return final_blocks

def parse_and_sanitize_output(raw_response, master_blocks):
    try:
        start = raw_response.find("[")
        end = raw_response.rfind("]") + 1
        clean_json = raw_response[start:end].strip()
        parsed = json.loads(clean_json)
        normalized = normalize_ollama_blocks(parsed)
        return enforce_all_guidelines(normalized, master_blocks)
    except Exception as e:
        return [{"section": "error", "subsection": "parse_fail", "content": safe_str(e)}]

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