# mcp_server/tools/fetch_job_postings.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

def fetch_job_postings(query="data analyst", location="San Diego", results_per_page=10):
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
                "posted": job.get("created"),  # Make sure this is there
                "created": job.get("created"),
                "description": job.get("description", "")
            }
            for job in data.get("results", [])
        ]

        return {"query": query, "location": location, "results": jobs}

    except Exception as e:
        return {"error": str(e)}
