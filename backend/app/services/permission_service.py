from sqlalchemy.orm import Session
from app.models.models import Feature, Permission, Role

class PermissionService:
    @staticmethod
    def check_permission(db: Session, role_name: str, org_name: str, feature_id: str) -> tuple[bool, str]:
        """
        Verifies whether a role in a given organisation has permission to use a feature.
        Returns (is_allowed: bool, reason: str)
        """
        feature = db.query(Feature).filter(Feature.feature_id == feature_id).first()
        if not feature:
            return False, f"Feature {feature_id} does not exist."

        # Check allowed organisations
        allowed_orgs = [o.strip() for o in feature.allowed_organisations.split(",")]
        if org_name not in allowed_orgs and "*" not in allowed_orgs:
            return False, f"Feature '{feature.feature_name}' is not available for organisation '{org_name}'."

        # Check allowed roles
        allowed_roles = [r.strip() for r in feature.allowed_roles.split(",")]
        if role_name not in allowed_roles and "*" not in allowed_roles:
            return False, f"This feature is not available for your role ({role_name})."

        # Check explicit RBAC permission override table if role_id exists
        role_obj = db.query(Role).filter(Role.name == role_name).first()
        if role_obj:
            perm = db.query(Permission).filter(
                Permission.role_id == role_obj.id,
                Permission.feature_code == feature_id
            ).first()
            if perm and not perm.can_access:
                return False, f"Explicit permission revoked for feature '{feature.feature_name}' on role '{role_name}'."

        return True, "Permission granted."
