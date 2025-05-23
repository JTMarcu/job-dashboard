# mcp_server/tools/rewrite_target_roles.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def rewrite_target_roles(job_description: str, original_roles: str):
    try:
        prompt = f"""
You are a resume assistant. Rewrite the candidate's list of target roles to align with the following job description. Use professional phrasing and separate roles with vertical bars (|). Limit to the top 3–5 most relevant roles.

Job Description:
{job_description}

Original Target Roles:
{original_roles}

Rewritten Target Roles:
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        new_roles = response.choices[0].message.content.strip()
        return {"rewritten": new_roles}

    except Exception as e:
        return {"error": str(e)}
