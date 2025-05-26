# 0_Select_Profile.py

import os
import streamlit as st
import json
import pandas as pd

USER_DIR = "users"
os.makedirs(USER_DIR, exist_ok=True)

st.set_page_config(page_title="Select Profile", layout="wide")

# Step 1: Profile selection
from utils.profile_loader import load_user_profile
if "active_profile" not in st.session_state:
    st.title("Select User Profile")

    # Load profile names
    profile_files = sorted([
        f for f in os.listdir(USER_DIR)
        if f.endswith(".json") and os.path.isfile(os.path.join(USER_DIR, f))
    ])
    profile_names = [os.path.splitext(f)[0] for f in profile_files]

    if profile_names:
        st.subheader("Click a profile to begin:")
        cols = st.columns(3)
        for i, name in enumerate(profile_names):
            with cols[i % 3]:
                if st.button(f"👤 {name.title()}", key=f"profile_{name}"):
                    st.session_state["active_profile"] = name
                    st.rerun()
    else:
        st.warning("No profiles found. Please upload one to continue.")

    st.divider()
    st.subheader("📤 Upload a New Profile")
    upload = st.file_uploader("Upload JSON", type=["json"])
    if upload:
        try:
            content = json.load(upload)
            new_name = os.path.splitext(upload.name)[0]
            with open(os.path.join(USER_DIR, f"{new_name}.json"), "w") as f:
                json.dump(content, f, indent=2)
            st.success(f"Uploaded and saved profile: {new_name}")
            st.rerun()
        except Exception as e:
            st.error(f"Upload failed: {e}")

    st.divider()
    st.subheader("📝 Set Up New Profile")
    with st.form("profile_form"):
        # Try to prefill from existing profile
        existing_profile = {}
        profile_files = sorted([
            f for f in os.listdir(USER_DIR)
            if f.endswith(".json") and os.path.isfile(os.path.join(USER_DIR, f))
        ])
        if "active_profile" in st.session_state and f"{st.session_state['active_profile']}.json" in profile_files:
            existing_profile = load_user_profile(st.session_state['active_profile'])

        name = st.text_input("Full Name", existing_profile.get("name", ""))
        email = st.text_input("Email", existing_profile.get("email", ""))
        phone = st.text_input("Phone", existing_profile.get("phone", ""))
        location = st.text_input("Location", existing_profile.get("location", ""))
        linkedin = st.text_input("LinkedIn", existing_profile.get("linkedin", ""))
        github = st.text_input("GitHub", existing_profile.get("github", ""))
        portfolio = st.text_input("Portfolio", existing_profile.get("portfolio", ""))
        submitted = st.form_submit_button("Save Profile")
        if submitted:
            if name:
                profile_data = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "location": location,
                    "linkedin": linkedin,
                    "github": github,
                    "portfolio": portfolio
                }
                profile_id = name.lower().replace(" ", "_")
                with open(os.path.join(USER_DIR, f"{profile_id}.json"), "w") as f:
                    json.dump(profile_data, f, indent=2)
                st.success(f"Profile '{profile_id}' created!")
                st.session_state["active_profile"] = profile_id
                st.rerun()
            else:
                st.warning("Name is required to create a profile.")

# Step 2: Tiled menu after profile selection
else:
    st.title(f"Welcome, {st.session_state['active_profile'].title()}!")
    st.subheader("What would you like to do?")

    profile_name = st.session_state['active_profile']
    master_resume_path = os.path.join(USER_DIR, f"{profile_name}_master_resume.csv")
    has_master_resume = os.path.exists(master_resume_path)

    if has_master_resume:
        st.success("Master Resume found!")
    else:
        st.warning("No Master Resume saved yet.")

    menu_items = [
        ("Explore Jobs", "pages/1_Explore_Jobs.py"),
        ("Tailor Resume", "pages/3_Tailor_Resume.py"),
        ("Create Resume", "pages/2_Create_Resume.py")
    ]

    cols = st.columns(3)
    for i, (label, page) in enumerate(menu_items):
        with cols[i % 3]:
            if st.button(label, key=f"menu_{i}"):
                st.switch_page(page)

    st.divider()
    st.subheader("📁 Manage Master Resume")

    uploaded_resume = st.file_uploader("Upload Master Resume (CSV)", type=["csv"], key="resume_upload")
    if uploaded_resume and "resume_uploaded" not in st.session_state:
        with open(master_resume_path, "wb") as f:
            f.write(uploaded_resume.getbuffer())
        st.session_state["resume_uploaded"] = True
        st.success("Master Resume uploaded successfully!")
        st.rerun()

    if "resume_uploaded" in st.session_state:
        del st.session_state["resume_uploaded"]

    if has_master_resume:
        with open(master_resume_path, "rb") as f:
            st.download_button("Download Master Resume", f, file_name=f"{profile_name}_master_resume.csv", mime="text/csv")