# mcp_server/server.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from mcp_server.tools.fetch_job_postings import fetch_job_postings


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
