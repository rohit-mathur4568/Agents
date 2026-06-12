from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from pypdf import PdfReader
from skill_extractor import extract_skills


class ATSResumeAnalyzerAgent:
    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def extract_text_from_pdf(self, pdf_file):
        pdf_file.file.seek(0)
        reader = PdfReader(pdf_file.file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text.strip()

    def calculate_similarity_score(self, jd_text, resume_text):
        embeddings = self.model.encode([jd_text, resume_text])
        score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        return float(round(score * 100, 2))

    def calculate_skill_score(self, jd_skills, resume_skills):
        if not jd_skills:
            return 0.0

        matched_skills = set(jd_skills).intersection(set(resume_skills))
        score = (len(matched_skills) / len(jd_skills)) * 100
        return float(round(score, 2))

    def final_score(self, similarity_score, skill_score):
        score = (similarity_score * 0.6) + (skill_score * 0.4)
        return float(round(score, 2))

    def generate_summary(self, final_score, matched_skills, missing_skills):
        if final_score >= 80:
            status = "Strong candidate"
        elif final_score >= 60:
            status = "Good candidate"
        elif final_score >= 40:
            status = "Average candidate"
        else:
            status = "Weak match"

        summary = (
            f"{status}. Candidate matches skills like "
            f"{', '.join(matched_skills[:5]) if matched_skills else 'no major required skills'}."
        )

        if missing_skills:
            summary += f" Missing important skills: {', '.join(missing_skills[:5])}."

        return summary

    def analyze_resumes(self, jd_text, resume_files):
        jd_skills = extract_skills(jd_text)
        results = []

        for resume in resume_files:
            resume_text = self.extract_text_from_pdf(resume)
            resume_skills = extract_skills(resume_text)

            similarity_score = self.calculate_similarity_score(jd_text, resume_text)
            skill_score = self.calculate_skill_score(jd_skills, resume_skills)
            final_score = self.final_score(similarity_score, skill_score)

            matched_skills = sorted(set(jd_skills).intersection(set(resume_skills)))
            missing_skills = sorted(set(jd_skills).difference(set(resume_skills)))

            results.append({
                "Resume Name": resume.filename,
                "Final Score (%)": final_score,
                "Similarity Score (%)": similarity_score,
                "Skill Score (%)": skill_score,
                "Matched Skills": ", ".join(matched_skills),
                "Missing Skills": ", ".join(missing_skills),
                "Candidate Summary": self.generate_summary(
                    final_score,
                    matched_skills,
                    missing_skills
                )
            })

        return sorted(results, key=lambda x: x["Final Score (%)"], reverse=True)