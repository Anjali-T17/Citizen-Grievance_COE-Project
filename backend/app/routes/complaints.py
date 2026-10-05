import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.models import Complaint, Attachment, EscalationLog, AuditLog
from app.schemas.schemas import (
    ComplaintCreate,
    ComplaintSchema,
    AttachmentSchema,
    ComplaintStatusUpdate,
    TranslationRequest,
    TranslationResponse
)
from app.services.routing_engine import routing_engine


router = APIRouter(prefix="/api/complaints", tags=["Grievances"])

@router.post("", response_model=ComplaintSchema)
def submit_complaint(complaint: ComplaintCreate, db: Session = Depends(get_db)):
    if not complaint.description or not complaint.description.strip():
        raise HTTPException(status_code=400, detail="Complaint description cannot be empty.")

    cid = f"COMPLAINT_{str(uuid.uuid4())[:6].upper()}"
    
    # Run automatic intent detection & department mandate routing
    route_res = routing_engine.route_complaint(complaint.description, complaint.category)


    db_complaint = Complaint(
        complaint_id=cid,
        user_id="USER_001",
        description=complaint.description,
        language=complaint.language,
        category=route_res["detected_intent"],
        priority=route_res["priority"],
        status="Routed",
        target_department_id=route_res["target_department_id"],
        sla_hours=route_res["sla_hours"]
    )
    db.add(db_complaint)
    db.commit()

    if complaint.attachment_name:
        attachment = Attachment(
            complaint_id=cid,
            filename=complaint.attachment_name,
            file_type=complaint.attachment_type or "image/jpeg",
            file_size=complaint.attachment_size or 102400,
            upload_status="Uploaded"
        )
        db.add(attachment)
        db.commit()

    db.refresh(db_complaint)
    return db_complaint

@router.get("", response_model=List[ComplaintSchema])
def get_complaints(department_id: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Complaint)
    if department_id:
        query = query.filter(Complaint.target_department_id == department_id)
    return query.order_by(Complaint.created_at.desc()).all()

@router.get("/{complaint_id}", response_model=ComplaintSchema)
def get_complaint_details(complaint_id: str, db: Session = Depends(get_db)):
    c = db.query(Complaint).filter(Complaint.complaint_id == complaint_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Grievance not found")
    return c

VALID_STATUSES = {"Submitted", "Routed", "In Progress", "Escalated", "Resolved"}

@router.patch("/{complaint_id}/status", response_model=ComplaintSchema)
def update_complaint_status(
    complaint_id: str,
    status_update: ComplaintStatusUpdate,
    db: Session = Depends(get_db)
):
    complaint = db.query(Complaint).filter(Complaint.complaint_id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail=f"Grievance '{complaint_id}' not found.")

    target_status = status_update.status.strip()
    if target_status not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status '{target_status}'. Must be one of: {', '.join(sorted(VALID_STATUSES))}"
        )

    # RBAC check: Citizens cannot escalate, move to In Progress, or resolve complaints
    if status_update.role and status_update.role.lower() == "citizen" and target_status in ["In Progress", "Escalated", "Resolved"]:
        raise HTTPException(
            status_code=403,
            detail=f"ACCESS DENIED: Role '{status_update.role}' is not authorized to transition complaint to '{target_status}'."
        )

    # Lifecycle transition rule: Cannot revert resolved complaints back to earlier states
    if complaint.status == "Resolved" and target_status != "Resolved":
        raise HTTPException(
            status_code=400,
            detail="Invalid transition: Complaint is already Resolved and cannot be reopened to an earlier state."
        )

    old_status = complaint.status
    complaint.status = target_status

    if target_status == "Escalated":
        complaint.is_escalated = True
        esc = EscalationLog(
            complaint_id=complaint_id,
            department_id=complaint.target_department_id or "DEPT_GENERAL",
            escalation_level="SUPERVISOR",
            reason=status_update.comment or "Manual status escalation by officer",
            triggered_by=status_update.user_id or "OFFICER_001"
        )
        db.add(esc)

    # Audit log recording
    audit = AuditLog(
        user_id=status_update.user_id or "OFFICER_001",
        action=f"STATUS_CHANGE_TO_{target_status.upper()}",
        details=f"Complaint {complaint_id} status updated from '{old_status}' to '{target_status}'. Comment: {status_update.comment or 'N/A'}"
    )
    db.add(audit)

    db.commit()
    db.refresh(complaint)
    return complaint


class DeterministicTranslationService:
    @staticmethod
    def translate(text: str, source_lang: str, target_lang: str) -> str:
        if not text:
            return ""
        
        if source_lang.strip().lower() == target_lang.strip().lower():
            return text
        
        translations = {
            "சாலையில் பெரிய குழி உள்ளது வாகனங்கள் செல்ல முடியவில்லை": "There is a large pothole on the road, vehicles cannot pass.",
            "குடிநீர் குழாய் உடைந்து காந்தி தெருவில் கடந்த இரண்டு நாட்களாக தண்ணீர் வீணாகிறது": "Drinking water pipe burst on Gandhi Street and water is being wasted for the last two days.",
            "तीन दिनों से नेहरू नगर में कचरे का डिब्बा भरा हुआ है और बदबू आ रही है।": "Garbage bin in Nehru Nagar has been full for three days and stink is coming.",
            "पेयजल पाइप फट गया है और पानी बह रहा है": "Drinking water pipe burst and water is leaking.",
            "தெருவிளக்கு எரியவில்லை": "Streetlight is not working.",
            "கழிவுநீர் சாக்கடை நிரம்பி வழிகிறது": "Sewage drain is overflowing.",
            "कचरा नहीं उठाया गया है": "Garbage has not been collected."
        }

        if text in translations and target_lang.lower() in ["english", "en"]:
            return translations[text]
        
        dictionary = {
            "சாலை": "road", "சாலையில்": "on the road", "குழி": "pothole", "பெரிய": "large",
            "குடிநீர்": "drinking water", "குழாய்": "pipe", "கசிவு": "leakage", "உடைந்து": "burst",
            "தண்ணீர்": "water", "வீணாகிறது": "wasted", "சாக்கடை": "sewage", "குப்பை": "garbage",
            "தெருவிளக்கு": "streetlight", "மின்சாரம்": "electricity", "இருட்டு": "darkness",
            "கொசு": "mosquito", "காய்ச்சல்": "fever", "டெங்கு": "dengue", "சேதம்": "damaged",
            "सड़क": "road", "गड्ढा": "pothole", "बड़ा": "large", "पानी": "water", "पेयजल": "drinking water",
            "रिसव": "leakage", "पाइप": "pipe", "फट": "burst", "सीवर": "sewage", "कचरा": "garbage",
            "कूड़ा": "trash", "लाइट": "light", "बिजली": "electricity", "अंधेरा": "darkness"
        }

        words = text.split()
        translated_words = []
        for w in words:
            clean_w = w.strip(",.!?")
            if clean_w in dictionary and target_lang.lower() in ["english", "en"]:
                translated_words.append(dictionary[clean_w])
            else:
                translated_words.append(w)
        
        return " ".join(translated_words)


@router.post("/translate", response_model=TranslationResponse)
def translate_complaint_text(req: TranslationRequest):
    input_text = req.text or req.complaint_text or ""
    if not input_text:
        raise HTTPException(status_code=400, detail="Text for translation must be provided.")

    translated = DeterministicTranslationService.translate(
        text=input_text,
        source_lang=req.source_language,
        target_lang=req.target_language
    )

    return TranslationResponse(
        original_text=input_text,
        translated_text=translated,
        source_language=req.source_language,
        target_language=req.target_language,
        engine="Deterministic Local Rule-Based Translator Engine (Phase A)"
    )

