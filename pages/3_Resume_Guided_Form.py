# job-dashboard/pages/3_Resume_Guided_Form.py

import streamlit as st
import pandas as pd
import os
from resume.generate_pdf import create_ats_resume_pdf

st.set_page_config(page_title="Guided Resume Form", layout="wide")
st.title("🧭 Guided Resume Builder")

st.markdown("""
Answer the questions below to generate a structured, ATS-ready resume.
Each section will guide you through the content and allow multiple entries.
""")

rows = []

# --- Personal Info ---
st.header("👤 Personal Info")
name = st.text_input("What is your full name?", placeholder="e.g. Jane Doe")
location = st.text_input("Where are you located?", placeholder="e.g. San Diego, CA")
contact_info = st.text_area("What is your contact info?", placeholder="e.g. jane@example.com, (555) 555-5555")
social_links = st.text_area("Do you have any portfolio/social links?", placeholder="e.g. linkedin.com/in/you, github.com/you")

rows.append({"section": "personal_info", "subsection": "name", "content": name})
rows.append({"section": "personal_info", "subsection": "location", "content": location})
rows.append({"section": "personal_info", "subsection": "contact", "content": contact_info})
rows.append({"section": "personal_info", "subsection": "social_links", "content": social_links})

# --- Target Roles ---
st.header("🎯 Target Roles")
roles = st.text_input("What roles are you targeting? (comma-separated)", placeholder="e.g. Data Scientist, AI Engineer")
rows.append({"section": "personal_info", "subsection": "target_roles", "content": " | ".join([r.strip() for r in roles.split(",") if r.strip()])})

# --- Professional Summary ---
st.header("📝 Professional Summary")
summary = st.text_area("Write a 2–4 sentence summary of your strengths and interests", height=180)
rows.append({"section": "professional_summary", "subsection": "", "content": summary})

# --- Technical Skills ---
st.header("🧠 Technical Skills")
st.markdown("You can add skill categories like 'Programming Languages' or 'Libraries & Frameworks', and list skills under each.")

skill_data = st.data_editor(
    pd.DataFrame([{"subsection": "Programming Languages", "content": "Python, SQL, R Programming, HTML/CSS, JavaScript"},
                  {"subsection": "Libraries & Frameworks", "content": "Pandas, NumPy, Scikit-learn, TensorFlow, Keras, PyTorch, Flask, ReportLab"}]),
    num_rows="dynamic",
    use_container_width=True,
    key="skills_editor"
)

for _, row in skill_data.iterrows():
    if row["content"]:
        pipe_formatted = " | ".join([s.strip() for s in row["content"].split(",") if s.strip()])
        rows.append({
            "section": "technical_skills",
            "subsection": row["subsection"],
            "content": pipe_formatted
        })

# --- Professional Experience ---
st.header("💼 Professional Experience")
exp_count = st.number_input("How many jobs do you want to add?", min_value=1, max_value=10, value=1, step=1)
for i in range(exp_count):
    with st.expander(f"Job #{i+1}"):
        job_title = st.text_input(f"What is your job title?", key=f"job_title_{i}")
        employer = st.text_input(f"Where did you work?", key=f"employer_{i}")
        job_dates = st.text_input(f"What were the dates?", key=f"job_dates_{i}")
        job_desc = st.text_area(f"Describe what you did (use '-' for bullet points or write a paragraph)", key=f"job_desc_{i}")

        if job_title and employer and job_dates and job_desc:
            header = f"**{job_title} | {employer} | {job_dates}**"
            rows.append({"section": "professional_experience", "subsection": employer, "content": header})
            for line in job_desc.strip().splitlines():
                if line.strip():
                    rows.append({"section": "professional_experience", "subsection": employer, "content": line.strip()})

# --- Projects ---
st.header("📁 Projects")
proj_count = st.number_input("How many projects do you want to add?", min_value=1, max_value=10, value=1, step=1)
for i in range(proj_count):
    with st.expander(f"Project #{i+1}"):
        proj_title = st.text_input("What is the name of your project?", key=f"proj_title_{i}")
        proj_desc = st.text_area("Describe it (bullets or paragraph)", key=f"proj_desc_{i}")
        if proj_title and proj_desc:
            rows.append({"section": "projects", "subsection": proj_title, "content": f"**{proj_title}**"})
            for line in proj_desc.strip().splitlines():
                if line.strip():
                    rows.append({"section": "projects", "subsection": proj_title, "content": line.strip()})

# --- Education ---
st.header("🎓 Education")
edu_count = st.number_input("How many education entries do you want to add?", min_value=1, max_value=5, value=1, step=1)
for i in range(edu_count):
    with st.expander(f"Education #{i+1}"):
        degree = st.text_input("What did you earn?", key=f"degree_{i}")
        school = st.text_input("Where?", key=f"school_{i}")
        grad = st.text_input("When?", key=f"grad_{i}")
        notes = st.text_area("(Optional) Highlights or focus area", key=f"ed_notes_{i}")
        if degree and school and grad:
            rows.append({"section": "education", "subsection": school, "content": f"**{degree} | {school} | {grad}**"})
            for line in notes.strip().splitlines():
                if line.strip():
                    rows.append({"section": "education", "subsection": school, "content": line.strip()})

# --- Certifications ---
st.header("📜 Certifications")
cert_count = st.number_input("How many certifications do you want to add?", min_value=1, max_value=10, value=1, step=1)
for i in range(cert_count):
    with st.expander(f"Certification #{i+1}"):
        cert = st.text_input("What is the certificate title?", key=f"cert_{i}")
        cert_date = st.text_input("When was it completed?", key=f"cert_date_{i}")
        if cert and cert_date:
            rows.append({"section": "certifications", "subsection": cert, "content": f"{cert} | {cert_date}"})

# --- Output ---
st.header("📄 Generate Resume")
df = pd.DataFrame(rows)
col1, col2 = st.columns([1, 2])

with col1:
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", csv_data, file_name="resume_data.csv", mime="text/csv")

with col2:
    if st.button("Generate ATS PDF"):
        os.makedirs("exports", exist_ok=True)
        csv_path = "exports/generated_resume.csv"
        pdf_path = "exports/resume_output.pdf"
        df.to_csv(csv_path, index=False)
        create_ats_resume_pdf(csv_path, pdf_path)
        with open(pdf_path, "rb") as f:
            st.download_button("⬇️ Download PDF", f, file_name="resume_output.pdf", mime="application/pdf")
