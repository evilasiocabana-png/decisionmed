"""Fail-closed orchestration for governed safety-check evaluators."""

from __future__ import annotations

from decisionmed.domain import ClinicalSnapshot
from decisionmed.evidence import EvidenceRegistry, EvidenceStatus

from .coordinator import SafetyCoordinator
from .definitions import SafetyCheckStatus
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
        if evaluators.providers.specifications.evidence is not evidence:
            raise SafetyError(
                "safety_preflight.evidence_registry",
                "preflight must use the specification evidence registry",
            )
        self._evaluators = evaluators
        self._evidence = evidence
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
        specifications_current = all(
            specification.status is SafetyCheckStatus.VALIDATED
            and specification.review_due_on is not None
            and not specification.review_overdue
            for specification in self._evaluators.providers.specifications.all()
        )
        evidence_current = all(
            (source := self._evidence.get(source_id)) is not None
            and source.status is EvidenceStatus.VALIDATED
            and source.review_due_on is not None
            and not source.review_overdue
            for specification in self._evaluators.providers.specifications.all()
            for source_id in specification.evidence_source_ids
        )
        if not specifications_current:
            results = tuple(
                self._not_evaluated(
                    evaluator,
                    snapshot.trace_id,
                    "Governed safety specification review is not current; evaluator was not invoked.",
                )
                for evaluator in evaluators
            )
        elif not evidence_current:
            results = tuple(
                self._not_evaluated(
                    evaluator,
                    snapshot.trace_id,
                    "Governed evidence review is not current; evaluator was not invoked.",
                )
                for evaluator in evaluators
            )
        elif not snapshot.structurally_complete:
            results = tuple(
                self._not_evaluated(
                    evaluator,
                    snapshot.trace_id,
                    "Snapshot is structurally incomplete; evaluator was not invoked.",
                )
                for evaluator in evaluators
            )
        elif not specialties_match:
            results = tuple(
                self._not_evaluated(
                    evaluator,
                    snapshot.trace_id,
                    "Snapshot specialty does not match the governed safety specification.",
                )
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
            return SafetyPreflight._not_evaluated(
                evaluator,
                snapshot.trace_id,
                "Evaluator did not produce a valid governed result.",
            )
        if (
            not isinstance(result, SafetyCheckResult)
            or result.check_id != evaluator.check_id
            or result.trace_id != snapshot.trace_id
        ):
            return SafetyPreflight._not_evaluated(
                evaluator,
                snapshot.trace_id,
                "Evaluator did not produce a valid governed result.",
            )
        return result

    @staticmethod
    def _not_evaluated(
        evaluator: SafetyCheckEvaluator, trace_id: str, explanation: str
    ) -> SafetyCheckResult:
        return SafetyCheckResult(
            check_id=evaluator.check_id,
            outcome=SafetyCheckOutcome.NOT_EVALUATED,
            trace_id=trace_id,
            explanation=explanation,
        )
