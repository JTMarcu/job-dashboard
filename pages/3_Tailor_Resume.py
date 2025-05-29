# pages/3_Tailor_Resume.py

import streamlit as st
import pandas as pd
import os
from utils.profile_loader import load_user_profile
from utils.resume_rewriter import full_resume_rewriter, sanitize_resume_blocks

st.set_page_config(page_title="Tailor Resume to Job", layout="wide")
st.title("Tailor Your Resume for Any Job")

# --- Load active profile and master resume ---
if "active_profile" not in st.session_state:
    st.warning("Please select a user profile before continuing.")
    st.stop()

profile_name = st.session_state["active_profile"]
profile = load_user_profile(f"users/{profile_name}.json")
master_resume_path = f"users/{profile_name}_master_resume.csv"

if not os.path.exists(master_resume_path):
    st.error(f"Master resume not found for {profile_name}. Please upload it first in the profile page.")
    st.stop()

# --- UI: Paste job description ---
st.subheader("Step 1: Paste the Job Description")
job_description = st.text_area(
    "Paste the full job description below:",
    height=280,
    placeholder="Paste job posting or requirements here..."
)

# --- Tailor Resume Button ---
st.subheader("Step 2: Generate Tailored Resume")
if st.button("Tailor Resume", disabled=not job_description.strip()):
    with st.spinner("Tailoring your resume to match the job..."):

        # Load master resume as list of dict blocks
        df_master = pd.read_csv(master_resume_path)
        resume_rows = df_master.to_dict(orient="records")

        # --- Call Llama3 (Ollama) to tailor resume ---
        result = full_resume_rewriter(job_description, resume_rows)
        tailored_blocks = result.get("rewritten_blocks", None)
        if isinstance(tailored_blocks, str):
            try:
                tailored_blocks = eval(tailored_blocks)
            except Exception:
                st.error("LLM output parse error. Try again or check server logs.")
                st.stop()

        # --- Python post-processing for strict resume rules ---
        tailored_blocks = sanitize_resume_blocks(tailored_blocks, resume_rows)
        df_tailored = pd.DataFrame([
            {
                "section": b.get("section", "").strip(),
                "subsection": b.get("subsection", "").strip(),
                "content": b.get("content", "").strip(),
            }
            for b in tailored_blocks
            if b.get("section") and b.get("content")
        ])

        # --- Show preview as table ---
        st.success("Tailored resume generated below! Review, then download or send to builder.")
        st.dataframe(df_tailored, use_container_width=True, hide_index=True)

        # --- Download CSV and send to 2_Create_Resume.py ---
        st.download_button(
            "⬇️ Download Tailored CSV",
            df_tailored.to_csv(index=False),
            file_name="tailored_resume.csv"
        )

        # Set session state so user can continue in 2_Create_Resume.py
        st.session_state["df_master"] = df_tailored.copy()
        st.markdown(
            """
            ### Next Step:
            [Go to Resume Builder](2_Create_Resume.py) to edit or export your tailored resume as PDF!
            """
        )

else:
    st.info("Paste a job description and click **Tailor Resume** to generate your tailored resume.")