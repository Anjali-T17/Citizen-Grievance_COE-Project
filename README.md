# Role-Aware Feature Discovery Assistant Embedded for Citizen Grievance Application

[![Project Status](https://img.shields.io/badge/System-100%25%20Fully%20Completed-emerald)](#)
[![Python FastAPI](https://img.shields.io/badge/Backend-FastAPI%20%7C%20SQLAlchemy%20%7C%20SQLite-blue)](#)
[![React Vite](https://img.shields.io/badge/Frontend-React%20%7C%20Vite%20%7C%20TailwindCSS-sky)](#)
[![Docker](https://img.shields.io/badge/Deployment-Docker%20Compose%20Ready-indigo)](#)

A role-aware feature discovery assistant embedded inside a citizen grievance application receiving multilingual complaints and photo/document attachments.

---

## 1. Complete System Summary

The **Role-Aware Feature Discovery Assistant** solves feature undiscoverability in complex municipal citizen grievance applications. The application receives multilingual complaints in Tamil (`தமிழ்`), Hindi (`हिंदी`), and English with photo/document attachments.

The embedded assistant analyzes:
- User role & organisation context across 4 organisations and 6 roles
- RBAC permission boundaries
- User task goals & help-search queries using TF-IDF vector similarity
- Synthetic feature usage histories (boosting underused features)
- Feature metadata (F001 to F011)

It provides 100% explainable recommendations with an interactive **"Why this recommendation?"** modal, enforces human confirmation on high-impact actions (`F005 - Escalate Complaint`), logs override reasons, protects against prompt injection attacks, and tracks A/B experiment discovery & task completion improvements.

---

## 2. Technology Stack

- **Frontend**: React 18, Vite, Tailwind CSS, React Router v6, Recharts, Lucide Icons
- **Backend API**: Python 3.13, FastAPI, Pydantic v2, SQLAlchemy 2.0 ORM, TF-IDF Vector Scorer
- **Database**: SQLite (`grievance_app.db`) for lightweight single-file storage (designed for instant PostgreSQL/MySQL migration)
- **Testing**: Pytest (10/10 test cases passed)
- **Deployment**: Docker, Docker Compose, `run_app.sh`

---

## 3. API Endpoints Overview

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/demo-login` | Demo role & organisation authentication |
| `GET` | `/api/organisations` | Fetch organisations list (Municipal, Partner, PWD, Health) |
| `GET` | `/api/roles` | Fetch roles filtered by organisation |
| `POST` | `/api/complaints` | Submit multilingual complaint & attachment |
| `GET` | `/api/complaints` | Fetch complaints list from SQLite DB |
| `GET` | `/api/complaints/{id}` | Fetch complaint details with attachments |
| `POST` | `/api/complaints/{id}/attachments` | Upload supporting document file |
| `GET` | `/api/features` | Fetch feature catalog (F001 - F011) |
| `GET` | `/api/features/{id}` | Check feature details & test backend permission |
| `POST` | `/api/recommendations` | Compute hybrid TF-IDF + rule-based recommendation |
| `POST` | `/api/recommendations/feedback` | Rate recommendation (`Helpful 👍` / `Not Helpful 👎`) |
| `POST` | `/api/overrides` | Log human override reason & comments |
| `GET` | `/api/analytics/usage` | Dynamic feature usage metrics & underuse count |
| `GET` | `/api/analytics/error-analysis` | System error & failure mode taxonomy |
| `GET` | `/api/experiments/baseline-vs-assistant` | A/B Baseline vs Assistant experiment metrics |
| `POST` | `/api/stakeholders/validation` | Submit stakeholder usability & explainability rating |
| `GET` | `/api/stakeholders/summary` | Fetch stakeholder evaluation summary |

---

## 4. How to Run

### Option A: Local Script Execution
```bash
./run_app.sh
```

### Option B: Manual Execution
```bash
# 1. Start Backend API & Run Tests
cd backend
source venv/bin/activate
./venv/bin/pytest tests/test_full_project.py -v   # Run 10/10 unit tests
python app/main.py                              # Runs on http://localhost:8000

# 2. Start Frontend App
cd frontend
npm run dev                                     # Runs on http://localhost:5173
```

### Option C: Docker Containerized Deployment
```bash
docker-compose up --build
```

---

## 5. Verification & Testing
Run the automated Pytest suite:
```bash
cd backend
./venv/bin/pytest tests/test_full_project.py -v
```
Output:
```text
backend/tests/test_full_project.py::test_1_officer_tamil_translation_recommendation PASSED [ 10%]
backend/tests/test_full_project.py::test_2_citizen_access_denied_for_restricted_feature PASSED [ 20%]
backend/tests/test_full_project.py::test_3_prompt_injection_protection PASSED [ 30%]
backend/tests/test_full_project.py::test_4_escalation_recommendation_requires_confirmation PASSED [ 40%]
backend/tests/test_full_project.py::test_5_override_escalation_reason_persistence PASSED [ 50%]
backend/tests/test_full_project.py::test_6_recommendation_feedback_rating PASSED [ 60%]
backend/tests/test_full_project.py::test_7_tfidf_similarity_scoring PASSED [ 70%]
backend/tests/test_full_project.py::test_8_ab_experiment_summary_metrics PASSED [ 80%]
backend/tests/test_full_project.py::test_9_stakeholder_validation_submission PASSED [ 90%]
backend/tests/test_full_project.py::test_10_error_analysis_taxonomy_report PASSED [100%]

======================= 10 passed in 0.61s =======================
```
