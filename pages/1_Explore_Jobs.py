# pages\1_Explore_Jobs.py

import streamlit as st
from utils.data_fetcher import call_mcp_tool
from modules.dashboard_template import display_dashboard
import json
import streamlit as st
from utils.profile_loader import load_user_profile

if "active_profile" not in st.session_state:
    st.warning("Please select a user profile before continuing.")
    st.stop()

profile = load_user_profile(st.session_state["active_profile"])

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
    custom_keywords = st.text_input("Or enter keywords (comma-separated):", value="")

    location = st.text_input("Location or ZIP", value="Remote")
    results_per_page = st.slider("Number of results:", 1, 20, 10)
    date_filter = st.selectbox("Posted Within:", ["Any time", "Today", "Past 3 days", "Past week", "Past month"])
    selected_source = st.selectbox("Job Source", ["Adzuna", "JSearch"])
    run_search = st.button("Search Jobs")

# --- Main Panel ---
if run_search:
    keyword_list = [k.strip() for k in custom_keywords.split(",") if k.strip()]
    selected_jobs = []

    if keyword_list:
        selected_jobs = [(kw, kw) for kw in keyword_list]
        query_label = f"Custom: {custom_keywords}"
    elif job_categories[selected_label] is None:
        selected_jobs = [(label, query) for label, query in job_categories.items() if query]
        query_label = selected_label
    else:
        selected_jobs = [(selected_label, job_categories[selected_label])]
        query_label = selected_label

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
        st.subheader(f"Results for '{query_label}' in {location}")
        display_dashboard({"results": all_results, "query": query_label, "location": location})

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