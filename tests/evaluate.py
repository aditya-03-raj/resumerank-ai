import os
import pandas as pd
from scipy.stats import spearmanr

from app.extraction import extract_text
from app.preprocessing import clean_text
from app.scoring import combined_score

RESUME_DIR = "data/resumes"
JD_PATH = "data/job_descriptions/ML_Intern.txt"
GROUND_TRUTH_PATH = "data/ground_truth.csv"
JOB_ID = "ml_intern"


def get_system_ranking(jd_path, resume_names):
    with open(jd_path, "r", encoding="utf-8") as f:
        jd_raw = f.read()
    jd_clean = clean_text(jd_raw)

    scores = {}
    for name in resume_names:
        path = os.path.join(RESUME_DIR, name)
        raw_text = extract_text(path)
        clean = clean_text(raw_text)
        final, _, _, _ = combined_score(jd_raw, jd_clean, raw_text, clean)
        scores[name] = final

    ranked = sorted(scores.items(), key=lambda pair: pair[1], reverse=True)
    return [name for name, score in ranked]


def precision_at_k(system_ranking, human_ranking, k):
    system_top_k = set(system_ranking[:k])
    human_top_k = set(human_ranking[:k])
    overlap = system_top_k & human_top_k
    return len(overlap) / k


ground_truth = pd.read_csv(GROUND_TRUTH_PATH)
job_rows = ground_truth[ground_truth["job_id"] == JOB_ID].sort_values("my_rank")

human_ranking = job_rows["resume_file"].tolist()
system_ranking = get_system_ranking(JD_PATH, human_ranking)

human_positions = {name: i for i, name in enumerate(human_ranking)}
system_positions = {name: i for i, name in enumerate(system_ranking)}

human_order = [human_positions[name] for name in human_ranking]
system_order = [system_positions[name] for name in human_ranking]

correlation, p_value = spearmanr(human_order, system_order)

print("Human ranking:", human_ranking)
print("System ranking:", system_ranking)
print()
print(f"Spearman correlation: {correlation:.3f} (p={p_value:.3f})")
print(f"Precision@3: {precision_at_k(system_ranking, human_ranking, 3):.2f}")
print(f"Precision@5: {precision_at_k(system_ranking, human_ranking, 5):.2f}")