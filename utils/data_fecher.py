# utils/data_fetcher.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000")

def call_mcp_tool(tool_name, payload={}):
    url = f"{MCP_SERVER_URL}/tools/{tool_name}/invoke"
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()
