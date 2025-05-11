#!/bin/bash

echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting MCP server in background..."
uvicorn mcp_server.server:app --reload &

sleep 2

echo "Starting Streamlit dashboard..."
streamlit run app.py
