# Job Dashboard + Resume Builder

A modular, AI-powered assistant that streamlines your entire job search—from finding roles, to building and tailoring your resume, to exporting ready-to-submit documents. Powered by **Streamlit** (UI), **FastAPI** (backend), and your choice of **local LLMs (Ollama)** or **OpenAI** for resume tailoring.

---

## Features

### 1. Explore Jobs
- Live job search via Adzuna or JSearch APIs
- Filter by title, keywords, location, posting date, and data source
- View all matching jobs or custom queries
- Click to view descriptions and begin tailoring your resume

### 2. Build Resume (Guided Form)
- Modular resume builder with Streamlit UI
- Add/edit jobs, projects, education, skills, certifications
- Upload your existing resume (CSV or JSON) for quick editing
- Download your structured resume as CSV, JSON, or ATS-optimized PDF

### 3. Tailor Resume to Any Job
- Paste any job description (or click from job results)
- Instantly rewrite your resume with local LLM (Ollama) or other LLMs (coming soon)
- Strict, ATS-friendly formatting: 3 jobs (4/4/2 bullets), up to 4 projects (2 bullets each)
- Download tailored resumes, or send directly to the builder for further editing

---

## Dynamic Profile System

- Supports **multiple user profiles**—easily switch, create, or upload via the profile selector
- Each session is *profile-aware*; resumes and job searches use active profile details (name, email, phone, links, etc.)
- Master resume saved per profile for easy reuse and exporting
- All personal info and contact fields are securely injected at runtime

---

## Tech Stack

- **Streamlit** — Fast, reactive UI for all workflows
- **FastAPI** — Modular backend for all tools and integrations
- **Ollama** (local LLM) or **OpenAI** (cloud) — for AI-powered resume rewriting
- **Pandas** / **ReportLab** — Resume data processing and PDF generation
- **Requests**, **python-dotenv** — API and environment management

---

## File Structure

```

job-dashboard/
│
├── mcp\_server/
│   ├── tools/
│   │   ├── fetch\_job\_postings.py
│   │   └── resume\_rewriter.py
│   └── server.py
│
├── modules/
│   └── dashboard\_template.py
│
├── pages/
│   ├── 1\_Explore\_Jobs.py
│   ├── 2\_Create\_Resume.py
│   └── 3\_Tailor\_Resume.py
│
├── resume/
│   └── generate\_pdf.py
│
├── tests/
│   └── test\_fetcher.py
│
├── users/
│   ├── active\_profile.json
│   ├── guest.json
│   └── user\_profile.json
│
├── utils/
│   ├── data\_fetcher.py
│   ├── profile\_loader.py
│   └── resume\_rewriter.py
│
├── .env                # <-- Leave blank or only include required API keys as variables
├── .gitignore
├── 0\_Select\_Profile.py
├── README.md
├── requirements.txt
├── setup\_env.bat
├── setup\_env.sh
├── start\_dashboard.bat
├── start\_dashboard.sh

````

---

## Coming Soon

- One-click cover letter generation (Ollama or OpenAI)
- Application tracking dashboard with export
- Resume versioning and tagging
- Smart job matching by skills and keywords
- LLM-powered interview prep

---

## Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/YOUR-USERNAME/job-dashboard.git
cd job-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure your environment variables (API keys, etc.)
cp .env.example .env
# (Or manually create .env and add required API keys. Leave blank if testing only local features.)

# 4. Start the backend (FastAPI server)
uvicorn mcp_server.server:app --reload

# 5. Start the Streamlit UI
streamlit run 0_Select_Profile.py
````

---

## Notes

* The `.env` file should be **blank by default** or include only placeholders for API keys:

  ```
  ADZUNA_APP_ID=
  ADZUNA_APP_KEY=
  RAPIDAPI_KEY=
  OLLAMA_URL=http://localhost:11434/api/generate
  OLLAMA_MODEL=llama3
  MCP_SERVER_URL=http://localhost:8000
  ```
* No personal names or sensitive info are included in code or data by default.
* Master resumes and user profiles are always saved and loaded locally, per user, in `/users`.

---

## Feedback or Contributions

Have suggestions or want to help improve the project?
Open an issue or PR! This project is always evolving.

---