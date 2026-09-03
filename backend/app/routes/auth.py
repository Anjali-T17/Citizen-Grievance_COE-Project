from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User, Role, Organisation
from app.schemas.schemas import DemoLoginRequest, DemoLoginResponse

router = APIRouter(prefix="/api/auth", tags=["Auth"])

ROLE_USER_MAPPING = {
    "Citizen": "USER_001",
    "Grievance Officer": "USER_002",
    "Supervisor": "USER_003",
    "External Partner": "USER_004"
}

@router.post("/demo-login", response_model=DemoLoginResponse)
def demo_login(req: DemoLoginRequest, db: Session = Depends(get_db)):
    user_id = ROLE_USER_MAPPING.get(req.role, "USER_001")
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        # Fallback synthetic user
        return DemoLoginResponse(
            user_id=user_id,
            name=f"Demo {req.role}",
            email=f"{req.role.lower().replace(' ', '')}@example.com",
            role=req.role,
            organisation=req.organisation
        )

    return DemoLoginResponse(
        user_id=user.id,
        name=user.name,
        email=user.email,
        role=req.role,
        organisation=req.organisation
    )
