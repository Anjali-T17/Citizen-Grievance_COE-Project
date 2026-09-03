from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Feature
from app.schemas.schemas import FeatureSchema
from app.services.permission_service import PermissionService

router = APIRouter(prefix="/api/features", tags=["Features"])

@router.get("", response_model=List[FeatureSchema])
def get_features(
    role: Optional[str] = None,
    org: Optional[str] = None,
    db: Session = Depends(get_db)
):
    features = db.query(Feature).all()
    if role and org:
        filtered = []
        for f in features:
            is_permitted, _ = PermissionService.check_permission(db, role, org, f.feature_id)
            if is_permitted:
                filtered.append(f)
        return filtered
    return features

@router.get("/{feature_id}", response_model=FeatureSchema)
def get_feature(
    feature_id: str,
    role: Optional[str] = Query(None),
    org: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    feature = db.query(Feature).filter(Feature.feature_id == feature_id).first()
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")

    if role and org:
        is_permitted, reason = PermissionService.check_permission(db, role, org, feature_id)
        if not is_permitted:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": "ACCESS DENIED", "reason": reason}
            )

    return feature
