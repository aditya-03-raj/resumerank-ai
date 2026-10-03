from fastapi import FastAPI, UploadFile, File, Form
from typing import List
import shutil
import os
import tempfile

from app.preprocessing import clean_text
from app.extraction import extract_text
from app.scoring import combined_score, get_matched_skills

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title = "ResumeRank AI")

app.mount("/static",StaticFiles(directory="static"),name="static")

@app.get("/app")
def serve_frontend():
    return FileResponse("static/index.html")

@app.get("/")
def health_check():
    return {"status":"ok", "message":"ResumeRank AI is running"}

@app.post("/rank")
async def rank_resumes(
    job_description : str = Form(...),
    resumes : List[UploadFile] = File(...)
):
    if not job_description.strip():
        return {"error":"Job description cannot be empty"}
    if not resumes:
        return {"error":"At least one resume file must be uploaded"}

    jd_raw = job_description
    jd_clean = clean_text(jd_raw)

    ranked = []

    for resume in resumes:
        try:
            suffix = os.path.splitext(resume.filename)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                shutil.copyfileobj(resume.file, temp_file)
                temp_path = temp_file.name

            raw_text = extract_text(temp_path)

            if not raw_text.strip():
                ranked.append({"filename":resume.filename,"error":"No text could be extracted"})
                os.remove(temp_path)
                continue

            clean_t = clean_text(raw_text)
            final, skill, tfidf, emb = combined_score(jd_raw,jd_clean,raw_text,clean_t)
            matched_skills, missing_skills = get_matched_skills(jd_raw, raw_text)
            
            ranked.append({
                "filename" : resume.filename,
                "score" : round(float(final),4),
                "skill_score" : round(float(skill),4),
                "tfidf_score" : round(float(tfidf),4),
                "embedding_score" : round(float(emb),4),
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
            })
            os.remove(temp_path)

        except Exception as error:
            ranked.append({"filename":resume.filename, "error":str(error)})

    scored = [r for r in ranked if "score" in r]
    failed = [r for r in ranked if "score" not in r]

    scored.sort(key=lambda r:r["score"],reverse=True)
    for position, item in enumerate(scored, start=1):
        item["rank"] = position

    return {"job_description_preview":jd_raw[:100],"results":scored+failed}