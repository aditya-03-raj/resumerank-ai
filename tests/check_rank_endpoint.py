import requests

url = "http://127.0.0.1:8000/rank"

job_description = """Machine Learning Intern. Collect, clean, and preprocess structured datasets.
Experiment with Logistic Regression, Random Forest, XGBoost, and clustering.
Good knowledge of Python, Pandas, NumPy, Scikit-learn, SQL, Git."""

resume_paths = [
    "data/resumes/resume_16.pdf",
    "data/resumes/resume_19.pdf",
    "data/resumes/resume_12.docx",
]

files = [("resumes", (path.split("/")[-1], open(path, "rb"))) for path in resume_paths]
data = {"job_description": job_description}

response = requests.post(url, data=data, files=files)
print(response.status_code)

import json
print(json.dumps(response.json(), indent=2))
