# mcp_server/tools/full_resume_rewriter.py

import pandas as pd
from utils.rewrite_utils import sanitize_resume_blocks
from utils.rewrite_blocks import (
    rewrite_target_roles,
    rewrite_summary,
    rewrite_bullets
)

def full_resume_rewriter(job_description: str, resume_rows: list):
    try:
        df = pd.DataFrame(resume_rows)
        if df.empty or not set(["section", "subsection", "content"]).issubset(df.columns):
            return {"error": "Invalid resume format. Must include section, subsection, content."}

        blocks = df.to_dict(orient="records")
        updated_blocks = []

        for block in blocks:
            section = block["section"].strip()
            sub = block["subsection"].strip()
            content = block["content"].strip()

            # Rewrite target_roles
            if section == "personal_info" and sub == "target_roles":
                block["content"] = rewrite_target_roles(job_description, content)

            # Rewrite professional summary
            elif section == "professional_summary":
                block["content"] = rewrite_summary(job_description, content)

            # Rewrite bullets in experience (4/4/2) using job_# tag
            elif section == "professional_experience":
                lines = [l for l in content.split("\n") if l.strip()]
                header = lines[0] if lines else ""
                bullets = [b.replace("\u2022", "").strip() for b in lines[1:]]
                limit = 4 if sub.endswith("1") or sub.endswith("2") else 2
                rewritten = rewrite_bullets(job_description, header, bullets, limit)
                block["content"] = f"{header}\n" + "\n".join(rewritten.splitlines())

            # Rewrite project bullets (2 each)
            elif section == "projects":
                lines = [l for l in content.split("\n") if l.strip()]
                header = lines[0] if lines else ""
                bullets = [b.replace("\u2022", "").strip() for b in lines[1:]]
                rewritten = rewrite_bullets(job_description, header, bullets, 2)
                block["content"] = f"{header}\n" + "\n".join(rewritten.splitlines())

            updated_blocks.append(block)

        return {"rewritten_blocks": sanitize_resume_blocks(updated_blocks)}

    except Exception as e:
        return {"error": str(e)}