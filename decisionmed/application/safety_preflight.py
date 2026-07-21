"""Application orchestration for auditable, fail-closed safety preflight."""

from __future__ import annotations

from decisionmed.audit import AuditLedger
from decisionmed.domain import ClinicalSnapshot, DomainEvent
from decisionmed.safety import SafetyAssessment, SafetyPreflight


class SafetyPreflightApplicationService:
    """Run safety preflight only when its status can be audit-recorded."""

    def __init__(self, preflight: SafetyPreflight, audit: AuditLedger) -> None:
        if not isinstance(preflight, SafetyPreflight):
            raise TypeError("preflight must be a SafetyPreflight")
        if not isinstance(audit, AuditLedger):
            raise TypeError("audit must be an AuditLedger")
        self._preflight = preflight
        self._audit = audit

    def run(self, snapshot: ClinicalSnapshot) -> SafetyAssessment:
        if not isinstance(snapshot, ClinicalSnapshot):
            raise TypeError("snapshot must be a ClinicalSnapshot")
        try:
            assessment = self._preflight.run(snapshot)
        except Exception as error:
            self._audit.append(
                DomainEvent(
                    name="safety.preflight_failed",
                    aggregate_id=str(snapshot.snapshot_id),
                    payload=(
                        ("error_type", type(error).__name__),
                        ("specialty", snapshot.specialty_key),
                        ("snapshot_version", snapshot.version),
                        ("snapshot_fingerprint", snapshot.content_fingerprint),
                        ("clinical_execution_allowed", "false"),
                    ),
                ),
                snapshot.trace_id,
            )
            raise
        self._audit.append(
            DomainEvent(
                name="safety.preflight_completed",
                aggregate_id=str(snapshot.snapshot_id),
                payload=(
                    ("status", assessment.status.value),
                    ("specialty", snapshot.specialty_key),
                    ("snapshot_version", snapshot.version),
                    ("snapshot_fingerprint", assessment.snapshot_fingerprint),
                    ("expected_check_count", str(len(assessment.expected_check_ids))),
                    ("result_count", str(len(assessment.results))),
                    ("missing_check_count", str(len(assessment.missing_check_ids))),
                    ("blocking_reason_count", str(len(assessment.blocking_reasons))),
                    ("clinical_execution_allowed", "false"),
                ),
            ),
            snapshot.trace_id,
        )
        return assessment

    @property
    def clinical_execution_allowed(self) -> bool:
        return False
