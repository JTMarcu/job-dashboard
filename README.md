# Job Dashboard (Powered by MCP)

A real-time, personalized job listings dashboard built using **Streamlit**, **FastAPI**, and **Model Context Protocol (MCP)**.  
This tool dynamically pulls job postings based on your skills and location — perfect for job seekers, career changers, or tech portfolio builders.

---

## Features

✅ Tailored job searches for categories like Data Science, AI, BI, and Full-Stack Dev  
✅ Location toggle (San Diego or Remote)  
✅ "View All" to explore all job types in a single view  
✅ Auto-refreshing query builder via Streamlit sidebar  
✅ Clean UI with job titles, companies, locations, and **posting dates**  
✅ Short descriptions previewed for fast skimming  
✅ Built entirely in Python with real-time API integration

---

## Powered by

- **Streamlit** for the frontend UI
- **FastAPI + MCP** for backend data tool orchestration
- **Adzuna API** for real-time job postings
- **Python packages**: `requests`, `dotenv`, `dateutil`, `pandas`

---

## Project Structure

```

job-dashboard/
├── app.py                         # Streamlit dashboard UI
├── mcp\_server/
│   ├── server.py                  # FastAPI + MCP tool registry
│   └── tools/
│       └── fetch\_job\_postings.py # Adzuna API integration
├── modules/
│   └── dashboard\_template.py      # Dynamic result rendering
├── utils/
│   └── data\_fetcher.py            # Calls tools via MCP
├── .env                           # API credentials and config
├── requirements.txt               # Dependencies
└── README.md                      # You're here!

````

---

## Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/JTMarcu/job-dashboard.git
cd job-dashboard
````

### 2. Create your `.env` file

```env
MCP_SERVER_URL=http://localhost:8000
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key
```

### 3. Install dependencies and run

```bash
pip install -r requirements.txt
uvicorn mcp_server.server:app --reload
streamlit run app.py
```

---

## Example Use

Choose a job category like:

* **Data Scientist**
* **LangChain Developer**
* **BI Analyst**
* **Full-Stack Developer**

Then set your preferred location and hit **Search Jobs** — job results appear with apply links, company names, and posting dates.

---

## Coming Soon

* ✅ CSV export
* ✅ Keyword highlighting
* ✅ Bookmark/saved jobs
* ✅ Salary filters and fuzzy skill matching

---

##  Created by

**Jonathan Marcu** — [jtmarcu.github.io](https://jtmarcu.github.io)
Data Scientist & Full-Stack Developer | AI Solutions Architect

[LinkedIn](https://www.linkedin.com/in/jon-marcu) · [GitHub](https://github.com/JTMarcu)

---

## License

MIT License