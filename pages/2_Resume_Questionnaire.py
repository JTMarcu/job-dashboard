# job-dashboard/pages/2_Resume_Questionnaire.py

import streamlit as st
import pandas as pd
import os
from resume.questionnaire import parse_resume_questionnaire
from resume.generate_pdf import create_ats_resume_pdf

st.set_page_config(page_title="Resume Questionnaire", layout="wide")
st.title("Resume Questionnaire")

st.markdown("""
Paste your structured resume text below using this format:

```
**Personal Info**
Name | Jane Doe
Email | jane@example.com
Location | San Diego, CA
Target Roles | Data Analyst, BI Developer

**Professional Summary**
Data professional with experience in dashboards, forecasting, and workflow automation.

**Technical Skills**
- Python | Pandas, NumPy
- Tools | Tableau, Power BI

**Professional Experience**
Company | ABC Corp
Title | Data Analyst
Years | 2021–2023
- Built KPI dashboards
- Automated Excel reporting

**Projects**
Project | Resume Generator
- Built resume PDF tool using pandas + ReportLab
```
""")

user_input = st.text_area("Paste your resume questionnaire here:", height=400)

if user_input.strip():
    try:
        df = parse_resume_questionnaire(user_input)
        st.success("Parsed successfully!")
        st.dataframe(df)

        # CSV download
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv_data, file_name="resume_data.csv", mime="text/csv")

        # PDF generation
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Generate ATS PDF"):
                os.makedirs("exports", exist_ok=True)
                csv_path = "exports/questionnaire_resume.csv"
                pdf_path = "exports/resume_output.pdf"
                df.to_csv(csv_path, index=False)
                create_ats_resume_pdf(csv_path, pdf_path)
                with open(pdf_path, "rb") as f:
                    st.download_button("Download PDF", f, file_name="resume_output.pdf", mime="application/pdf")

    except Exception as e:
        st.error(f"Failed to parse input: {e}")
else:
    st.info("Waiting for input...")
