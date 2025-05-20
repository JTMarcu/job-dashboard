# job-dashboard/pages/1_Build_Resume.py

import streamlit as st
import pandas as pd
import os
from resume.generate_pdf import create_ats_resume_pdf

st.set_page_config(page_title="Build Resume", layout="wide")
st.title("Build Your Resume")

st.markdown("Use this form to generate an ATS-ready resume PDF from your own inputs.")

# --- Upload Existing CSV (Optional) ---
st.markdown("#### Optional: Upload an Existing Resume CSV")
uploaded_file = st.file_uploader("Upload resume_data.csv", type=["csv"])

if uploaded_file:
    try:
        uploaded_df = pd.read_csv(uploaded_file)
        st.success("Loaded previous resume data.")
    except Exception as e:
        st.error(f"Error reading uploaded file: {e}")
        uploaded_df = None
else:
    uploaded_df = None

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
def get_field(subsection):
    if uploaded_df is not None:
        result = uploaded_df[(uploaded_df["section"] == "personal_info") & (uploaded_df["subsection"] == subsection)]
        return result["content"].values[0] if not result.empty else ""
    return ""

name = st.text_input("Full Name", value=get_field("name"))
location = st.text_input("Location", value=get_field("location"))
email = st.text_input("Email", value=get_field("email"))
phone = st.text_input("Phone", value=get_field("phone"))
linkedin = st.text_input("LinkedIn URL", value=get_field("linkedin"))
github = st.text_input("GitHub URL", value=get_field("github"))
portfolio = st.text_input("Portfolio URL", value=get_field("portfolio"))
target_roles = st.text_input("Target Roles (comma-separated)", value=get_field("target_roles"))

# Collect rows for DataFrame
rows = []
rows.append({"section": "personal_info", "subsection": "name", "content": name})
rows.append({"section": "personal_info", "subsection": "target_roles", "content": target_roles})
for label, val in [("email", email), ("phone", phone), ("location", location),
                   ("linkedin", linkedin), ("github", github), ("portfolio", portfolio)]:
    if val:
        rows.append({"section": "personal_info", "subsection": label, "content": val})

# Optional Sections
if include_summary:
    st.subheader("Professional Summary")
    summary_val = ""
    if uploaded_df is not None:
        summary_section = uploaded_df[uploaded_df["section"] == "professional_summary"]
        if not summary_section.empty:
            summary_val = summary_section["content"].values[0]
    summary = st.text_area("Write 2–4 sentences about your strengths and interests", value=summary_val)
    rows.append({"section": "professional_summary", "subsection": "", "content": summary})

if include_skills:
    st.subheader("Technical Skills")
    skills_editor = st.data_editor(
        uploaded_df.query("section == 'technical_skills'")[["subsection", "content"]]
        if uploaded_df is not None and "technical_skills" in uploaded_df["section"].values
        else pd.DataFrame(columns=["subsection", "content"]),
        num_rows="dynamic",
        use_container_width=True,
        key="skills_editor"
    )
    for _, row in skills_editor.iterrows():
        if row["content"]:
            rows.append({
                "section": "technical_skills",
                "subsection": row["subsection"] if pd.notnull(row["subsection"]) else "",
                "content": row["content"]
            })

if include_work:
    st.subheader("Work Experience")
    work_editor = st.data_editor(
        uploaded_df.query("section == 'professional_experience'")[["subsection", "content"]]
        if uploaded_df is not None and "professional_experience" in uploaded_df["section"].values
        else pd.DataFrame(columns=["subsection", "content"]),
        num_rows="dynamic",
        use_container_width=True,
        key="work_editor"
    )
    for _, row in work_editor.iterrows():
        if row["content"]:
            rows.append({"section": "professional_experience", "subsection": row["subsection"], "content": row["content"]})

if include_projects:
    st.subheader("Projects")
    proj_editor = st.data_editor(
        uploaded_df.query("section == 'projects'")[["subsection", "content"]]
        if uploaded_df is not None and "projects" in uploaded_df["section"].values
        else pd.DataFrame(columns=["subsection", "content"]),
        num_rows="dynamic",
        use_container_width=True,
        key="proj_editor"
    )
    for _, row in proj_editor.iterrows():
        if row["content"]:
            rows.append({"section": "projects", "subsection": row["subsection"], "content": row["content"]})

if include_edu:
    st.subheader("Education")
    edu_editor = st.data_editor(
        uploaded_df.query("section == 'education'")[["subsection", "content"]]
        if uploaded_df is not None and "education" in uploaded_df["section"].values
        else pd.DataFrame(columns=["subsection", "content"]),
        num_rows="dynamic",
        use_container_width=True,
        key="edu_editor"
    )
    for _, row in edu_editor.iterrows():
        if row["content"]:
            rows.append({"section": "education", "subsection": row["subsection"], "content": row["content"]})

if include_certs:
    st.subheader("Certifications")
    cert_editor = st.data_editor(
        uploaded_df.query("section == 'certifications'")[["subsection", "content"]]
        if uploaded_df is not None and "certifications" in uploaded_df["section"].values
        else pd.DataFrame(columns=["subsection", "content"]),
        num_rows="dynamic",
        use_container_width=True,
        key="cert_editor"
    )
    for _, row in cert_editor.iterrows():
        if row["content"]:
            rows.append({"section": "certifications", "subsection": row["subsection"], "content": row["content"]})

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