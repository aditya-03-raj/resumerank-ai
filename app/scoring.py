from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from app.preprocessing import extract_skills

_model = None

def score_resumes(job_description_text, resume_texts):
    documents = [job_description_text] + resume_texts

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    job_vector = tfidf_matrix[0:1]
    resume_vectors = tfidf_matrix[1:]

    scores = cosine_similarity(job_vector,resume_vectors)[0]

    return scores

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def score_resumes_embeddings(job_description_text,resume_texts):
    model = get_model()

    all_texts = [job_description_text] + resume_texts
    embeddings = model.encode(all_texts)

    job_embedding = embeddings[0:1]
    resume_embeddings = embeddings[1:]

    scores = cosine_similarity(job_embedding, resume_embeddings)[0]

    return scores

def skill_overlap_score(jd_text,resume_text):
    jd_skills = extract_skills(jd_text)
    resume_skills = extract_skills(resume_text)

    if not jd_skills:
        return 0.0

    matched = set(jd_skills) & set(resume_skills)
    return len(matched) / len(jd_skills)

def combined_score(jd_raw_text, jd_clean_text, resume_raw_text, resume_clean_text,
                   skill_weight=0.5, embedding_weight=0.3,tfidf_weight=0.2):

    skill_score = skill_overlap_score(jd_raw_text,resume_raw_text)
    tfidf_score = score_resumes(jd_clean_text,[resume_clean_text])[0]
    embedding_score = score_resumes_embeddings(jd_raw_text,[resume_raw_text])[0]

    final = (skill_weight * skill_score) + (embedding_weight * embedding_score) + (tfidf_weight * tfidf_score)
    return final, skill_score, tfidf_score, embedding_score

def get_matched_skills(jd_text, resume_text):
    jd_skills = extract_skills(jd_text)
    resume_skills = extract_skills(resume_text)

    matched = sorted(set(jd_skills) & set(resume_skills))
    missing = sorted(set(jd_skills) - set(resume_skills))

    return matched, missing