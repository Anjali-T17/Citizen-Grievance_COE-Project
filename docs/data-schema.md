# Database Schema & Entity-Relationship Documentation

## 1. Overview
The database layer uses SQLAlchemy ORM over SQLite for Phase 1. The schema is designed with standard relational constraints and foreign keys to enable seamless migration to PostgreSQL or MySQL in Phase 2.

All data is strictly synthetic and anonymised (`USER_001`, `ORG_001`, `COMPLAINT_001`). No real citizen personal data is used.

---

## 2. Table Schemas

### 2.1 `organisations`
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | VARCHAR | PRIMARY KEY | Unique Org ID (e.g. `ORG_001`) |
| `name` | VARCHAR | NOT NULL | Organisation Name (e.g. Municipal Corporation) |
| `code` | VARCHAR | UNIQUE, NOT NULL | Machine code (e.g. `MUNICIPAL_CORP`) |

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
| `status` | VARCHAR | DEFAULT 'Submitted' | Status (Submitted, Under Review, Escalated, Resolved) |
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

### 2.8 `usage_events`
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `event_id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Event ID |
| `anonymous_user_id` | VARCHAR | NOT NULL | Anonymous user ID |
| `organisation_id` | VARCHAR | NOT NULL | Organisation ID |
| `role` | VARCHAR | NOT NULL | Role at time of event |
| `feature_id` | VARCHAR | NOT NULL | Invoked feature ID |
| `task_goal` | VARCHAR | NULLABLE | Contextual task goal |
| `help_query` | VARCHAR | NULLABLE | Contextual help query |
| `timestamp` | DATETIME | DEFAULT UTC | Event timestamp |
| `action` | VARCHAR | DEFAULT 'view' | Action type (view, execute) |
| `success` | BOOLEAN | DEFAULT TRUE | Execution outcome |

### 2.9 `recommendations`
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Recommendation ID |
| `anonymous_user_id` | VARCHAR | NOT NULL | Targeted user ID |
| `task_goal` | VARCHAR | NULLABLE | Input task goal |
| `help_query` | VARCHAR | NULLABLE | Input help query |
| `recommended_feature_id` | VARCHAR | NOT NULL | Recommended feature ID |
| `score` | FLOAT | NOT NULL | Total score (0 - 100) |
| `allowed` | BOOLEAN | DEFAULT TRUE | Permission status |
| `evidence` | TEXT | NOT NULL | JSON string array of evidence |
| `timestamp` | DATETIME | DEFAULT UTC | Generation timestamp |

### 2.10 `overrides`
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Override ID |
| `recommendation_id` | INTEGER | NULLABLE | Associated recommendation ID |
| `anonymous_user_id` | VARCHAR | NOT NULL | User ID |
| `action` | VARCHAR | NOT NULL | Cancelled action code |
| `override_reason` | VARCHAR | NOT NULL | Reason dropdown selection |
| `comment` | TEXT | NULLABLE | Optional user comment |
| `timestamp` | DATETIME | DEFAULT UTC | Override timestamp |

### 2.11 `audit_logs`
| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Log ID |
| `anonymous_user_id` | VARCHAR | NOT NULL | User ID |
| `action` | VARCHAR | NOT NULL | Security or system action code |
| `details` | TEXT | NULLABLE | Additional context |
| `timestamp` | DATETIME | DEFAULT UTC | Log timestamp |
