import os
from app.extraction import extract_text
from app.preprocessing import clean_text
from app.scoring import score_resumes_embeddings, score_resumes, combined_score

RESUME_DIR = "data/resumes"
JD_PATH= "data/job_descriptions/ML_Intern.txt"

with open(JD_PATH,"r",encoding="utf-8") as f:
    jd_raw = f.read()
jd_clean = clean_text(jd_raw)

resume_names = sorted(os.listdir(RESUME_DIR))
resume_raw_texts = [extract_text(os.path.join(RESUME_DIR,n)) for n in resume_names]
resume_clean_texts = [clean_text(t) for t in resume_raw_texts]

print(f"{'Resume':22s} {'skills':>8s} {'TF-IDF':>8s} {'Embed':>8s} {'Combined':>10s}")

results = []

for name, raw, clean in zip(resume_names, resume_raw_texts,resume_clean_texts):
    final, skill, tfidf, emb = combined_score(jd_raw, jd_clean, raw, clean)
    results.append((name,final,skill,tfidf,emb))

results.sort(key=lambda r: r[1], reverse=True)

for name, final, skill, tfidf, emb in results:
    print(f"{name:22s} {skill:8.3f} {tfidf:8.3f} {emb:8.3f} {final:10.3f}")
