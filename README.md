# Job Dashboard + Resume Builder (Powered by MCP)

A Python-powered job dashboard and smart resume builder that helps you:

✅ Discover job listings tailored to your skills  
✅ Build and export clean, ATS-friendly resumes  
✅ Integrate with real-time job APIs like Adzuna and JSearch  
✅ Maintain a portable, modular codebase

---

## 🔍 Features

### 💼 Job Dashboard
- Browse jobs by category (Data, AI, BI, Full-Stack, etc.)
- Keyword + location filtering (e.g. "Remote", "San Diego")
- Real-time listings from Adzuna or JSearch (via MCP)

### 📄 Resume Builder
- Upload or build your resume using an interactive form
- Edit technical skills using grouped subsections
- Export fully formatted PDF resumes from structured CSV
- Save and reload resume data

---

## 🛠 Tech Stack

- **Streamlit** – frontend dashboard & builder
- **FastAPI** – backend server for tool orchestration
- **MCP (Model Context Protocol)** – connects job tools via tool calls
- **ReportLab** – clean PDF generation from CSV
- **Pandas + Requests** – data wrangling and API calls

---

## 📁 Project Structure

```

JOB-DASHBOARD/
├── app.py                    # Main Streamlit app
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .env                      # API credentials

├── exports/                  # Generated CSV and PDF resumes

├── pages/
│   └── 1\_Build\_Resume.py     # Streamlit resume builder

├── resume/
│   ├── generate\_pdf.py       # CSV → PDF logic
│   └── exports/              # (optional PDF output location)

├── mcp\_server/
│   ├── server.py             # FastAPI MCP server
│   └── tools/
│       └── fetch\_job\_postings.py  # Job API tool

├── modules/
│   └── dashboard\_template.py # UI for job listings

├── utils/
│   └── data\_fetcher.py       # MCP tool caller

├── tests/
│   └── test\_fetcher.py       # Job tool test stub

├── setup\_env.bat / .sh       # Quick-start shell scripts
├── start\_dashboard.bat / .sh

````

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/job-dashboard.git
cd job-dashboard
````

### 2. Add `.env` with your API keys

```env
MCP_SERVER_URL=http://localhost:8000
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key
RAPIDAPI_KEY=your_jsearch_api_key
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the backend + frontend

```bash
uvicorn mcp_server.server:app --reload
streamlit run app.py
```

---

## 💡 Example Use

* Search for job listings with filters like `Full-Stack Developer`, `Remote`
* Click into **Build Resume** tab
* Upload your existing CSV or fill out the resume form
* Click **Generate PDF** to download your tailored resume

---

## ✅ Completed Milestones

* [x] Job dashboard with API sources
* [x] Resume builder form + CSV upload
* [x] PDF export from CSV (ATS-friendly)
* [x] Full local development support

---

## 🪪 License

MIT License