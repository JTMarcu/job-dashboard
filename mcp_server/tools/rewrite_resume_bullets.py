# mcp_server/tools/rewrite_resume_bullets.py

import re
from typing import List
from openai import OpenAI
import os

# Optional: replace with a local model or other LLM backend
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_bullets(text: str) -> List[str]:
    lines = text.strip().splitlines()
    bullets = [line.strip("• ") for line in lines if line.strip().startswith("•")]
    return bullets


def format_block_with_bullets(header: str, bullets: List[str]) -> str:
    bullet_lines = [f"• {b.strip()}" for b in bullets if b.strip()]
    return header.strip() + "\n" + "\n".join(bullet_lines)


def rewrite_resume_bullets(job_description: str, resume_block: str, bullet_limit: int = 4):
    try:
        lines = resume_block.strip().splitlines()
        header = lines[0] if lines else ""
        body = "\n".join(lines[1:])

        prompt = f"""
You are a resume assistant. Rewrite the bullet points in the following resume block to match the job description below. Return exactly {bullet_limit} strong, clear bullets that demonstrate fit for the role. Keep formatting clean and concise.

Job Description:
{job_description}

Resume Block:
{resume_block}
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        new_text = response.choices[0].message.content.strip()
        new_bullets = extract_bullets(new_text)
        final_block = format_block_with_bullets(header, new_bullets[:bullet_limit])

        return {"rewritten": final_block, "count": len(new_bullets)}

    except Exception as e:
        return {"error": str(e)}
