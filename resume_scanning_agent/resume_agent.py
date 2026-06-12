from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from pypdf import PdfReader
import numpy as np


class ResumeScreeningAgent:

    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def extract_text_from_pdf(self, pdf_file):
        reader = PdfReader(pdf_file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text.strip()

    def calculate_match_score(self, jd_text, resume_text):
        embeddings = self.model.encode([jd_text, resume_text])
        score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        return round(score * 100, 2)

    def rank_resumes(self, jd_text, resume_files):
        results = []

        for resume in resume_files:
            resume_text = self.extract_text_from_pdf(resume)
            score = self.calculate_match_score(jd_text, resume_text)

            results.append({
                "Resume Name": resume.name,
                "Match Score (%)": score,
                "Extracted Text Preview": resume_text[:500]
            })

        results = sorted(
            results,
            key=lambda x: x["Match Score (%)"],
            reverse=True
        )

        return results