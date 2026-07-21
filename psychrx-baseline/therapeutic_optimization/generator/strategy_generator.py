"""Candidate strategy generator."""

from __future__ import annotations

from therapeutic_optimization.models import CandidateStrategy, ClinicalGoal


class StrategyGenerator:
    """Generates structural candidates from explicit goals only."""

    def generate(self, goals: tuple[ClinicalGoal, ...]) -> tuple[CandidateStrategy, ...]:
        return tuple(
            CandidateStrategy(
                strategy_id=f"CAND-{goal.goal_id}",
                label="candidate_for_physician_review",
                goals=(goal.goal_id,),
            )
            for goal in goals
        )
