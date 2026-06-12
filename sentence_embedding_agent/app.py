import streamlit as st
from sentence_agent import SentenceEmbeddingAgent

st.title("Sentence Embedding Agent")

agent = SentenceEmbeddingAgent()

st.header("Compare Two Sentences")

sentence1 = st.text_input("Enter first sentence")
sentence2 = st.text_input("Enter second sentence")

if st.button("Compare"):
    score = agent.compare_sentences(sentence1, sentence2)
    st.write(f"Similarity Score: {score:.4f}")

    if score > 0.75:
        st.success("Both sentences are highly similar.")
    elif score > 0.45:
        st.warning("Both sentences are somewhat similar.")
    else:
        st.error("Both sentences are not very similar.")


st.header("Find Most Similar Sentence")

query = st.text_input("Enter your query")

sentences_text = st.text_area(
    "Enter multiple sentences, one per line",
    """Python is used in machine learning.
Java is used for backend development.
SQL is used for database management.
Cyber security protects systems from attacks.
AWS provides cloud computing services."""
)

if st.button("Find Best Match"):
    sentences = [
        s.strip() for s in sentences_text.split("\n") if s.strip()
    ]

    best_sentence, score = agent.find_most_similar(query, sentences)

    st.subheader("Best Matching Sentence")
    st.write(best_sentence)
    st.write(f"Similarity Score: {score:.4f}")