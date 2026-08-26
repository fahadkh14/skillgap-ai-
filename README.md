# SkillGap AI

**Discover your skill gaps. Build your career roadmap.**

SkillGap AI is a career intelligence platform for students, freshers, and job
seekers. It compares your current skills against the requirements of a target
job role, calculates a transparent, deterministic job-readiness score,
identifies skill gaps, parses resumes, and builds a personalized, trackable
learning roadmap.

Built as a BCA final-year project with production-style DevOps practices:
Docker, Docker Compose, Nginx, Gunicorn, and MongoDB with authentication.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Technology Stack](#technology-stack)
5. [Project Structure](#project-structure)
6. [MongoDB Architecture](#mongodb-architecture)
7. [Environment Variables](#environment-variables)
8. [Docker Setup](#docker-setup)
9. [Local Development](#local-development)
10. [API Documentation](#api-documentation)
11. [Authentication](#authentication)
12. [Skill Gap Algorithm](#skill-gap-algorithm)
13. [Resume Processing](#resume-processing)
14. [Testing](#testing)
15. [Security](#security)
16. [Production Deployment](#production-deployment)
17. [Troubleshooting](#troubleshooting)
18. [Future Enhancements](#future-enhancements)

---

## Project Overview

SkillGap AI implements the full user journey:

```
Register → Login → Complete Profile → Add Skills → Upload Resume →
Select Target Job Role → Analyze Skills → Skill Gap Report →
Job Readiness Score → Personalized Roadmap → Track Progress → Re-analyze
```

Every number the app shows — readiness score, matched/partial/missing
counts, roadmap progress — is computed from real MongoDB data. Nothing is
hard-coded or randomized.

## Features

- Full JWT authentication (register, login, logout, current user)
- Editable professional profile (education, experience level, target role, bio)
- Skill management: add, edit, delete, search, and filter by proficiency
- Database-driven job roles with weighted, required/optional skill requirements
- Deterministic **Skill Gap Analysis Engine** (matched / partial / missing)
- Transparent, explainable **Job Readiness Score** (0-100)
- Skill priority ranking (Critical / High / Medium / Low)
- Personalized, phased **Learning Roadmap** with progress tracking
- PDF/DOCX **resume upload** with automatic skill detection and user approval
- Analysis history with score-over-time comparison
- Professional dashboard with circular readiness gauge, skill breakdown,
  top gaps, and recent analyses
- Responsive, accessible SaaS-style UI: sidebar, cards, tables, progress
  bars, modals, toasts, skeleton/empty/error states

## Architecture

```
                         USER
                           |
                           v
                  +----------------+
                  | Nginx          |
                  | React + Vite   |
                  | Port 8050      |
                  +-------+--------+
                          |
                       /api/*
                          |
                          v
                  +----------------+
                  | Flask API      |
                  | Gunicorn       |
                  | Port 5678      |
                  +-------+--------+
                          |
                       PyMongo
                          |
                          v
                  +----------------+
                  | MongoDB        |
                  | Port 27017     |
                  | (internal only)|
                  +----------------+
```

The frontend never talks to MongoDB directly — only Flask does.

## Technology Stack

**Frontend:** React, Vite, React Router, Axios, plain CSS (custom design system)
**Backend:** Python 3.12, Flask, PyMongo, Flask-JWT-Extended, bcrypt, Gunicorn, python-dotenv
**Database:** MongoDB 8.x
**DevOps:** Docker, Docker Compose, Nginx, healthchecks, persistent volumes

## Project Structure

```
skillgap-ai/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/      # Reusable UI (icons, gauge, modals, etc.)
│   │   ├── pages/            # Route-level pages
│   │   ├── layouts/          # AppLayout (sidebar + topbar)
│   │   ├── services/         # Axios-based API modules
│   │   ├── context/          # Auth + Toast context providers
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   ├── nginx.conf
│   └── Dockerfile
│
├── backend/
│   ├── app/
│   │   ├── routes/           # auth, profile, skills, job_roles, analysis,
│   │   │                       resume, roadmap, dashboard, health
│   │   ├── services/         # skill_gap_service, roadmap_service,
│   │   │                       resume_parser_service, ai_recommendation_service
│   │   ├── middleware/       # auth.py, error_handler.py
│   │   ├── utils/            # validators.py, responses.py
│   │   ├── config.py
│   │   ├── extensions.py
│   │   └── __init__.py       # app factory
│   ├── tests/
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── run.py
│   └── Dockerfile
│
├── database/
│   └── seed.py                # job roles, skill catalog, demo user, indexes
│
├── docker-compose.yml
├── .env.example
├── .gitignore
├── .dockerignore
└── README.md
```

## MongoDB Architecture

Collections:

| Collection          | Purpose                                             |
|----------------------|------------------------------------------------------|
| `users`              | Account credentials (bcrypt-hashed passwords)       |
| `profiles`           | Extended user profile fields                        |
| `skills`             | Per-user skills with proficiency and experience     |
| `skill_catalog`      | Standard catalog of known skill names (used for resume detection) |
| `job_roles`          | Roles with weighted, required/optional skill lists  |
| `analyses`           | Stored skill-gap analysis results                    |
| `roadmaps`           | Per-user, per-role generated learning roadmaps       |
| `resumes`            | Resume upload metadata + detected skills (never raw resume content) |

Indexes created by `database/seed.py`:

```
users.email                (unique)
analyses.user_id
analyses.created_at
job_roles.name              (unique)
skills.user_id + skill_name
skill_catalog.name          (unique)
roadmaps.user_id + job_role_id
```

## Environment Variables

Copy `.env.example` to `.env` and replace every placeholder:

```env
FLASK_ENV=production

SECRET_KEY=change_this_secret
JWT_SECRET_KEY=change_this_jwt_secret

MONGO_URI=mongodb://admin:change_this_root_password@mongodb:27017/skillgap?authSource=admin
MONGO_DB_NAME=skillgap

MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=change_this_root_password

BACKEND_PORT=5678
FRONTEND_PORT=8050

CORS_ORIGINS=http://localhost:8050
```

Generate strong secrets with:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

**Never commit `.env`.** It's already listed in `.gitignore`.

## Docker Setup

```bash
git clone <repository>
cd skillgap-ai

cp .env.example .env
# edit .env and set real secrets/passwords

docker compose up -d --build
```

Then seed the database (job roles, skill catalog, demo user):

```bash
docker compose exec backend python database/seed.py
```

Verify:

```bash
docker compose ps
```

- Frontend: http://localhost:8050
- Backend health: http://localhost:5678/api/health

Useful commands:

```bash
docker compose ps
docker compose logs -f
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f mongodb
docker compose restart
docker compose down
```

For complete cleanup **(this permanently deletes the MongoDB volume and all data)**:

```bash
docker compose down -v
```

## Local Development

**Backend:**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate           # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt

export MONGO_URI="mongodb://localhost:27017/skillgap"
export MONGO_DB_NAME="skillgap"
export SECRET_KEY="dev-secret"
export JWT_SECRET_KEY="dev-jwt-secret"
export FLASK_ENV="development"

python run.py     # dev server on :5678
```

Seed locally with a running MongoDB instance:

```bash
python ../database/seed.py
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev        # dev server on :5173, proxies /api to :5678
```

## API Documentation

All responses follow a consistent envelope:

```json
{ "success": true, "message": "...", "data": {} }
{ "success": false, "message": "...", "error": {} }
```

### Auth
```
POST /api/auth/register   { full_name, email, password, confirm_password }
POST /api/auth/login      { email, password }
POST /api/auth/logout     (auth required)
GET  /api/auth/me         (auth required)
```

### Profile
```
GET /api/profile          (auth required)
PUT /api/profile          (auth required)
```

### Skills
```
GET    /api/skills?search=&proficiency=   (auth required)
POST   /api/skills        { skill_name, proficiency, years_of_experience }
PUT    /api/skills/:id    { proficiency?, years_of_experience?, skill_name? }
DELETE /api/skills/:id
```

### Job Roles
```
GET /api/job-roles
GET /api/job-roles/:id
```

### Analysis
```
POST /api/analysis        { job_role_id }   -> runs analysis + generates roadmap
GET  /api/analysis
GET  /api/analysis/:id
```

### Resume
```
POST /api/resume/upload   multipart/form-data, field name "file" (PDF/DOCX, max 5MB)
```

### Roadmap
```
GET /api/roadmap?job_role_id=
PUT /api/roadmap/:id      { skill, status?, progress? }
```

### Dashboard
```
GET /api/dashboard
```

### Health
```
GET /api/health   -> { "status": "healthy", "database": "connected" }
```

## Authentication

- Passwords are hashed with **bcrypt**; plain-text passwords are never stored or returned.
- Login issues a **JWT** (12-hour expiry) signed with `JWT_SECRET_KEY`.
- Protected routes require `Authorization: Bearer <token>`.
- Logout revokes the token via an in-memory blocklist (suitable for a
  single-instance deployment; swap for a Redis-backed blocklist for
  multi-instance production use).

## Skill Gap Algorithm

Implemented in `backend/app/services/skill_gap_service.py`.

For each required/optional skill on the target role:

- **Matched** — user has the skill at or above the minimum required proficiency → 100% of the skill's weight
- **Partial** — user has the skill but below the required proficiency → 50% of the skill's weight
- **Missing** — user doesn't have the skill → 0% of the skill's weight

```
readiness_score = round(100 * sum(earned_weight) / sum(total_weight))
```

This is fully deterministic and reproducible — running the same analysis
twice against unchanged skill data always returns the same score (verified
in `tests/test_analysis.py::test_readiness_score_is_deterministic`).

Priority for partial/missing skills (Critical/High/Medium/Low) factors in:
required vs. optional status, the skill's weight, and how large the
proficiency gap is.

## Resume Processing

Implemented in `backend/app/services/resume_parser_service.py`.

```
Upload → Validate (extension, MIME type, size) → Extract text (PyPDF2 / python-docx)
       → Match against skill_catalog → Return suggestions → User approves → Add skills
```

- Only PDF and DOCX are accepted, capped at 5 MB.
- Detected skills are returned to the frontend for explicit user approval —
  nothing is added to the profile automatically.
- Raw resume text is **never persisted** to the database or written to logs;
  only the filename and the list of detected skill names are stored.

## Testing

Backend tests (pytest + mongomock, no live MongoDB required):

```bash
cd backend
pip install -r requirements-dev.txt
pytest tests/ -v
```

Covers: registration, login, protected routes, skill creation/deletion,
analysis calculation, deterministic readiness scoring, roadmap generation,
and the health endpoint. All 15 tests pass.

## Security

- bcrypt password hashing; password hashes never returned by any API
- JWT auth with secrets sourced from environment variables
- Centralized input validation (`app/utils/validators.py`)
- MongoDB queries use PyMongo's parameterized operators (no string-built queries)
- CORS restricted to configured origins
- File upload validation: extension, MIME type, and 5 MB max size
- MongoDB requires authentication and is not published to the host
- Generic error responses in production — no stack traces leaked to clients
- Non-root user inside the backend Docker container

**Never exposed by any endpoint:** MongoDB credentials, the JWT secret,
password hashes, stack traces, or uploaded resume contents.

## Production Deployment

1. Provision a host with Docker + Docker Compose installed.
2. Copy the repository and create `.env` with strong, unique secrets.
3. **Change or remove the demo account** (`demo@skillgap.local`) before
   exposing the app publicly — see [Demo Account](#demo-account) below.
4. Run `docker compose up -d --build`.
5. Put the stack behind a reverse proxy / load balancer with TLS termination
   if exposing it to the public internet (this project's built-in Nginx
   serves plain HTTP on port 8050 inside the Docker network).
6. Monitor `docker compose logs -f` and the `/api/health` endpoint.

### Demo Account

`database/seed.py` creates a demo account for evaluation:

```
Email:    demo@skillgap.local
Password: ChangeMe123!
```

**Change or remove this account before any real deployment.**

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `backend` unhealthy / restarting | MongoDB not ready yet, or wrong `MONGO_URI` | Check `docker compose logs mongodb` and confirm `.env` credentials match |
| `403`/`401` on every request | Missing/expired JWT | Log in again; check `Authorization: Bearer <token>` header |
| Frontend shows blank page | Build failed | Run `docker compose logs frontend`; verify `npm run build` succeeds locally |
| Resume upload fails with 422 | File isn't PDF/DOCX, or exceeds 5 MB | Convert or compress the file |
| `docker compose up` can't reach Docker Hub | No network / firewall | Verify your host has outbound internet access |
| Data disappeared after `docker compose down -v` | The `-v` flag deletes the MongoDB volume | Use `docker compose down` (without `-v`) to preserve data |

## Future Enhancements

The backend includes an `AIRecommendationService` abstraction
(`backend/app/services/ai_recommendation_service.py`) reserved for future,
optional AI-powered features — **no external AI API is required for the
current version to function**:

- AI-generated resume analysis and improvement suggestions
- AI career recommendations and job-description matching
- AI-assisted roadmap generation
- Conversational AI career assistant
- Job description analysis against a user's live skill profile
