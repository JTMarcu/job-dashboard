# mcp_server/server.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from tools.tool_a import do_something

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/tools/tool_a/invoke")
async def invoke_tool_a(request: Request):
    data = await request.json()
    return do_something(**data)
