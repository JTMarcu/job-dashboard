# Job Dashboard + Resume Builder

A modular, AI-powered assistant that streamlines your entire job search—from finding roles, to building and tailoring your resume, to exporting ready-to-submit documents. Powered by **Streamlit** (UI), **FastAPI** (backend), and your choice of **local LLMs (Ollama/Llama 3)** (with OpenAI and others coming soon) for resume tailoring.

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
- Instantly rewrite your resume with **local LLM (Llama 3 via Ollama)**
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
- **Ollama** (local LLM with Llama 3) — for AI-powered resume rewriting
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

## Getting Started

### 1. Clone the repo

```sh
git clone https://github.com/YOUR-USERNAME/job-dashboard.git
cd job-dashboard
````

### 2. Install Python dependencies

```sh
pip install -r requirements.txt
```

### 3. Configure your environment variables (API keys, etc.)

```sh
cp .env.example .env
# Or manually create .env and add required API keys as variables.
# You can leave blank if only using local Ollama features.
```

---

## 🦙 Using Ollama for Local AI Resume Tailoring

**Ollama with Llama 3 is required for resume rewriting to work locally.**

1. **Install Ollama**

   * [Download Ollama](https://ollama.com/download) for Windows, macOS, or Linux and install.

2. **Start the Ollama server**

   ```sh
   ollama serve
   ```

   * You should see something like `Listening on 127.0.0.1:11434`.

3. **Download the Llama 3 model (do this once)**

   ```sh
   ollama pull llama3
   ```

   * Wait for the download (\~4GB the first time).

4. **(Optional) Change Model**

   * By default, the app uses `llama3`.
   * To use a different model, update `OLLAMA_MODEL` in your `.env`.

5. **Start the backend and UI**

   In two new terminals:

   ```sh
   uvicorn mcp_server.server:app --reload
   ```

   ```sh
   streamlit run 0_Select_Profile.py
   ```

**Tip:** Ollama, the FastAPI backend, and Streamlit should each run in their own terminal/tab.

---

## Environment File Example

The `.env` file should be **blank by default** or include only placeholders for API keys:

```
ADZUNA_APP_ID=
ADZUNA_APP_KEY=
RAPIDAPI_KEY=
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=llama3
MCP_SERVER_URL=http://localhost:8000
```

---

## ❗ OpenAI & Other LLM Integrations — Coming Soon!

* OpenAI (cloud) support and other LLM integrations are planned but **not yet implemented**.
* For now, resume tailoring works **only with local Ollama/Llama 3**.
* When OpenAI is ready, instructions will be provided here!

---

## Coming Soon

* One-click cover letter generation (Ollama or OpenAI)
* Application tracking dashboard with export
* Resume versioning and tagging
* Smart job matching by skills and keywords
* LLM-powered interview prep

---

## Notes

* No personal names or sensitive info are included in code or data by default.
* Master resumes and user profiles are always saved and loaded locally, per user, in `/users`.

---

## Feedback or Contributions

Have suggestions or want to help improve the project?
Open an issue or PR! This project is always evolving.

---