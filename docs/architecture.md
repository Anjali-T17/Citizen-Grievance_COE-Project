# System Architecture & Technical Design Document (Review 2 Complete)

## 1. Executive Summary
This document defines the system architecture for the **Role-Aware Feature Discovery Assistant Embedded for Citizen Grievance Application**. The application provides a multilingual grievance mechanism and an embedded recommendation engine that guides users (citizens, officers, supervisors, external partners) to underused and role-relevant features.

---

## 2. Overall System Architecture

```
                       ┌──────────────────────────────────────────────┐
                       │               React 18 Frontend              │
                       │ (Vite + React.lazy Code Splitting + Recharts) │
                       └──────────────────────┬───────────────────────┘
                                              │ HTTP JSON API
                                              ▼
┌───────────────────────────────────────────────────────────────────────────────────────────┐
│                                FastAPI Backend Service                                    │
│                                                                                           │
│  ┌───────────────────────┐   ┌───────────────────────┐   ┌─────────────────────────────┐  │
│  │   PermissionService   │   │  RecommendationEngine │   │     TranslationService      │  │
│  │ (Multi-Org & RBAC Rules)  │   │  (TF-IDF + Rules Engine)  │   │ (Tamil/Hindi/English Engine)│  │
│  └───────────┬───────────┘   └───────────┬───────────┘   └──────────────┬──────────────┘  │
│              │                           │                              │                 │
│              └───────────────────────────┼──────────────────────────────┘                 │
│                                          │                                                │
│                                          ▼                                                │
│                              ┌───────────────────────┐                                    │
│                              │  SQLAlchemy ORM Layer │                                    │
│                              └───────────┬───────────┘                                    │
└──────────────────────────────────────────┼────────────────────────────────────────────────┘
                                           │
                                           ▼
                                ┌──────────────────────┐
                                │ SQLite Database      │
                                │ (`grievance_app.db`) │
                                └──────────────────────┘
```

---

## 3. Key Subsystems & Design Choices

### 3.1 Explainable Recommendation Scoring Matrix (100 Points Max)
Recommendations are computed deterministically:
1. **Role Match (30 pts)**: Granted if user's role is listed in `allowed_roles`.
2. **Task Goal Match (30 pts)**: Granted if task goal string overlaps with feature `task_tags`.
3. **Help Query Match (20 pts)**: Granted if search query matches feature keywords/capabilities.
4. **Underuse Boost (10 pts)**: Granted if usage frequency of the feature is below average threshold in `usage_events`.
5. **Permission Verification (10 pts)**: Granted if backend RBAC check passes.

### 3.2 Standalone TF-IDF Help Search Subsystem
Vector cosine similarity index (`TfIdfScorer`) computes term-frequency inverse-document-frequency relevance over feature descriptions and task tags for `POST /api/recommendations/help-search`. Results are filtered by RBAC permissions and ranked by similarity score.

### 3.3 Multilingual Translation Service
Determines source language (Tamil, Hindi, English) and maps vocabulary to target language deterministically while preserving original complaint text in database records.

### 3.4 Complaint Lifecycle State Machine
Strict state machine enforces transitions: `Submitted` → `Routed` → `In Progress` → `Escalated` → `Resolved`. Reopening resolved grievances is rejected with HTTP 400. All status updates are audited in `AuditLog`.

### 3.5 Multi-Organisation Isolation & RBAC
`PermissionService` enforces rigid tenant isolation (preventing `ORG_001` GCMC users from accessing `ORG_002` CBE_CORP resources) and role-level boundaries (preventing Citizens from executing officer/supervisor workflows).

---

## 4. Frontend Performance & Code Splitting
Route-level dynamic imports via `React.lazy()` and `<Suspense>` combined with Rollup `manualChunks` vendor splitting separate React, Recharts, Lucide Icons, and Axios dependencies into 13 modular bundle chunks.
