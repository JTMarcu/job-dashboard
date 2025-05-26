# pages/3_Tailor_Resume.py

import streamlit as st
import pandas as pd
import os
import csv
import ast
import json
from utils.data_fetcher import call_mcp_tool
from utils.profile_loader import load_user_profile

st.set_page_config(page_title="Tailor Resume", layout="wide")
st.title("Tailor Resume")

if "active_profile" not in st.session_state:
    st.warning("Please select a user profile before continuing.")
    st.stop()

profile_name = st.session_state["active_profile"]
profile_data = load_user_profile(profile_name)
master_resume_path = os.path.join("users", f"{profile_name}_master_resume.csv")

uploaded = st.file_uploader("Upload your resume (CSV)", type=["csv"])
use_master = False
if os.path.exists(master_resume_path):
    if st.button("Use Master Resume"):
        use_master = True

if uploaded:
    resume_df = pd.read_csv(uploaded, quoting=csv.QUOTE_MINIMAL)
elif use_master:
    resume_df = pd.read_csv(master_resume_path, quoting=csv.QUOTE_MINIMAL)
    st.success("Loaded Master Resume.")
else:
    st.info("Please upload a resume CSV or use your Master Resume to get started.")
    st.stop()

resume_rows = resume_df.to_dict(orient="records")

st.subheader("Paste Job Description")
job_desc = st.text_area("Job Description", height=300)

engine = st.radio("Choose model engine:", ["ollama", "openai"], index=0, horizontal=True)

if st.button("Rewrite Entire Resume") and job_desc.strip():
    tool_name = "full_resume_rewriter_openai" if engine == "openai" else "full_resume_rewriter"
    with st.spinner(f"Rewriting resume with {engine.upper()}..."):
        response = call_mcp_tool(tool_name, {
            "job_description": job_desc,
            "resume_rows": resume_rows
        })

    if "error" in response:
        st.error(response["error"])
    elif "rewritten_blocks" in response:
        rewritten_output = response["rewritten_blocks"]
        st.success("Resume rewritten successfully.")
        st.code(rewritten_output, language="json")

        try:
            parsed = ast.literal_eval(rewritten_output)
            parsed_df = pd.DataFrame(parsed)
            st.download_button("Download Rewritten CSV", parsed_df.to_csv(index=False).encode("utf-8"), file_name="rewritten_resume.csv")
        except Exception as e:
            st.warning("Could not parse response to CSV format. You may copy manually or refine your prompt.")
            st.text_area("Raw Output", rewritten_output, height=300)