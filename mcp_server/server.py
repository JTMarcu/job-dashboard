# mcp_server/server.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from mcp_server.tools.fetch_job_postings import fetch_job_postings
from mcp_server.tools.resume_rewriter import full_resume_rewriter
from mcp_server.tools.full_resume_rewriter_openai import full_resume_rewriter as full_resume_rewriter_openai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/tools/fetch_job_postings/invoke")
async def invoke_job_postings(request: Request):
    data = await request.json()
    return fetch_job_postings(**data)

@app.post("/tools/full_resume_rewriter/invoke")
async def invoke_resume_rewriter(request: Request):
    data = await request.json()
    return full_resume_rewriter(**data)

@app.post("/tools/full_resume_rewriter_openai/invoke")
async def invoke_resume_rewriter_openai(request: Request):
    data = await request.json()
    return full_resume_rewriter_openai(**data)