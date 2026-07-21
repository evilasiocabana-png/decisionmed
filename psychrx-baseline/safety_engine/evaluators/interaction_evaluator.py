"""Interaction evaluator shell."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from safety_engine.models import Interaction


@dataclass(frozen=True)
class InteractionEvaluation:
    interactions: tuple[Interaction, ...] = field(default_factory=tuple)
    missing_data: tuple[str, ...] = field(default_factory=tuple)


class InteractionEvaluator:
    """Accepts future validated interaction objects; contains no clinical rules."""

    def evaluate(
        self,
        patient_context: dict[str, Any] | None = None,
        interactions: tuple[Interaction, ...] = (),
    ) -> InteractionEvaluation:
        if patient_context is None:
            return InteractionEvaluation(missing_data=("patient_context",))
        return InteractionEvaluation(interactions=interactions)
