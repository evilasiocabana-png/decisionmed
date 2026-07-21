"""Formal safety-check evaluation port with no concrete implementation."""

from __future__ import annotations

from typing import Protocol

from decisionmed.domain import ClinicalSnapshot

from .models import SafetyCheckResult


class SafetyCheckEvaluator(Protocol):
    """Required shape of a future governed safety-check implementation."""

    @property
    def check_id(self) -> str: ...

    @property
    def specification_version(self) -> str: ...

    def evaluate(
        self, snapshot: ClinicalSnapshot, *, trace_id: str
    ) -> SafetyCheckResult: ...
