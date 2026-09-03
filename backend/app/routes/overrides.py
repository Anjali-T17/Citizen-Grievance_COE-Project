from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Override, AuditLog
from app.schemas.schemas import OverrideCreate, OverrideSchema

router = APIRouter(prefix="/api/overrides", tags=["Overrides"])

@router.post("", response_model=OverrideSchema, status_code=status.HTTP_201_CREATED)
def record_override(req: OverrideCreate, db: Session = Depends(get_db)):
    override_entry = Override(
        recommendation_id=req.recommendation_id,
        anonymous_user_id=req.anonymous_user_id,
        action=req.action,
        override_reason=req.override_reason,
        comment=req.comment
    )
    db.add(override_entry)

    # Log to audit log as well
    audit_entry = AuditLog(
        anonymous_user_id=req.anonymous_user_id,
        action="RECOMMENDATION_OVERRIDDEN",
        details=f"Action: {req.action}, Reason: {req.override_reason}, Comment: {req.comment}"
    )
    db.add(audit_entry)

    db.commit()
    db.refresh(override_entry)

    return override_entry
