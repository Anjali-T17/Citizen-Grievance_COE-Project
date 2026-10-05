# Database Schema & Entity-Relationship Documentation (Review 2 Complete)

## 1. Overview
The database layer uses SQLAlchemy ORM over SQLite (`grievance_app.db`). The schema is designed with standard relational constraints and foreign keys to enable seamless migration to PostgreSQL or MySQL.

All data is strictly synthetic and anonymised (`USER_001`, `ORG_001`, `COMPLAINT_001`). No real citizen personal data is used.

---

## 2. Table Schemas

### 2.1 `organisations`
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | VARCHAR | PRIMARY KEY | Unique Org ID (e.g. `ORG_001`, `ORG_002`) |
| `name` | VARCHAR | NOT NULL | Organisation Name (e.g. Municipal Corporation) |
| `code` | VARCHAR | UNIQUE, NOT NULL | Machine code (e.g. `GCMC`, `CBE_CORP`) |

### 2.2 `roles`
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | VARCHAR | PRIMARY KEY | Role ID (e.g. `ROLE_CITIZEN`, `ROLE_OFFICER`) |
| `name` | VARCHAR | NOT NULL | Role Name (Citizen, Grievance Officer, Supervisor, Partner) |
| `org_id` | VARCHAR | FOREIGN KEY (`organisations.id`) | Owning organisation ID |

### 2.3 `users`
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | VARCHAR | PRIMARY KEY | User ID (e.g. `USER_001`) |
| `name` | VARCHAR | NOT NULL | Synthetic User Name |
| `email` | VARCHAR | NOT NULL | Synthetic Email |
| `role_id` | VARCHAR | FOREIGN KEY (`roles.id`) | Assigned Role ID |
| `org_id` | VARCHAR | FOREIGN KEY (`organisations.id`) | Assigned Organisation ID |

### 2.4 `permissions`
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Permission Record ID |
| `role_id` | VARCHAR | FOREIGN KEY (`roles.id`) | Targeted Role |
| `feature_code` | VARCHAR | NOT NULL | Target Feature ID (e.g. `F003`) |
| `can_access` | BOOLEAN | DEFAULT TRUE | Explicit permission flag |

### 2.5 `features`
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `feature_id` | VARCHAR | PRIMARY KEY | Feature Code (F001 - F008) |
| `feature_name` | VARCHAR | NOT NULL | Human-readable name |
| `description` | TEXT | NOT NULL | Detailed capability description |
| `allowed_roles` | TEXT | NOT NULL | Comma-separated allowed roles |
| `allowed_organisations` | TEXT | NOT NULL | Comma-separated allowed orgs |
| `permission_level` | VARCHAR | DEFAULT 'BASIC' | Access tier (BASIC, OFFICER, SUPERVISOR, PARTNER) |
| `impact_level` | VARCHAR | DEFAULT 'LOW' | Impact tier (LOW, HIGH) |
| `task_tags` | TEXT | NOT NULL | Comma-separated keyword tags |

### 2.6 `complaints`
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `complaint_id` | VARCHAR | PRIMARY KEY | Anonymous ID (`COMPLAINT_001`) |
| `user_id` | VARCHAR | FOREIGN KEY (`users.id`) | Submitting user ID |
| `description` | TEXT | NOT NULL | Grievance description text |
| `language` | VARCHAR | NOT NULL | Language (English, Tamil, Hindi) |
| `category` | VARCHAR | NOT NULL | Category (Public Safety, Water, Roads, etc.) |
| `priority` | VARCHAR | DEFAULT 'Medium' | Priority level (Low, Medium, High) |
| `status` | VARCHAR | DEFAULT 'Submitted' | Lifecycle Status (Submitted, Routed, In Progress, Escalated, Resolved) |
| `created_at` | DATETIME | DEFAULT UTC | Submission timestamp |

### 2.7 `attachments`
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Attachment ID |
| `complaint_id` | VARCHAR | FOREIGN KEY (`complaints.complaint_id`) | Related complaint ID |
| `filename` | VARCHAR | NOT NULL | Attachment filename |
| `file_type` | VARCHAR | NOT NULL | MIME content type |
| `file_size` | INTEGER | NOT NULL | Size in bytes |
| `upload_status` | VARCHAR | DEFAULT 'Uploaded' | Verification status |

### 2.8 `experiment_metrics`
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Metric ID |
| `group` | VARCHAR | NOT NULL | Test Group (`BASELINE`, `ASSISTANT`) |
| `feature_id` | VARCHAR | NOT NULL | Targeted Feature ID (`F003`, `F006`, `F008`) |
| `discovered` | BOOLEAN | DEFAULT FALSE | Whether feature was discovered |
| `completed` | BOOLEAN | DEFAULT FALSE | Whether task was successfully completed |
| `time_to_discover_sec` | FLOAT | DEFAULT 0.0 | Time spent discovering feature |

### 2.9 `stakeholder_validations`
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Record ID |
| `stakeholder_role` | VARCHAR | NOT NULL | Evaluator Role (Routing Officer, Engineer, etc.) |
| `usability_rating` | INTEGER | NOT NULL | Score 1–5 |
| `explainability_rating` | INTEGER | NOT NULL | Score 1–5 |
| `routing_speedup_pct` | FLOAT | DEFAULT 45.0 | Speedup percentage estimate |
| `feedback_notes` | TEXT | NULLABLE | Qualitative evaluator findings |
| `timestamp` | DATETIME | DEFAULT UTC | Evaluation timestamp |
