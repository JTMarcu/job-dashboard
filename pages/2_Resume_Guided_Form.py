import streamlit as st
import pandas as pd
import os
import csv
from resume.generate_pdf import create_ats_resume_pdf

st.set_page_config(page_title="Guided Resume Builder", layout="wide")
st.title("🧭 Guided Resume Builder")

# --- Upload optional ---
uploaded = st.file_uploader("📤 Upload a resume CSV (optional)", type="csv")
df_master = pd.read_csv(uploaded, quoting=csv.QUOTE_MINIMAL) if uploaded else pd.DataFrame(columns=["section", "subsection", "content"])
rows = []

def group_blocks(df, section):
    grouped = []
    for sub in df[df.section == section].subsection.unique():
        merged = "\n".join(df[(df.section == section) & (df.subsection == sub)].content.tolist())
        lines = [line for line in merged.split("\n") if line.strip()]
        grouped.append((sub, lines))
    return grouped

def get_val(sec, sub):
    match = df_master[(df_master.section == sec) & (df_master.subsection == sub)]
    return match.content.values[0] if not match.empty else ""

# --- Personal Info ---
st.header("👤 Personal Info")
name = st.text_input("Full Name", get_val("personal_info", "name"))
location = st.text_input("Location", get_val("personal_info", "location"))
email = st.text_input("Email", get_val("personal_info", "email"))
phone = st.text_input("Phone", get_val("personal_info", "phone"))
linkedin = st.text_input("LinkedIn", get_val("personal_info", "linkedin"))
github = st.text_input("GitHub", get_val("personal_info", "github"))
portfolio = st.text_input("Portfolio", get_val("personal_info", "portfolio"))
rows += [
    {"section": "personal_info", "subsection": "name", "content": name},
    {"section": "personal_info", "subsection": "location", "content": location},
    {"section": "personal_info", "subsection": "email", "content": email},
    {"section": "personal_info", "subsection": "phone", "content": phone},
    {"section": "personal_info", "subsection": "linkedin", "content": linkedin},
    {"section": "personal_info", "subsection": "github", "content": github},
    {"section": "personal_info", "subsection": "portfolio", "content": portfolio},
]

# --- Target Roles ---
st.header("🎯 Target Roles")
roles = st.text_input("What roles are you targeting? (comma-separated)", get_val("personal_info", "target_roles"))
rows.append({"section": "personal_info", "subsection": "target_roles", "content": roles})

# --- Summary ---
st.header("📝 Professional Summary")
summary = st.text_area("Write a 2–4 sentence summary of your strengths and interests", get_val("professional_summary", "summary"), height=180)
rows.append({"section": "professional_summary", "subsection": "summary", "content": summary})

# --- Skills ---
st.header("🧠 Technical Skills")
skills_df = df_master[df_master.section == "technical_skills"][['subsection', 'content']].copy() if not df_master.empty else pd.DataFrame([{"subsection": "Programming Languages", "content": "Python, SQL"}])
skills_df["content"] = skills_df["content"].str.replace(" \| ", ", ", regex=False)
edited = st.data_editor(skills_df, num_rows="dynamic", use_container_width=True)
for _, row in edited.iterrows():
    pipe = " | ".join([s.strip() for s in row["content"].split(",")])
    rows.append({"section": "technical_skills", "subsection": row["subsection"], "content": pipe})

# --- Experience ---
st.header("💼 Professional Experience")
exp_blocks = group_blocks(df_master, "professional_experience") if not df_master.empty else []
st.number_input("How many jobs do you want to add?", min_value=1, max_value=20, value=max(1, len(exp_blocks)), step=1, key="exp_count")

for i, (sub, lines) in enumerate(exp_blocks):
    header = lines[0] if lines else ""
    try:
        title, company, dates = [s.strip() for s in header.replace("**", "").split("|")]
    except:
        title, company, dates = "", "", ""
    bullets = lines[1:]
    with st.expander(f"Job #{i+1}"):
        title = st.text_input("Job Title", title, key=f"job_title_{i}")
        company = st.text_input("Company", company, key=f"employer_{i}")
        dates = st.text_input("Dates", dates, key=f"job_dates_{i}")
        desc = st.text_area("Description", "\n".join(bullets), key=f"job_desc_{i}", height=180)
        block = f"**{title} | {company} | {dates}**\n{desc}"
        rows.append({"section": "professional_experience", "subsection": sub, "content": block})

# --- Certifications ---
st.header("📜 Certifications")
cert_blocks = group_blocks(df_master, "certifications") if not df_master.empty else []
st.number_input("How many certifications do you want to add?", min_value=1, max_value=20, value=max(1, len(cert_blocks)), step=1, key="cert_count")

for i, (sub, lines) in enumerate(cert_blocks):
    cert = lines[0] if lines else ""
    title, date = (cert.split("|") + [""])[:2]
    with st.expander(f"Certificate #{i+1}"):
        title = st.text_input("Certificate Title", title.strip(), key=f"cert_title_{i}")
        date = st.text_input("Completion Date", date.strip(), key=f"cert_date_{i}")
        rows.append({"section": "certifications", "subsection": sub, "content": f"{title.strip()} | {date.strip()}"})

# --- Education ---
st.header("🎓 Education")
edu_blocks = group_blocks(df_master, "education") if not df_master.empty else []
st.number_input("How many education entries do you want to add?", min_value=1, max_value=10, value=max(1, len(edu_blocks)), step=1, key="edu_count")

for i, (sub, lines) in enumerate(edu_blocks):
    header = lines[0] if lines else ""
    try:
        degree, school, date = [s.strip() for s in header.replace("**", "").split("|")]
    except:
        degree, school, date = "", "", ""
    notes = lines[1:]
    with st.expander(f"Education #{i+1}"):
        degree = st.text_input("What did you earn?", degree, key=f"degree_{i}")
        school = st.text_input("Where?", school, key=f"school_{i}")
        date = st.text_input("When?", date, key=f"date_{i}")
        notes_val = st.text_area("(Optional) Highlights or focus area", "\n".join(notes), key=f"ed_notes_{i}")
        full = f"**{degree} | {school} | {date}**"
        if notes_val.strip():
            full += "\n" + notes_val
        rows.append({"section": "education", "subsection": sub, "content": full})

# --- Projects ---
st.header("📁 Projects")
proj_blocks = group_blocks(df_master, "projects") if not df_master.empty else []
st.number_input("How many projects do you want to add?", min_value=1, max_value=30, value=max(1, len(proj_blocks)), step=1, key="proj_count")

for i, (sub, lines) in enumerate(proj_blocks):
    header = lines[0] if lines else ""
    title = header.replace("**", "").strip()
    bullets = lines[1:]
    with st.expander(f"Project #{i+1}"):
        title = st.text_input("Project Title", title, key=f"proj_title_{i}")
        desc = st.text_area("Project Description", "\n".join(bullets), key=f"proj_desc_{i}", height=160)
        full_block = f"**{title}**\n{desc}"
        rows.append({"section": "projects", "subsection": sub, "content": full_block})

# --- Output ---
st.header("📄 Generate Resume")
df_out = pd.DataFrame(rows)
col1, col2 = st.columns([1, 2])

with col1:
    st.download_button("⬇️ Download CSV", df_out.to_csv(index=False).encode("utf-8"), file_name="resume_data.csv")

with col2:
    if st.button("Generate ATS PDF"):
        os.makedirs("exports", exist_ok=True)
        df_out.to_csv("exports/generated_resume.csv", index=False)
        create_ats_resume_pdf("exports/generated_resume.csv", "exports/resume_output.pdf")
        with open("exports/resume_output.pdf", "rb") as f:
            st.download_button("⬇️ Download PDF", f, file_name="resume_output.pdf", mime="application/pdf")
