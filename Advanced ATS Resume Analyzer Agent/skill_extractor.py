COMMON_SKILLS = [
    "python", "java", "c++", "javascript", "html", "css",
    "machine learning", "deep learning", "artificial intelligence",
    "data analysis", "sql", "mysql", "mongodb",
    "flask", "django", "fastapi", "streamlit",
    "aws", "azure", "git", "github",
    "rest api", "oop", "pandas", "numpy",
    "scikit-learn", "tensorflow", "pytorch",
    "hugging face", "langchain", "rag", "vector database"
]


def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in COMMON_SKILLS:
        if skill in text:
            found_skills.append(skill.title())

    return sorted(set(found_skills))