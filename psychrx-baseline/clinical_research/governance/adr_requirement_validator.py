"""ADR requirement validator."""

from __future__ import annotations


class AdrRequirementValidator:
    REQUIRED = ("ADR", "documentation update", "benchmark report", "validation report")

    def validate(self, artifacts: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(f"missing:{item}" for item in self.REQUIRED if item not in artifacts)

