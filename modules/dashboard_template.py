import streamlit as st
from dateutil import parser as date_parser

def display_dashboard(data):
    if "error" in data:
        st.error(data["error"])
        return

    if "results" in data:
        for job in data["results"]:
            st.markdown(f"### {job['title']}")

            col1, col2, col3 = st.columns([3, 3, 2])
            with col1:
                st.markdown(f"**{job['company']}**")
            with col2:
                st.markdown(f"{job['location']}")
            with col3:
                st.markdown(job.get("date_display", "Date not available"))

            if job.get("description"):
                desc = job["description"].split(".")[0] + "." if "." in job["description"] else job["description"][:150] + "..."
                st.caption(desc)

            st.markdown(f"<a href='{job['url']}' target='_blank'>Apply Now</a>", unsafe_allow_html=True)
            st.markdown("<hr style='margin: 1rem 0;' />", unsafe_allow_html=True)
    else:
        st.json(data)