import re
from sqlalchemy.orm import Session
from app.models.models import AuditLog

INJECTION_PATTERNS = [
    r"ignore (your|all|previous) (instructions|rules|prompts)",
    r"show (me )?(admin|restricted|all|supervisor) (only )?features",
    r"bypass (role|permission|security|auth) (controls|checks)",
    r"reveal (system|hidden|internal) (prompt|data|schema)",
    r"act as (admin|root|superuser|developer)",
    r"grant (me )?(admin|all) (access|privileges)",
    r"override (security|permission)",
    r"select\s+.*\s+from\s+users",
    r"<script\b[^>]*>",
    r"sudo\s+escalate",
    r"exec\s*\("
]

class SecurityService:
    @staticmethod
    def inspect_untrusted_input(input_text: str, user_id: str, db: Session) -> tuple[bool, str]:
        if not input_text:
            return False, ""

        lowered = input_text.lower()
        for pattern in INJECTION_PATTERNS:
            if re.search(pattern, lowered):
                log_entry = AuditLog(
                    anonymous_user_id=user_id,
                    action="PROMPT_INJECTION_ATTEMPT",
                    details=f"Malicious instruction pattern detected: '{input_text[:100]}...'"
                )
                db.add(log_entry)
                db.commit()

                warning = "Untrusted instruction detected. Role and permission controls remain enforced."
                return True, warning

        return False, ""
