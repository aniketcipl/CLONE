import streamlit as st
import pandas as pd

st.set_page_config(page_title="GRCS Simulator")

st.title("Golden Record Confidence Score (GRCS)")
st.write("Citizen Golden Record Simulator")

# Reference data
REFERENCE_DATA = [
    {"Attribute": "Aadhaar", "Weight": 0.0711, "Authority": 85},
    {"Attribute": "Name", "Weight": 0.0460, "Authority": 80},
    {"Attribute": "Date of Birth", "Weight": 0.0560, "Authority": 80},
    {"Attribute": "Mobile Number", "Weight": 0.0453, "Authority": 78},
    {"Attribute": "Gender", "Weight": 0.0467, "Authority": 80},
    {"Attribute": "Father's Name", "Weight": 0.0501, "Authority": 70},
    {"Attribute": "Mother's Name", "Weight": 0.0501, "Authority": 70},
    {"Attribute": "Permanent Address", "Weight": 0.0456, "Authority": 75},
    {"Attribute": "Correspondence Address", "Weight": 0.0346, "Authority": 70},
    {"Attribute": "Caste", "Weight": 0.0534, "Authority": 82},
]

st.sidebar.header("Attribute Match Strength")

results = []

for item in REFERENCE_DATA:

    attribute = item["Attribute"]
    weight = item["Weight"]
    si = item["Authority"] / 100

    mi = st.sidebar.slider(
        f"{attribute}",
        0.0,
        1.0,
        1.0
    )

    contribution = weight * mi * si

    results.append({
        "Attribute": attribute,
        "Weight": weight,
        "Match Strength (Mi)": mi,
        "Authority (Si)": si,
        "Contribution": contribution
    })

df = pd.DataFrame(results)

st.subheader("Attribute Contribution")
st.dataframe(df)

ics_score = df["Contribution"].sum()

st.subheader("Identity Confidence Score")
st.metric("ICS", f"{round(ics_score * 100,2)}%")

# Classification
if ics_score >= 0.92:
    status = "Golden"
elif ics_score >= 0.75:
    status = "Silver"
else:
    status = "Grey"

st.subheader(f"Record Classification: {status}")

st.bar_chart(df.set_index("Attribute")["Contribution"])
