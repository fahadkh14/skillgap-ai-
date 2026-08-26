"""
Seed script for SkillGap AI.

Populates:
  - Unique/query indexes
  - Standard skills catalog
  - Job roles with weighted skill requirements
  - A demo user account (clearly marked; change/remove before real deployment)

Run inside the backend container / environment where PyMongo + the same
MONGO_URI are available:

    python database/seed.py
"""
import os
import sys
from datetime import datetime, timezone

import bcrypt
from pymongo import MongoClient, ASCENDING

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/skillgap")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "skillgap")

SKILL_CATALOG = [
    "Python", "Java", "JavaScript", "TypeScript", "React", "Node.js", "Flask",
    "Django", "Git", "GitHub", "Docker", "Kubernetes", "AWS", "Azure", "GCP",
    "Terraform", "Ansible", "Linux", "MongoDB", "MySQL", "PostgreSQL", "Redis",
    "Jenkins", "GitHub Actions", "CI/CD", "Prometheus", "Grafana", "REST API",
    "GraphQL", "HTML", "CSS", "SQL", "NoSQL", "Bash", "Shell Scripting",
    "Agile", "Scrum", "Unit Testing", "Selenium", "Cypress", "Postman",
    "Data Structures", "Algorithms", "Machine Learning", "Pandas", "NumPy",
    "Power BI", "Tableau", "Excel", "Networking", "Cybersecurity Fundamentals",
    "Nginx", "Microservices", "System Design", "OOP",
]

JOB_ROLES = [
    {
        "name": "DevOps Engineer",
        "description": "Infrastructure automation, CI/CD pipelines, and deployment engineering.",
        "skills": [
            {"name": "Linux", "required": True, "weight": 10, "minimum_proficiency": "Intermediate"},
            {"name": "Git", "required": True, "weight": 8, "minimum_proficiency": "Intermediate"},
            {"name": "Docker", "required": True, "weight": 10, "minimum_proficiency": "Intermediate"},
            {"name": "CI/CD", "required": True, "weight": 9, "minimum_proficiency": "Intermediate"},
            {"name": "Kubernetes", "required": True, "weight": 12, "minimum_proficiency": "Intermediate"},
            {"name": "AWS", "required": True, "weight": 10, "minimum_proficiency": "Intermediate"},
            {"name": "Terraform", "required": True, "weight": 9, "minimum_proficiency": "Beginner"},
            {"name": "Python", "required": False, "weight": 6, "minimum_proficiency": "Beginner"},
            {"name": "Prometheus", "required": False, "weight": 5, "minimum_proficiency": "Beginner"},
            {"name": "Grafana", "required": False, "weight": 5, "minimum_proficiency": "Beginner"},
            {"name": "Bash", "required": False, "weight": 6, "minimum_proficiency": "Intermediate"},
            {"name": "Ansible", "required": False, "weight": 5, "minimum_proficiency": "Beginner"},
        ],
    },
    {
        "name": "Python Developer",
        "description": "Backend and application development using Python.",
        "skills": [
            {"name": "Python", "required": True, "weight": 12, "minimum_proficiency": "Advanced"},
            {"name": "Flask", "required": True, "weight": 9, "minimum_proficiency": "Intermediate"},
            {"name": "Django", "required": False, "weight": 8, "minimum_proficiency": "Intermediate"},
            {"name": "REST API", "required": True, "weight": 9, "minimum_proficiency": "Intermediate"},
            {"name": "SQL", "required": True, "weight": 8, "minimum_proficiency": "Intermediate"},
            {"name": "Git", "required": True, "weight": 7, "minimum_proficiency": "Intermediate"},
            {"name": "MongoDB", "required": False, "weight": 6, "minimum_proficiency": "Beginner"},
            {"name": "Docker", "required": False, "weight": 6, "minimum_proficiency": "Beginner"},
            {"name": "Unit Testing", "required": False, "weight": 6, "minimum_proficiency": "Beginner"},
            {"name": "Data Structures", "required": True, "weight": 8, "minimum_proficiency": "Intermediate"},
        ],
    },
    {
        "name": "Backend Developer",
        "description": "Server-side application logic, APIs, and databases.",
        "skills": [
            {"name": "Node.js", "required": True, "weight": 9, "minimum_proficiency": "Intermediate"},
            {"name": "REST API", "required": True, "weight": 10, "minimum_proficiency": "Intermediate"},
            {"name": "SQL", "required": True, "weight": 8, "minimum_proficiency": "Intermediate"},
            {"name": "MongoDB", "required": False, "weight": 7, "minimum_proficiency": "Beginner"},
            {"name": "Git", "required": True, "weight": 7, "minimum_proficiency": "Intermediate"},
            {"name": "Docker", "required": False, "weight": 6, "minimum_proficiency": "Beginner"},
            {"name": "System Design", "required": False, "weight": 8, "minimum_proficiency": "Beginner"},
            {"name": "Microservices", "required": False, "weight": 7, "minimum_proficiency": "Beginner"},
            {"name": "Redis", "required": False, "weight": 5, "minimum_proficiency": "Beginner"},
        ],
    },
    {
        "name": "Frontend Developer",
        "description": "User interface development with modern JavaScript frameworks.",
        "skills": [
            {"name": "JavaScript", "required": True, "weight": 12, "minimum_proficiency": "Advanced"},
            {"name": "React", "required": True, "weight": 12, "minimum_proficiency": "Intermediate"},
            {"name": "HTML", "required": True, "weight": 8, "minimum_proficiency": "Advanced"},
            {"name": "CSS", "required": True, "weight": 8, "minimum_proficiency": "Advanced"},
            {"name": "TypeScript", "required": False, "weight": 7, "minimum_proficiency": "Beginner"},
            {"name": "Git", "required": True, "weight": 6, "minimum_proficiency": "Intermediate"},
            {"name": "REST API", "required": False, "weight": 6, "minimum_proficiency": "Beginner"},
        ],
    },
    {
        "name": "Full Stack Developer",
        "description": "End-to-end web application development.",
        "skills": [
            {"name": "JavaScript", "required": True, "weight": 10, "minimum_proficiency": "Advanced"},
            {"name": "React", "required": True, "weight": 10, "minimum_proficiency": "Intermediate"},
            {"name": "Node.js", "required": True, "weight": 9, "minimum_proficiency": "Intermediate"},
            {"name": "MongoDB", "required": False, "weight": 7, "minimum_proficiency": "Beginner"},
            {"name": "SQL", "required": False, "weight": 6, "minimum_proficiency": "Beginner"},
            {"name": "Git", "required": True, "weight": 7, "minimum_proficiency": "Intermediate"},
            {"name": "REST API", "required": True, "weight": 8, "minimum_proficiency": "Intermediate"},
            {"name": "Docker", "required": False, "weight": 5, "minimum_proficiency": "Beginner"},
        ],
    },
    {
        "name": "Cloud Engineer",
        "description": "Design and manage cloud infrastructure and services.",
        "skills": [
            {"name": "AWS", "required": True, "weight": 12, "minimum_proficiency": "Advanced"},
            {"name": "Azure", "required": False, "weight": 7, "minimum_proficiency": "Beginner"},
            {"name": "Terraform", "required": True, "weight": 10, "minimum_proficiency": "Intermediate"},
            {"name": "Linux", "required": True, "weight": 9, "minimum_proficiency": "Intermediate"},
            {"name": "Networking", "required": True, "weight": 8, "minimum_proficiency": "Intermediate"},
            {"name": "Docker", "required": True, "weight": 8, "minimum_proficiency": "Intermediate"},
            {"name": "Kubernetes", "required": False, "weight": 8, "minimum_proficiency": "Beginner"},
            {"name": "Bash", "required": False, "weight": 5, "minimum_proficiency": "Beginner"},
        ],
    },
    {
        "name": "Software Engineer",
        "description": "General-purpose software engineering across the stack.",
        "skills": [
            {"name": "Data Structures", "required": True, "weight": 10, "minimum_proficiency": "Advanced"},
            {"name": "Algorithms", "required": True, "weight": 10, "minimum_proficiency": "Advanced"},
            {"name": "OOP", "required": True, "weight": 8, "minimum_proficiency": "Intermediate"},
            {"name": "Git", "required": True, "weight": 7, "minimum_proficiency": "Intermediate"},
            {"name": "SQL", "required": False, "weight": 6, "minimum_proficiency": "Beginner"},
            {"name": "System Design", "required": False, "weight": 7, "minimum_proficiency": "Beginner"},
            {"name": "Unit Testing", "required": False, "weight": 6, "minimum_proficiency": "Beginner"},
        ],
    },
    {
        "name": "Data Analyst",
        "description": "Analyze data to generate business insights.",
        "skills": [
            {"name": "SQL", "required": True, "weight": 12, "minimum_proficiency": "Advanced"},
            {"name": "Excel", "required": True, "weight": 9, "minimum_proficiency": "Advanced"},
            {"name": "Python", "required": False, "weight": 7, "minimum_proficiency": "Beginner"},
            {"name": "Pandas", "required": False, "weight": 6, "minimum_proficiency": "Beginner"},
            {"name": "Power BI", "required": False, "weight": 7, "minimum_proficiency": "Beginner"},
            {"name": "Tableau", "required": False, "weight": 6, "minimum_proficiency": "Beginner"},
            {"name": "NumPy", "required": False, "weight": 4, "minimum_proficiency": "Beginner"},
        ],
    },
    {
        "name": "Cybersecurity Analyst",
        "description": "Protect systems, networks, and data from security threats.",
        "skills": [
            {"name": "Cybersecurity Fundamentals", "required": True, "weight": 12, "minimum_proficiency": "Advanced"},
            {"name": "Networking", "required": True, "weight": 10, "minimum_proficiency": "Advanced"},
            {"name": "Linux", "required": True, "weight": 8, "minimum_proficiency": "Intermediate"},
            {"name": "Bash", "required": False, "weight": 5, "minimum_proficiency": "Beginner"},
            {"name": "Python", "required": False, "weight": 6, "minimum_proficiency": "Beginner"},
        ],
    },
    {
        "name": "QA Engineer",
        "description": "Ensure software quality through manual and automated testing.",
        "skills": [
            {"name": "Unit Testing", "required": True, "weight": 9, "minimum_proficiency": "Intermediate"},
            {"name": "Selenium", "required": True, "weight": 9, "minimum_proficiency": "Intermediate"},
            {"name": "Cypress", "required": False, "weight": 7, "minimum_proficiency": "Beginner"},
            {"name": "Postman", "required": True, "weight": 7, "minimum_proficiency": "Intermediate"},
            {"name": "Git", "required": True, "weight": 6, "minimum_proficiency": "Beginner"},
            {"name": "Agile", "required": False, "weight": 5, "minimum_proficiency": "Beginner"},
        ],
    },
]

DEMO_EMAIL = "demo@skillgap.local"
DEMO_PASSWORD = "ChangeMe123!"


def run_seed():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[MONGO_DB_NAME]

    print(f"Connected to MongoDB database '{MONGO_DB_NAME}'. Seeding...")

    # --- Indexes ---
    db.users.create_index([("email", ASCENDING)], unique=True)
    db.analyses.create_index([("user_id", ASCENDING)])
    db.analyses.create_index([("created_at", ASCENDING)])
    db.job_roles.create_index([("name", ASCENDING)], unique=True)
    db.skills.create_index([("user_id", ASCENDING), ("skill_name", ASCENDING)])
    db.skill_catalog.create_index([("name", ASCENDING)], unique=True)
    db.roadmaps.create_index([("user_id", ASCENDING), ("job_role_id", ASCENDING)])
    print("Indexes created.")

    # --- Skill catalog ---
    for name in SKILL_CATALOG:
        db.skill_catalog.update_one({"name": name}, {"$set": {"name": name}}, upsert=True)
    print(f"Seeded {len(SKILL_CATALOG)} catalog skills.")

    # --- Job roles ---
    for role in JOB_ROLES:
        db.job_roles.update_one(
            {"name": role["name"]},
            {"$set": role},
            upsert=True,
        )
    print(f"Seeded {len(JOB_ROLES)} job roles.")

    # --- Demo user ---
    if not db.users.find_one({"email": DEMO_EMAIL}):
        password_hash = bcrypt.hashpw(DEMO_PASSWORD.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        now = datetime.now(timezone.utc)
        result = db.users.insert_one({
            "name": "Demo User",
            "email": DEMO_EMAIL,
            "password_hash": password_hash,
            "created_at": now,
            "updated_at": now,
        })
        db.profiles.insert_one({
            "user_id": result.inserted_id,
            "full_name": "Demo User",
            "email": DEMO_EMAIL,
            "phone": "",
            "college": "Demo College of Engineering",
            "education": "BCA",
            "graduation_year": 2026,
            "experience_level": "Fresher",
            "current_role": "",
            "target_role": "DevOps Engineer",
            "bio": "This is a demo account seeded for evaluation purposes.",
            "created_at": now,
            "updated_at": now,
        })
        db.skills.insert_many([
            {"user_id": result.inserted_id, "skill_name": "Linux", "proficiency": "Intermediate",
             "years_of_experience": 1, "created_at": now, "updated_at": now},
            {"user_id": result.inserted_id, "skill_name": "Git", "proficiency": "Intermediate",
             "years_of_experience": 1, "created_at": now, "updated_at": now},
            {"user_id": result.inserted_id, "skill_name": "Docker", "proficiency": "Beginner",
             "years_of_experience": 0.5, "created_at": now, "updated_at": now},
            {"user_id": result.inserted_id, "skill_name": "Python", "proficiency": "Intermediate",
             "years_of_experience": 1.5, "created_at": now, "updated_at": now},
        ])
        print(f"Demo user created: {DEMO_EMAIL} / {DEMO_PASSWORD}")
        print("!! This is a DEMO account. Change or remove it before any real deployment. !!")
    else:
        print("Demo user already exists, skipping.")

    print("Seeding complete.")


if __name__ == "__main__":
    try:
        run_seed()
    except Exception as e:
        print(f"Seeding failed: {e}", file=sys.stderr)
        sys.exit(1)
