# 📊 Job Dashboard + Resume Builder

An AI-powered job search assistant that helps you find jobs, build resumes, and tailor applications with one click — using local LLMs (Ollama) or OpenAI.

---

## 🔍 Features

### ✅ 1. Explore Jobs
- Live job search powered by API (Adzuna, JSearch, etc.)
- Filter by title, location, and source
- Click a job to view full description and tailor your resume

### ✅ 2. Build Resume (Guided Form)
- Fully modular resume builder using Streamlit
- Add jobs, projects, education, skills, and certifications
- Upload an existing resume CSV to prefill the form
- Download structured resume as CSV or PDF

### ✅ 3. Tailor Resume to Any Job
- Paste a job description or click from the job search results
- Select your master resume (or use the active profile’s version)
- Instantly generate a tailored version using Ollama or OpenAI
- All outputs follow ATS-optimized structure for CSV/PDF export

---

## 👤 Dynamic Profile System

### 🧠 Profile-Aware Resume Tailoring
- `users/active_profile.json` tracks which user is active
- Automatically loads user data from `users/{name}.json`
- Injects personal_info fields (name, email, phone, etc.) into tailored output
- Supports multiple user profiles and switching via `0_Select_Profile.py`

---

## 💡 Tech Stack

- **Streamlit** — Front-end UI
- **FastAPI** — Backend API server
- **Ollama** (local LLM) or **OpenAI** (cloud)
- **LangChain** — optional LLM agent support
- **Pandas** / **ReportLab** — Resume PDF generation
- **FAISS / HuggingFace / Gradio** — planned add-ons for cover letters & RAG

---

## 📂 File Structure

```

job-dashboard/
│
├── app.py                      # Main Streamlit entry
├── mcp\_server/                # FastAPI backend tools
│   ├── server.py
│   └── tools/
│   └── utils/
│
├── resume/                    # Resume CSVs + PDF generation
│   ├── generate\_pdf.py
│   ├── jtmarcu\_master\_resume.csv
│
├── users/                     # Dynamic user profiles
│   ├── active\_profile.json
│   ├── jonathan\_marcu.json
│
├── pages/                     # Streamlit pages
│   ├── 0\_Select\_Profile.py
│   ├── 1\_Explore\_Jobs.py
│   ├── 2\_Create\_Resume.py
│   └── 3\_Tailor\_Resume.py

````

---

## 🧪 Coming Soon

- 📝 One-click cover letter generation (Ollama or OpenAI)
- 💾 Application tracking dashboard (with export)
- 📌 Resume version history and tagging
- 🔍 Smart job matching by role, skills, and keywords
- 🧠 LLM interview prep and Q&A

---

## 🚀 Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/yourname/job-dashboard.git
cd job-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the backend (FastAPI)
uvicorn mcp_server.server:app --reload

# 4. Start the Streamlit UI
streamlit run app.py
````

---

## 📬 Feedback or Contributions

Found a bug or want to improve the experience?
Feel free to open an issue or PR. This project is actively evolving.

---