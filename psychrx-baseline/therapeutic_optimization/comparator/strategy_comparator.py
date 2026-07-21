"""Strategy comparison matrix."""

from __future__ import annotations

from therapeutic_optimization.models import CandidateStrategy, StrategyComparison


class StrategyComparator:
    """Creates structural comparison entries."""

    def compare(self, candidates: tuple[CandidateStrategy, ...]) -> tuple[StrategyComparison, ...]:
        return tuple(
            StrategyComparison(strategy_id=candidate.strategy_id, goals=candidate.goals)
            for candidate in candidates
        )
