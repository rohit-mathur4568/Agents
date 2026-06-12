import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Advanced ATS Resume Analyzer", layout="wide")

st.title("Advanced ATS Resume Analyzer Agent")
st.write("Frontend connected with FastAPI backend.")

API_URL = "http://127.0.0.1:8000/analyze"

jd_text = st.text_area(
    "Paste Job Description",
    height=250,
    placeholder="Paste company JD here..."
)

resume_files = st.file_uploader(
    "Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if st.button("Analyze Resumes"):
    if not jd_text.strip():
        st.error("Please paste the Job Description.")
    elif not resume_files:
        st.error("Please upload at least one resume PDF.")
    else:
        files = [
            ("resumes", (file.name, file.getvalue(), "application/pdf"))
            for file in resume_files
        ]

        data = {"jd_text": jd_text}

        with st.spinner("Sending resumes to backend..."):
            response = requests.post(API_URL, data=data, files=files)

        if response.status_code == 200:
            results = response.json()["results"]
            df = pd.DataFrame(results)

            st.success("Analysis completed!")

            st.subheader("Candidate Ranking")
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Download Result CSV",
                data=csv,
                file_name="ats_resume_analysis.csv",
                mime="text/csv"
            )

            st.subheader("Detailed Candidate Report")

            for item in results:
                with st.expander(f"{item['Resume Name']} - {item['Final Score (%)']}%"):
                    st.write("**Candidate Summary:**")
                    st.write(item["Candidate Summary"])

                    st.write("**Matched Skills:**")
                    st.write(item["Matched Skills"] or "No matched skills found.")

                    st.write("**Missing Skills:**")
                    st.write(item["Missing Skills"] or "No missing skills.")
        else:
            st.error("Backend error occurred.")
            st.write(response.text)