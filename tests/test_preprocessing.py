from app.preprocessing import clean_text, extract_skills

def test_clean_text_removes_email():
    result = clean_text("contact me at test@examples.com for details")
    assert "@" not in result
    assert "example" not in result

def test_clean_text_lowercase():
    result = clean_text("Python is GOOD")
    assert result == result.lower()

def test_extract_skills_finds_known_skill():
    skills = extract_skills("I have experience with Python and Tensorflow")
    assert "python" in skills
    assert "tensorflow" in skills

def test_extract_skills_no_match_returns_empty():
    skills = extract_skills("I enjoy painting and playing")
    assert skills == []