"""Language guardrails for explanation text."""

from __future__ import annotations


class LanguageGuardrails:
    """Rejects prescriptive or definitive language."""

    forbidden = (
        "must prescribe",
        "best medication",
        "recommended prescription",
        "definitive diagnosis",
        "automatic treatment",
        "prescrever agora",
        "dose recomendada",
    )
    required = (
        "hypothesis",
        "requires clinical judgment",
        "based on available data",
    )

    def violations(self, text: str) -> tuple[str, ...]:
        lowered = text.lower()
        return tuple(term for term in self.forbidden if term in lowered)

    def is_safe(self, text: str) -> bool:
        return not self.violations(text)
