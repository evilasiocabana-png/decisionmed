"""Fail-closed orchestration for governed safety-check evaluators."""

from __future__ import annotations

from decisionmed.domain import ClinicalSnapshot
from decisionmed.evidence import EvidenceRegistry

from .coordinator import SafetyCoordinator
from .evaluator import SafetyCheckEvaluator
from .evaluator_registry import SafetyCheckEvaluatorRegistry
from .models import (
    SafetyAssessment,
    SafetyCheckOutcome,
    SafetyCheckResult,
    SafetyError,
)


class SafetyPreflight:
    """Run registered evaluators and reduce every contract failure to incomplete."""

    def __init__(
        self,
        evaluators: SafetyCheckEvaluatorRegistry,
        evidence: EvidenceRegistry,
    ) -> None:
        if not isinstance(evaluators, SafetyCheckEvaluatorRegistry):
            raise TypeError("evaluators must be a SafetyCheckEvaluatorRegistry")
        if not evaluators.complete:
            raise SafetyError(
                "safety_preflight.evaluator_coverage",
                "complete evaluator coverage is required",
            )
        if not isinstance(evidence, EvidenceRegistry):
            raise TypeError("evidence must be an EvidenceRegistry")
        self._evaluators = evaluators
        self._coordinator = SafetyCoordinator(evaluators.providers, evidence)

    def run(self, snapshot: ClinicalSnapshot) -> SafetyAssessment:
        if not isinstance(snapshot, ClinicalSnapshot):
            raise TypeError("snapshot must be a ClinicalSnapshot")
        evaluators = self._evaluators.all()
        specialties_match = all(
            self._evaluators.providers.specifications.require(
                evaluator.check_id
            ).specialty_key
            == snapshot.specialty_key
            for evaluator in evaluators
        )
        if not snapshot.structurally_complete or not specialties_match:
            results = tuple(
                self._not_evaluated(evaluator, snapshot.trace_id)
                for evaluator in evaluators
            )
        else:
            results = tuple(
                self._evaluate(evaluator, snapshot) for evaluator in evaluators
            )
        return self._coordinator.assess(results, snapshot.trace_id)

    @property
    def clinical_execution_allowed(self) -> bool:
        return False

    @staticmethod
    def _evaluate(
        evaluator: SafetyCheckEvaluator, snapshot: ClinicalSnapshot
    ) -> SafetyCheckResult:
        try:
            result = evaluator.evaluate(snapshot, trace_id=snapshot.trace_id)
        except Exception:
            return SafetyPreflight._not_evaluated(evaluator, snapshot.trace_id)
        if (
            not isinstance(result, SafetyCheckResult)
            or result.check_id != evaluator.check_id
            or result.trace_id != snapshot.trace_id
        ):
            return SafetyPreflight._not_evaluated(evaluator, snapshot.trace_id)
        return result

    @staticmethod
    def _not_evaluated(
        evaluator: SafetyCheckEvaluator, trace_id: str
    ) -> SafetyCheckResult:
        return SafetyCheckResult(
            check_id=evaluator.check_id,
            outcome=SafetyCheckOutcome.NOT_EVALUATED,
            trace_id=trace_id,
        )
