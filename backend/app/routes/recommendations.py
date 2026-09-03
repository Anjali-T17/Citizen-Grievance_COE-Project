from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import RecommendationRequest, RecommendationResponse
from app.services.recommendation_engine import RecommendationEngine

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

@router.post("", response_model=RecommendationResponse)
def generate_recommendation(
    req: RecommendationRequest,
    db: Session = Depends(get_db)
):
    try:
        return RecommendationEngine.get_recommendation(
            db=db,
            role=req.role,
            organisation=req.organisation,
            task_goal=req.task_goal,
            help_query=req.help_query,
            user_id=req.anonymous_user_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
