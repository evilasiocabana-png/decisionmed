"""Explanation generation for optimization outputs."""

from __future__ import annotations

from therapeutic_optimization.models import CandidateStrategy, OptimizationExplanation


class OptimizationExplanationEngine:
    """Produces traceable explanations, not prescriptive justifications."""

    def explain(self, candidates: tuple[CandidateStrategy, ...]) -> tuple[OptimizationExplanation, ...]:
        return tuple(
            OptimizationExplanation(
                explanation_id=f"EXP-{candidate.strategy_id}",
                strategy_id=candidate.strategy_id,
                included_reason="Candidate retained for physician review.",
                limitations=("No clinical recommendation generated.",),
                uncertainties=("Real clinical validation not implemented.",),
            )
            for candidate in candidates
        )
