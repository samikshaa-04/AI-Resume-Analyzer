JOB_ROLE_MAP = {

"python":["Python Developer","Backend Developer","Data Scientist"],

"machine learning":[
"Machine Learning Engineer",
"AI Engineer",
"Data Scientist"
],

"data analysis":[
"Data Analyst",
"Business Analyst"
],

"html":[
"Frontend Developer",
"Web Developer"
],

"css":[
"Frontend Developer"
],

"javascript":[
"Frontend Developer",
"Full Stack Developer"
],

"react":[
"Frontend Developer"
],

"node":[
"Backend Developer",
"Full Stack Developer"
],

"sql":[
"Database Developer",
"Data Analyst"
],

"data science":[
"Data Scientist"
],

"mongodb":[
"Database Developer"
],

"docker":[
"DevOps Engineer"
]

}

def suggest_jobs_from_skills(skills):

    jobs = []

    for skill in skills:

        if skill in JOB_ROLE_MAP:
            jobs.extend(JOB_ROLE_MAP[skill])

    return list(set(jobs))