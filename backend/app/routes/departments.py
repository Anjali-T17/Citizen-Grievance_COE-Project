from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import Department, DepartmentMandate
from app.schemas.schemas import DepartmentSchema, DepartmentMandateSchema

router = APIRouter(prefix="/api/departments", tags=["Departments & Mandates"])

@router.get("", response_model=List[DepartmentSchema])
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()

@router.get("/{department_id}", response_model=DepartmentSchema)
def get_department_by_id(department_id: str, db: Session = Depends(get_db)):
    dept = db.query(Department).filter(Department.id == department_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept

@router.get("/{department_id}/mandates", response_model=List[DepartmentMandateSchema])
def get_department_mandates(department_id: str, db: Session = Depends(get_db)):
    return db.query(DepartmentMandate).filter(DepartmentMandate.department_id == department_id).all()
