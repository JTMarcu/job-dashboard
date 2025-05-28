import os
import streamlit as st
import json
from utils.profile_loader import load_user_profile

USER_DIR = "users"
os.makedirs(USER_DIR, exist_ok=True)

st.set_page_config(page_title="Select or Edit Profile", layout="wide")

# Step 1: Profile selection (if no active profile)
if "active_profile" not in st.session_state:
    st.title("Select User Profile")

    profile_files = sorted([
        f for f in os.listdir(USER_DIR)
        if f.endswith(".json") and os.path.isfile(os.path.join(USER_DIR, f)) and f != "active_profile.json"
    ])
    profile_names = [os.path.splitext(f)[0] for f in profile_files]

    if profile_names:
        st.subheader("Choose a profile:")
        cols = st.columns(3)
        for i, name in enumerate(profile_names):
            with cols[i % 3]:
                if st.button(f"{name.title()}", key=f"profile_{name}"):
                    st.session_state["active_profile"] = name
                    with open(os.path.join(USER_DIR, "active_profile.json"), "w") as f:
                        json.dump({"active_profile": name}, f)
                    st.rerun()
    else:
        st.warning("No profiles found. Upload or create one below.")

    st.divider()
    st.subheader("Upload New Profile (JSON)")
    upload = st.file_uploader("Upload JSON file", type=["json"])
    if upload:
        try:
            content = json.load(upload)
            new_name = os.path.splitext(upload.name)[0]
            with open(os.path.join(USER_DIR, f"{new_name}.json"), "w") as f:
                json.dump(content, f, indent=2)
            with open(os.path.join(USER_DIR, "active_profile.json"), "w") as f:
                json.dump({"active_profile": new_name}, f)
            st.success(f"Uploaded and saved profile: {new_name}")
            st.session_state["active_profile"] = new_name
            st.rerun()
        except Exception as e:
            st.error(f"Upload failed: {e}")

    st.divider()
    st.subheader("Create New Profile")
    with st.form("new_profile_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        location = st.text_input("Location")
        linkedin = st.text_input("LinkedIn")
        github = st.text_input("GitHub")
        portfolio = st.text_input("Portfolio")
        submitted = st.form_submit_button("Create Profile")
        if submitted:
            if name:
                profile_id = name.lower().replace(" ", "_")
                profile_data = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "location": location,
                    "linkedin": linkedin,
                    "github": github,
                    "portfolio": portfolio
                }
                with open(os.path.join(USER_DIR, f"{profile_id}.json"), "w") as f:
                    json.dump(profile_data, f, indent=2)
                with open(os.path.join(USER_DIR, "active_profile.json"), "w") as f:
                    json.dump({"active_profile": profile_id}, f)
                st.success(f"Profile '{profile_id}' created!")
                st.session_state["active_profile"] = profile_id
                st.rerun()
            else:
                st.warning("Name is required to create a profile.")

# Step 2: Post-selection dashboard with profile editing
else:
    profile_name = st.session_state["active_profile"]
    st.title(f"Welcome, {profile_name.title()}")

    st.subheader("Resume Builder & Job Tools")
    menu_items = [
        ("Explore Jobs", "pages/1_Explore_Jobs.py"),
        ("Tailor Resume", "pages/3_Tailor_Resume.py"),
        ("Create Resume", "pages/2_Create_Resume.py")
    ]

    cols = st.columns(len(menu_items))
    for i, (label, path) in enumerate(menu_items):
        with cols[i]:
            if st.button(label):
                st.switch_page(path)

    st.divider()
    st.subheader("🧾 Edit Profile Information")

    profile_path = os.path.join(USER_DIR, f"{profile_name}.json")
    existing = load_user_profile(profile_path)

    with st.form("edit_profile_form"):
        name = st.text_input("Full Name", existing.get("name", ""))
        email = st.text_input("Email", existing.get("email", ""))
        phone = st.text_input("Phone", existing.get("phone", ""))
        location = st.text_input("Location", existing.get("location", ""))
        linkedin = st.text_input("LinkedIn", existing.get("linkedin", ""))
        github = st.text_input("GitHub", existing.get("github", ""))
        portfolio = st.text_input("Portfolio", existing.get("portfolio", ""))
        submitted = st.form_submit_button("Save Changes")
        if submitted:
            profile_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "location": location,
                "linkedin": linkedin,
                "github": github,
                "portfolio": portfolio
            }
            with open(profile_path, "w") as f:
                json.dump(profile_data, f, indent=2)
            st.success("Profile updated successfully!")
            st.rerun()

    st.divider()
    st.subheader("📁 Resume Tools")
    master_resume_path = os.path.join(USER_DIR, f"{profile_name}_master_resume.csv")
    has_master = os.path.exists(master_resume_path)

    if has_master:
        st.success("Master Resume is saved.")
        with open(master_resume_path, "rb") as f:
            st.download_button("⬇️ Download Master Resume", f, file_name=f"{profile_name}_master_resume.csv", mime="text/csv")
    else:
        st.warning("No Master Resume uploaded yet.")

    uploaded_resume = st.file_uploader("Upload Master Resume (CSV)", type=["csv"])
    if uploaded_resume:
        with open(master_resume_path, "wb") as f:
            f.write(uploaded_resume.getbuffer())
        st.success("Master Resume uploaded.")
        st.rerun()
