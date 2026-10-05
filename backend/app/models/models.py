import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Organisation(Base):
    __tablename__ = "organisations"

    id = Column(String, primary_key=True, index=True) # e.g. ORG_001
    name = Column(String, nullable=False) # Municipal Corporation, PWD, Water Board, Public Health
    code = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="organisation")
    roles = relationship("Role", back_populates="organisation")

class Role(Base):
    __tablename__ = "roles"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False) # Citizen, Routing Officer, PWD Officer, Sanitation Officer, Department Supervisor
    org_id = Column(String, ForeignKey("organisations.id"))

    organisation = relationship("Organisation", back_populates="roles")
    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role_id = Column(String, ForeignKey("roles.id"))
    org_id = Column(String, ForeignKey("organisations.id"))

    organisation = relationship("Organisation", back_populates="users")
    role = relationship("Role", back_populates="users")
    complaints = relationship("Complaint", back_populates="user")

class Department(Base):
    __tablename__ = "departments"

    id = Column(String, primary_key=True, index=True) # e.g. DEPT_PWD, DEPT_WATER, DEPT_SAN
    name = Column(String, nullable=False) # Public Works Dept, Water & Sewerage, Sanitation & Waste, etc.
    code = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    head_officer = Column(String, nullable=False)

    mandates = relationship("DepartmentMandate", back_populates="department")

class DepartmentMandate(Base):
    __tablename__ = "department_mandates"

    mandate_id = Column(String, primary_key=True, index=True) # e.g. MND_PWD_01
    department_id = Column(String, ForeignKey("departments.id"))
    intent_category = Column(String, nullable=False) # Road Potholes, Pipe Burst, Garbage Overflow, etc.
    keywords = Column(Text, nullable=False) # Comma-separated or JSON list of intent keywords
    sla_hours = Column(Integer, default=48)
    default_priority = Column(String, default="Medium")
    jurisdiction = Column(String, default="Municipal Limits")
    mandatory_actions = Column(Text, nullable=False)

    department = relationship("Department", back_populates="mandates")

class Complaint(Base):
    __tablename__ = "complaints"

    complaint_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    description = Column(Text, nullable=False)
    language = Column(String, nullable=False) # Tamil, Hindi, English
    category = Column(String, nullable=False) # Auto-detected intent category
    priority = Column(String, default="Medium")
    status = Column(String, default="Submitted") # Submitted, Routed, In Progress, Escalated, Resolved
    target_department_id = Column(String, nullable=True)
    sla_hours = Column(Integer, default=48)
    is_escalated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="complaints")
    attachments = relationship("Attachment", back_populates="complaint")

class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    complaint_id = Column(String, ForeignKey("complaints.complaint_id"))
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    upload_status = Column(String, default="Uploaded")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    complaint = relationship("Complaint", back_populates="attachments")

class RoutingResult(Base):
    __tablename__ = "routing_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    complaint_id = Column(String, nullable=False)
    detected_intent = Column(String, nullable=False)
    target_department_id = Column(String, nullable=False)
    target_department_name = Column(String, nullable=False)
    matched_mandate_id = Column(String, nullable=False)
    confidence_score = Column(Float, nullable=False)
    priority = Column(String, nullable=False)
    sla_hours = Column(Integer, nullable=False)
    assigned_role = Column(String, nullable=False)
    routing_explanation = Column(Text, nullable=False)
    is_ambiguous = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class OverrideLog(Base):
    __tablename__ = "override_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    complaint_id = Column(String, nullable=False)
    original_department_id = Column(String, nullable=False)
    overridden_department_id = Column(String, nullable=False)
    officer_user_id = Column(String, nullable=False)
    override_reason = Column(String, nullable=False)
    comment = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class EscalationLog(Base):
    __tablename__ = "escalation_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    complaint_id = Column(String, nullable=False)
    department_id = Column(String, nullable=False)
    escalation_level = Column(String, default="SUPERVISOR")
    reason = Column(String, nullable=False)
    triggered_by = Column(String, nullable=False) # System SLA or Manual Officer
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Feature(Base):
    __tablename__ = "features"

    feature_id = Column(String, primary_key=True, index=True) # e.g. F001 - F008
    feature_name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    allowed_roles = Column(String, default="*")
    allowed_organisations = Column(String, default="*")
    task_tags = Column(String, default="")
    impact_level = Column(String, default="NORMAL") # HIGH or NORMAL

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(String, ForeignKey("roles.id"))
    feature_code = Column(String, nullable=False)
    can_access = Column(Boolean, default=True)

class UsageEvent(Base):
    __tablename__ = "usage_events"

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    feature_id = Column(String, ForeignKey("features.feature_id"))
    user_id = Column(String, nullable=False)
    group = Column(String, default="ASSISTANT") # BASELINE or ASSISTANT
    action = Column(String, default="DISCOVERED") # DISCOVERED or COMPLETED
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    anonymous_user_id = Column(String, nullable=False)
    task_goal = Column(Text, nullable=True)
    help_query = Column(Text, nullable=True)
    recommended_feature_id = Column(String, nullable=False)
    score = Column(Float, default=0.0)
    allowed = Column(Boolean, default=True)
    evidence = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class RecommendationFeedback(Base):
    __tablename__ = "recommendation_feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    recommendation_id = Column(Integer, nullable=True)
    anonymous_user_id = Column(String, nullable=False)
    is_helpful = Column(Boolean, default=True)
    feedback_text = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class ExperimentMetric(Base):
    __tablename__ = "experiment_metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group = Column(String, nullable=False) # 'BASELINE' (or 'MANUAL_BASELINE') or 'ASSISTANT' (or 'AI_ROUTING_TOOL')
    complaint_id = Column(String, nullable=True)
    feature_id = Column(String, nullable=True) # e.g. F003, F006, F008
    routing_time_seconds = Column(Float, default=3600.0)
    routing_accuracy_pct = Column(Float, default=95.0)
    sla_breached = Column(Boolean, default=False)
    discovered = Column(Boolean, default=True)
    completed = Column(Boolean, default=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class StakeholderValidation(Base):
    __tablename__ = "stakeholder_validations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stakeholder_role = Column(String, nullable=False) # Citizen, Routing Officer, Dept Supervisor, Auditor
    usability_rating = Column(Integer, nullable=False) # 1 to 5
    explainability_rating = Column(Integer, nullable=False) # 1 to 5
    routing_speedup_pct = Column(Float, default=45.0)
    feedback_notes = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    action = Column(String, nullable=False)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

