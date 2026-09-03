import datetime
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models.models import (
    Organisation, Role, User, Permission, Feature, Complaint, Attachment, UsageEvent, AuditLog
)

def seed_database(db: Session):
    # Recreate tables cleanly
    Base.metadata.create_all(bind=engine)

    # Check if already seeded
    if db.query(Organisation).first():
        print("Database already contains data. Skipping seed.")
        return

    print("Seeding synthetic data into SQLite database...")

    # 1. Seed Organisations
    org_muni = Organisation(id="ORG_001", name="Municipal Corporation", code="MUNICIPAL_CORP")
    org_part = Organisation(id="ORG_002", name="External Partner", code="EXTERNAL_PARTNER")
    db.add_all([org_muni, org_part])
    db.flush()

    # 2. Seed Roles
    role_citizen = Role(id="ROLE_CITIZEN", name="Citizen", org_id="ORG_001")
    role_officer = Role(id="ROLE_OFFICER", name="Grievance Officer", org_id="ORG_001")
    role_supervisor = Role(id="ROLE_SUPERVISOR", name="Supervisor", org_id="ORG_001")
    role_partner = Role(id="ROLE_PARTNER", name="External Partner", org_id="ORG_002")
    db.add_all([role_citizen, role_officer, role_supervisor, role_partner])
    db.flush()

    # 3. Seed Users (Synthetic / Anonymised)
    user1 = User(id="USER_001", name="Citizen Alpha", email="citizen@demo.org", role_id="ROLE_CITIZEN", org_id="ORG_001")
    user2 = User(id="USER_002", name="Officer Beta", email="officer@demo.org", role_id="ROLE_OFFICER", org_id="ORG_001")
    user3 = User(id="USER_003", name="Supervisor Gamma", email="supervisor@demo.org", role_id="ROLE_SUPERVISOR", org_id="ORG_001")
    user4 = User(id="USER_004", name="Partner Delta", email="partner@demo.org", role_id="ROLE_PARTNER", org_id="ORG_002")
    db.add_all([user1, user2, user3, user4])

    # 4. Seed Features (F001 - F008)
    features = [
        Feature(
            feature_id="F001",
            feature_name="Submit Complaint",
            description="Allows citizens and officers to log a new grievance with details and attachments.",
            allowed_roles="Citizen, Grievance Officer",
            allowed_organisations="Municipal Corporation",
            permission_level="BASIC",
            impact_level="LOW",
            task_tags="submit, complaint, new, file grievance, log issue"
        ),
        Feature(
            feature_id="F002",
            feature_name="Track Complaint",
            description="View real-time status and historical updates of submitted complaints.",
            allowed_roles="Citizen, Grievance Officer, Supervisor",
            allowed_organisations="Municipal Corporation",
            permission_level="BASIC",
            impact_level="LOW",
            task_tags="track, status, history, view, progress"
        ),
        Feature(
            feature_id="F003",
            feature_name="Translate Complaint",
            description="Translate multilingual complaint text (Tamil, Hindi, English) into working officer language.",
            allowed_roles="Grievance Officer, Supervisor",
            allowed_organisations="Municipal Corporation",
            permission_level="OFFICER",
            impact_level="LOW",
            task_tags="translation, multilingual, language, understand complaint, tamil, hindi, english"
        ),
        Feature(
            feature_id="F004",
            feature_name="Verify Attachment",
            description="Inspect, download, and validate supporting photos or PDF documents.",
            allowed_roles="Grievance Officer, Supervisor, External Partner",
            allowed_organisations="Municipal Corporation, External Partner",
            permission_level="OFFICER",
            impact_level="LOW",
            task_tags="verify, attachment, upload, document, image, proof"
        ),
        Feature(
            feature_id="F005",
            feature_name="Escalate Complaint",
            description="Formally escalate a high-priority or SLA-breaching complaint to higher supervisory authorities.",
            allowed_roles="Grievance Officer, Supervisor",
            allowed_organisations="Municipal Corporation",
            permission_level="OFFICER",
            impact_level="HIGH",
            task_tags="escalate, urgent, high priority, sla breach, supervisor review"
        ),
        Feature(
            feature_id="F006",
            feature_name="Internal Notes",
            description="Add confidential case notes visible only to internal officers and supervisors.",
            allowed_roles="Grievance Officer, Supervisor",
            allowed_organisations="Municipal Corporation",
            permission_level="OFFICER",
            impact_level="LOW",
            task_tags="notes, internal, officer note, comment, discussion"
        ),
        Feature(
            feature_id="F007",
            feature_name="Complaint Monitoring",
            description="Comprehensive dashboard to monitor department resolution metrics and SLA bottlenecks.",
            allowed_roles="Supervisor",
            allowed_organisations="Municipal Corporation",
            permission_level="SUPERVISOR",
            impact_level="LOW",
            task_tags="monitoring, supervisor, overview, analytics, dashboard, metrics"
        ),
        Feature(
            feature_id="F008",
            feature_name="Upload Evidence",
            description="Allows external contractors and partner agencies to upload execution evidence.",
            allowed_roles="External Partner, Grievance Officer",
            allowed_organisations="External Partner, Municipal Corporation",
            permission_level="PARTNER",
            impact_level="LOW",
            task_tags="evidence, upload proof, document, external evidence, resolution photo"
        ),
    ]
    db.add_all(features)
    db.flush()

    # 5. Seed Permissions
    permissions = [
        Permission(role_id="ROLE_CITIZEN", feature_code="F001", can_access=True),
        Permission(role_id="ROLE_CITIZEN", feature_code="F002", can_access=True),
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
        Permission(role_id="ROLE_PARTNER", feature_code="F008", can_access=True),
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

    # 7. Seed Synthetic Usage Events (to create intentional underuse for F003, F006, F008)
    events = []
    # F001 (Submit Complaint) - heavily used
    for i in range(18):
        events.append(UsageEvent(
            anonymous_user_id=f"USER_00{i % 4 + 1}",
            organisation_id="ORG_001",
            role="Citizen",
            feature_id="F001",
            task_goal="Submit new grievance",
            action="execute",
            success=True
        ))
    # F002 (Track Complaint) - heavily used
    for i in range(15):
        events.append(UsageEvent(
            anonymous_user_id=f"USER_00{i % 4 + 1}",
            organisation_id="ORG_001",
            role="Citizen",
            feature_id="F002",
            task_goal="Check complaint status",
            action="view",
            success=True
        ))
    # F004 (Verify Attachment) - medium used
    for i in range(8):
        events.append(UsageEvent(
            anonymous_user_id="USER_002",
            organisation_id="ORG_001",
            role="Grievance Officer",
            feature_id="F004",
            task_goal="Inspect image photo proof",
            action="view",
            success=True
        ))
    # F003 (Translate Complaint) - UNDERUSED (only 2 usages)
    events.append(UsageEvent(
        anonymous_user_id="USER_002",
        organisation_id="ORG_001",
        role="Grievance Officer",
        feature_id="F003",
        task_goal="Translate Tamil complaint",
        action="execute",
        success=True
    ))
    # F006 (Internal Notes) - UNDERUSED (1 usage)
    events.append(UsageEvent(
        anonymous_user_id="USER_002",
        organisation_id="ORG_001",
        role="Grievance Officer",
        feature_id="F006",
        task_goal="Add note",
        action="execute",
        success=True
    ))
    # F008 (Upload Evidence) - UNDERUSED (1 usage)
    events.append(UsageEvent(
        anonymous_user_id="USER_004",
        organisation_id="ORG_002",
        role="External Partner",
        feature_id="F008",
        task_goal="Upload repair photo",
        action="execute",
        success=True
    ))

    db.add_all(events)
    db.commit()
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
