from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Role
from app.schemas.schemas import RoleSchema

router = APIRouter(prefix="/api/roles", tags=["Roles"])

@router.get("", response_model=List[RoleSchema])
def get_roles(org_id: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Role)
    if org_id:
        query = query.filter(Role.org_id == org_id)
    return query.all()
