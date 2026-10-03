import os

from app.extraction import extract_text
from app.preprocessing import clean_text
from app.preprocessing import extract_skills

RESUME_DIR = "data/resumes"

for name in sorted(os.listdir(RESUME_DIR)):
     path = os.path.join(RESUME_DIR,name)

     raw_text = extract_text(path)
     cleaned = clean_text(raw_text)
     skills = extract_skills(raw_text)

     print(name)
     print("Raw length : ",len(raw_text),"-> cleaned length", len(cleaned))
     print("skills found (",len(skills),"):",skills)
     print()

