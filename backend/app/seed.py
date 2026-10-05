import datetime
from sqlalchemy.orm import Session
from app.models.models import (
    Organisation, Role, User, Department, DepartmentMandate,
    Complaint, Attachment, RoutingResult, OverrideLog, EscalationLog,
    ExperimentMetric, StakeholderValidation, AuditLog, Feature, UsageEvent
)

def seed_database(db: Session):
    # Check if already seeded
    if db.query(Department).first():
        return

    # 1. Seed Organisations
    org1 = Organisation(id="ORG_001", name="Greater Chennai Municipal Corporation", code="GCMC")
    org2 = Organisation(id="ORG_002", name="Public Works Department (PWD)", code="PWD")
    org3 = Organisation(id="ORG_003", name="Water Supply & Sewerage Board", code="TWAD")
    org4 = Organisation(id="ORG_004", name="Public Health & Hygiene Dept", code="PHHD")

    db.add_all([org1, org2, org3, org4])
    db.commit()

    # 2. Seed Roles
    r1 = Role(id="ROLE_001", name="Citizen", org_id="ORG_001")
    r2 = Role(id="ROLE_002", name="Routing Officer", org_id="ORG_001")
    r3 = Role(id="ROLE_003", name="PWD Road Engineer", org_id="ORG_002")
    r4 = Role(id="ROLE_004", name="Water Line Inspector", org_id="ORG_003")
    r5 = Role(id="ROLE_005", name="Sanitation Officer", org_id="ORG_001")
    r6 = Role(id="ROLE_006", name="Department Supervisor", org_id="ORG_001")

    db.add_all([r1, r2, r3, r4, r5, r6])
    db.commit()

    # 3. Seed Users
    u1 = User(id="USER_001", name="Anjali Citizen", email="anjali@citizen.in", role_id="ROLE_001", org_id="ORG_001")
    u2 = User(id="USER_002", name="Kumar Routing Officer", email="kumar@routing.in", role_id="ROLE_002", org_id="ORG_001")
    u3 = User(id="USER_003", name="Dr. Selvam PWD Engineer", email="selvam@pwd.gov.in", role_id="ROLE_003", org_id="ORG_002")
    u4 = User(id="USER_004", name="Priya Water Inspector", email="priya@waterboard.gov.in", role_id="ROLE_004", org_id="ORG_003")
    u5 = User(id="USER_005", name="Ramesh Supervisor", email="ramesh@supervisor.gov.in", role_id="ROLE_006", org_id="ORG_001")

    db.add_all([u1, u2, u3, u4, u5])
    db.commit()

    # 4. Seed Departments
    d1 = Department(id="DEPT_PWD", name="Public Works Department (PWD)", code="PWD", description="Road infrastructure, bridges, tarring, and pavement repair.", head_officer="Dr. Selvam (Chief Engineer)")
    d2 = Department(id="DEPT_WATER", name="Water Supply & Sewerage Board", code="TWAD", description="Drinking water mainlines, pipe bursts, and sewage drainage clearing.", head_officer="Er. Priya (Executive Engineer)")
    d3 = Department(id="DEPT_SAN", name="Sanitation & Waste Management Dept", code="SAN", description="Solid waste collection, garbage bins, and street sanitization.", head_officer="Officer Murugan (Health Officer)")
    d4 = Department(id="DEPT_ELEC", name="Electricity & Streetlighting Board", code="ELEC", description="Streetlights, electrical transformer line sparks, and public lighting.", head_officer="Er. Karthik (Divisional Engineer)")
    d5 = Department(id="DEPT_HEALTH", name="Public Health & Hygiene Dept", code="HEALTH", description="Vector control, stagnant water spraying, anti-dengue fogging.", head_officer="Dr. Kavitha (Public Health Director)")
    d6 = Department(id="DEPT_GENERAL", name="General Grievance Review Board", code="GEN", description="General queue for ambiguous, unclassified, or multi-department grievances.", head_officer="Kumar (Routing Officer)")

    db.add_all([d1, d2, d3, d4, d5, d6])
    db.commit()

    # 5. Seed Department Mandates
    m1 = DepartmentMandate(
        mandate_id="MND_PWD_01",
        department_id="DEPT_PWD",
        intent_category="Road Potholes & Infrastructure",
        keywords="pothole,road,tar,asphalt,bridge,pavement,சாலை,குழி,பாலம்,சேதம்,सड़क,गड्ढा,पुल",
        sla_hours=48,
        default_priority="Medium",
        jurisdiction="Municipal Limits & Arterial Roads",
        mandatory_actions="Inspect pavement structural damage, deploy repair crew, patch asphalt within 48h."
    )
    m2 = DepartmentMandate(
        mandate_id="MND_WATER_02",
        department_id="DEPT_WATER",
        intent_category="Water Leakage & Sewage Drainage",
        keywords="water,leak,pipe,sewage,drain,burst,drinking water,குடிநீர்,கசிவு,சாக்கடை,पानी,रिसव,सीवर",
        sla_hours=24,
        default_priority="High",
        jurisdiction="Water Supply Grid & Sewerage Mains",
        mandatory_actions="Isolate pipe leak within 4 hours, restore clean water supply within 24h."
    )
    m3 = DepartmentMandate(
        mandate_id="MND_SAN_03",
        department_id="DEPT_SAN",
        intent_category="Garbage & Waste Sanitation",
        keywords="garbage,trash,waste,bin,cleanliness,dump,stench,குப்பை,கழிவு,துப்புரவு,கचरा,कूड़ा,सफाई",
        sla_hours=24,
        default_priority="Medium",
        jurisdiction="Residential & Commercial Wards",
        mandatory_actions="Dispatch compactor vehicle, clear waste dump, apply disinfectant within 24h."
    )
    m4 = DepartmentMandate(
        mandate_id="MND_ELEC_04",
        department_id="DEPT_ELEC",
        intent_category="Streetlighting & Electrical Lines",
        keywords="streetlight,electricity,pole,wire,power,dark,sparking,தெருவிளக்கு,மின்சாரம்,स्ट्रीट लाइट,बिजली",
        sla_hours=24,
        default_priority="High",
        jurisdiction="Public Street Lighting & Overhead Lines",
        mandatory_actions="Repair burnt wiring, fix LED fixture, eliminate electrical hazards within 24h."
    )
    m5 = DepartmentMandate(
        mandate_id="MND_HEALTH_05",
        department_id="DEPT_HEALTH",
        intent_category="Public Health & Disease Prevention",
        keywords="mosquito,fever,stagnant,dengue,hygiene,spraying,fogging,கொசு,காய்ச்சல்,டெங்கு,मच्छर,डेंगू",
        sla_hours=48,
        default_priority="Medium",
        jurisdiction="Public Health Wards & Water Bodies",
        mandatory_actions="Spray larvicide on stagnant pools, conduct vector control fogging drive within 48h."
    )

    db.add_all([m1, m2, m3, m4, m5])
    db.commit()

    # 6. Seed Application Features (F001 - F008)
    f1 = Feature(feature_id="F001", feature_name="Submit Multilingual Grievance", description="File a new citizen complaint with automatic language intent detection and category tagging.", allowed_roles="*", allowed_organisations="*", task_tags="submit,grievance,complaint,file,new", impact_level="NORMAL")
    f2 = Feature(feature_id="F002", feature_name="View Complaint History", description="Access citizen complaint history, live status progression, and SLA tracking.", allowed_roles="*", allowed_organisations="*", task_tags="history,status,my complaints,view,track", impact_level="NORMAL")
    f3 = Feature(feature_id="F003", feature_name="Translate Complaint", description="Translate regional language complaint text (Tamil/Hindi) into English for departmental officers.", allowed_roles="Routing Officer,PWD Road Engineer,Water Line Inspector,Sanitation Officer,Department Supervisor", allowed_organisations="*", task_tags="translate,language,tamil,hindi,multilingual", impact_level="NORMAL")
    f4 = Feature(feature_id="F004", feature_name="Verify Attachments", description="Inspect and validate attached photo/document metadata uploaded with grievance.", allowed_roles="Routing Officer,PWD Road Engineer,Water Line Inspector,Sanitation Officer,Department Supervisor", allowed_organisations="*", task_tags="attachment,photo,verify,evidence,document", impact_level="NORMAL")
    f5 = Feature(feature_id="F005", feature_name="Escalate SLA Breach", description="Trigger supervisor escalation workflow when SLA resolution timeframe is exceeded.", allowed_roles="Routing Officer,Department Supervisor", allowed_organisations="*", task_tags="escalate,sla,breach,supervisor,urgent", impact_level="HIGH")
    f6 = Feature(feature_id="F006", feature_name="Internal Case Notes", description="Append confidential departmental inspection notes and repair crew updates.", allowed_roles="Routing Officer,PWD Road Engineer,Water Line Inspector,Sanitation Officer,Department Supervisor", allowed_organisations="*", task_tags="notes,internal,case,comment,update", impact_level="NORMAL")
    f7 = Feature(feature_id="F007", feature_name="Reassign Department Override", description="Override automated intent routing and reassign grievance to another department with reason logging.", allowed_roles="Routing Officer,Department Supervisor", allowed_organisations="*", task_tags="override,reassign,department,change,routing", impact_level="HIGH")
    f8 = Feature(feature_id="F008", feature_name="System Analytics & Audit Logs", description="Review system error taxonomy, discovery uplift metrics, and security audit logs.", allowed_roles="Department Supervisor", allowed_organisations="*", task_tags="analytics,audit,logs,metrics,reports", impact_level="NORMAL")

    db.add_all([f1, f2, f3, f4, f5, f6, f7, f8])
    db.commit()

    # 7. Seed Sample Grievances (Tamil, Hindi, English)
    c1 = Complaint(
        complaint_id="COMPLAINT_001",
        user_id="USER_001",
        description="Deep pothole on Anna Salai Main Road causing vehicle accidents and severe traffic delays.",
        language="English",
        category="Road Potholes & Infrastructure",
        priority="High",
        status="Routed",
        target_department_id="DEPT_PWD",
        sla_hours=48,
        is_escalated=False,
        created_at=datetime.datetime.utcnow() - datetime.timedelta(hours=6)
    )
    c2 = Complaint(
        complaint_id="COMPLAINT_002",
        user_id="USER_001",
        description="குடிநீர் குழாய் உடைந்து காந்தி தெருவில் கடந்த இரண்டு நாட்களாக தண்ணீர் வீணாகிறது.",
        language="Tamil",
        category="Water Leakage & Sewage Drainage",
        priority="High",
        status="Routed",
        target_department_id="DEPT_WATER",
        sla_hours=24,
        is_escalated=False,
        created_at=datetime.datetime.utcnow() - datetime.timedelta(hours=12)
    )
    c3 = Complaint(
        complaint_id="COMPLAINT_003",
        user_id="USER_001",
        description="तीन दिनों से नेहरू नगर में कचरे का डिब्बा भरा हुआ है और बदबू आ रही है।",
        language="Hindi",
        category="Garbage & Waste Sanitation",
        priority="Medium",
        status="Escalated",
        target_department_id="DEPT_SAN",
        sla_hours=24,
        is_escalated=True,
        created_at=datetime.datetime.utcnow() - datetime.timedelta(hours=30)
    )
    c4 = Complaint(
        complaint_id="COMPLAINT_004",
        user_id="USER_001",
        description="Streetlights on 5th Cross Road flickering and completely blacked out at night.",
        language="English",
        category="Streetlighting & Electrical Lines",
        priority="High",
        status="Routed",
        target_department_id="DEPT_ELEC",
        sla_hours=24,
        is_escalated=False,
        created_at=datetime.datetime.utcnow() - datetime.timedelta(hours=4)
    )

    db.add_all([c1, c2, c3, c4])
    db.commit()

    # 8. Seed Attachments
    att1 = Attachment(complaint_id="COMPLAINT_001", filename="pothole_photo.jpg", file_type="image/jpeg", file_size=245000)
    att2 = Attachment(complaint_id="COMPLAINT_002", filename="water_leak_video.mp4", file_type="video/mp4", file_size=1850000)

    db.add_all([att1, att2])
    db.commit()

    # 9. Seed Routing Results
    r_res1 = RoutingResult(
        complaint_id="COMPLAINT_001",
        detected_intent="Road Potholes & Infrastructure",
        target_department_id="DEPT_PWD",
        target_department_name="Public Works Department (PWD)",
        matched_mandate_id="MND_PWD_01",
        confidence_score=0.965,
        priority="High",
        sla_hours=48,
        assigned_role="PWD_ROAD_ENGINEER",
        routing_explanation="Matched intent 'Road Potholes & Infrastructure' with 96.5% confidence. Routed to PWD under mandate MND_PWD_01."
    )
    r_res2 = RoutingResult(
        complaint_id="COMPLAINT_002",
        detected_intent="Water Leakage & Sewage Drainage",
        target_department_id="DEPT_WATER",
        target_department_name="Water Supply & Sewerage Board",
        matched_mandate_id="MND_WATER_02",
        confidence_score=0.942,
        priority="High",
        sla_hours=24,
        assigned_role="WATER_LINE_INSPECTOR",
        routing_explanation="Matched Tamil keywords 'குடிநீர்' (drinking water) and 'குழாய்' (pipe) with 94.2% confidence. Routed to Water Board."
    )

    db.add_all([r_res1, r_res2])
    db.commit()

    # 10. Seed Escalation Log
    esc1 = EscalationLog(
        complaint_id="COMPLAINT_003",
        department_id="DEPT_SAN",
        escalation_level="DEPARTMENT_SUPERVISOR",
        reason="SLA time limit (24 hours) breached without dispatching waste compactor truck.",
        triggered_by="Automated System SLA Auditor"
    )
    db.add(esc1)
    db.commit()

    # 11. Seed Experiment Metrics (Baseline vs Assistant per feature F003, F006, F008)
    exp_data = [
        # Feature F003 (Translate Complaint) Baseline vs Assistant
        ExperimentMetric(group="BASELINE", feature_id="F003", complaint_id="C_M_01", routing_time_seconds=14400.0, routing_accuracy_pct=72.0, sla_breached=True, discovered=False, completed=True),
        ExperimentMetric(group="BASELINE", feature_id="F003", complaint_id="C_M_02", routing_time_seconds=18000.0, routing_accuracy_pct=68.0, sla_breached=True, discovered=False, completed=False),
        ExperimentMetric(group="BASELINE", feature_id="F003", complaint_id="C_M_03", routing_time_seconds=10800.0, routing_accuracy_pct=75.0, sla_breached=False, discovered=True, completed=True),
        ExperimentMetric(group="ASSISTANT", feature_id="F003", complaint_id="C_AI_01", routing_time_seconds=0.8, routing_accuracy_pct=96.5, sla_breached=False, discovered=True, completed=True),
        ExperimentMetric(group="ASSISTANT", feature_id="F003", complaint_id="C_AI_02", routing_time_seconds=0.6, routing_accuracy_pct=98.0, sla_breached=False, discovered=True, completed=True),
        ExperimentMetric(group="ASSISTANT", feature_id="F003", complaint_id="C_AI_03", routing_time_seconds=1.1, routing_accuracy_pct=95.0, sla_breached=False, discovered=True, completed=True),

        # Feature F006 (Internal Case Notes) Baseline vs Assistant
        ExperimentMetric(group="BASELINE", feature_id="F006", complaint_id="C_M_04", routing_time_seconds=12000.0, routing_accuracy_pct=70.0, sla_breached=True, discovered=False, completed=True),
        ExperimentMetric(group="BASELINE", feature_id="F006", complaint_id="C_M_05", routing_time_seconds=15000.0, routing_accuracy_pct=65.0, sla_breached=True, discovered=False, completed=False),
        ExperimentMetric(group="ASSISTANT", feature_id="F006", complaint_id="C_AI_04", routing_time_seconds=0.7, routing_accuracy_pct=97.0, sla_breached=False, discovered=True, completed=True),
        ExperimentMetric(group="ASSISTANT", feature_id="F006", complaint_id="C_AI_05", routing_time_seconds=0.9, routing_accuracy_pct=96.0, sla_breached=False, discovered=True, completed=True),

        # Feature F008 (Audit & Escalation Logs) Baseline vs Assistant
        ExperimentMetric(group="BASELINE", feature_id="F008", complaint_id="C_M_06", routing_time_seconds=16000.0, routing_accuracy_pct=74.0, sla_breached=True, discovered=False, completed=False),
        ExperimentMetric(group="ASSISTANT", feature_id="F008", complaint_id="C_AI_06", routing_time_seconds=0.5, routing_accuracy_pct=99.0, sla_breached=False, discovered=True, completed=True)
    ]
    db.add_all(exp_data)
    db.commit()

    # 12. Seed Usage Events
    u_events = [
        UsageEvent(feature_id="F001", user_id="USER_001", group="ASSISTANT", action="COMPLETED"),
        UsageEvent(feature_id="F002", user_id="USER_001", group="ASSISTANT", action="DISCOVERED"),
        UsageEvent(feature_id="F003", user_id="USER_002", group="ASSISTANT", action="DISCOVERED"),
        UsageEvent(feature_id="F006", user_id="USER_003", group="ASSISTANT", action="DISCOVERED"),
        UsageEvent(feature_id="F008", user_id="USER_005", group="ASSISTANT", action="DISCOVERED")
    ]
    db.add_all(u_events)
    db.commit()

    # 13. Seed Stakeholder Validations
    stk1 = StakeholderValidation(stakeholder_role="Routing Officer", usability_rating=5, explainability_rating=5, routing_speedup_pct=98.5, feedback_notes="Instant multilingual intent detection reduces routing time from hours to seconds.")
    stk2 = StakeholderValidation(stakeholder_role="PWD Engineer", usability_rating=5, explainability_rating=4, routing_speedup_pct=92.0, feedback_notes="Clear department mandate matching ensures grievances reach correct engineers directly.")
    stk3 = StakeholderValidation(stakeholder_role="Department Supervisor", usability_rating=4, explainability_rating=5, routing_speedup_pct=95.0, feedback_notes="Automated SLA escalation and override logging provide great accountability.")

    db.add_all([stk1, stk2, stk3])
    db.commit()

    print("Database successfully seeded for Citizen Grievance Routing Tool (Intent Detection, Department Mandates, Escalation, Features & Experiments).")

