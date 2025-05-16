# modules/dashboard_template.py

import streamlit as st
from datetime import datetime
from dateutil import parser as date_parser

def display_dashboard(data):
    if "error" in data:
        st.error(data["error"])
        return

    if "results" in data:
        st.markdown(f"<h4>Results for '{data['query']}' in {data['location']}</h4><hr>", unsafe_allow_html=True)

        for job in data["results"]:
            # --- Posted Date Logic ---
            posted_days_ago = "Date not available"
            created = job.get("posted") or job.get("created")
            if created:
                try:
                    posted_date = date_parser.parse(created)
                    delta = datetime.utcnow() - posted_date
                    posted_days_ago = f"Posted {delta.days} day(s) ago"
                except Exception as e:
                    # fallback: try to show original date string
                    posted_days_ago = f"Posted on {created.split('T')[0]}" if 'T' in created else f"Posted: {created}"

            # --- Description Preview ---
            desc = job.get("description", "")
            preview = ""
            if desc:
                preview = desc.split(".")[0] + "." if "." in desc else desc[:150] + "..."

            # --- Layout ---
            st.markdown(f"### {job['title']}")

            col1, col2, col3 = st.columns([3, 3, 2])
            with col1:
                st.markdown(f"🏢 **{job['company']}**")
            with col2:
                st.markdown(f"📍 {job['location']}")
            with col3:
                st.markdown(f"🕒 {posted_days_ago}")

            if preview:
                st.caption(preview)

            st.markdown(f"<a href='{job['url']}' target='_blank'>🔗 Apply Now</a>", unsafe_allow_html=True)
            st.markdown("<hr style='margin: 1rem 0;' />", unsafe_allow_html=True)
    else:
        st.json(data)
