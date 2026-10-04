from fastapi import FastAPI, UploadFile, File, Form
from typing import List
import shutil
import os
import tempfile
from fastapi.responses import RedirectResponse
from app.preprocessing import clean_text
from app.extraction import extract_text
from app.scoring import score_resumes, score_resumes_embeddings, skill_overlap_score, combine_scores, get_matched_skills

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title = "ResumeRank AI")

app.mount("/static",StaticFiles(directory="static"),name="static")

@app.get("/app")
def serve_frontend():
    return FileResponse("static/index.html")

@app.get("/health")
def health_check():
    return {"status":"ok", "message":"ResumeRank AI is running"}

@app.get("/")
def root():
    return RedirectResponse(url="/app")

@app.post("/rank")
async def rank_resumes(
    job_description: str = Form(...),
    resumes: List[UploadFile] = File(...)
):
    if not job_description.strip():
        return {"error": "Job description cannot be empty"}
    if not resumes:
        return {"error": "At least one resume file must be uploaded"}

    jd_raw = job_description
    jd_clean = clean_text(jd_raw)

    filenames = []
    raw_texts = []
    clean_texts = []
    failed = []

    for resume in resumes:
        try:
            suffix = os.path.splitext(resume.filename)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                shutil.copyfileobj(resume.file, temp_file)
                temp_path = temp_file.name

            raw_text = extract_text(temp_path)
            os.remove(temp_path)

            if not raw_text.strip():
                failed.append({"filename": resume.filename, "error": "No text could be extracted"})
                continue

            filenames.append(resume.filename)
            raw_texts.append(raw_text)
            clean_texts.append(clean_text(raw_text))

        except Exception as error:
            failed.append({"filename": resume.filename, "error": str(error)})

   
    scored = []
    if filenames:
        tfidf_scores = score_resumes(jd_clean, clean_texts)
        embedding_scores = score_resumes_embeddings(jd_raw, raw_texts)

        for i, filename in enumerate(filenames):
            skill_score = skill_overlap_score(jd_raw, raw_texts[i])
            final = combine_scores(skill_score, tfidf_scores[i], embedding_scores[i])
            matched_skills, missing_skills = get_matched_skills(jd_raw, raw_texts[i])

            scored.append({
                "filename": filename,
                "score": round(float(final), 4),
                "skill_score": round(float(skill_score), 4),
                "tfidf_score": round(float(tfidf_scores[i]), 4),
                "embedding_score": round(float(embedding_scores[i]), 4),
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
            })

    scored.sort(key=lambda r: r["score"], reverse=True)
    for position, item in enumerate(scored, start=1):
        item["rank"] = position

    return {"job_description_preview": jd_raw[:100], "results": scored + failed}