import streamlit as st
import pandas as pd
import json
import os
import csv
import unicodedata
from resume.generate_pdf import create_ats_resume_pdf

st.set_page_config(page_title="Guided Resume Builder", layout="wide")
st.title("🧭 Guided Resume Builder")

def normalize_text(text):
    return unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode("ascii")

def group_blocks(df, section):
    grouped = []
    for sub in df[df.section == section].subsection.unique():
        merged = "\n".join(df[(df.section == section) & (df.subsection == sub)].content.tolist())
        lines = [line for line in merged.split("\n") if line.strip()]
        if lines:
            grouped.append((sub, lines))
    return grouped

def get_val(df, sec, sub):
    match = df[(df.section == sec) & (df.subsection == sub)]
    return match.content.values[0] if not match.empty else ""

uploaded = st.file_uploader("\U0001F4E4 Upload a resume (CSV or JSON)", type=["csv", "json"])
if uploaded:
    if uploaded.name.endswith(".json"):
        df_master = pd.DataFrame(json.load(uploaded))
        st.success("JSON uploaded and loaded.")
    else:
        df_master = pd.read_csv(uploaded, quoting=csv.QUOTE_MINIMAL)
        st.success("CSV uploaded and loaded.")
else:
    df_master = pd.DataFrame(columns=["section", "subsection", "content"])
    st.info("No file uploaded. Starting with a blank resume.")

rows = []

st.header("\U0001F464 Personal Info")
name = st.text_input("Full Name", get_val(df_master, "personal_info", "name"))
location = st.text_input("Location", get_val(df_master, "personal_info", "location"))
email = st.text_input("Email", get_val(df_master, "personal_info", "email"))
phone = st.text_input("Phone", get_val(df_master, "personal_info", "phone"))
linkedin = st.text_input("LinkedIn", get_val(df_master, "personal_info", "linkedin"))
github = st.text_input("GitHub", get_val(df_master, "personal_info", "github"))
portfolio = st.text_input("Portfolio", get_val(df_master, "personal_info", "portfolio"))
rows += [
    {"section": "personal_info", "subsection": "name", "content": name},
    {"section": "personal_info", "subsection": "location", "content": location},
    {"section": "personal_info", "subsection": "email", "content": email},
    {"section": "personal_info", "subsection": "phone", "content": phone},
    {"section": "personal_info", "subsection": "linkedin", "content": linkedin},
    {"section": "personal_info", "subsection": "github", "content": github},
    {"section": "personal_info", "subsection": "portfolio", "content": portfolio},
]

st.header("\U0001F3AF Target Roles")
roles = st.text_input("What roles are you targeting?", get_val(df_master, "personal_info", "target_roles"))
rows.append({"section": "personal_info", "subsection": "target_roles", "content": roles})

st.header("\U0001F4DD Professional Summary")
summary = st.text_area("Write a 2–4 sentence summary of your strengths and interests", get_val(df_master, "professional_summary", "summary"), height=180)
if summary.strip():
    rows.append({"section": "professional_summary", "subsection": "summary", "content": summary})

st.header("\U0001F9E0 Technical Skills")
skills_df = df_master[df_master.section == "technical_skills"][["subsection", "content"]].copy()
skills_df["content"] = skills_df["content"].str.replace(r" \| ", ", ", regex=False)
skills_editor = st.data_editor(skills_df if not skills_df.empty else pd.DataFrame([
    {"subsection": "Programming Languages", "content": "Python, SQL"},
]), num_rows="dynamic", use_container_width=True)

for _, row in skills_editor.iterrows():
    if row["subsection"] and row["content"].strip():
        pipe = " | ".join([s.strip() for s in str(row["content"]).split(",")])
        rows.append({"section": "technical_skills", "subsection": row["subsection"], "content": pipe})

st.header("\U0001F4BC Professional Experience")
exp_blocks = group_blocks(df_master, "professional_experience")
exp_count = st.number_input("How many jobs?", min_value=1, max_value=10, value=max(1, len(exp_blocks)), step=1)

for i in range(exp_count):
    if i < len(exp_blocks):
        sub, lines = exp_blocks[i]
        header = lines[0] if lines else ""
        bullets = lines[1:]
        try:
            title, company, dates = [s.strip() for s in header.replace("**", "").split("|")]
        except:
            title, company, dates = "", "", ""
    else:
        sub, title, company, dates, bullets = f"job_{i}", "", "", "", []

    with st.expander(f"Job #{i+1}"):
        title = st.text_input("Job Title", title, key=f"job_title_{i}")
        company = st.text_input("Company", company, key=f"employer_{i}")
        dates = st.text_input("Dates", dates, key=f"job_dates_{i}")
        desc = st.text_area("Description", "\n".join(bullets), key=f"job_desc_{i}", height=180)
        if title and company and dates:
            block = f"**{title} | {company} | {dates}**"
            if desc.strip():
                bullets_cleaned = "\n" + "\n".join(
                    line.strip() if line.strip().startswith("•") else f"• {line.strip()}"
                    for line in desc.strip().splitlines() if line.strip()
                )
                block += bullets_cleaned
            rows.append({"section": "professional_experience", "subsection": sub, "content": block})

st.header("\U0001F4DC Certifications")
cert_blocks = group_blocks(df_master, "certifications")
cert_count = st.number_input("How many certifications?", min_value=1, max_value=20, value=max(1, len(cert_blocks)), step=1)

for i in range(cert_count):
    if i < len(cert_blocks):
        sub, lines = cert_blocks[i]
        cert = lines[0] if lines else ""
        title, date = (cert.split("|") + [""])[:2]
    else:
        sub, title, date = f"cert_{i}", "", ""
    with st.expander(f"Certificate #{i+1}"):
        title = st.text_input("Certificate Title", title.strip(), key=f"cert_title_{i}")
        date = st.text_input("Completion Date", date.strip(), key=f"cert_date_{i}")
        if title and date:
            rows.append({"section": "certifications", "subsection": sub, "content": f"{title.strip()} | {date.strip()}"})

st.header("\U0001F393 Education")
edu_blocks = group_blocks(df_master, "education")
edu_count = st.number_input("How many education entries?", min_value=1, max_value=10, value=max(1, len(edu_blocks)), step=1)

for i in range(edu_count):
    if i < len(edu_blocks):
        sub, lines = edu_blocks[i]
        header = lines[0] if lines else ""
        notes = lines[1:]
        try:
            degree, school, date = [s.strip() for s in header.replace("**", "").split("|")]
        except:
            degree, school, date = "", "", ""
    else:
        sub, degree, school, date, notes = f"edu_{i}", "", "", "", []

    with st.expander(f"Education #{i+1}"):
        degree = st.text_input("Degree", degree, key=f"degree_{i}")
        school = st.text_input("School", school, key=f"school_{i}")
        date = st.text_input("Date", date, key=f"ed_date_{i}")
        notes_val = st.text_area("Highlights (optional)", "\n".join(notes), key=f"ed_notes_{i}")
        if degree and school and date:
            block = f"**{degree} | {school} | {date}**"
            if notes_val.strip():
                block += "\n" + "\n".join(
                    line.strip() if line.strip().startswith("•") else f"• {line.strip()}"
                    for line in notes_val.strip().splitlines() if line.strip()
                )
            rows.append({"section": "education", "subsection": sub, "content": block})

st.header("\U0001F4C1 Projects")
proj_blocks = group_blocks(df_master, "projects")
proj_count = st.number_input("How many projects?", min_value=1, max_value=30, value=max(1, len(proj_blocks)), step=1)

for i in range(proj_count):
    if i < len(proj_blocks):
        sub, lines = proj_blocks[i]
        header = lines[0] if lines else ""
        bullets = lines[1:]
        title = header.replace("**", "").strip()
    else:
        sub, title, bullets = f"proj_{i}", "", []

    with st.expander(f"Project #{i+1}"):
        title = st.text_input("Project Title", title, key=f"proj_title_{i}")
        desc = st.text_area("Description", "\n".join(bullets), height=160, key=f"proj_desc_{i}")
        if title.strip():
            block = f"**{title}**"
            if desc.strip():
                block += "\n" + "\n".join(
                    line.strip() if line.strip().startswith("•") else f"• {line.strip()}"
                    for line in desc.strip().splitlines() if line.strip()
                )
            rows.append({"section": "projects", "subsection": sub, "content": block})

st.header("\U0001F4C4 Export Resume")
df_out = pd.DataFrame([r for r in rows if str(r["content"]).strip()])
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    st.download_button("⬇️ CSV", df_out.to_csv(index=False).encode("utf-8"), file_name="resume_data.csv")

with col2:
    st.download_button("⬇️ JSON", json.dumps(df_out.to_dict(orient="records"), indent=2).encode("utf-8"), file_name="resume_data.json")

with col3:
    if st.button("Generate ATS PDF"):
        os.makedirs("exports", exist_ok=True)
        df_out.to_csv("exports/generated_resume.csv", index=False)
        create_ats_resume_pdf("exports/generated_resume.csv", "exports/resume_output.pdf")
        with open("exports/resume_output.pdf", "rb") as f:
            st.download_button("⬇️ Download PDF", f, file_name="resume_output.pdf", mime="application/pdf")