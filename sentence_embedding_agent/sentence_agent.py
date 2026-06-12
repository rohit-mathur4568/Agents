from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class SentenceEmbeddingAgent:

    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def compare_sentences(self, sentence1, sentence2):
        embeddings = self.model.encode([sentence1, sentence2])
        score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        return score

    def find_most_similar(self, query, sentences):
        sentence_embeddings = self.model.encode(sentences)
        query_embedding = self.model.encode([query])

        scores = cosine_similarity(query_embedding, sentence_embeddings)[0]
        best_index = np.argmax(scores)

        return sentences[best_index], scores[best_index]