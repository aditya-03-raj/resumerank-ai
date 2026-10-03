import os
from app.extraction import extract_text
from app.preprocessing import clean_text
from app.scoring import score_resumes

RESUME_DIR = "data/resumes"
JD_PATH = "data/job_descriptions/ML_Intern.txt"

with open(JD_PATH,"r",encoding="utf=8") as file:
    job_description_raw = file.read()

job_description_clean = clean_text(job_description_raw)

resume_names = sorted(os.listdir(RESUME_DIR))
resume_texts = []

for name in resume_names:
    path = os.path.join(RESUME_DIR,name)
    raw_text = extract_text(path)
    resume_texts.append(clean_text(raw_text))

scores = score_resumes(job_description_clean, resume_texts)

ranked = sorted(zip(resume_names,scores),key = lambda pair : pair[1],reverse = True)

print("Ranking for : ",JD_PATH)
print()
for rank, (name,score) in enumerate(ranked,start=1):
    print(f"{rank}. {name} - score: {score:4f}")