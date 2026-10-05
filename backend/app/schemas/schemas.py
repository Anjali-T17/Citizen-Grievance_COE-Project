from typing import List, Optional
from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)

class RoleSchema(BaseModel):
    id: str
    name: str
    org_id: str

    model_config = ConfigDict(from_attributes=True)

# Department & Mandate Schemas
class DepartmentMandateSchema(BaseModel):
    mandate_id: str
    department_id: str
    intent_category: str
    keywords: str
    sla_hours: int
    default_priority: str
    jurisdiction: str
    mandatory_actions: str

    model_config = ConfigDict(from_attributes=True)

class DepartmentSchema(BaseModel):
    id: str
    name: str
    code: str
    description: str
    head_officer: str
    mandates: List[DepartmentMandateSchema] = []

    model_config = ConfigDict(from_attributes=True)

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

    model_config = ConfigDict(from_attributes=True)

# Complaint & Routing
class ComplaintCreate(BaseModel):
    description: str
    language: str # Tamil, Hindi, English
    category: Optional[str] = "General"
    priority: Optional[str] = "Medium"
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
    target_department_id: Optional[str] = None
    sla_hours: int = 48
    is_escalated: bool = False
    created_at: datetime
    attachments: List[AttachmentSchema] = []

    model_config = ConfigDict(from_attributes=True)

class RoutingRequest(BaseModel):
    complaint_id: Optional[str] = None
    description: str
    language: str = "English"
    category_hint: Optional[str] = None
    urgent_flag: bool = False

class RoutingResponse(BaseModel):
    detected_intent: str
    target_department_id: str
    target_department_name: str
    matched_mandate_id: str
    confidence_score: float
    priority: str
    sla_hours: int
    assigned_role: str
    routing_explanation: str
    is_ambiguous: bool = False
    matched_keywords: List[str] = []
    security_warning: Optional[str] = None

class OverrideCreate(BaseModel):
    complaint_id: str
    original_department_id: str
    overridden_department_id: str
    officer_user_id: str = "OFFICER_001"
    override_reason: str
    comment: Optional[str] = ""

class OverrideSchema(BaseModel):
    id: int
    complaint_id: str
    original_department_id: str
    overridden_department_id: str
    officer_user_id: str
    override_reason: str
    comment: Optional[str]
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

class EscalationCreate(BaseModel):
    complaint_id: str
    department_id: str
    escalation_level: str = "SUPERVISOR"
    reason: str
    triggered_by: str = "Manual Officer Escalation"

class EscalationSchema(BaseModel):
    id: int
    complaint_id: str
    department_id: str
    escalation_level: str
    reason: str
    triggered_by: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

# Analytics
class AnalyticsSummaryResponse(BaseModel):
    total_complaints: int
    total_routed: int
    total_escalated: int
    total_overrides: int
    avg_routing_accuracy_pct: float
    department_distribution: List[dict]
    override_reasons: List[dict]

class ComplaintStatusUpdate(BaseModel):
    status: str # Submitted, Routed, In Progress, Escalated, Resolved
    role: Optional[str] = None
    organisation: Optional[str] = None
    user_id: Optional[str] = "USER_001"
    comment: Optional[str] = None

class TranslationRequest(BaseModel):
    text: Optional[str] = None
    complaint_text: Optional[str] = None
    source_language: str = "Tamil" # English, Tamil, Hindi
    target_language: str = "English"

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    engine: str = "Deterministic Local Rule-Based Translator Engine (Phase A)"

class FeatureSchema(BaseModel):
    feature_id: str
    feature_name: str
    description: str
    allowed_roles: str
    allowed_organisations: str
    task_tags: str
    impact_level: str

    model_config = ConfigDict(from_attributes=True)

class DiscoveryUpliftResponse(BaseModel):
    baseline_discovery_rate: float
    assistant_discovery_rate: float
    discovery_uplift_percentage: float
    baseline_completion_rate: float
    assistant_completion_rate: float
    completion_uplift_percentage: float
    feature_level_results: dict
    total_events: int
    total_users: int
    formula: str = "uplift = ((assistant_rate - baseline_rate) / baseline_rate) * 100"

class HelpSearchRequest(BaseModel):
    query: Optional[str] = ""
    help_query: Optional[str] = ""
    role: Optional[str] = "Citizen"
    organisation: Optional[str] = "GCMC"

class HelpSearchResult(BaseModel):
    feature_id: str
    feature_name: str
    description: str
    similarity_score: float
    allowed: bool
    impact_level: str

class HelpSearchResponse(BaseModel):
    query: str
    total_matches: int
    results: List[HelpSearchResult]

class RecommendationRequest(BaseModel):
    role: str = "Citizen"
    organisation: str = "GCMC"
    task_goal: str = ""
    help_query: str = ""
    anonymous_user_id: str = "USER_001"

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
    hybrid_similarity_score: float
    allowed: bool
    requires_confirmation: bool
    impact_level: str
    evidence: List[str]
    matched_rules: List[RecommendationScoreDetail]
    security_warning: Optional[str] = None

class RecommendationFeedbackCreate(BaseModel):
    recommendation_id: Optional[int] = None
    anonymous_user_id: str = "USER_001"
    is_helpful: bool = True
    feedback_text: Optional[str] = ""

class RecommendationFeedbackSchema(BaseModel):
    id: int
    recommendation_id: Optional[int]
    anonymous_user_id: str
    is_helpful: bool
    feedback_text: Optional[str]
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

class ExperimentSummaryResponse(BaseModel):
    manual_baseline_routing_time_hours: float
    ai_routing_time_seconds: float
    manual_baseline_accuracy_pct: float
    ai_routing_accuracy_pct: float
    sla_breach_reduction_pct: float
    routing_speedup_factor: float
    feature_experiments: Optional[dict] = None

class StakeholderValidationCreate(BaseModel):
    stakeholder_role: str
    usability_rating: int
    explainability_rating: int
    routing_speedup_pct: float = 45.0
    feedback_notes: Optional[str] = ""

class StakeholderSummaryResponse(BaseModel):
    avg_usability_rating: float
    avg_explainability_rating: float
    avg_speedup_gain_pct: float
    total_validations: int
    role_breakdown: List[dict]

