from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class EmbeddingAgent:

    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def load_notes(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            notes = f.read().split("\n\n")

        return [note.strip() for note in notes if note.strip()]

    def search(self, query, notes):

        note_embeddings = self.model.encode(notes)

        query_embedding = self.model.encode([query])

        scores = cosine_similarity(
            query_embedding,
            note_embeddings
        )[0]

        best_index = np.argmax(scores)

        return notes[best_index], scores[best_index]