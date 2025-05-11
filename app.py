# app.py

import streamlit as st
from utils.data_fetcher import call_mcp_tool
from modules.dashboard_template import display_dashboard
import json

st.set_page_config(page_title="MCP Dashboard Template", layout="wide")
st.title("MCP Dashboard Template")

tool_name = st.text_input("Tool name:", value="tool_a")
tool_payload = st.text_area("Tool input (JSON):", value='{"input1": "value1"}', height=100)

if st.button("Run Tool"):
    try:
        payload = json.loads(tool_payload)
        result = call_mcp_tool(tool_name, payload)
        display_dashboard(result)
    except Exception as e:
        st.error(f"Error: {e}")
