"""Constraint matcher."""

from __future__ import annotations

from typing import Any

from therapeutic_optimization.models import CandidateStrategy


class ConstraintMatcher:
    """Applies SafetyResult structurally without mutating it."""

    def apply(
        self,
        candidates: tuple[CandidateStrategy, ...],
        safety_result: dict[str, Any],
    ) -> tuple[CandidateStrategy, ...]:
        if safety_result.get("blocking_flags"):
            return ()
        return candidates
