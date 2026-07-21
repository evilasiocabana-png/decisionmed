"""Goal interpreter without clinical inference."""

from __future__ import annotations

from therapeutic_optimization.models import ClinicalGoal


class GoalInterpreter:
    """Normalizes explicit goals supplied by context."""

    def normalize(self, goals: tuple[ClinicalGoal, ...]) -> tuple[ClinicalGoal, ...]:
        return tuple(sorted(goals, key=lambda goal: goal.priority))
