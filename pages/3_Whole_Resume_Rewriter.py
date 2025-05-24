# pages/3_Whole_Resume_Rewriter.py

import streamlit as st
import pandas as pd
import csv
import json
import ast
import os
from utils.data_fetcher import call_mcp_tool

st.set_page_config(page_title="Whole Resume Rewriter", layout="wide")
st.title("Whole Resume Rewriter")

engine = st.radio("Choose model engine:", ["ollama", "openai"], index=0, horizontal=True)

uploaded = st.file_uploader("Upload your master resume (CSV)", type=["csv"])
if not uploaded:
    st.info("Please upload your resume CSV to get started.")
    st.stop()

# Load CSV
resume_df = pd.read_csv(uploaded, quoting=csv.QUOTE_MINIMAL)
resume_rows = resume_df.to_dict(orient="records")

st.header("Paste Job Description")
job_desc = st.text_area("Job Description", height=300)

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

        st.success("Resume rewritten! Preview below:")
        st.code(rewritten_output, language="json")

        # Attempt to parse output safely
        try:
            parsed = ast.literal_eval(rewritten_output)
            parsed_df = pd.DataFrame(parsed)
            st.download_button("⬇️ Download Rewritten CSV", parsed_df.to_csv(index=False).encode("utf-8"), file_name="rewritten_resume.csv")
        except Exception as e:
            st.warning("Could not parse response to CSV format. You may copy manually or refine your prompt.")
            st.text_area("Raw Output", rewritten_output, height=300)