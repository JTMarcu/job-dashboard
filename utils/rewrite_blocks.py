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
You are a resume assistant. Rewrite the candidate's list of target roles to align with the job description.

Return exactly 4 roles separated by ` | `, highly tailored to the job.

Job Description:
{job_description}

Original Roles:
{original_roles}

Rewritten Roles:
"""
    return run_ollama(prompt)


def rewrite_summary(job_description, original_summary):
    prompt = f"""
You are a resume assistant. Rewrite the candidate's professional summary to better match the job description.

Write 3–4 complete sentences. Emphasize analytical thinking, dashboards, strategy, and automation.

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
You are a resume assistant. Rewrite the bullet points below to better align with the job description.

Job Header:
{header}

Job Description:
{job_description}

Original Bullets:
{bullet_text}

Rules:
- Return exactly {limit} bullets
- Short, punchy, and achievement-driven
- Each bullet must start with •

Rewritten Bullets:
"""
    return run_ollama(prompt)