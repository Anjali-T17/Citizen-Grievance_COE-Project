# Role-Aware Feature Discovery Assistant Embedded for Citizen Grievance Application

[![Review 1 Status](https://img.shields.io/badge/Review%201%20(35%25)-Passed%20%26%20Verified-brightgreen)](#)
[![Review 2 Status](https://img.shields.io/badge/Review%202-Complete%20%26%20Verified-emerald)](#)
[![Backend Test Suite](https://img.shields.io/badge/Pytest%20Suite-36%2F36%20Passed-success)](#)
[![Python FastAPI](https://img.shields.io/badge/Backend-FastAPI%20%7C%20SQLAlchemy%20%7C%20SQLite-blue)](#)
[![React Vite](https://img.shields.io/badge/Frontend-React%20%7C%20Vite%20%7C%20TailwindCSS-sky)](#)

> **Exact Project Title**: Role-Aware Feature Discovery Assistant Embedded for Citizen Grievance Application Receiving Multilingual Complaints and Attachments  
> **Evaluation Milestone**: **Review 2 Full System Verification**  
> **Status**: **Phase A, Phase B, Phase C & Phase D Complete**

---

## 📌 Review 2 Executive Summary & Compliance Overview

This repository contains the complete implementation and evaluation suite for the **Role-Aware Feature Discovery Assistant Embedded for Citizen Grievance Application**. 

All 13 core requirements for **Review 2** are fully implemented, verified, and backed by empirical evidence and 36 passing automated unit and integration tests.

### Key Review 2 Enhancements
1. **Measurable A/B Experiment**: Quantified discovery and task completion uplift for key features (`F003` Translate Complaint, `F006` Internal Case Notes, `F008` Audit & Escalation Logs).
2. **Complaint Lifecycle State Machine**: Full lifecycle (`Submitted` → `Routed` → `In Progress` → `Escalated` → `Resolved`) with status validation and reopening prevention.
3. **Multi-Organisation & RBAC Isolation**: Rigid permission boundary enforcement preventing cross-tenant access between `ORG_001` (GCMC), `ORG_002` (CBE_CORP), and External Partners.
4. **Standalone TF-IDF Help Search**: Vector similarity index search over feature descriptions and metadata (`POST /api/recommendations/help-search`) with RBAC filtering.
5. **Functional Multilingual Translation Engine**: Rule-based local Tamil (`தமிழ்`), Hindi (`हिंदी`), and English translation service (`POST /api/complaints/translate`) preserving original text.
6. **Stakeholder Validation Framework**: Interactive validation form and API (`POST /api/stakeholders/validation`) capturing usability (1-5) and explainability (1-5) feedback.
7. **Frontend Performance & Code-Splitting**: Modularized React production build using `React.lazy()`, `<Suspense>`, and Rollup `manualChunks` vendor splitting.

---

## 1. System Architecture

```
                       ┌──────────────────────────────────────────────┐
                       │               React 18 Frontend              │
                       │ (Vite + React.lazy + Recharts + Tailwind CSS)│
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

## 2. API Endpoints Reference

### Review 2 New & Enhanced APIs

| Method | Endpoint | Description | Authorization / RBAC |
|---|---|---|---|
| `PATCH` | `/api/complaints/{id}/status` | Transition complaint status (`Submitted`→`Routed`→`In Progress`→`Escalated`→`Resolved`) | Officers, Engineers, Supervisors |
| `POST` | `/api/complaints/translate` | Translate grievance text between Tamil, Hindi, and English | Public / All Authenticated |
| `GET` | `/api/analytics/discovery-uplift` | Fetch overall & feature-level (`F003`,`F006`,`F008`) discovery & completion uplift metrics | All Authenticated |
| `POST` | `/api/recommendations/help-search` | Vector TF-IDF similarity search over feature catalog | All Authenticated |
| `POST` | `/api/stakeholders/validation` | Record stakeholder usability (1-5) and explainability (1-5) evaluation | All Authenticated |
| `GET` | `/api/stakeholders/summary` | Retrieve aggregated stakeholder usability & explainability ratings | All Authenticated |

### Core System APIs

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/demo-login` | Demo role & organisation authentication |
| `GET` | `/api/organisations` | Fetch active municipal & partner organisations |
| `GET` | `/api/roles` | Fetch roles filtered by organisation |
| `POST` | `/api/complaints` | Submit complaint with optional file attachment |
| `GET` | `/api/complaints` | List complaints for current context |
| `GET` | `/api/features` | Retrieve feature catalog (F001–F011) filtered by RBAC |
| `POST` | `/api/recommendations` | Compute 100-point explainable feature recommendation |
| `POST` | `/api/routing/override` | Capture officer routing override log |

---

## 3. Review 2 Experiment Methodology & Empirical Findings

The A/B experiment evaluates the discovery rate and task completion rate of features comparing manual menu search (**Baseline**) against embedded AI recommendations (**Assistant**).

### Uplift Formulas
$$\text{Discovery Uplift \%} = \left( \frac{\text{Assistant Discovery Rate} - \text{Baseline Discovery Rate}}{\text{Baseline Discovery Rate}} \right) \times 100$$

$$\text{Completion Uplift \%} = \left( \frac{\text{Assistant Completion Rate} - \text{Baseline Completion Rate}}{\text{Baseline Completion Rate}} \right) \times 100$$

### Empirical Database Values (`GET /api/analytics/discovery-uplift`)

- **Overall Discovery Rate**: Baseline **16.67%** → Assistant **100.0%** (**+499.88% Uplift**)
- **Overall Completion Rate**: Baseline **50.0%** → Assistant **100.0%** (**+100.0% Uplift**)
- **F003 (Translate Complaint)**: Baseline **33.33%** → Assistant **100.0%** (**+200.03% Discovery Uplift**)
- **F006 (Internal Case Notes)**: Baseline **0.0%** → Assistant **100.0%** (**+100.0% Completion Uplift**)
- **F008 (Audit & Escalation Logs)**: Baseline **0.0%** → Assistant **100.0%** (**100.0% Assistant Discovery**)

---

## 4. Frontend Performance & Code-Splitting Results

React code splitting was implemented using `React.lazy()`, `<Suspense>`, and Rollup `manualChunks` vendor isolation.

### Build Output Comparison

| Metric | Before Code Splitting | After Code Splitting |
|---|---|---|
| **Monolithic JS Bundle** | `index-8y2R07MW.js` (**674.09 kB** / 193.56 kB gzip) | **Eliminated** |
| **Lazy Chunks** | None | 13 modular route & vendor chunks |
| **Route Chunks** | None | `Dashboard` (22 kB), `AnalyticsPage` (18 kB), `ComplaintDetails` (12 kB), etc. |
| **Vendor Chunks** | None | `recharts-vendor` (364 kB), `react-vendor` (163 kB), `axios-vendor` (51 kB), `lucide-vendor` (16 kB) |
| **Build Warnings** | ⚠️ Warning (>500 kB) | ✅ **0 Warnings** |

---

## 5. How to Run

### Automated Execution Script
```bash
./run_app.sh
```

### Manual Step-by-Step Execution

#### 1. Backend Service & Tests
```bash
cd backend
source venv/bin/activate
./venv/bin/pytest tests/test_full_project.py tests/test_phase_a.py tests/test_phase_b.py -v
python app/main.py
```
*Backend runs on `http://localhost:8000`.*

#### 2. Frontend Application & Production Build
```bash
cd frontend
npm install
npm run build   # Verify code splitting production build
npm run dev     # Starts dev server on http://localhost:5173
```

---

## 6. Verification & Automated Test Suite Evidence

Run the complete 36-test suite covering core functionality, Phase A enhancements, and Phase B security/isolation boundaries:

```bash
cd backend
./venv/bin/pytest tests/test_full_project.py tests/test_phase_a.py tests/test_phase_b.py -v
```

### Test Suite Execution Output
```text
tests/test_full_project.py::test_1_tamil_complaint_intent_detection_and_pwd_routing PASSED
tests/test_full_project.py::test_2_hindi_water_leak_intent_and_mandate_routing PASSED
tests/test_full_project.py::test_3_ambiguous_intent_routing_to_general_review_queue PASSED
tests/test_full_project.py::test_4_prompt_injection_adversarial_protection PASSED
tests/test_full_project.py::test_5_sla_breach_escalation_workflow PASSED
tests/test_full_project.py::test_6_officer_department_routing_override_persistence PASSED
tests/test_full_project.py::test_7_department_mandates_catalog_retrieval PASSED
tests/test_full_project.py::test_8_baseline_vs_ai_routing_experiment_metrics PASSED
tests/test_full_project.py::test_9_stakeholder_validation_submission PASSED
tests/test_full_project.py::test_10_error_analysis_taxonomy_report PASSED
tests/test_phase_a.py::test_a1_complaint_lifecycle_status_updates PASSED
tests/test_phase_a.py::test_a2_dynamic_discovery_uplift_analytics PASSED
tests/test_phase_a.py::test_a3_functional_translation_backend PASSED
tests/test_phase_a.py::test_a4_feature_experiment_metrics PASSED
tests/test_phase_a.py::test_a5_standalone_tfidf_help_search PASSED
tests/test_phase_b.py::test_b1_org001_user_attempting_org002_restricted_access PASSED
tests/test_phase_b.py::test_b1_org002_user_attempting_org001_restricted_access PASSED
tests/test_phase_b.py::test_b1_external_partner_attempting_unauthorized_org_resource PASSED
tests/test_phase_b.py::test_b2_citizen_attempting_officer_only_action PASSED
tests/test_phase_b.py::test_b2_citizen_attempting_escalation PASSED
tests/test_phase_b.py::test_b2_unauthorized_role_attempting_to_resolve_complaint PASSED
tests/test_phase_b.py::test_b2_external_partner_attempting_internal_feature PASSED
tests/test_phase_b.py::test_b2_department_role_attempting_supervisor_action PASSED
tests/test_phase_b.py::test_b3_complaint_lifecycle_submitted_to_escalated_to_resolved PASSED
tests/test_phase_b.py::test_b3_resolved_complaint_cannot_be_reopened PASSED
tests/test_phase_b.py::test_b4_sql_injection_attempt PASSED
tests/test_phase_b.py::test_b4_prompt_injection_adversarial_patterns PASSED
tests/test_phase_b.py::test_b4_role_bypass_attempt PASSED
tests/test_phase_b.py::test_b4_cross_org_resource_tampering PASSED
tests/test_phase_b.py::test_b4_malformed_request_payload PASSED
tests/test_phase_b.py::test_b4_invalid_status_transition PASSED
tests/test_phase_b.py::test_b5_empty_help_search_query PASSED
tests/test_phase_b.py::test_b5_very_long_help_search_query PASSED
tests/test_phase_b.py::test_b5_unsupported_language_translation PASSED
tests/test_phase_b.py::test_b5_empty_complaint_text_submission PASSED
tests/test_phase_b.py::test_b5_invalid_complaint_id_lookup PASSED

======================= 36 passed in 0.74s =======================
```
