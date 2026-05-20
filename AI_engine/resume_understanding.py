import spacy
from pdfminer.high_level import extract_text

nlp = spacy.load("en_core_web_sm")

SKILLS_DB = [
"python","java","sql","machine learning","deep learning",
"data analysis","pandas","numpy","flask","django",
"html","css","javascript","react","node","git","docker",
"tensorflow","pytorch","statistics","data visualization"
]


def extract_resume_data(pdf_path):

    text = extract_text(pdf_path)

    doc = nlp(text.lower())

    skills = []

    for token in doc:
        if token.text in SKILLS_DB:
            skills.append(token.text)

    skills = list(set(skills))

    return {
        "skills": skills
    }


def extract_job_skills(job_description):

    doc = nlp(job_description.lower())

    skills = []

    for token in doc:
        if token.text in SKILLS_DB:
            skills.append(token.text)

    return list(set(skills))