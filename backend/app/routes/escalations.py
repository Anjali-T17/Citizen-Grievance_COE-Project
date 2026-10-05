from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import EscalationLog, Complaint
from app.schemas.schemas import EscalationCreate, EscalationSchema

router = APIRouter(prefix="/api/escalations", tags=["Escalation Workflow"])

@router.post("", response_model=EscalationSchema)
def trigger_escalation(esc_data: EscalationCreate, db: Session = Depends(get_db)):
    complaint = db.query(Complaint).filter(Complaint.complaint_id == esc_data.complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    complaint.is_escalated = True
    complaint.status = "Escalated"
    
    esc_record = EscalationLog(
        complaint_id=esc_data.complaint_id,
        department_id=esc_data.department_id,
        escalation_level=esc_data.escalation_level,
        reason=esc_data.reason,
        triggered_by=esc_data.triggered_by
    )
    db.add(esc_record)
    db.commit()
    db.refresh(esc_record)
    return esc_record

@router.get("", response_model=List[EscalationSchema])
def list_escalations(db: Session = Depends(get_db)):
    return db.query(EscalationLog).order_by(EscalationLog.timestamp.desc()).all()
