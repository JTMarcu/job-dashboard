# pages/1_Build_Resume.py

import streamlit as st
import pandas as pd
import os
from resume.generate_pdf import create_ats_resume_pdf

st.set_page_config(page_title="Build Resume", layout="wide")
st.title("Build Your Resume")

st.markdown("Use this form to generate an ATS-ready resume PDF from your own inputs.")

# --- Section Toggles ---
st.sidebar.header("Choose Sections to Include")
include_summary = st.sidebar.checkbox("Professional Summary", True)
include_skills = st.sidebar.checkbox("Technical Skills", True)
include_work = st.sidebar.checkbox("Work Experience", True)
include_projects = st.sidebar.checkbox("Projects", True)
include_edu = st.sidebar.checkbox("Education", False)
include_certs = st.sidebar.checkbox("Certifications", False)

# --- Basic Info ---
st.subheader("Personal Info")
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone")
location = st.text_input("Location")
linkedin = st.text_input("LinkedIn URL")
github = st.text_input("GitHub URL")
portfolio = st.text_input("Portfolio URL")
target_roles = st.text_input("Target Roles (comma-separated)")

# Collect rows for DataFrame
rows = []

# Required: Personal Info
rows.append({"section": "personal_info", "subsection": "name", "content": name})
rows.append({"section": "personal_info", "subsection": "target_roles", "content": target_roles})
for label, val in [("email", email), ("phone", phone), ("location", location),
                   ("linkedin", linkedin), ("github", github), ("portfolio", portfolio)]:
    if val:
        rows.append({"section": "personal_info", "subsection": label, "content": val})

# Optional Sections
if include_summary:
    st.subheader("Professional Summary")
    summary = st.text_area("Write 2–4 sentences about your strengths and interests")
    rows.append({"section": "professional_summary", "subsection": "", "content": summary})

if include_skills:
    st.subheader("Technical Skills")
    skills = st.text_area("Comma-separated skills", placeholder="Python, SQL, Tableau...")
    rows.append({"section": "technical_skills", "subsection": "", "content": skills})

if include_work:
    st.subheader("Work Experience")
    jobs = st.data_editor(
        pd.DataFrame(columns=["subsection", "content"]),
        num_rows="dynamic",
        use_container_width=True,
        key="work_editor"
    )
    for _, row in jobs.iterrows():
        if row["content"]:
            rows.append({
                "section": "professional_experience",
                "subsection": row["subsection"],
                "content": row["content"]
            })

if include_projects:
    st.subheader("Projects")
    projects = st.data_editor(
        pd.DataFrame(columns=["subsection", "content"]),
        num_rows="dynamic",
        use_container_width=True,
        key="proj_editor"
    )
    for _, row in projects.iterrows():
        if row["content"]:
            rows.append({
                "section": "projects",
                "subsection": row["subsection"],
                "content": row["content"]
            })

if include_edu:
    st.subheader("Education")
    edu = st.data_editor(
        pd.DataFrame(columns=["subsection", "content"]),
        num_rows="dynamic",
        use_container_width=True,
        key="edu_editor"
    )
    for _, row in edu.iterrows():
        if row["content"]:
            rows.append({
                "section": "education",
                "subsection": row["subsection"],
                "content": row["content"]
            })

if include_certs:
    st.subheader("Certifications")
    certs = st.data_editor(
        pd.DataFrame(columns=["subsection", "content"]),
        num_rows="dynamic",
        use_container_width=True,
        key="cert_editor"
    )
    for _, row in certs.iterrows():
        if row["content"]:
            rows.append({
                "section": "certifications",
                "subsection": row["subsection"],
                "content": row["content"]
            })

# --- Build + Download ---
df = pd.DataFrame(rows)

st.subheader("Generate Resume")

col1, col2 = st.columns([1, 2])
with col1:
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv_data, file_name="resume_data.csv", mime="text/csv")

with col2:
    if st.button("Generate PDF"):
        os.makedirs("exports", exist_ok=True)
        csv_path = "exports/generated_resume.csv"
        pdf_path = "exports/resume_output.pdf"
        df.to_csv(csv_path, index=False)
        create_ats_resume_pdf(csv_path, pdf_path)
        with open(pdf_path, "rb") as f:
            st.download_button("Download PDF", f, file_name="resume_output.pdf", mime="application/pdf")
