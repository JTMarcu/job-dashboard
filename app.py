# app.py

import streamlit as st
from utils.data_fetcher import call_mcp_tool
from modules.dashboard_template import display_dashboard
import json

st.set_page_config(page_title="Job Listings Dashboard", layout="wide")
st.title("Job Dashboard")

# --- Sidebar Controls ---
with st.sidebar:
    st.header("Search Settings")

    job_categories = {
        "View All Matching Jobs": None,
        "Data Scientist": "data scientist",
        "Machine Learning Engineer": "machine learning engineer",
        "Business Intelligence Analyst": "BI analyst",
        "Data Analyst": "data analyst",
        "AI / RAG Developer": "LangChain developer",
        "Python / Flask Developer": "python developer",
        "Full-Stack Developer": "full-stack developer",
        "Health Data Analyst": "medical data analyst",
        "EdTech / Education Tools": "education technologist",
    }

    selected_label = st.selectbox("Choose a job type:", list(job_categories.keys()))
    location = st.text_input("Location or ZIP", value="Remote")
    results_per_page = st.slider("Number of results:", 1, 20, 10)
    date_filter = st.selectbox("Posted Within:", ["Any time", "Today", "Past 3 days", "Past week", "Past month"])
    selected_source = st.selectbox("Job Source", ["Adzuna", "JSearch"])
    run_search = st.button("Search Jobs")

# --- Main Panel ---
if run_search:
    selected_jobs = (
        [(label, query) for label, query in job_categories.items() if query is not None]
        if job_categories[selected_label] is None
        else [(selected_label, job_categories[selected_label])]
    )

    all_results = []

    for label, query in selected_jobs:
        with st.spinner(f"Fetching jobs for '{query}' in {location} from {selected_source}..."):
            payload = {
                "query": query,
                "location": location,
                "results_per_page": results_per_page,
                "posted_within": date_filter,
                "source": selected_source.lower()
            }
            try:
                result = call_mcp_tool("fetch_job_postings", payload)
                if "results" in result:
                    for job in result["results"]:
                        job["search_label"] = label
                    all_results.extend(result["results"])
            except Exception as e:
                st.error(f"Failed to fetch jobs for {label}: {e}")

    if all_results:
        st.subheader(f"Results for '{selected_label}' in {location}")
        display_dashboard({"results": all_results, "query": selected_label, "location": location})

# --- Dev Section ---
st.markdown("### Developer Tool (Manual Input)")
with st.expander("Try a raw query (advanced)", expanded=False):
    raw_tool = st.text_input("Tool name", value="fetch_job_postings")
    raw_json = st.text_area("JSON input", value='{"query": "data analyst", "location": "Remote", "results_per_page": 5, "source": "jsearch"}', height=100)

    if st.button("Run Raw Tool"):
        try:
            parsed = json.loads(raw_json)
            result = call_mcp_tool(raw_tool, parsed)
            display_dashboard(result)
        except Exception as e:
            st.error(f"Error: {e}")
