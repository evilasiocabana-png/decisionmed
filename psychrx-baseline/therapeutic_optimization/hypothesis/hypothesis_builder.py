"""Therapeutic hypothesis builder."""

from __future__ import annotations

from therapeutic_optimization.models import CandidateStrategy, OptimizationExplanation, TherapeuticHypothesis


class TherapeuticHypothesisBuilder:
    """Builds hypotheses for review without recommending treatment."""

    def build(
        self,
        candidates: tuple[CandidateStrategy, ...],
        explanations: tuple[OptimizationExplanation, ...],
        evidence_links: dict[str, tuple[str, ...]],
    ) -> tuple[TherapeuticHypothesis, ...]:
        explanation_by_strategy = {
            explanation.strategy_id: explanation.explanation_id for explanation in explanations
        }
        return tuple(
            TherapeuticHypothesis(
                hypothesis_id=f"HYP-{candidate.strategy_id}",
                candidate_strategy_id=candidate.strategy_id,
                supporting_evidence=evidence_links.get(candidate.strategy_id, ()),
                goals=candidate.goals,
                confidence=0.0,
                explanation_id=explanation_by_strategy.get(candidate.strategy_id, ""),
            )
            for candidate in candidates
        )
