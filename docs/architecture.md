# System Architecture & Technical Design Document

## 1. Executive Summary
This document defines the 100% complete system architecture for the **Role-Aware Feature Discovery Assistant Embedded for Citizen Grievance Application**. The application provides a multilingual grievance mechanism and an embedded recommendation engine that guides users (citizens, officers, supervisors, external partners) to underused and role-relevant features.

---

## 2. Overall System Architecture (100% System Blueprint)

```
 +-----------------------------------------------------------------------+
 |                         PRESENTATION LAYER                            |
 |  React + Vite + Tailwind CSS + Recharts + Lucide UI                   |
 |  - Role-aware Dynamic Navigation Sidebar                             |
 |  - Embedded Assistant Chat/Widget Panel                              |
 |  - Explainability Evidence Modal & High-Impact Confirmation Dialog   |
 +-----------------------------------+-----------------------------------+
                                     |
                                     | REST API (HTTP / JSON)
                                     v
 +-----------------------------------------------------------------------+
 |                         APPLICATION & API LAYER                       |
 |  FastAPI Async Micro-Framework                                        |
 |  - Auth / Demo Context Handler                                        |
 |  - Role-Based Access Control (RBAC) Enforcement Engine                |
 |  - Explainable Scoring Engine (100-Point Transparent Rule Matrix)     |
 |  - Adversarial Prompt Injection Protection Shield                     |
 |  - Analytics & Audit Logging Handler                                  |
 +-----------------------------------+-----------------------------------+
                                     |
                                     | ORM (SQLAlchemy)
                                     v
 +-----------------------------------------------------------------------+
 |                           PERSISTENCE LAYER                           |
 |  SQLite Database (Phase 1) -> PostgreSQL / MySQL (Phases 2 & 3)        |
 |  - Users, Roles, Organisations, Permissions                           |
 |  - Complaints & Attachments Metadata                                  |
 |  - Feature Catalog (F001-F008)                                        |
 |  - Synthetic Usage Events, Recommendations, Overrides, Audit Logs    |
 +-----------------------------------------------------------------------+
```

---

## 3. Key Subsystems & Design Choices

### 3.1 Explainable Recommendation Scoring Matrix (100 Points Max)
To guarantee 100% explainability without black-box opacity in Phase 1, recommendations are computed deterministically:
1. **Role Match (30 pts)**: Granted if user's role is listed in `allowed_roles`.
2. **Task Goal Match (30 pts)**: Granted if task goal string overlaps with feature `task_tags`.
3. **Help Query Match (20 pts)**: Granted if search query matches feature keywords/capabilities.
4. **Underuse Boost (10 pts)**: Granted if usage frequency of the feature is below average threshold in `usage_events`.
5. **Permission Verification (10 pts)**: Granted if backend RBAC check passes.

### 3.2 High-Impact Action Workflow
Features with `impact_level = "HIGH"` (such as `F005 - Escalate Complaint`) return `requires_confirmation = true`. The frontend interrupts automated execution and presents a human confirmation modal. If the user cancels, an override reason (`"Not urgent"`, `"Wrong recommendation"`, `"Already handled"`, `"Permission issue"`, `"Other"`) and comment are captured and logged to the SQLite `overrides` table.

### 3.3 Adversarial Prompt-Injection Protection
Untrusted user inputs (complaint descriptions, help queries) are sanitized against prompt-injection signatures (e.g., `"ignore instructions"`, `"show admin features"`, `"bypass permissions"`). When an attack vector is detected:
- The system flags `is_malicious = True`.
- Security warning is displayed ("Untrusted instruction detected. Role and permission controls remain enforced.").
- Role and permission restrictions remain 100% active and unbypassed.

---

## 4. Architectural Roadmap Across Evaluation Phases
- **Phase 1 (Review 1 — 35%) [CURRENT IMPLEMENTATION]**: End-to-end working MVP with React, FastAPI, SQLite DB, rule-based recommendation engine, RBAC enforcement, high-impact dialogs, override tracking, analytics charts, and unit tests.
- **Phase 2 (Review 2 — 35%) [RESERVED]**: ML/NLP TF-IDF & Vector embeddings for semantic search, PostgreSQL migration, baseline vs assistant discovery experiment.
- **Phase 3 (Final Review — 30%) [RESERVED]**: Production LLM RAG integration, final experiment evaluation, containerized deployment (Docker), and stakeholder validation.
