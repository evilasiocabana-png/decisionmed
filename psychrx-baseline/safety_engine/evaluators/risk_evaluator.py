"""Risk evaluator shell."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from safety_engine.models import Risk
from safety_engine.registry import RiskRegistry


@dataclass(frozen=True)
class RiskEvaluation:
    matched_risks: tuple[Risk, ...] = field(default_factory=tuple)
    missing_data: tuple[str, ...] = field(default_factory=tuple)
    severity: str = "informational"
    confidence: float = 0.0


@dataclass(frozen=True)
class RiskSummary:
    risks: tuple[Risk, ...] = field(default_factory=tuple)
    highest_severity: str = "informational"
    traceable: bool = True


class RiskEvaluator:
    """Evaluates registered risks without making treatment decisions."""

    def __init__(self, registry: RiskRegistry | None = None) -> None:
        self._registry = registry or RiskRegistry()

    def evaluate(self, patient_context: dict[str, Any] | None = None) -> RiskEvaluation:
        if patient_context is None:
            return RiskEvaluation(missing_data=("patient_context",))
        return RiskEvaluation(matched_risks=self._registry.all())

    def aggregate(self, risks: tuple[Risk, ...]) -> RiskSummary:
        highest = "informational"
        for candidate in ("critical", "blocking", "restriction", "caution"):
            if any(risk.severity == candidate for risk in risks):
                highest = candidate
                break
        return RiskSummary(risks=risks, highest_severity=highest)
