"""Therapeutic Optimization coordinator."""

from __future__ import annotations

from typing import Any

from therapeutic_optimization.audit import OptimizationAudit, OptimizationAuditEntry
from therapeutic_optimization.comparator import StrategyComparator
from therapeutic_optimization.explanation import OptimizationExplanationEngine
from therapeutic_optimization.generator import StrategyGenerator
from therapeutic_optimization.goals import GoalInterpreter, GoalValidator
from therapeutic_optimization.hypothesis import TherapeuticHypothesisBuilder, UncertaintyRegistry
from therapeutic_optimization.matcher import ConstraintMatcher, EvidenceMatcher
from therapeutic_optimization.models import ClinicalGoal, TherapeuticOptimizationResult, Uncertainty
from therapeutic_optimization.scoring import ConfidenceCalculator, ScoringEngine


class OptimizationCoordinator:
    """Coordinates non-prescriptive therapeutic hypothesis generation."""

    def __init__(self) -> None:
        self.goal_interpreter = GoalInterpreter()
        self.goal_validator = GoalValidator()
        self.strategy_generator = StrategyGenerator()
        self.constraint_matcher = ConstraintMatcher()
        self.evidence_matcher = EvidenceMatcher()
        self.strategy_comparator = StrategyComparator()
        self.scoring_engine = ScoringEngine()
        self.confidence_calculator = ConfidenceCalculator()
        self.explanation_engine = OptimizationExplanationEngine()
        self.hypothesis_builder = TherapeuticHypothesisBuilder()
        self.uncertainty_registry = UncertaintyRegistry()
        self.audit = OptimizationAudit()

    def execute(
        self,
        goals: tuple[ClinicalGoal, ...] = (),
        safety_result: dict[str, Any] | None = None,
        evidence_result: dict[str, Any] | None = None,
        knowledge_context: dict[str, Any] | None = None,
    ) -> TherapeuticOptimizationResult:
        normalized_goals = self.goal_interpreter.normalize(goals)
        validation = self.goal_validator.validate(normalized_goals)
        candidates = self.strategy_generator.generate(normalized_goals)
        filtered_candidates = self.constraint_matcher.apply(
            candidates,
            safety_result or {},
        )
        evidence_links = self.evidence_matcher.match(
            filtered_candidates,
            evidence_result or {},
        )
        comparisons = self.strategy_comparator.compare(filtered_candidates)
        scores = self.scoring_engine.score(filtered_candidates)
        explanations = self.explanation_engine.explain(filtered_candidates)
        hypotheses = self.hypothesis_builder.build(
            filtered_candidates,
            explanations,
            evidence_links,
        )
        if validation.missing_goals:
            self.uncertainty_registry.register(
                Uncertainty(
                    category="missing_context",
                    explanation="No explicit clinical goals were supplied.",
                )
            )
        uncertainties = self.uncertainty_registry.all()
        confidence = self.confidence_calculator.calculate(
            knowledge_completeness=1.0 if knowledge_context else 0.0,
            evidence_quality=1.0 if evidence_links else 0.0,
            constraint_coverage=1.0 if safety_result else 0.0,
            missing_data=1.0 if validation.missing_goals else 0.0,
        )
        result = TherapeuticOptimizationResult(
            status="completed_read_only",
            goals=normalized_goals,
            candidate_strategies=candidates,
            evaluated_strategies=(),
            scores=scores,
            hypotheses=hypotheses,
            uncertainties=uncertainties,
            explanations=explanations,
            confidence=confidence,
        )
        self.audit.record(
            OptimizationAuditEntry(
                event="TherapeuticOptimizationFinished",
                candidate_strategies=tuple(item.strategy_id for item in candidates),
                discarded_strategies=tuple(
                    item.strategy_id
                    for item in candidates
                    if item not in filtered_candidates
                ),
                scores=tuple(score.to_dict() for score in scores),
                hypotheses=tuple(item.hypothesis_id for item in hypotheses),
                trace_id=result.trace_id,
            )
        )
        _ = comparisons
        return result
