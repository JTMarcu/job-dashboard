# utils/rewrite_utils.py
import ast

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

def sanitize_resume_blocks(blocks):
    sanitized = []
    job_counter = 0
    proj_counter = 0
    personal_info_keys = set()
    personal_info_blocks = []
    cert_seen = set()
    cert_blocks = []
    required_personal_fields = [
        "name", "location", "email", "phone", "linkedin", "github", "portfolio"
    ]
    tech_skills_fields = [
        "programming_languages", "libraries_frameworks", "tools_platforms", "other_skills"
    ]
    skill_blocks = {key: None for key in tech_skills_fields}

    for block in blocks:
        section = block.get("section", "").strip()
        subsection = block.get("subsection", "").strip()
        content = block.get("content", "").strip()

        if section == "personal_info":
            personal_info_keys.add(subsection)
            personal_info_blocks.append(block)
            continue

        if section == "personal_info" and subsection == "target_roles":
            roles = [r.strip() for r in content.split("|") if r.strip()]
            if len(roles) < 4:
                roles += ["(Other Relevant Role)"] * (4 - len(roles))
            block["content"] = " | ".join(roles[:4])

        if section == "professional_experience":
            job_counter += 1
            lines = [l for l in content.split("\n") if l.strip()]
            header = lines[0] if lines else ""
            bullets = lines[1:]
            limit = 4 if job_counter in [1, 2] else 2
            bullets = pad_bullets(bullets, limit)
            block["subsection"] = f"job_{job_counter}"
            block["content"] = "\n".join([header] + bullets)

        elif section == "projects":
            if proj_counter >= 4:
                continue
            lines = [l for l in content.split("\n") if l.strip()]
            header = lines[0] if lines else ""
            bullets = lines[1:]
            if header:
                proj_counter += 1
                bullets = pad_bullets(bullets, 2)
                block["subsection"] = f"proj_{proj_counter}"
                block["content"] = "\n".join([header] + bullets)
                sanitized.append(block)
            continue

        elif section == "technical_skills" and subsection in tech_skills_fields:
            items = [x.strip() for x in content.split("|") if x.strip()]
            items = (items + ["..."] * 5)[:5]
            skill_blocks[subsection] = {
                "section": section,
                "subsection": subsection,
                "content": " | ".join(items)
            }
            continue

        elif section == "certifications":
            if content not in cert_seen:
                cert_seen.add(content)
                cert_blocks.append(block)
            continue

        sanitized.append(block)

    for req in required_personal_fields:
        if req not in personal_info_keys:
            personal_info_blocks.append({
                "section": "personal_info", "subsection": req, "content": ""
            })

    for sub, block in skill_blocks.items():
        if block:
            sanitized.append(block)
        else:
            sanitized.append({
                "section": "technical_skills", "subsection": sub, "content": ""
            })

    return personal_info_blocks + sanitized + cert_blocks

def parse_and_sanitize_output(raw_response):
    try:
        parsed = ast.literal_eval(raw_response.strip())
        return sanitize_resume_blocks(parsed)
    except Exception as e:
        return [{"section": "error", "subsection": "parse_fail", "content": str(e)}]