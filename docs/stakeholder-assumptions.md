# Stakeholder Assumptions & Constraints Document

## 1. Stakeholders & User Persona Matrix

### 1.1 Citizen (End User)
- **Primary Goal**: Submit complaints quickly in their native regional language (Tamil, Hindi, English) with photo evidence.
- **Pain Point**: Overwhelmed by municipal administrative portals and unaware of tracking tools.
- **System Solution**: Simplified complaint submission form, automatic language detection tagging, and simple status tracking (F001, F002).

### 1.2 Grievance Officer (Departmental Staff)
- **Primary Goal**: Process incoming grievances efficiently across multiple regional languages and verify photo attachments.
- **Pain Point**: Difficulty comprehending grievances filed in non-native languages (e.g. Tamil grievances assigned to English-speaking officers) and discovering internal tools like Translation and Internal Notes.
- **System Solution**: Embedded Discovery Assistant recommending `F003 - Translate Complaint`, `F004 - Verify Attachment`, and `F006 - Internal Notes`.

### 1.3 Supervisor (Departmental Manager)
- **Primary Goal**: Monitor department SLA compliance, review escalations, and track feature usage analytics across staff.
- **Pain Point**: Lack of visibility into underused productivity features.
- **System Solution**: Access to `F007 - Complaint Monitoring` and real-time Feature Usage Analytics dashboard.

### 1.4 External Partner Agency (Contractor / Vendor)
- **Primary Goal**: Receive assigned maintenance tickets and upload execution proof/evidence.
- **System Solution**: Restricted access to `F008 - Upload Evidence` and `F004 - Verify Attachment`.

---

## 2. Key Operational Assumptions

1. **Synthetic Data Policy**: Real PII (Aadhaar, real names, phone numbers) is strictly prohibited. All demo users, complaints, and organisations use synthetic identifier conventions (`USER_001`, `COMPLAINT_001`, `ORG_001`).
2. **Transparent Explainability**: Stakeholders require explicit evidence breakdown ("Why this recommendation?") before accepting automated assistance.
3. **Human Control Over High-Impact Actions**: Automated tools must NOT automatically execute state-changing actions (like escalation) without explicit human confirmation.
4. **Backend Security Integrity**: Hiding buttons on the client is insufficient; backend REST endpoints must independently verify RBAC permissions and reject unauthorized requests with HTTP 403.
