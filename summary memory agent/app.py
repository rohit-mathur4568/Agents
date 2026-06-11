import streamlit as st
from memory import load_summary, save_summary, update_summary

st.set_page_config(page_title="Summary Memory Agent")

st.title("Summary Memory Agent")

if "summary" not in st.session_state:
    st.session_state.summary = load_summary()

st.subheader("Current Summary")

if st.session_state.summary:
    st.write(st.session_state.summary)
else:
    st.write("No summary yet")

prompt = st.chat_input("Enter a message")

if prompt:

    st.chat_message("user").write(prompt)

    updated_summary = update_summary(
        st.session_state.summary,
        prompt
    )

    st.session_state.summary = updated_summary

    save_summary(updated_summary)

    response = f"Summary Updated!\n\n{updated_summary}"

    st.chat_message("assistant").write(response)