"""Non-prescriptive scoring engine."""

from __future__ import annotations

from therapeutic_optimization.models import CandidateStrategy, StrategyScore


class ScoringEngine:
    """Scores structural dimensions without producing recommendations."""

    def score(self, candidates: tuple[CandidateStrategy, ...]) -> tuple[StrategyScore, ...]:
        return tuple(
            StrategyScore(
                strategy_id=candidate.strategy_id,
                goal_alignment=0.0,
                constraint_compatibility=0.0,
                evidence_support=0.0,
                clinical_completeness=0.0,
            )
            for candidate in candidates
        )
