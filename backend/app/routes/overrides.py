from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import OverrideLog, AuditLog
from app.schemas.schemas import OverrideCreate, OverrideSchema

router = APIRouter(prefix="/api/overrides", tags=["Overrides"])

@router.post("", response_model=OverrideSchema, status_code=status.HTTP_201_CREATED)
def record_override(req: OverrideCreate, db: Session = Depends(get_db)):
    override_entry = OverrideLog(
        complaint_id=req.complaint_id,
        original_department_id=req.original_department_id,
        overridden_department_id=req.overridden_department_id,
        officer_user_id=req.officer_user_id,
        override_reason=req.override_reason,
        comment=req.comment
    )
    db.add(override_entry)

    audit_entry = AuditLog(
        user_id=req.officer_user_id,
        action="ROUTING_DEPARTMENT_OVERRIDDEN",
        details=f"Complaint: {req.complaint_id}, Original: {req.original_department_id}, New: {req.overridden_department_id}, Reason: {req.override_reason}"
    )
    db.add(audit_entry)

    db.commit()
    db.refresh(override_entry)

    return override_entry
