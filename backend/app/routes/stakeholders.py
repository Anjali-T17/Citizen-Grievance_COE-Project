from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.models import StakeholderValidation
from app.schemas.schemas import StakeholderValidationCreate, StakeholderSummaryResponse

router = APIRouter(prefix="/api/stakeholders", tags=["Stakeholders"])

@router.post("/validation", status_code=status.HTTP_201_CREATED)
def submit_stakeholder_validation(req: StakeholderValidationCreate, db: Session = Depends(get_db)):
    val = StakeholderValidation(
        stakeholder_role=req.stakeholder_role,
        usability_rating=req.usability_rating,
        explainability_rating=req.explainability_rating,
        efficiency_improvement_pct=req.efficiency_improvement_pct,
        feedback_notes=req.feedback_notes
    )
    db.add(val)
    db.commit()
    return {"message": "Stakeholder validation rating recorded successfully."}

@router.get("/summary", response_model=StakeholderSummaryResponse)
def get_stakeholder_summary(db: Session = Depends(get_db)):
    validations = db.query(StakeholderValidation).all()
    total = len(validations) or 1

    avg_u = sum(v.usability_rating for v in validations) / total
    avg_e = sum(v.explainability_rating for v in validations) / total
    avg_eff = sum(v.efficiency_improvement_pct for v in validations) / total

    role_counts = {}
    for v in validations:
        role_counts[v.stakeholder_role] = role_counts.get(v.stakeholder_role, 0) + 1

    role_breakdown = [{"role": r, "count": c} for r, c in role_counts.items()]

    return StakeholderSummaryResponse(
        avg_usability_rating=round(avg_u, 2),
        avg_explainability_rating=round(avg_e, 2),
        avg_efficiency_gain_pct=round(avg_eff, 1),
        total_validations=len(validations),
        role_breakdown=role_breakdown
    )
