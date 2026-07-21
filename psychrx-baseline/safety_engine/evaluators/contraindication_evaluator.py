"""Contraindication evaluator shell."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from safety_engine.models import Contraindication


@dataclass(frozen=True)
class ContraindicationEvaluation:
    contraindications: tuple[Contraindication, ...] = field(default_factory=tuple)
    missing_data: tuple[str, ...] = field(default_factory=tuple)


class ContraindicationEvaluator:
    """Accepts future validated contraindication objects; contains no clinical rules."""

    def evaluate(
        self,
        patient_context: dict[str, Any] | None = None,
        contraindications: tuple[Contraindication, ...] = (),
    ) -> ContraindicationEvaluation:
        if patient_context is None:
            return ContraindicationEvaluation(missing_data=("patient_context",))
        return ContraindicationEvaluation(contraindications=contraindications)
