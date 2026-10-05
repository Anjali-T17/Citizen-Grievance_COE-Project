import re
from typing import Optional

INJECTION_PATTERNS = [
    r"ignore\s+.*?\s*(instructions|rules|prompts)",
    r"show\s+.*?\s*(admin|restricted|all|supervisor)\s+features",
    r"bypass\s+.*?\s*(role|permission|security|auth)",
    r"reveal\s+.*?\s*(system|hidden|internal)\s+(prompt|data|schema)",
    r"act\s+as\s+(admin|root|superuser|developer)",
    r"grant\s+.*?\s*(admin|all)\s+(access|privileges)",
    r"override\s+.*?\s*(security|permission)",
    r"select\s+.*\s+from\s+users",
    r"<script\b[^>]*>",
    r"sudo\s+escalate",
    r"exec\s*\("
]


class SecurityService:
    def check_prompt_injection(self, input_text: str) -> Optional[str]:
        if not input_text:
            return None

        lowered = input_text.lower()
        for pattern in INJECTION_PATTERNS:
            if re.search(pattern, lowered):
                return pattern

        return None

security_service = SecurityService()
