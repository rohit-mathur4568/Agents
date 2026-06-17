import streamlit as st
import pandas as pd
from dataset_agent import get_dataset_summary, answer_question

st.set_page_config(
    page_title="Smart CSV Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Smart CSV Dataset Agent")
st.markdown("### Upload any CSV and ask dataset-related questions")

uploaded_file = st.file_uploader(
    "Upload your CSV dataset",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("Dataset uploaded successfully!")

    summary = get_dataset_summary(df)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📄 Rows", summary["rows"])

    with col2:
        st.metric("📊 Columns", summary["columns"])

    with col3:
        st.metric("🔢 Numeric Columns", len(summary["numeric_columns"]))

    st.subheader("📌 Column Names")
    st.write(summary["column_names"])

    st.divider()

    st.subheader("🤖 Ask Your Dataset Agent")

    question = st.text_input(
        "Ask a question about your dataset"
    )

    if st.button("Ask Agent"):
        if question.strip():
            answer = answer_question(df, question)
            st.info(answer)
        else:
            st.warning("Please enter a question first.")

    st.divider()

    with st.expander("📁 View Dataset"):
        st.dataframe(df)

else:
    st.info("Please upload a CSV file to start.")