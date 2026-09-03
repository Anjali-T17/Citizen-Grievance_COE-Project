from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Organisation
from app.schemas.schemas import OrganisationSchema

router = APIRouter(prefix="/api/organisations", tags=["Organisations"])

@router.get("", response_model=List[OrganisationSchema])
def get_organisations(db: Session = Depends(get_db)):
    return db.query(Organisation).all()
