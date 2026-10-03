from app.scoring import score_resumes

def test_identical_text_scores_close_to_one():
    scores = score_resumes("python machine learning", ["python machine learning"])
    assert scores[0] > 0.99

def test_unrelated_text_scores_low():
    scores = score_resumes("python machine learning", ["cooking recipes baking"])
    assert scores[0] < 0.3

def test_returns_one_score_per_resume():
    scores = score_resumes("python",["python developer","jave developer","chef"])
    assert len(scores) == 3