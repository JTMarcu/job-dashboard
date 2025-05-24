# utils/rewrite_blocks.py
import os
import requests
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

def rewrite_target_roles(job_description, original_roles):
    prompt = f"""
You are a resume assistant. Rewrite the candidate's list of target roles to align with the job description below.

Rules:
- Return exactly 4 professional roles separated by ` | `
- Roles must be highly relevant to the job

Job Description:
{job_description}

Original Roles:
{original_roles}

Rewritten Roles:
"""
    return run_ollama(prompt)

def rewrite_summary(job_description, original_summary):
    prompt = f"""
You are a resume assistant. Rewrite the candidate's professional summary to align with the job description.

Rules:
- Write 3–4 complete, polished sentences
- Emphasize data, automation, dashboards, analytics, and impact

Job Description:
{job_description}

Original Summary:
{original_summary}

Rewritten Summary:
"""
    return run_ollama(prompt)

def rewrite_bullets(job_description, header, bullets, limit):
    bullet_text = "\n".join([f"• {b}" for b in bullets if b.strip()])
    prompt = f"""
You are a resume assistant. Rewrite the bullet points to better align with the job description.

Keep this job/project header:
{header}

Job Description:
{job_description}

Original Bullets:
{bullet_text}

Rules:
- Return exactly {limit} new bullet points
- Short, punchy, achievement-focused
- Use professional tone
- Each bullet must start with `•`

Rewritten Bullets:
"""
    return run_ollama(prompt)

def rewrite_job_block(job_description, content, limit):
    lines = [l for l in content.split("\n") if l.strip()]
    header = lines[0] if lines else ""
    bullets = [l.replace("•", "").strip() for l in lines[1:]]
    rewritten = rewrite_bullets(job_description, header, bullets, limit)
    return f"{header}\n" + "\n".join(rewritten.splitlines())

def rewrite_project_block(job_description, content):
    lines = [l for l in content.split("\n") if l.strip()]
    header = lines[0] if lines else ""
    bullets = [l.replace("•", "").strip() for l in lines[1:]]
    rewritten = rewrite_bullets(job_description, header, bullets, 2)
    return f"{header}\n" + "\n".join(rewritten.splitlines())