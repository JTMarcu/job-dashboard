# Job Dashboard + Resume Builder (Powered by MCP)

A modular Python project to supercharge your job search with automation and AI. This tool helps you:

- ✅ Discover real-time job listings tailored to your role and location  
- ✅ Build and export clean, ATS-optimized resumes from structured data  
- ✅ Seamlessly integrate job search tools via a local FastAPI backend  
- ✅ Maintain a portable, extensible, and Pythonic codebase  
- ✅ Switch between multiple user profiles and Master Resumes

---

## 🔐 New: User Profile System

- Select or upload your profile on first launch
- Each profile gets its own editable JSON and optional Master Resume CSV
- All pages auto-load profile and resume data tied to the selected user

---

## 💼 Current Features

### Explore Jobs
- Browse categorized job listings (Data, ML, BI, Full-Stack, EdTech, etc.)
- Filter by keyword, location (e.g. "Remote", "San Diego"), date, and API source
- Fetch live results from **Adzuna** or **JSearch** (via FastAPI tool calls)

### Create Resume
- Build or upload your resume using a smart CSV-based form
- Supports multiple jobs, projects, and certifications with grouped inputs
- Autofill with your profile + Master Resume CSV
- Fields persist after export (no reset on PDF download)
- Outputs to CSV, JSON, and polished ATS-friendly PDF

### Tailor Resume (Beta)
- Paste a job description and generate a customized resume using OpenAI or Ollama
- Still under active development for full job-to-resume matching
- Choose between OpenAI or Ollama (local) for rewriting
- Fully supports LLaMA 3 and other Ollama-hosted models

---

## 🧠 Future Goals

- **One-Click Cover Letter Generator**  
  Click a job → output matching resume + AI-written cover letter

- **Interview Assistant Q&A**  
  "How should I answer this job's most likely questions?"

- **Application Tracker**  
  Track jobs applied to, export to CSV/Notion

- **Unified Job + Resume Dashboard**  
  One page to view jobs, tailor, and apply

---

## 🛠️ Tech Stack

- **Streamlit** – frontend UI for dashboard and resume builder
- **FastAPI** – local backend for job tools (MCP)
- **ReportLab** – ATS-optimized PDF resume generation
- **Pandas** – structured resume storage + export
- **Requests** – API calls to Adzuna, JSearch, Ollama/OpenAI
- **Ollama + LLaMA 3** – run local LLMs for resume rewriting without API cost

---

## 📁 Project Structure (v0.5)

```

job-dashboard/
├── 0\_Select\_Profile.py           # New entry point: choose or upload a user
├── pages/
│   ├── 1\_Explore\_Jobs.py         # Job listings dashboard
│   ├── 2\_Create\_Resume.py        # Guided resume builder (form-based)
│   └── 3\_Tailor\_Resume.py        # AI-based resume tailoring (OpenAI/Ollama)

├── resume/
│   └── generate\_pdf.py           # CSV → ATS PDF exporter

├── modules/
│   └── dashboard\_template.py     # Job card display logic

├── utils/
│   ├── data\_fetcher.py           # Calls FastAPI tools
│   ├── rewrite\_utils.py          # Bullet/summary rewriting helpers
│   └── profile\_loader.py         # Load/save profile JSONs

├── mcp\_server/
│   ├── server.py                 # FastAPI backend
│   └── tools/fetch\_job\_postings.py

├── users/
│   └── \[name].json               # User profile
│   └── \[name]\_master\_resume.csv  # (optional) full resume data

````

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/job-dashboard.git
cd job-dashboard
````

### 2. Create `.env` with your API keys

```env
MCP_SERVER_URL=http://localhost:8000
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key
RAPIDAPI_KEY=your_jsearch_api_key
```

### 3. Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Launch the dashboard

```bash
bash start_dashboard.sh
# or on Windows
start_dashboard.bat
```

---

## ✅ Completed Milestones (v0.5)

* [x] User profiles with stored resume and profile info
* [x] Real-time job dashboard with category + keyword filtering
* [x] CSV-based guided resume builder with grouped inputs
* [x] Full-form persistence using Streamlit `session_state`
* [x] Clean PDF exports from form or uploaded data
* [x] Modular, scalable FastAPI + Streamlit architecture

---

## 📜 License

MIT License
