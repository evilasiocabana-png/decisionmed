"""Governance rules for the Clinical Operating Mind."""

from __future__ import annotations


class GovernanceRuleRegistry:
    """Lists non-negotiable structural rules."""

    RULES = (
        "Safety before Optimization",
        "Evidence before Hypothesis",
        "Snapshot after Explanation",
        "Timeline after Snapshot",
        "Workspace reads Snapshot",
        "Navigation never mutates clinical state",
        "No prescription output",
        "No autonomous clinical decision",
    )

    def all(self) -> tuple[str, ...]:
        return self.RULES

    def validate_output(self, payload: str) -> tuple[str, ...]:
        lowered = payload.lower()
        errors = []
        for forbidden in ("prescrever", "dose recomendada", "decisao clinica autonoma"):
            if forbidden in lowered:
                errors.append(f"forbidden_output:{forbidden}")
        return tuple(errors)

