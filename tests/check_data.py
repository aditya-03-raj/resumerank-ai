import os

RESUME_DIR = "data/resumes"
JD_DIR = "data/job_descriptions"


def list_files(folder, allowed_extensions):
    found = []
    for name in os.listdir(folder):
        extension = os.path.splitext(name)[1].lower()
        if extension in allowed_extensions:
            found.append(os.path.join(folder, name))
    return found


if __name__ == "__main__":
    resumes = list_files(RESUME_DIR, [".pdf", ".docx"])
    job_descriptions = list_files(JD_DIR, [".txt"])

    print("Resumes found:", len(resumes))
    for path in resumes:
        print("  ", path)

    print("Job descriptions found:", len(job_descriptions))
    for path in job_descriptions:
        print("  ", path)