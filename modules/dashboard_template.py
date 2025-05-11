# modules/dashboard_template.py

import streamlit as st

def display_dashboard(data):
    st.subheader("Tool Output")
    if isinstance(data, dict):
        st.json(data)
    else:
        st.write(data)
