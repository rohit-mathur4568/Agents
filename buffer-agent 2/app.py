import streamlit as st
from memory import load_memory, save_message

st.set_page_config(page_title="Buffer Memory Agent")

st.title("Buffer Memory Agent")

# Load History
if "messages" not in st.session_state:

    history = load_memory()

    st.session_state.messages = []

    for line in history:

        if line.startswith("User:"):
            st.session_state.messages.append(
                {"role": "user",
                 "content": line.replace("User:", "").strip()}
            )

        elif line.startswith("Agent:"):
            st.session_state.messages.append(
                {"role": "assistant",
                 "content": line.replace("Agent:", "").strip()}
            )

# Display Chat
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input
prompt = st.chat_input("Type your message")

if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    save_message("User", prompt)

    with st.chat_message("user"):
        st.write(prompt)

    # Simple Agent Logic
    response = f"I remember your message: {prompt}"

    st.session_state.messages.append(
        {"role": "assistant",
         "content": response}
    )

    save_message("Agent", response)

    with st.chat_message("assistant"):
        st.write(response)