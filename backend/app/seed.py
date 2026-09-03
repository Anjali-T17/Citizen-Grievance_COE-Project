import datetime
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models.models import (
    Organisation, Role, User, Permission, Feature, Complaint, Attachment, UsageEvent, AuditLog,
    ExperimentMetric, StakeholderValidation, RecommendationFeedback
)

def seed_database(db: Session):
    # Recreate tables cleanly
    Base.metadata.create_all(bind=engine)

    # Check if already seeded
    if db.query(Organisation).first():
        print("Database already contains data. Skipping seed.")
        return

    print("Seeding synthetic data for Phase 1, Phase 2, and Phase 3...")

    # 1. Seed Organisations
    org_muni = Organisation(id="ORG_001", name="Municipal Corporation", code="MUNICIPAL_CORP")
    org_part = Organisation(id="ORG_002", name="External Partner", code="EXTERNAL_PARTNER")
    org_pwd = Organisation(id="ORG_003", name="Public Works Department", code="PWD")
    org_health = Organisation(id="ORG_004", name="Public Health & Sanitation", code="HEALTH")
    db.add_all([org_muni, org_part, org_pwd, org_health])
    db.flush()

    # 2. Seed Roles
    role_citizen = Role(id="ROLE_CITIZEN", name="Citizen", org_id="ORG_001")
    role_officer = Role(id="ROLE_OFFICER", name="Grievance Officer", org_id="ORG_001")
    role_supervisor = Role(id="ROLE_SUPERVISOR", name="Supervisor", org_id="ORG_001")
    role_partner = Role(id="ROLE_PARTNER", name="External Partner", org_id="ORG_002")
    role_inspector = Role(id="ROLE_INSPECTOR", name="Field Inspector", org_id="ORG_003")
    role_auditor = Role(id="ROLE_AUDITOR", name="SLA Auditor", org_id="ORG_001")
    db.add_all([role_citizen, role_officer, role_supervisor, role_partner, role_inspector, role_auditor])
    db.flush()

    # 3. Seed Users
    user1 = User(id="USER_001", name="Citizen Alpha", email="citizen@demo.org", role_id="ROLE_CITIZEN", org_id="ORG_001")
    user2 = User(id="USER_002", name="Officer Beta", email="officer@demo.org", role_id="ROLE_OFFICER", org_id="ORG_001")
    user3 = User(id="USER_003", name="Supervisor Gamma", email="supervisor@demo.org", role_id="ROLE_SUPERVISOR", org_id="ORG_001")
    user4 = User(id="USER_004", name="Partner Delta", email="partner@demo.org", role_id="ROLE_PARTNER", org_id="ORG_002")
    user5 = User(id="USER_005", name="Inspector Echo", email="inspector@pwd.demo.org", role_id="ROLE_INSPECTOR", org_id="ORG_003")
    user6 = User(id="USER_006", name="Auditor Foxtrot", email="auditor@demo.org", role_id="ROLE_AUDITOR", org_id="ORG_001")
    db.add_all([user1, user2, user3, user4, user5, user6])

    # 4. Seed Features (F001 - F011)
    features = [
        Feature(
            feature_id="F001",
            feature_name="Submit Complaint",
            description="Allows citizens and officers to log a new grievance with details and attachments.",
            allowed_roles="Citizen, Grievance Officer",
            allowed_organisations="Municipal Corporation, Public Works Department, Public Health & Sanitation",
            permission_level="BASIC",
            impact_level="LOW",
            task_tags="submit, complaint, new, file grievance, log issue"
        ),
        Feature(
            feature_id="F002",
            feature_name="Track Complaint",
            description="View real-time status and historical updates of submitted complaints.",
            allowed_roles="Citizen, Grievance Officer, Supervisor, Field Inspector, SLA Auditor",
            allowed_organisations="Municipal Corporation, Public Works Department, Public Health & Sanitation",
            permission_level="BASIC",
            impact_level="LOW",
            task_tags="track, status, history, view, progress"
        ),
        Feature(
            feature_id="F003",
            feature_name="Translate Complaint",
            description="Translate multilingual complaint text (Tamil, Hindi, English) into working officer language.",
            allowed_roles="Grievance Officer, Supervisor, SLA Auditor",
            allowed_organisations="Municipal Corporation, Public Works Department, Public Health & Sanitation",
            permission_level="OFFICER",
            impact_level="LOW",
            task_tags="translation, multilingual, language, understand complaint, tamil, hindi, english"
        ),
        Feature(
            feature_id="F004",
            feature_name="Verify Attachment",
            description="Inspect, download, and validate supporting photos or PDF documents.",
            allowed_roles="Grievance Officer, Supervisor, External Partner, Field Inspector",
            allowed_organisations="Municipal Corporation, External Partner, Public Works Department",
            permission_level="OFFICER",
            impact_level="LOW",
            task_tags="verify, attachment, upload, document, image, proof"
        ),
        Feature(
            feature_id="F005",
            feature_name="Escalate Complaint",
            description="Formally escalate a high-priority or SLA-breaching complaint to higher supervisory authorities.",
            allowed_roles="Grievance Officer, Supervisor, SLA Auditor",
            allowed_organisations="Municipal Corporation, Public Works Department",
            permission_level="OFFICER",
            impact_level="HIGH",
            task_tags="escalate, urgent, high priority, sla breach, supervisor review"
        ),
        Feature(
            feature_id="F006",
            feature_name="Internal Notes",
            description="Add confidential case notes visible only to internal officers and supervisors.",
            allowed_roles="Grievance Officer, Supervisor, SLA Auditor",
            allowed_organisations="Municipal Corporation, Public Works Department",
            permission_level="OFFICER",
            impact_level="LOW",
            task_tags="notes, internal, officer note, comment, discussion"
        ),
        Feature(
            feature_id="F007",
            feature_name="Complaint Monitoring",
            description="Comprehensive dashboard to monitor department resolution metrics and SLA bottlenecks.",
            allowed_roles="Supervisor, SLA Auditor",
            allowed_organisations="Municipal Corporation, Public Works Department, Public Health & Sanitation",
            permission_level="SUPERVISOR",
            impact_level="LOW",
            task_tags="monitoring, supervisor, overview, analytics, dashboard, metrics"
        ),
        Feature(
            feature_id="F008",
            feature_name="Upload Evidence",
            description="Allows external contractors and partner agencies to upload execution evidence.",
            allowed_roles="External Partner, Grievance Officer, Field Inspector",
            allowed_organisations="External Partner, Municipal Corporation, Public Works Department",
            permission_level="PARTNER",
            impact_level="LOW",
            task_tags="evidence, upload proof, document, external evidence, resolution photo"
        ),
        Feature(
            feature_id="F009",
            feature_name="Field Inspection Verification",
            description="On-site verification tool for PWD and Health inspectors to upload geotagged inspection reports.",
            allowed_roles="Field Inspector, Supervisor",
            allowed_organisations="Public Works Department, Public Health & Sanitation, Municipal Corporation",
            permission_level="OFFICER",
            impact_level="LOW",
            task_tags="inspection, field visit, photo proof, verify on site, geotag report, road damage, geotagged inspection"
        ),
        Feature(
            feature_id="F010",
            feature_name="SLA Breach Audit Report",
            description="Detailed audit reporting tool to analyze overdue complaints and generate compliance certificates.",
            allowed_roles="SLA Auditor, Supervisor",
            allowed_organisations="Municipal Corporation, Public Works Department",
            permission_level="SUPERVISOR",
            impact_level="HIGH",
            task_tags="sla, audit, breach report, compliance, performance, bottleneck"
        ),
        Feature(
            feature_id="F011",
            feature_name="Citizen Feedback Survey",
            description="Captures citizen satisfaction ratings and resolution quality feedback after case closure.",
            allowed_roles="Citizen, Supervisor",
            allowed_organisations="Municipal Corporation, Public Works Department, Public Health & Sanitation",
            permission_level="BASIC",
            impact_level="LOW",
            task_tags="feedback, survey, rating, citizen satisfaction, case closure"
        )
    ]
    db.add_all(features)
    db.flush()

    # 5. Seed Permissions
    permissions = [
        Permission(role_id="ROLE_CITIZEN", feature_code="F001", can_access=True),
        Permission(role_id="ROLE_CITIZEN", feature_code="F002", can_access=True),
        Permission(role_id="ROLE_CITIZEN", feature_code="F011", can_access=True),
        Permission(role_id="ROLE_CITIZEN", feature_code="F003", can_access=False),
        Permission(role_id="ROLE_CITIZEN", feature_code="F005", can_access=False),
        Permission(role_id="ROLE_CITIZEN", feature_code="F007", can_access=False),
        Permission(role_id="ROLE_OFFICER", feature_code="F001", can_access=True),
        Permission(role_id="ROLE_OFFICER", feature_code="F002", can_access=True),
        Permission(role_id="ROLE_OFFICER", feature_code="F003", can_access=True),
        Permission(role_id="ROLE_OFFICER", feature_code="F004", can_access=True),
        Permission(role_id="ROLE_OFFICER", feature_code="F005", can_access=True),
        Permission(role_id="ROLE_OFFICER", feature_code="F006", can_access=True),
        Permission(role_id="ROLE_SUPERVISOR", feature_code="F007", can_access=True),
        Permission(role_id="ROLE_SUPERVISOR", feature_code="F010", can_access=True),
        Permission(role_id="ROLE_PARTNER", feature_code="F008", can_access=True),
        Permission(role_id="ROLE_INSPECTOR", feature_code="F009", can_access=True),
        Permission(role_id="ROLE_AUDITOR", feature_code="F010", can_access=True),
    ]
    db.add_all(permissions)

    # 6. Seed Sample Multilingual Complaints
    c1 = Complaint(
        complaint_id="COMPLAINT_001",
        user_id="USER_001",
        description="தெரு விளக்கு எரியவில்லை. இரவில் மக்கள் செல்வது ஆபத்தாக உள்ளது.",
        language="Tamil",
        category="Public Safety",
        priority="High",
        status="Submitted",
        created_at=datetime.datetime.utcnow() - datetime.timedelta(hours=5)
    )
    a1 = Attachment(
        complaint_id="COMPLAINT_001",
        filename="dark_street_photo.jpg",
        file_type="image/jpeg",
        file_size=245000,
        upload_status="Uploaded"
    )

    c2 = Complaint(
        complaint_id="COMPLAINT_002",
        user_id="USER_001",
        description="हमारे इलाके में पीने के पानी की आपूर्ति पिछले 3 दिनों से बंद है।",
        language="Hindi",
        category="Water Supply",
        priority="Medium",
        status="Under Review",
        created_at=datetime.datetime.utcnow() - datetime.timedelta(days=1)
    )

    c3 = Complaint(
        complaint_id="COMPLAINT_003",
        user_id="USER_001",
        description="Deep pothole near Central Bus Terminal causing vehicle damages and accidents.",
        language="English",
        category="Roads",
        priority="High",
        status="Escalated",
        created_at=datetime.datetime.utcnow() - datetime.timedelta(days=2)
    )

    db.add_all([c1, a1, c2, c3])

    # 7. Seed Synthetic Usage Events
    events = []
    for i in range(25):
        events.append(UsageEvent(
            anonymous_user_id=f"USER_00{i % 4 + 1}",
            organisation_id="ORG_001",
            role="Citizen",
            feature_id="F001",
            task_goal="Submit grievance",
            action="execute",
            success=True
        ))
    for i in range(18):
        events.append(UsageEvent(
            anonymous_user_id=f"USER_00{i % 4 + 1}",
            organisation_id="ORG_001",
            role="Citizen",
            feature_id="F002",
            task_goal="Track status",
            action="view",
            success=True
        ))
    # Underused features
    events.append(UsageEvent(anonymous_user_id="USER_002", organisation_id="ORG_001", role="Grievance Officer", feature_id="F003", task_goal="Translate Tamil", action="execute", success=True))
    events.append(UsageEvent(anonymous_user_id="USER_002", organisation_id="ORG_001", role="Grievance Officer", feature_id="F006", task_goal="Add note", action="execute", success=True))
    events.append(UsageEvent(anonymous_user_id="USER_004", organisation_id="ORG_002", role="External Partner", feature_id="F008", task_goal="Upload proof", action="execute", success=True))
    events.append(UsageEvent(anonymous_user_id="USER_005", organisation_id="ORG_003", role="Field Inspector", feature_id="F009", task_goal="Onsite inspection", action="execute", success=True))
    events.append(UsageEvent(anonymous_user_id="USER_006", organisation_id="ORG_001", role="SLA Auditor", feature_id="F010", task_goal="SLA audit", action="execute", success=True))

    db.add_all(events)

    # 8. Seed Synthetic Experiment A/B Metrics (Group Baseline vs Group Assistant)
    exp_metrics = []
    # Baseline group: low discovery (28%), moderate completion (62%), higher discovery time (85s)
    for i in range(50):
        disc = (i % 4 == 0)
        comp = (i % 3 != 0)
        exp_metrics.append(ExperimentMetric(
            group="BASELINE",
            user_id=f"USER_BASE_{i}",
            feature_id="F003" if i % 2 == 0 else "F005",
            discovered_via_assistant=False,
            task_completed=comp,
            time_to_discover_sec=85.0 + (i % 15)
        ))

    # Assistant group: high discovery (84%), high completion (91%), reduced discovery time (18s)
    for i in range(50):
        disc = (i % 6 != 0)
        comp = (i % 10 != 0)
        exp_metrics.append(ExperimentMetric(
            group="ASSISTANT",
            user_id=f"USER_AST_{i}",
            feature_id="F003" if i % 2 == 0 else "F005",
            discovered_via_assistant=True,
            task_completed=comp,
            time_to_discover_sec=18.0 + (i % 5)
        ))
    db.add_all(exp_metrics)

    # 9. Seed Stakeholder Validation Ratings
    validations = [
        StakeholderValidation(stakeholder_role="Citizen", usability_rating=5, explainability_rating=4, efficiency_improvement_pct=42.0, feedback_notes="Easy to track my Tamil complaint status."),
        StakeholderValidation(stakeholder_role="Officer", usability_rating=5, explainability_rating=5, efficiency_improvement_pct=55.0, feedback_notes="Translate Complaint recommendation saved significant time."),
        StakeholderValidation(stakeholder_role="Supervisor", usability_rating=4, explainability_rating=5, efficiency_improvement_pct=48.0, feedback_notes="Human confirmation on escalation prevents accidental workflow triggers."),
        StakeholderValidation(stakeholder_role="Auditor", usability_rating=5, explainability_rating=5, efficiency_improvement_pct=50.0, feedback_notes="Audit log transparency and prompt injection protection are robust.")
    ]
    db.add_all(validations)

    db.commit()
    print("Database seeding for Phase 1, Phase 2, and Phase 3 completed successfully.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
