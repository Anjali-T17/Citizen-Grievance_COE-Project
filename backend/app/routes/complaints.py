from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Complaint, Attachment, User, UsageEvent
from app.schemas.schemas import ComplaintCreate, ComplaintSchema, AttachmentSchema

router = APIRouter(prefix="/api/complaints", tags=["Complaints"])

@router.post("", response_model=ComplaintSchema, status_code=status.HTTP_201_CREATED)
def create_complaint(
    req: ComplaintCreate,
    user_id: str = "USER_001",
    db: Session = Depends(get_db)
):
    # Ensure user exists or fallback
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user_id = "USER_001"

    # Generate sequential complaint ID (COMPLAINT_001, COMPLAINT_002, ...)
    count = db.query(Complaint).count()
    new_complaint_id = f"COMPLAINT_{str(count + 1).zfill(3)}"

    new_complaint = Complaint(
        complaint_id=new_complaint_id,
        user_id=user_id,
        description=req.description,
        language=req.language,
        category=req.category,
        priority=req.priority,
        status="Submitted"
    )
    db.add(new_complaint)
    db.flush()

    # Save attachment if provided
    if req.attachment_name:
        attachment = Attachment(
            complaint_id=new_complaint_id,
            filename=req.attachment_name,
            file_type=req.attachment_type or "application/pdf",
            file_size=req.attachment_size or 102400,
            upload_status="Uploaded"
        )
        db.add(attachment)

    # Log feature usage event for F001 - Submit Complaint
    event = UsageEvent(
        anonymous_user_id=user_id,
        organisation_id="ORG_001",
        role="Citizen",
        feature_id="F001",
        task_goal="Submit new complaint",
        action="execute",
        success=True
    )
    db.add(event)

    db.commit()
    db.refresh(new_complaint)

    return new_complaint

@router.get("", response_model=List[ComplaintSchema])
def get_complaints(db: Session = Depends(get_db)):
    return db.query(Complaint).order_by(Complaint.created_at.desc()).all()

@router.get("/{complaint_id}", response_model=ComplaintSchema)
def get_complaint(complaint_id: str, db: Session = Depends(get_db)):
    complaint = db.query(Complaint).filter(Complaint.complaint_id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail=f"Complaint {complaint_id} not found")
    return complaint

@router.post("/{complaint_id}/attachments", response_model=AttachmentSchema)
def upload_attachment(
    complaint_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    complaint = db.query(Complaint).filter(Complaint.complaint_id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail=f"Complaint {complaint_id} not found")

    attachment = Attachment(
        complaint_id=complaint_id,
        filename=file.filename,
        file_type=file.content_type or "application/octet-stream",
        file_size=1024 * 50, # Demo size
        upload_status="Uploaded"
    )
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    return attachment
