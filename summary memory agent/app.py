import streamlit as st
from memory import update_summary, save_summary, load_summary

st.title("Summary Memory Agent")

if "summary" not in st.session_state:
    st.session_state.summary = [line.strip() for line in load_summary()]

st.subheader("Summary")

for point in st.session_state.summary:
    st.write(point)

prompt = st.chat_input("Type something")

if prompt:

    st.chat_message("user").write(prompt)

    updated_summary = update_summary(prompt)

    st.session_state.summary = updated_summary

    save_summary(updated_summary)

    st.chat_message("assistant").write("Summary Updated!")