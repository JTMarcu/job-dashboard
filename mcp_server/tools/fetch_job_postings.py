# mcp_server/tools/fetch_job_postings.py

import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

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
        return True

def format_post_date(created_str):
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            created_dt = datetime.strptime(created_str, fmt)
            delta = (datetime.utcnow() - created_dt).days
            created_pretty = created_dt.strftime("%Y-%m-%d")
            if delta == 0:
                return f"Posted on {created_pretty} (Today)"
            elif delta == 1:
                return f"Posted on {created_pretty} (1 day ago)"
            else:
                return f"Posted on {created_pretty} ({delta} days ago)"
        except ValueError:
            continue
    return f"Posted: {created_str}"

def fetch_from_jsearch(query, location, results_per_page, posted_within):
    if not RAPIDAPI_KEY:
        return {"error": "Missing RAPIDAPI_KEY in .env"}

    url = "https://jsearch.p.rapidapi.com/search"
    params = {
        "query": f"{query} in {location}",
        "page": "1",
        "num_pages": "1"
    }
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        raw_results = data.get("data", [])
        print(f"JSearch returned {len(raw_results)} raw jobs for '{query}'")

        jobs = []
        for job in raw_results:
            created_str = job.get("job_posted_at_datetime_utc")
            if is_recent(created_str, posted_within):
                date_display = format_post_date(created_str) if created_str else "Date not available"
                jobs.append({
                    "title": job.get("job_title", "No Title"),
                    "company": job.get("employer_name", "N/A"),
                    "location": job.get("job_city", "N/A"),
                    "url": job.get("job_apply_link", "#"),
                    "posted": created_str,
                    "created": created_str,
                    "date_display": date_display,
                    "description": job.get("job_description", "")
                })

        jobs.sort(key=lambda x: x.get("created") or "", reverse=True)
        jobs = jobs[:results_per_page]

        print(f"Filtered to {len(jobs)} jobs after date check and slicing")
        return {"query": query, "location": location, "results": jobs}

    except Exception as e:
        return {"error": str(e)}

def fetch_from_adzuna(query, location, results_per_page, posted_within):
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

        jobs = []
        for job in data.get("results", []):
            created_str = job.get("created")
            date_display = format_post_date(created_str) if created_str else "Date not available"
            if is_recent(created_str, posted_within):
                jobs.append({
                    "title": job.get("title", "No Title"),
                    "company": job.get("company", {}).get("display_name", "N/A"),
                    "location": job.get("location", {}).get("display_name", "N/A"),
                    "url": job.get("redirect_url", "#"),
                    "posted": created_str,
                    "created": created_str,
                    "date_display": date_display,
                    "description": job.get("description", "")
                })

        jobs.sort(key=lambda x: x.get("created") or "", reverse=True)
        return {"query": query, "location": location, "results": jobs}

    except Exception as e:
        return {"error": str(e)}

def fetch_job_postings(query="data analyst", location="San Diego", results_per_page=10, posted_within="Any time", source="adzuna"):
    if source == "jsearch":
        return fetch_from_jsearch(query, location, results_per_page, posted_within)
    else:
        return fetch_from_adzuna(query, location, results_per_page, posted_within)
