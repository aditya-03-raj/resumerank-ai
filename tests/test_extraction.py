from app.extraction import extract_text


def test_unsupported_type_returns_empty():
    assert extract_text("notes.xyz") == ""


def test_missing_file_returns_empty():
    assert extract_text("data/resumes/does_not_exist.pdf") == ""
    