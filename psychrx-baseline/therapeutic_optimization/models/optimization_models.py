"""Typed models for non-prescriptive therapeutic optimization."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class OptimizationTrace:
    """Trace links for every future hypothesis."""

    trace_id: str = field(default_factory=lambda: f"TOE-TRC-{uuid4()}")
    safety_trace: str = "not_bound"
    evidence_trace: str = "not_bound"
    runtime_trace: str = "not_bound"
    knowledge_version: str = "not_bound"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ClinicalGoal:
    """Structured goal supplied by clinical context, not inferred."""

    goal_id: str
    label: str
    priority: int = 0
    weight: float = 0.0
    dependencies: tuple[str, ...] = field(default_factory=tuple)
    conflicts: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GoalPriority:
    """Priority contract for a goal."""

    goal_id: str
    priority: int = 0
    weight: float = 0.0
    dependencies: tuple[str, ...] = field(default_factory=tuple)
    conflicts: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class CandidateStrategy:
    """Candidate strategy hypothesis, never a treatment instruction."""

    strategy_id: str
    label: str = "candidate_strategy"
    goals: tuple[str, ...] = field(default_factory=tuple)
    source: str = "structural"
    trace: OptimizationTrace = field(default_factory=OptimizationTrace)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class StrategyScore:
    """Structured score dimensions without recommendation semantics."""

    strategy_id: str
    goal_alignment: float = 0.0
    constraint_compatibility: float = 0.0
    evidence_support: float = 0.0
    clinical_completeness: float = 0.0

    def total(self) -> float:
        return (
            self.goal_alignment
            + self.constraint_compatibility
            + self.evidence_support
            + self.clinical_completeness
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvaluatedStrategy:
    """Candidate with structural score and explanation."""

    candidate: CandidateStrategy
    score: StrategyScore
    included: bool = True
    reasons: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class StrategyComparison:
    """Comparison matrix entry."""

    strategy_id: str
    benefits: tuple[str, ...] = field(default_factory=tuple)
    risks: tuple[str, ...] = field(default_factory=tuple)
    constraints: tuple[str, ...] = field(default_factory=tuple)
    goals: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class OptimizationExplanation:
    """Traceable explanation without prescriptive wording."""

    explanation_id: str
    strategy_id: str
    included_reason: str = ""
    excluded_reason: str = ""
    strengths: tuple[str, ...] = field(default_factory=tuple)
    limitations: tuple[str, ...] = field(default_factory=tuple)
    uncertainties: tuple[str, ...] = field(default_factory=tuple)
    trace: OptimizationTrace = field(default_factory=OptimizationTrace)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TherapeuticHypothesis:
    """Physician-review hypothesis, not a recommendation."""

    hypothesis_id: str
    candidate_strategy_id: str
    supporting_evidence: tuple[str, ...] = field(default_factory=tuple)
    constraints: tuple[str, ...] = field(default_factory=tuple)
    goals: tuple[str, ...] = field(default_factory=tuple)
    confidence: float = 0.0
    explanation_id: str = ""
    trace: OptimizationTrace = field(default_factory=OptimizationTrace)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Uncertainty:
    """Structured uncertainty category."""

    category: str
    explanation: str
    trace: OptimizationTrace = field(default_factory=OptimizationTrace)


@dataclass(frozen=True)
class TherapeuticOptimizationResult:
    """Complete structural output of the TOE."""

    status: str
    goals: tuple[ClinicalGoal, ...] = field(default_factory=tuple)
    candidate_strategies: tuple[CandidateStrategy, ...] = field(default_factory=tuple)
    evaluated_strategies: tuple[EvaluatedStrategy, ...] = field(default_factory=tuple)
    scores: tuple[StrategyScore, ...] = field(default_factory=tuple)
    hypotheses: tuple[TherapeuticHypothesis, ...] = field(default_factory=tuple)
    uncertainties: tuple[Uncertainty, ...] = field(default_factory=tuple)
    explanations: tuple[OptimizationExplanation, ...] = field(default_factory=tuple)
    confidence: float = 0.0
    trace_id: str = field(default_factory=lambda: f"TOE-{uuid4()}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
