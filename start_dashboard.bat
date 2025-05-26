@echo off
echo Starting MCP server...
start cmd /k "call venv\Scripts\activate && uvicorn mcp_server.server:app --reload"

timeout /t 3 >nul

echo Starting Streamlit app...
start cmd /k "call venv\Scripts\activate && streamlit run 0_Select_profile.py"