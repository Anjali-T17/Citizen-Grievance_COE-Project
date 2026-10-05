from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import RecommendationFeedback, Feature
from app.schemas.schemas import (
    RecommendationRequest,
    RecommendationResponse,
    RecommendationFeedbackCreate,
    RecommendationFeedbackSchema,
    HelpSearchRequest,
    HelpSearchResponse,
    HelpSearchResult
)
from app.services.recommendation_engine import RecommendationEngine, TfIdfScorer
from app.services.permission_service import PermissionService


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

@router.post("/feedback", response_model=RecommendationFeedbackSchema, status_code=status.HTTP_201_CREATED)
def record_feedback(req: RecommendationFeedbackCreate, db: Session = Depends(get_db)):
    fb = RecommendationFeedback(
        recommendation_id=req.recommendation_id,
        anonymous_user_id=req.anonymous_user_id,
        is_helpful=req.is_helpful,
        feedback_text=req.feedback_text
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return fb

@router.post("/help-search", response_model=HelpSearchResponse)
def vector_help_search(
    req: HelpSearchRequest,
    db: Session = Depends(get_db)
):
    search_query = (req.query or req.help_query or "").strip()
    if not search_query:
        raise HTTPException(status_code=400, detail="Search query cannot be empty.")

    features = db.query(Feature).all()
    if not features:
        return HelpSearchResponse(query=search_query, total_matches=0, results=[])

    search_results = []
    user_role = req.role or "Citizen"
    user_org = req.organisation or "GCMC"

    for feat in features:
        doc_text = f"{feat.feature_name} {feat.description} {feat.task_tags}"
        sim_score = TfIdfScorer.compute_similarity(search_query, doc_text)
        
        is_permitted, _ = PermissionService.check_permission(db, user_role, user_org, feat.feature_id)

        search_results.append({
            "feature_id": feat.feature_id,
            "feature_name": feat.feature_name,
            "description": feat.description,
            "similarity_score": sim_score,
            "allowed": is_permitted,
            "impact_level": feat.impact_level
        })

    # Sort results by similarity score descending, prioritizing permitted features
    search_results.sort(key=lambda x: (x["similarity_score"], x["allowed"]), reverse=True)

    return HelpSearchResponse(
        query=search_query,
        total_matches=len(search_results),
        results=[HelpSearchResult(**r) for r in search_results]
    )

