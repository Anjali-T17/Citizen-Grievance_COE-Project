# Review 2 API Endpoint Inventory & Technical Specification

This document provides a detailed specification for the primary REST API endpoints implemented in Review 2.

---

## 1. Complaint Status Lifecycle API

### `PATCH /api/complaints/{complaint_id}/status`
- **Purpose**: Update complaint lifecycle state (`Submitted` → `Routed` → `In Progress` → `Escalated` → `Resolved`).
- **Authorization / RBAC**: Restricted to `Supervisor`, `Routing Officer`, `PWD Engineer`, `Water Engineer`, `Sanitation Lead`, `System Admin`. Blocked for `Citizen` and `External Partner` roles (HTTP 403 Forbidden).
- **Request Payload**:
  ```json
  {
    "status": "Resolved",
    "role": "Supervisor",
    "organisation": "GCMC",
    "user_id": "OFFICER_001",
    "comment": "Issue fixed by field team."
  }
  ```
- **Response**: Returns updated `ComplaintSchema` object. Reopening a `Resolved` complaint or attempting invalid state jumps returns `HTTP 400 Bad Request`.

---

## 2. Multilingual Translation API

### `POST /api/complaints/translate`
- **Purpose**: Translate grievance description text deterministically between Tamil, Hindi, and English.
- **Authorization / RBAC**: Unrestricted / All authenticated application roles.
- **Request Payload**:
  ```json
  {
    "text": "தெரு விளக்கு எரியவில்லை.",
    "source_language": "Tamil",
    "target_language": "English"
  }
  ```
- **Response**:
  ```json
  {
    "original_text": "தெரு விளக்கு எரியவில்லை.",
    "translated_text": "Street light is not working.",
    "source_language": "Tamil",
    "target_language": "English",
    "engine": "Deterministic Local Rule-Based Translator Engine"
  }
  ```

---

## 3. A/B Discovery Uplift Analytics API

### `GET /api/analytics/discovery-uplift`
- **Purpose**: Compute dynamic overall and feature-level (`F003`, `F006`, `F008`) discovery & completion rates, uplift percentages, and sample sizes from SQLite `experiment_metrics` and `usage_events` tables.
- **Authorization / RBAC**: All authenticated users.
- **Response Schema**:
  ```json
  {
    "baseline_discovery_rate": 16.67,
    "assistant_discovery_rate": 100.0,
    "discovery_uplift_percentage": 499.88,
    "baseline_completion_rate": 50.0,
    "assistant_completion_rate": 100.0,
    "completion_uplift_percentage": 100.0,
    "feature_level_results": {
      "F003": {
        "feature_id": "F003",
        "feature_name": "Translate Complaint",
        "baseline_discovery_rate": 33.33,
        "assistant_discovery_rate": 100.0,
        "discovery_uplift_percentage": 200.03,
        "baseline_completion_rate": 66.67,
        "assistant_completion_rate": 100.0,
        "completion_uplift_percentage": 49.99,
        "baseline_sample_size": 3,
        "assistant_sample_size": 3
      }
    },
    "total_events": 17,
    "total_users": 5
  }
  ```

---

## 4. Standalone TF-IDF Help Search API

### `POST /api/recommendations/help-search`
- **Purpose**: Compute vector cosine similarity scores over feature metadata catalog (`TfIdfScorer`) with role/organisation RBAC permission checks.
- **Authorization / RBAC**: All authenticated roles. Returns `allowed: true/false` per feature based on caller's role & organisation.
- **Request Payload**:
  ```json
  {
    "query": "Tamil translation",
    "role": "Grievance Officer",
    "organisation": "GCMC"
  }
  ```
- **Response**:
  ```json
  {
    "query": "Tamil translation",
    "total_matches": 8,
    "results": [
      {
        "feature_id": "F003",
        "feature_name": "Translate Complaint",
        "description": "Translate Tamil/Hindi complaint text to English",
        "similarity_score": 0.45,
        "allowed": true,
        "impact_level": "Medium"
      }
    ]
  }
  ```

---

## 5. Stakeholder System Validation APIs

### `POST /api/stakeholders/validation`
- **Purpose**: Record evaluator usability, explainability, speedup gain, and qualitative findings into `stakeholder_validations` database table.
- **Request Payload**:
  ```json
  {
    "stakeholder_role": "Routing Officer",
    "usability_rating": 5,
    "explainability_rating": 5,
    "routing_speedup_pct": 45.0,
    "feedback_notes": "Multilingual translation reduces manual processing time."
  }
  ```

### `GET /api/stakeholders/summary`
- **Purpose**: Aggregate average usability score, explainability score, speedup gain, and role breakdown from `stakeholder_validations` database table.
- **Response**: Returns aggregated mean ratings and persona review breakdown.
