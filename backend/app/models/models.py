import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Organisation(Base):
    __tablename__ = "organisations"

    id = Column(String, primary_key=True, index=True) # e.g. ORG_001
    name = Column(String, nullable=False) # Municipal Corporation, External Partner, PWD, Health Dept
    code = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="organisation")
    roles = relationship("Role", back_populates="organisation")

class Role(Base):
    __tablename__ = "roles"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False) # Citizen, Grievance Officer, Supervisor, External Partner, Field Inspector, SLA Auditor
    org_id = Column(String, ForeignKey("organisations.id"))

    organisation = relationship("Organisation", back_populates="roles")
    users = relationship("User", back_populates="role")
    permissions = relationship("Permission", back_populates="role")

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

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(String, ForeignKey("roles.id"))
    feature_code = Column(String, nullable=False)
    can_access = Column(Boolean, default=True)

    role = relationship("Role", back_populates="permissions")

class Feature(Base):
    __tablename__ = "features"

    feature_id = Column(String, primary_key=True, index=True) # F001 - F011
    feature_name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    allowed_roles = Column(Text, nullable=False)
    allowed_organisations = Column(Text, nullable=False)
    permission_level = Column(String, default="BASIC")
    impact_level = Column(String, default="LOW")
    task_tags = Column(Text, nullable=False)

class Complaint(Base):
    __tablename__ = "complaints"

    complaint_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    description = Column(Text, nullable=False)
    language = Column(String, nullable=False)
    category = Column(String, nullable=False)
    priority = Column(String, default="Medium")
    status = Column(String, default="Submitted")
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

class UsageEvent(Base):
    __tablename__ = "usage_events"

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    anonymous_user_id = Column(String, nullable=False)
    organisation_id = Column(String, nullable=False)
    role = Column(String, nullable=False)
    feature_id = Column(String, nullable=False)
    task_goal = Column(String, nullable=True)
    help_query = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    action = Column(String, default="view")
    success = Column(Boolean, default=True)

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    anonymous_user_id = Column(String, nullable=False)
    task_goal = Column(String, nullable=True)
    help_query = Column(String, nullable=True)
    recommended_feature_id = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    allowed = Column(Boolean, default=True)
    evidence = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class RecommendationFeedback(Base):
    __tablename__ = "recommendation_feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    recommendation_id = Column(Integer, nullable=True)
    anonymous_user_id = Column(String, nullable=False)
    is_helpful = Column(Boolean, nullable=False)
    feedback_text = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Override(Base):
    __tablename__ = "overrides"

    id = Column(Integer, primary_key=True, autoincrement=True)
    recommendation_id = Column(Integer, nullable=True)
    anonymous_user_id = Column(String, nullable=False)
    action = Column(String, nullable=False)
    override_reason = Column(String, nullable=False)
    comment = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class ExperimentMetric(Base):
    __tablename__ = "experiment_metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group = Column(String, nullable=False) # 'BASELINE' or 'ASSISTANT'
    user_id = Column(String, nullable=False)
    feature_id = Column(String, nullable=False)
    discovered_via_assistant = Column(Boolean, default=False)
    task_completed = Column(Boolean, default=True)
    time_to_discover_sec = Column(Float, default=30.0)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class StakeholderValidation(Base):
    __tablename__ = "stakeholder_validations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stakeholder_role = Column(String, nullable=False) # Citizen, Officer, Supervisor, Auditor
    usability_rating = Column(Integer, nullable=False) # 1 to 5
    explainability_rating = Column(Integer, nullable=False) # 1 to 5
    efficiency_improvement_pct = Column(Float, default=45.0)
    feedback_notes = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    anonymous_user_id = Column(String, nullable=False)
    action = Column(String, nullable=False)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
