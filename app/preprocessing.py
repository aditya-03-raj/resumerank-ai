import re
from nltk.corpus import stopwords
from app.skills_list import SKILLS, SKILL_ALIASES

stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()

    text = re.sub(r'\S+@\S',' ',text)
    text = re.sub(r'http\S+|www\.\S',' ',text)
    text = re.sub(r'\+?\d[\d\s\-()]{7,}\d', ' ', text)
    text = re.sub(r'[^a-z0-9\s]',' ',text)
    text = re.sub(r'\s+',' ',text).strip()

    text = text.replace("c++", "cplusplus")
    text = text.replace("c#", "csharp")
    text = text.replace(".net", "dotnet")

    words = text.split()
    words = [w for w in words if w not in stop_words]

    return ' '.join(words)

def normalize_skill_text(text):
    for alias, skill in SKILL_ALIASES.items():
        pattern = r'(?<![a-z0-9])' + re.escape(alias) + r'(?![a-z0-9])'
        text = re.sub(pattern, skill, text)
    return text


def extract_skills(text):
    text_lower = text.lower()
    text_lower = normalize_skill_text(text_lower)
    found=[]

    for skill in SKILLS:
        pattern = r'(?<![a-z0-9])' + re.escape(skill) + r'(?![a-z0-9])'
        if re.search(pattern,text_lower):
            found.append(skill)

    return found