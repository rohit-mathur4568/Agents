import streamlit as st
from embedding_agent import EmbeddingAgent

st.title("Word Embedding Agent")

agent = EmbeddingAgent()

notes = agent.load_notes("data/notes.txt")

query = st.text_input("Ask Something")

if st.button("Search"):

    result, score = agent.search(query, notes)

    st.subheader("Best Match")

    st.write(result)

    st.write(f"Similarity Score: {score:.4f}")