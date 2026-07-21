"""Deterministic scientific validation replay."""

from __future__ import annotations

from scientific_validation.models import ScientificValidationResult


class ScientificReplay:
    def replay(self, result: ScientificValidationResult) -> ScientificValidationResult:
        return result

