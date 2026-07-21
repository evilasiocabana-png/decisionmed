"""Fail-closed aggregation of externally produced safety check results."""

from __future__ import annotations

from collections.abc import Iterable
import re

from decisionmed.evidence import EvidenceRegistry, EvidenceStatus

from .models import (
    SafetyAssessment,
    SafetyCheckOutcome,
    SafetyCheckResult,
    SafetyError,
    SafetyGateStatus,
    SafetySeverity,
)
from .providers import SafetyCheckProviderRegistry


class SafetyCoordinator:
    """Aggregate check metadata; does not evaluate patient data or risk."""

    def __init__(
        self,
        providers: SafetyCheckProviderRegistry,
        evidence: EvidenceRegistry,
    ) -> None:
        if not isinstance(providers, SafetyCheckProviderRegistry):
            raise TypeError("providers must be a SafetyCheckProviderRegistry")
        if not isinstance(evidence, EvidenceRegistry):
            raise TypeError("evidence must be an EvidenceRegistry")
        coverage = providers.coverage()
        if not coverage.complete:
            raise SafetyError(
                "safety.provider_coverage",
                "complete compatible provider coverage is required",
            )
        self._expected = coverage.bound_check_ids
        self._specifications = providers.specifications
        self._evidence = evidence

    def assess(
        self,
        results: Iterable[SafetyCheckResult],
        trace_id: str,
        snapshot_fingerprint: str,
    ) -> SafetyAssessment:
        items = tuple(results)
        if not isinstance(trace_id, str) or not trace_id.strip():
            raise SafetyError("safety.trace_id", "trace id cannot be empty")
        if (
            not isinstance(snapshot_fingerprint, str)
            or not re.fullmatch(r"[0-9a-f]{64}", snapshot_fingerprint)
        ):
            raise SafetyError(
                "safety.snapshot_fingerprint",
                "snapshot fingerprint must be SHA-256",
            )
        if not all(isinstance(item, SafetyCheckResult) for item in items):
            raise TypeError("results must contain only SafetyCheckResult values")
        mismatched_traces = tuple(
            item.check_id for item in items if item.trace_id != trace_id
        )
        if mismatched_traces:
            raise SafetyError(
                "safety.trace_mismatch",
                "check results must belong to the assessment trace",
            )
        mismatched_snapshots = tuple(
            item.check_id
            for item in items
            if item.snapshot_fingerprint != snapshot_fingerprint
        )
        if mismatched_snapshots:
            raise SafetyError(
                "safety.snapshot_mismatch",
                "check results must belong to the exact assessment snapshot",
            )
        ids = tuple(item.check_id for item in items)
        if len(set(ids)) != len(ids):
            raise SafetyError("safety.duplicate_result", "check results must be unique")
        unknown = tuple(check_id for check_id in ids if check_id not in self._expected)
        if unknown:
            raise SafetyError(
                "safety.unknown_check", f"unknown check results: {', '.join(unknown)}"
            )

        missing = tuple(check_id for check_id in self._expected if check_id not in ids)
        not_evaluated = tuple(
            item.check_id
            for item in items
            if item.outcome is SafetyCheckOutcome.NOT_EVALUATED
        )
        unvalidated_evidence = tuple(
            item.check_id
            for item in items
            if item.outcome is not SafetyCheckOutcome.NOT_EVALUATED
            and not self._has_validated_evidence(item)
        )
        overdue_evidence = tuple(
            item.check_id
            for item in items
            if item.outcome is not SafetyCheckOutcome.NOT_EVALUATED
            and self._has_validated_evidence(item)
            and not self._has_current_evidence(item)
        )
        undeclared_evidence = tuple(
            item.check_id
            for item in items
            if item.outcome is not SafetyCheckOutcome.NOT_EVALUATED
            and not self._uses_declared_evidence(item)
        )
        critical = tuple(
            finding.finding_id
            for item in items
            for finding in item.findings
            if finding.severity is SafetySeverity.CRITICAL
        )
        noncritical = tuple(
            finding.finding_id
            for item in items
            for finding in item.findings
            if finding.severity is not SafetySeverity.CRITICAL
        )
        has_findings = any(item.findings for item in items)

        reasons = tuple(
            [*(f"missing_check:{item}" for item in missing)]
            + [*(f"not_evaluated:{item}" for item in not_evaluated)]
            + [*(f"unvalidated_evidence:{item}" for item in unvalidated_evidence)]
            + [*(f"overdue_evidence:{item}" for item in overdue_evidence)]
            + [*(f"undeclared_evidence:{item}" for item in undeclared_evidence)]
            + [*(f"critical_finding:{item}" for item in critical)]
            + [*(f"finding:{item}" for item in noncritical)]
        )
        if critical:
            status = SafetyGateStatus.BLOCKED
        elif (
            missing
            or not_evaluated
            or unvalidated_evidence
            or overdue_evidence
            or undeclared_evidence
        ):
            status = SafetyGateStatus.INCOMPLETE
        elif has_findings:
            status = SafetyGateStatus.HUMAN_REVIEW_REQUIRED
        else:
            status = SafetyGateStatus.READY_FOR_HUMAN_REVIEW

        return SafetyAssessment(
            status=status,
            expected_check_ids=self._expected,
            results=items,
            missing_check_ids=missing,
            blocking_reasons=reasons,
            trace_id=trace_id,
            snapshot_fingerprint=snapshot_fingerprint,
        )

    def _has_validated_evidence(self, result: SafetyCheckResult) -> bool:
        source_ids = set(result.evidence_source_ids)
        source_ids.update(
            source_id for finding in result.findings for source_id in finding.evidence_source_ids
        )
        return bool(source_ids) and all(
            (source := self._evidence.get(source_id)) is not None
            and source.status is EvidenceStatus.VALIDATED
            for source_id in source_ids
        )

    def _has_current_evidence(self, result: SafetyCheckResult) -> bool:
        source_ids = set(result.evidence_source_ids)
        source_ids.update(
            source_id
            for finding in result.findings
            for source_id in finding.evidence_source_ids
        )
        return bool(source_ids) and all(
            (source := self._evidence.get(source_id)) is not None
            and source.status is EvidenceStatus.VALIDATED
            and source.review_due_on is not None
            and not source.review_overdue
            for source_id in source_ids
        )

    def _uses_declared_evidence(self, result: SafetyCheckResult) -> bool:
        declared = set(
            self._specifications.require(result.check_id).evidence_source_ids
        )
        cited = set(result.evidence_source_ids)
        cited.update(
            source_id
            for finding in result.findings
            for source_id in finding.evidence_source_ids
        )
        return bool(cited) and cited.issubset(declared)
