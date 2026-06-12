import streamlit as st
import pandas as pd
from resume_agent import ResumeScreeningAgent

st.set_page_config(page_title="AI Resume Screening Agent", layout="wide")

st.title("AI Resume Screening Agent")
st.write("Upload a Job Description and multiple PDF resumes to rank candidates.")

agent = ResumeScreeningAgent()

jd_text = st.text_area(
    "Paste Job Description here",
    height=250,
    placeholder="Example: We need a Python developer with ML, SQL, Flask, and AWS knowledge..."
)

resume_files = st.file_uploader(
    "Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if st.button("Scan Resumes"):
    if not jd_text:
        st.error("Please paste the Job Description.")
    elif not resume_files:
        st.error("Please upload at least one resume PDF.")
    else:
        with st.spinner("Scanning resumes..."):
            results = agent.rank_resumes(jd_text, resume_files)

        st.success("Resume scanning completed!")

        df = pd.DataFrame(results)

        st.subheader("Candidate Ranking")
        st.dataframe(df[["Resume Name", "Match Score (%)"]], use_container_width=True)

        st.subheader("Resume Text Preview")
        for item in results:
            with st.expander(f"{item['Resume Name']} - {item['Match Score (%)']}% Match"):
                st.write(item["Extracted Text Preview"])