from flask import Flask, render_template, request
import os
from pdfminer.high_level import extract_text
import re

app = Flask(__name__)

UPLOAD_FOLDER = "resumes"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# -------------------------
# SKILLS DATABASE
# -------------------------

SKILLS_DB = [
"python","java","c","c++","sql","mysql","mongodb",
"machine learning","deep learning","data science",
"data analysis","statistics",
"pandas","numpy","matplotlib","scikit-learn",
"tensorflow","pytorch","keras",
"flask","django","fastapi",
"html","css","javascript","react","node",
"git","github","docker","kubernetes",
"aws","azure","gcp",
"power bi","tableau",
"nlp","computer vision","data visualization"
]

# -------------------------
# EXTRACT SKILLS
# -------------------------

def extract_resume_skills(text):
    text = text.lower()
    skills_found = []

    for skill in SKILLS_DB:
        if skill in text:
            skills_found.append(skill)

    return list(set(skills_found))


def extract_job_skills(job_description):
    job_description = job_description.lower()
    skills = []

    for skill in SKILLS_DB:
        if skill in job_description:
            skills.append(skill)

    return list(set(skills))


# -------------------------
# RESUME SCORE
# -------------------------

def calculate_resume_score(resume_skills, required_skills):
    if len(required_skills) == 0:
        return 70

    matched = len(set(resume_skills) & set(required_skills))
    score = int((matched / len(required_skills)) * 100)

    return score


# -------------------------
# SMART SUGGESTION ENGINE
# -------------------------

def get_ai_suggestions(resume_text, resume_skills, required_skills, missing_skills):

    text = resume_text.lower()
    suggestions = ""

    suggestions += "Resume Review\n\n"

    # -------------------------
    # SECTION ANALYSIS
    # -------------------------

    if "project" not in text:
        suggestions += "- Add at least 2 projects to your resume.\n"
    else:
        if len(resume_text) < 800:
            suggestions += "- Your project descriptions are too short. Explain what you built and technologies used.\n"

    if "intern" not in text:
        suggestions += "- Add internship or real-world experience.\n"

    if len(resume_skills) < 5:
        suggestions += "- Add more technical skills to improve your resume.\n"

    # -------------------------
    # IMPROVEMENTS
    # -------------------------

    suggestions += "\nHow to Improve:\n"
    suggestions += "- Use bullet points\n"
    suggestions += "- Mention tools and technologies\n"
    suggestions += "- Add results (like accuracy or performance)\n"

    # -------------------------
    # WEAK SENTENCE FIX
    # -------------------------

    suggestions += "\nWeak Resume Example:\n"
    suggestions += "Instead of:\n"
    suggestions += "\"Built a website\"\n"
    suggestions += "Write:\n"
    suggestions += "\"Developed a responsive website using HTML, CSS, and JavaScript\"\n"

    # -------------------------
    # JOB ROLES
    # -------------------------

    suggestions += "\nSuggested Job Roles:\n"

    if "react" in resume_skills or "html" in resume_skills:
        suggestions += "- Frontend Developer\n"

    if "python" in resume_skills and "sql" in resume_skills:
        suggestions += "- Data Analyst\n"

    if "machine learning" in resume_skills:
        suggestions += "- Machine Learning Engineer\n"

    if "node" in resume_skills or "flask" in resume_skills:
        suggestions += "- Backend Developer\n"

    if len(resume_skills) < 3:
        suggestions += "- Software Developer\n"

    # -------------------------
    # SKILLS TO LEARN
    # -------------------------

    suggestions += "\nSkills to Learn:\n"

    if missing_skills:
        for skill in missing_skills:
            suggestions += f"- {skill}\n"
    else:
        suggestions += "- Your skills match the job well\n"

    return suggestions


# -------------------------
# ROUTES
# -------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload")
def upload():
    return render_template("upload.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files["resume"]
    job_description = request.form["job_description"]

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    resume_text = extract_text(filepath)

    resume_skills = extract_resume_skills(resume_text)
    required_skills = extract_job_skills(job_description)

    missing_skills = list(set(required_skills) - set(resume_skills))

    score = calculate_resume_score(resume_skills, required_skills)

    if missing_skills:
        suggestion = "Improve your resume by learning: " + ", ".join(missing_skills)
    else:
        suggestion = "Great! Your resume matches the job."

    ai_advice = get_ai_suggestions(
        resume_text,
        resume_skills,
        required_skills,
        missing_skills
    )

    return render_template(
        "result.html",
        skills=resume_skills,
        required_skills=required_skills,
        missing=missing_skills,
        score=score,
        suggestion=suggestion,
        ai_advice=ai_advice
    )


# -------------------------
# RUN APP
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)