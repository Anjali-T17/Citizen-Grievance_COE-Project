from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import DepartmentMandate, RoutingResult, OverrideLog
from app.schemas.schemas import RoutingRequest, RoutingResponse, OverrideCreate, OverrideSchema, DepartmentMandateSchema
from app.services.routing_engine import routing_engine
from app.services.security_service import security_service

router = APIRouter(prefix="/api/routing", tags=["Grievance Routing Engine"])

@router.post("/detect-and-route", response_model=RoutingResponse)
def detect_and_route(req: RoutingRequest, db: Session = Depends(get_db)):
    # 1. Security Check for Prompt Injection / Adversarial input (Edge Case 2)
    security_alert = security_service.check_prompt_injection(req.description)
    
    # 2. Execute NLP Intent Detection & Mandate Routing
    route_res = routing_engine.route_complaint(
        description=req.description,
        category_hint=req.category_hint,
        urgent_flag=req.urgent_flag
    )
    
    if security_alert:
        route_res["security_warning"] = f"Security Alert: Potential adversarial text pattern detected ('{security_alert}'). Standard mandate rules enforced."

    # Save routing log to DB if complaint_id is provided
    if req.complaint_id:
        r_log = RoutingResult(
            complaint_id=req.complaint_id,
            detected_intent=route_res["detected_intent"],
            target_department_id=route_res["target_department_id"],
            target_department_name=route_res["target_department_name"],
            matched_mandate_id=route_res["matched_mandate_id"],
            confidence_score=route_res["confidence_score"],
            priority=route_res["priority"],
            sla_hours=route_res["sla_hours"],
            assigned_role=route_res["assigned_role"],
            routing_explanation=route_res["routing_explanation"],
            is_ambiguous=route_res["is_ambiguous"]
        )
        db.add(r_log)
        db.commit()

    return route_res

@router.post("/override", response_model=OverrideSchema)
def log_routing_override(override_data: OverrideCreate, db: Session = Depends(get_db)):
    override_rec = OverrideLog(
        complaint_id=override_data.complaint_id,
        original_department_id=override_data.original_department_id,
        overridden_department_id=override_data.overridden_department_id,
        officer_user_id=override_data.officer_user_id,
        override_reason=override_data.override_reason,
        comment=override_data.comment
    )
    db.add(override_rec)
    db.commit()
    db.refresh(override_rec)
    return override_rec

@router.get("/mandates", response_model=List[DepartmentMandateSchema])
def list_all_mandates(db: Session = Depends(get_db)):
    return db.query(DepartmentMandate).all()
