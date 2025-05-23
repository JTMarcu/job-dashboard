# mcp_server/server.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from mcp_server.tools.fetch_job_postings import fetch_job_postings
from mcp_server.tools.job_matcher import match_resume_to_job
from mcp_server.tools.rewrite_resume_bullets import rewrite_resume_bullets
from mcp_server.tools.rewrite_target_roles import rewrite_target_roles

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

@app.post("/tools/job_matcher/invoke")
async def invoke_job_matcher(request: Request):
    data = await request.json()
    return match_resume_to_job(**data)

@app.post("/tools/rewrite_resume_bullets/invoke")
async def invoke_rewriter(request: Request):
    data = await request.json()
    return rewrite_resume_bullets(**data)

@app.post("/tools/rewrite_target_roles/invoke")
async def invoke_roles(request: Request):
    data = await request.json()
    return rewrite_target_roles(**data)