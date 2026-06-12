from fastapi import FastAPI, UploadFile, File, Form
from typing import List
from ats_agent import ATSResumeAnalyzerAgent

app = FastAPI(title="ATS Resume Analyzer Backend")

agent = ATSResumeAnalyzerAgent()


@app.get("/")
def home():
    return {"message": "ATS Resume Analyzer Backend is running"}


@app.post("/analyze")
async def analyze_resumes(
    jd_text: str = Form(...),
    resumes: List[UploadFile] = File(...)
):
    results = agent.analyze_resumes(jd_text, resumes)
    return {"results": results}