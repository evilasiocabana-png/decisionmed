"""Goal validation."""

from __future__ import annotations

from dataclasses import dataclass, field

from therapeutic_optimization.models import ClinicalGoal


@dataclass(frozen=True)
class GoalValidation:
    duplicates: tuple[str, ...] = field(default_factory=tuple)
    missing_goals: bool = False
    invalid_priorities: tuple[str, ...] = field(default_factory=tuple)


class GoalValidator:
    """Validates structural goal data."""

    def validate(self, goals: tuple[ClinicalGoal, ...]) -> GoalValidation:
        ids = [goal.goal_id for goal in goals]
        duplicates = tuple(sorted({goal_id for goal_id in ids if ids.count(goal_id) > 1}))
        invalid = tuple(goal.goal_id for goal in goals if goal.priority < 0)
        return GoalValidation(
            duplicates=duplicates,
            missing_goals=not goals,
            invalid_priorities=invalid,
        )
