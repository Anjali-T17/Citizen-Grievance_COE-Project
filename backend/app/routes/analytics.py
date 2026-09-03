from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.models import Feature, UsageEvent, Recommendation, Override
from app.schemas.schemas import AnalyticsSummaryResponse, FeatureUsageStat, OverrideStat

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/usage", response_model=AnalyticsSummaryResponse)
def get_usage_analytics(db: Session = Depends(get_db)):
    features = db.query(Feature).all()
    feature_map = {f.feature_id: f.feature_name for f in features}

    # Count usage per feature
    usage_counts = {}
    events = db.query(UsageEvent.feature_id, func.count(UsageEvent.event_id)).group_by(UsageEvent.feature_id).all()
    for fid, cnt in events:
        usage_counts[fid] = cnt

    total_events = sum(usage_counts.values()) or 1
    avg_usage = total_events / max(len(features), 1)

    most_used = []
    underused = []

    for f in features:
        cnt = usage_counts.get(f.feature_id, 0)
        is_underused = cnt < avg_usage or cnt < 10
        stat = FeatureUsageStat(
            feature_id=f.feature_id,
            feature_name=f.feature_name,
            usage_count=cnt,
            underused=is_underused
        )
        if is_underused:
            underused.append(stat)
        else:
            most_used.append(stat)

    # Override statistics
    override_stats = []
    override_counts = db.query(Override.override_reason, func.count(Override.id)).group_by(Override.override_reason).all()
    for reason, cnt in override_counts:
        override_stats.append(OverrideStat(reason=reason, count=cnt))

    total_recs = db.query(Recommendation).count()
    total_overrides = db.query(Override).count()

    return AnalyticsSummaryResponse(
        total_usage_events=sum(usage_counts.values()),
        total_recommendations=total_recs,
        total_overrides=total_overrides,
        most_used_features=sorted(most_used, key=lambda x: x.usage_count, reverse=True),
        underused_features=sorted(underused, key=lambda x: x.usage_count),
        override_reasons=override_stats
    )
