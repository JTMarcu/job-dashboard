# Job Dashboard + Resume Builder (Powered by MCP)

A modular Python project to supercharge your job search with automation and AI. This tool helps you:

[x] Discover real-time job listings tailored to your role and location  
[x] Build and export clean, ATS-optimized resumes from structured data  
[x] Seamlessly integrate job search tools via a local FastAPI backend  
[x] Maintain a portable, extensible, and Pythonic codebase

---

## Future Goals (Planned Features)

**Intelligent Job-to-Resume Matching**  
Enter a job description → auto-tune your master resume to match  
**1-Click Tailored Resume + Cover Letter Generator**  
Click a job → output custom resume and AI-generated cover letter  
**Chatbot Q&A for Job Prep**  
Ask "How should I answer this interview question?" or "What are they looking for?"  
**Application Tracker & Exporter**  
Save roles you're applying to and export application logs

---

## Current Features

### Job Dashboard
- Browse categorized job listings (Data, ML, BI, Full-Stack, EdTech, etc.)
- Filter by keyword, location (e.g. "Remote", "San Diego"), date, and API source
- Pull listings in real-time from **Adzuna** or **JSearch** (via MCP tool calls)

### Guided Resume Builder
- Upload or build your resume using a CSV-based form
- Supports multiple jobs, projects, and certifications with grouped inputs
- Exports structured data to PDF with consistent formatting
- PDF is optimized for ATS scanning and clean presentation

---

## Tech Stack

- **Streamlit** – frontend dashboard and resume builder UI
- **FastAPI** – backend server to orchestrate job tool calls
- **MCP (Model Context Protocol)** – tool call routing and modular execution
- **ReportLab** – high-quality PDF generation
- **Pandas** – data structuring and transformation
- **Requests** – job API integration (Adzuna, JSearch)

---

## Project Structure

```

job-dashboard/
├── app.py                      # Streamlit frontend
├── requirements.txt            # Dependencies
├── .env                        # API credentials
├── start\_dashboard.sh/.bat     # Startup scripts

├── resume/
│   ├── generate\_pdf.py         # CSV → PDF exporter

├── pages/
│   └── 1\_Build\_Resume.py       # Guided resume builder (Streamlit)

├── mcp\_server/
│   ├── server.py               # FastAPI backend server
│   └── tools/
│       └── fetch\_job\_postings.py  # Job API integration

├── modules/
│   └── dashboard\_template.py   # Job card UI logic

├── utils/
│   └── data\_fetcher.py         # Calls MCP tool endpoints

````

---

## Setup Instructions

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

### 4. Run the dashboard

```bash
bash start_dashboard.sh
# or on Windows
start_dashboard.bat
```

---

## Completed Milestones

* [x] Real-time job dashboard with filters
* [x] Resume builder with grouped form sections
* [x] CSV-to-PDF resume export with ATS format
* [x] Modular FastAPI + Streamlit local dev setup

---

## License

MIT License