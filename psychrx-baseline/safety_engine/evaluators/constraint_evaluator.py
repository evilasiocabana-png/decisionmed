"""Constraint evaluator shell."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from safety_engine.models import Constraint
from safety_engine.registry import ConstraintRegistry


@dataclass(frozen=True)
class ConstraintEvaluation:
    matched_constraints: tuple[Constraint, ...] = field(default_factory=tuple)
    missing_data: tuple[str, ...] = field(default_factory=tuple)
    severity: str = "informational"
    confidence: float = 0.0


class ConstraintEvaluator:
    """Evaluates registered constraints only when future knowledge is supplied."""

    def __init__(self, registry: ConstraintRegistry | None = None) -> None:
        self._registry = registry or ConstraintRegistry()

    def evaluate(self, patient_context: dict[str, Any] | None = None) -> ConstraintEvaluation:
        if patient_context is None:
            return ConstraintEvaluation(missing_data=("patient_context",))
        return ConstraintEvaluation(matched_constraints=self._registry.all())
