import json
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import Feature, UsageEvent, Recommendation
from app.schemas.schemas import RecommendationResponse, RecommendationScoreDetail
from app.services.permission_service import PermissionService
from app.services.security_service import SecurityService

class RecommendationEngine:
    @staticmethod
    def get_recommendation(
        db: Session,
        role: str,
        organisation: str,
        task_goal: str,
        help_query: str,
        user_id: str = "USER_001"
    ) -> RecommendationResponse:
        # Step 1: Check security / prompt injection on inputs
        full_text = f"{task_goal} {help_query}"
        is_malicious, security_warning = SecurityService.inspect_untrusted_input(full_text, user_id, db)

        # Step 2: Fetch all features
        features = db.query(Feature).all()
        if not features:
            raise ValueError("No features available in catalog.")

        # Step 3: Compute usage statistics for Underuse Boost
        usage_counts = {}
        usage_data = db.query(
            UsageEvent.feature_id, func.count(UsageEvent.event_id).label("cnt")
        ).group_by(UsageEvent.feature_id).all()
        for fid, cnt in usage_data:
            usage_counts[fid] = cnt

        # Calculate average usage to determine underuse threshold
        total_usage = sum(usage_counts.values()) or 1
        avg_usage = total_usage / max(len(features), 1)

        feature_scores = []

        for feature in features:
            is_permitted, perm_reason = PermissionService.check_permission(
                db, role_name=role, org_name=organisation, feature_id=feature.feature_id
            )

            evidence = []
            matched_rules = []
            score = 0.0

            # 1. Role Match (30 pts)
            allowed_roles = [r.strip() for r in feature.allowed_roles.split(",")]
            role_match = (role in allowed_roles or "*" in allowed_roles)
            if role_match:
                score += 30.0
                evidence.append(f"Role matches {role}")
                matched_rules.append(RecommendationScoreDetail(
                    rule_name="Role Match",
                    points=30.0,
                    matched=True,
                    explanation=f"User role '{role}' is explicitly permitted for feature."
                ))
            else:
                matched_rules.append(RecommendationScoreDetail(
                    rule_name="Role Match",
                    points=0.0,
                    matched=False,
                    explanation=f"Role '{role}' is not in allowed roles."
                ))

            # 2. Task Match (30 pts)
            task_lower = task_goal.lower()
            tags = [t.strip().lower() for t in feature.task_tags.split(",") if t.strip()]
            task_matched_keywords = [tag for tag in tags if tag in task_lower]
            if task_matched_keywords:
                score += 30.0
                evidence.append(f"Task relates to {', '.join(task_matched_keywords)}")
                matched_rules.append(RecommendationScoreDetail(
                    rule_name="Task Goal Match",
                    points=30.0,
                    matched=True,
                    explanation=f"Task goal matched keywords: {', '.join(task_matched_keywords)}"
                ))
            else:
                matched_rules.append(RecommendationScoreDetail(
                    rule_name="Task Goal Match",
                    points=0.0,
                    matched=False,
                    explanation="No task tag keywords found in task goal."
                ))

            # 3. Help Query Match (20 pts)
            query_lower = help_query.lower()
            feat_name_lower = feature.feature_name.lower()
            feat_desc_lower = feature.description.lower()
            
            help_matched = any(tag in query_lower for tag in tags) or (feat_name_lower in query_lower) or any(w in feat_desc_lower for w in query_lower.split() if len(w) > 3)
            if help_matched and query_lower.strip():
                score += 20.0
                evidence.append(f"Help query matches {feature.feature_name.lower()}")
                matched_rules.append(RecommendationScoreDetail(
                    rule_name="Help Query Match",
                    points=20.0,
                    matched=True,
                    explanation=f"Help search query matched feature capabilities."
                ))
            else:
                matched_rules.append(RecommendationScoreDetail(
                    rule_name="Help Query Match",
                    points=0.0,
                    matched=False,
                    explanation="Help query did not match feature keywords."
                ))

            # 4. Underuse Boost (10 pts)
            feat_usage = usage_counts.get(feature.feature_id, 0)
            is_underused = feat_usage < avg_usage or feat_usage < 10
            if is_underused:
                score += 10.0
                evidence.append("Feature is underused")
                matched_rules.append(RecommendationScoreDetail(
                    rule_name="Underuse Boost",
                    points=10.0,
                    matched=True,
                    explanation=f"Usage count ({feat_usage}) is lower than average threshold."
                ))
            else:
                matched_rules.append(RecommendationScoreDetail(
                    rule_name="Underuse Boost",
                    points=0.0,
                    matched=False,
                    explanation=f"Feature has standard/high usage ({feat_usage} events)."
                ))

            # 5. Permission Check (10 pts)
            if is_permitted:
                score += 10.0
                evidence.append("Permission granted")
                matched_rules.append(RecommendationScoreDetail(
                    rule_name="Permission Verification",
                    points=10.0,
                    matched=True,
                    explanation="Backend security verification passed successfully."
                ))
            else:
                evidence.append(f"Permission denied: {perm_reason}")
                matched_rules.append(RecommendationScoreDetail(
                    rule_name="Permission Verification",
                    points=0.0,
                    matched=False,
                    explanation=perm_reason
                ))

            feature_scores.append({
                "feature": feature,
                "score": score,
                "allowed": is_permitted,
                "evidence": evidence,
                "matched_rules": matched_rules,
            })

        # Filter permitted features first if available, otherwise consider all
        permitted_candidates = [item for item in feature_scores if item["allowed"]]
        
        if permitted_candidates:
            best_match = max(permitted_candidates, key=lambda x: x["score"])
        else:
            # If no permitted features match, select top overall to demonstrate permission denial
            best_match = max(feature_scores, key=lambda x: x["score"])

        selected_feature: Feature = best_match["feature"]
        requires_conf = (selected_feature.impact_level == "HIGH")

        # Save recommendation record to DB
        rec_record = Recommendation(
            anonymous_user_id=user_id,
            task_goal=task_goal,
            help_query=help_query,
            recommended_feature_id=selected_feature.feature_id,
            score=best_match["score"],
            allowed=best_match["allowed"],
            evidence=json.dumps(best_match["evidence"])
        )
        db.add(rec_record)
        db.commit()

        return RecommendationResponse(
            feature_id=selected_feature.feature_id,
            feature_name=selected_feature.feature_name,
            description=selected_feature.description,
            score=best_match["score"],
            allowed=best_match["allowed"],
            requires_confirmation=requires_conf,
            impact_level=selected_feature.impact_level,
            evidence=best_match["evidence"],
            matched_rules=best_match["matched_rules"],
            security_warning=security_warning if is_malicious else None
        )
