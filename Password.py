import streamlit as st
import json
import os
import pandas as pd
from io import StringIO

# File to store passwords
DATA_FILE = "passwords.json"


# Load existing data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


# Save data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)


# Convert passwords to JSON (formatted nicely)
def get_json_data():
    return json.dumps(st.session_state["passwords"], indent=4, sort_keys=True)


# Convert passwords to CSV format
def get_csv_data():
    if not st.session_state["passwords"]:
        return "Site,Username,Password\n"

    df = pd.DataFrame.from_dict(st.session_state["passwords"], orient="index")
    df.reset_index(inplace=True)
    df.columns = ["Site", "Username", "Password"]

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()


# Initialize session state for data
if "passwords" not in st.session_state:
    st.session_state["passwords"] = load_data()

st.title("🔑 Simple Password Manager")

# Input fields
site = st.text_input("Site:")
username = st.text_input("Username:")
password = st.text_input("Password:", type="password")

# Add Password Button
if st.button("Add Password"):
    if site and username and password:
        st.session_state["passwords"][site] = {"username": username, "password": password}
        save_data(st.session_state["passwords"])
        st.success("Password added successfully!")
    else:
        st.error("Please fill in all fields.")

# View Passwords
st.subheader("Stored Passwords")
if st.session_state["passwords"]:
    for site, credentials in st.session_state["passwords"].items():
        with st.expander(f"🔐 {site}"):
            st.write(f"**Username:** {credentials['username']}")
            st.write(f"**Password:** {credentials['password']}")
else:
    st.info("No passwords stored.")

# Download options
st.subheader("📥 Download Passwords")
col1, col2 = st.columns(2)

with col1:
    st.download_button(
        label="Download as JSON",
        data=get_json_data(),
        file_name="passwords.json",
        mime="application/json"
    )

with col2:
    st.download_button(
        label="Download as CSV",
        data=get_csv_data(),
        file_name="passwords.csv",
        mime="text/csv"
    )

# Run with: `streamlit run your_script.py`
