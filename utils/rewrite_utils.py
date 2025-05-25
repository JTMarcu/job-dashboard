# utils/rewrite_utils.py
import ast
import json

USER_PROFILE_PATH = "users/user_profile.json"

# Utility: Pad or trim bullet lines
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

# Final cleanup and enforcement
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

    # Process all blocks
    for block in blocks:
        key = tuple(block.items())
        if key in seen:
            continue
        seen.add(key)

        section = block.get("section", "").strip()
        subsection = block.get("subsection", "").strip()
        content = block.get("content", "").strip()

        if section == "personal_info" and subsection == "target_roles":
            roles = [r.strip() for r in content.split("|") if r.strip()]
            if len(roles) < 4:
                roles += ["(Other Relevant Role)"] * (4 - len(roles))
            block["content"] = " | ".join(roles[:4])

        elif section == "professional_experience":
            job_counter += 1
            lines = [l for l in content.split("\n") if l.strip()]
            header = lines[0] if lines else ""
            bullets = pad_bullets(lines[1:], 4 if job_counter in [1, 2] else 2)
            block["subsection"] = f"job_{job_counter}"
            block["content"] = "\n".join([header] + bullets)

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
            if content in cert_seen:
                continue
            cert_seen.add(content)
            cert_blocks.append(block)
            continue

        final_blocks.append(block)

    # Inject stable personal_info
    try:
        with open(USER_PROFILE_PATH, "r") as f:
            profile = json.load(f)
        for field in ["name", "location", "email", "phone", "linkedin", "github", "portfolio"]:
            final_blocks.insert(0, {
                "section": "personal_info",
                "subsection": field,
                "content": profile.get(field, "")
            })
    except Exception:
        pass

    # Insert cleaned skill blocks
    for sub, b in skill_blocks.items():
        final_blocks.append(b if b else {
            "section": "technical_skills", "subsection": sub, "content": ""
        })

    final_blocks += cert_blocks
    return final_blocks

# Parse and clean final model response
def parse_and_sanitize_output(raw_response):
    try:
        parsed = ast.literal_eval(raw_response.strip())
        return sanitize_resume_blocks(parsed)
    except Exception as e:
        return [{"section": "error", "subsection": "parse_fail", "content": str(e)}]