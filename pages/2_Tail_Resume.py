# pages/2_Tail_Resume.py

import streamlit as st
import pandas as pd
import json
import csv
from utils.data_fetcher import call_mcp_tool

st.set_page_config(page_title="Tailor Resume", layout="wide")
st.title("Tailor Your Resume to a Job")

uploaded = st.file_uploader("Upload your master resume (CSV)", type=["csv"])
if not uploaded:
    st.info("Please upload your resume to continue.")
    st.stop()

# Load resume rows
resume_df = pd.read_csv(uploaded, quoting=csv.QUOTE_MINIMAL)
resume_rows = resume_df.to_dict(orient="records")

# --- Job Description Input ---
st.header("Paste a Job Description")
st.caption("Or, use 'Tailor Resume' from the job dashboard to prefill.")
job_desc = st.text_area("Job Description", height=300)

# --- Match and Display ---
if st.button("Match My Resume") and job_desc.strip():
    with st.spinner("Analyzing resume blocks vs. job description..."):
        response = call_mcp_tool("job_matcher", {
            "job_description": job_desc,
            "resume_rows": resume_rows
        })

    if "error" in response:
        st.error(response["error"])
    else:
        matches = response.get("matches", [])
        if not matches:
            st.warning("No strong matches found. Try revising your resume or job description.")
        else:
            st.success(f"{len(matches)} matching blocks found.")
            selected = []
            for i, row in enumerate(matches):
                with st.expander(f"{row['section']} / {row['subsection']}", expanded=True):
                    keep = st.checkbox("Include this block", value=True, key=f"match_{i}")
                    st.code(row["content"], language="markdown")
                    if keep:
                        selected.append(row)

            if selected:
                section_order = [
                    "personal_info",
                    "professional_summary",
                    "technical_skills",
                    "professional_experience",
                    "education",
                    "certifications",
                    "projects"
                ]

                final_rows = []
                personal_info = resume_df[resume_df.section == "personal_info"]
                summary = resume_df[resume_df.section == "professional_summary"]
                tech = resume_df[resume_df.section == "technical_skills"]
                education = resume_df[resume_df.section == "education"]
                certifications = resume_df[resume_df.section == "certifications"]
                all_experience = resume_df[resume_df.section == "professional_experience"]
                all_projects = resume_df[resume_df.section == "projects"]

                matched_df = pd.DataFrame(selected).drop_duplicates(subset=["section", "subsection"])

                # --- Rewrite bullets for matched blocks ---
                exp_counter = 0
                for i, row in matched_df.iterrows():
                    section = row["section"]
                    sub = row["subsection"]
                    content = row["content"]

                    bullet_limit = None
                    if section == "professional_experience":
                        if exp_counter == 0:
                            bullet_limit = 4
                        elif exp_counter == 1:
                            bullet_limit = 4
                        elif exp_counter == 2:
                            bullet_limit = 2
                        exp_counter += 1
                    elif section == "projects":
                        bullet_limit = 2

                    if bullet_limit:
                        try:
                            rewrite_result = call_mcp_tool("rewrite_resume_bullets", {
                                "job_description": job_desc,
                                "resume_block": content,
                                "bullet_limit": bullet_limit
                            })
                            if "rewritten" in rewrite_result:
                                matched_df.at[i, "content"] = rewrite_result["rewritten"]
                        except Exception as e:
                            st.warning(f"Bullet rewrite failed for {sub}: {e}")

                # Collect matched professional experience in original order
                matched_exp_subs = matched_df[matched_df.section == "professional_experience"]["subsection"].tolist()
                filtered_experience = all_experience[all_experience.subsection.isin(matched_exp_subs)]

                # Collect top 4 matching projects
                matched_projects = matched_df[matched_df.section == "projects"].head(4)
                filtered_projects = all_projects[all_projects.subsection.isin(matched_projects["subsection"])]

                # Replace rewritten project content
                for i, proj_row in matched_projects.iterrows():
                    filtered_projects.loc[filtered_projects.subsection == proj_row["subsection"], "content"] = proj_row["content"]

                for section in section_order:
                    if section == "personal_info":
                        final_rows.extend(personal_info.to_dict(orient="records"))
                    elif section == "professional_summary":
                        final_rows.extend(summary.to_dict(orient="records"))
                    elif section == "technical_skills":
                        final_rows.extend(tech.to_dict(orient="records"))
                    elif section == "professional_experience":
                        final_rows.extend(filtered_experience.to_dict(orient="records"))
                    elif section == "education":
                        final_rows.extend(education.to_dict(orient="records"))
                    elif section == "certifications":
                        final_rows.extend(certifications.to_dict(orient="records"))
                    elif section == "projects":
                        final_rows.extend(filtered_projects.to_dict(orient="records"))

                df_out = pd.DataFrame([r for r in final_rows if str(r["content"]).strip()])

                st.download_button("⬇️ Download Tailored CSV", df_out.to_csv(index=False).encode("utf-8"), file_name="tailored_resume.csv")
                st.markdown("---")
                st.caption("You can now upload this tailored file in the resume builder to generate a PDF.")
