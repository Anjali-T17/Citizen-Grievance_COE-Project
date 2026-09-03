from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

# Auth / Demo Login
class DemoLoginRequest(BaseModel):
    organisation: str
    role: str

class DemoLoginResponse(BaseModel):
    user_id: str
    name: str
    email: str
    role: str
    organisation: str
    token: str = "demo_session_token"

# Organisation & Role
class OrganisationSchema(BaseModel):
    id: str
    name: str
    code: str

    class Config:
        from_attributes = True

class RoleSchema(BaseModel):
    id: str
    name: str
    org_id: str

    class Config:
        from_attributes = True

# Attachment
class AttachmentCreate(BaseModel):
    filename: str
    file_type: str
    file_size: int

class AttachmentSchema(BaseModel):
    id: int
    complaint_id: str
    filename: str
    file_type: str
    file_size: int
    upload_status: str
    created_at: datetime

    class Config:
        from_attributes = True

# Complaint
class ComplaintCreate(BaseModel):
    description: str
    language: str
    category: str
    priority: str = "Medium"
    attachment_name: Optional[str] = None
    attachment_type: Optional[str] = None
    attachment_size: Optional[int] = 0

class ComplaintSchema(BaseModel):
    complaint_id: str
    user_id: str
    description: str
    language: str
    category: str
    priority: str
    status: str
    created_at: datetime
    attachments: List[AttachmentSchema] = []

    class Config:
        from_attributes = True

# Feature
class FeatureSchema(BaseModel):
    feature_id: str
    feature_name: str
    description: str
    allowed_roles: str
    allowed_organisations: str
    permission_level: str
    impact_level: str
    task_tags: str

    class Config:
        from_attributes = True

# Recommendation Request & Response
class RecommendationRequest(BaseModel):
    anonymous_user_id: str = "USER_001"
    role: str
    organisation: str
    task_goal: str
    help_query: str

class RecommendationScoreDetail(BaseModel):
    rule_name: str
    points: float
    matched: bool
    explanation: str

class RecommendationResponse(BaseModel):
    feature_id: str
    feature_name: str
    description: str
    score: float
    hybrid_similarity_score: float = 0.0
    allowed: bool
    requires_confirmation: bool = False
    impact_level: str = "LOW"
    evidence: List[str]
    matched_rules: List[RecommendationScoreDetail]
    security_warning: Optional[str] = None

# Recommendation Feedback
class RecommendationFeedbackCreate(BaseModel):
    recommendation_id: Optional[int] = None
    anonymous_user_id: str = "USER_001"
    is_helpful: bool
    feedback_text: Optional[str] = ""

class RecommendationFeedbackSchema(BaseModel):
    id: int
    recommendation_id: Optional[int]
    anonymous_user_id: str
    is_helpful: bool
    feedback_text: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True

# Override Request & Response
class OverrideCreate(BaseModel):
    recommendation_id: Optional[int] = None
    anonymous_user_id: str = "USER_001"
    action: str = "CANCEL_ESCALATION"
    override_reason: str
    comment: Optional[str] = ""

class OverrideSchema(BaseModel):
    id: int
    recommendation_id: Optional[int]
    anonymous_user_id: str
    action: str
    override_reason: str
    comment: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True

# Analytics
class FeatureUsageStat(BaseModel):
    feature_id: str
    feature_name: str
    usage_count: int
    underused: bool

class OverrideStat(BaseModel):
    reason: str
    count: int

class AnalyticsSummaryResponse(BaseModel):
    total_usage_events: int
    total_recommendations: int
    total_overrides: int
    most_used_features: List[FeatureUsageStat]
    underused_features: List[FeatureUsageStat]
    override_reasons: List[OverrideStat]

# Experiment & Evaluation Schemas (Phase 2 & 3)
class GroupExperimentStat(BaseModel):
    group_name: str # "BASELINE" or "ASSISTANT"
    discovery_rate_pct: float
    completion_rate_pct: float
    avg_time_to_discovery_sec: float

class ExperimentSummaryResponse(BaseModel):
    baseline_stats: GroupExperimentStat
    assistant_stats: GroupExperimentStat
    discovery_improvement_pct: float
    completion_improvement_pct: float
    time_saved_pct: float

class StakeholderValidationCreate(BaseModel):
    stakeholder_role: str # Citizen, Officer, Supervisor, Auditor
    usability_rating: int # 1 to 5
    explainability_rating: int # 1 to 5
    efficiency_improvement_pct: float = 45.0
    feedback_notes: Optional[str] = ""

class StakeholderSummaryResponse(BaseModel):
    avg_usability_rating: float
    avg_explainability_rating: float
    avg_efficiency_gain_pct: float
    total_validations: int
    role_breakdown: List[dict]

class ErrorAnalysisItem(BaseModel):
    error_category: str # "Task Tag Misclassification", "Explicit Permission Block", "High-Impact User Override", "Adversarial Injection Block"
    frequency: int
    percentage: float
    root_cause_explanation: str
