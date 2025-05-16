# mcp_server/tools/fetch_job_postings.py

import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

def is_recent(posted_str, filter_value):
    try:
        posted_date = datetime.strptime(posted_str, "%Y-%m-%dT%H:%M:%SZ")
        days_map = {
            "Today": 0,
            "Past 3 days": 3,
            "Past week": 7,
            "Past month": 30
        }
        if filter_value == "Any time":
            return True
        delta_days = days_map.get(filter_value, 0)
        return (datetime.utcnow() - posted_date).days <= delta_days
    except:
        return True  # allow through if we can't parse it

def fetch_job_postings(query="data analyst", location="San Diego", results_per_page=10, posted_within="Any time"):
    if not APP_ID or not APP_KEY:
        return {"error": "Missing ADZUNA_APP_ID or ADZUNA_APP_KEY in .env"}

    url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": results_per_page,
        "what": query,
        "where": location,
        "content-type": "application/json"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        jobs = [
            {
                "title": job.get("title", "No Title"),
                "company": job.get("company", {}).get("display_name", "N/A"),
                "location": job.get("location", {}).get("display_name", "N/A"),
                "url": job.get("redirect_url", "#"),
                "posted": job.get("created"),
                "created": job.get("created"),
                "description": job.get("description", "")
            }
            for job in data.get("results", [])
            if is_recent(job.get("created", ""), posted_within)
        ]

        return {"query": query, "location": location, "results": jobs}

    except Exception as e:
        return {"error": str(e)}