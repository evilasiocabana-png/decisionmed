from datetime import datetime, timedelta, timezone
import unittest
from unittest.mock import Mock

from decisionmed.application import SafetyPreflightApplicationService
from decisionmed.audit import AuditError, AuditLedger
from decisionmed.domain import ClinicalSnapshot, EntityId, SubjectReference
from decisionmed.safety import (
    SafetyAssessment,
    SafetyCheckOutcome,
    SafetyCheckResult,
    SafetyGateStatus,
    SafetyPreflight,
)


class FailingAuditLedger(AuditLedger):
    def append(self, event, trace_id):  # type: ignore[no-untyped-def]
        raise AuditError("audit.synthetic_failure", "synthetic audit failure")


class SafetyPreflightApplicationServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.snapshot = ClinicalSnapshot(
            snapshot_id=EntityId("snapshot-audited-preflight"),
            lineage_id=EntityId("lineage-audited-preflight"),
            subject_reference=SubjectReference(
                "sub-0123456789abcdef0123456789abcdef"
            ),
            session_id=EntityId("session-audited-preflight"),
            specialty_key="cardiology",
            captured_at=datetime.now(timezone.utc) - timedelta(seconds=1),
            trace_id="trace.audited-preflight",
        )
        self.assessment = SafetyAssessment(
            status=SafetyGateStatus.INCOMPLETE,
            expected_check_ids=("check.synthetic-audit",),
            results=(
                SafetyCheckResult(
                    check_id="check.synthetic-audit",
                    outcome=SafetyCheckOutcome.NOT_EVALUATED,
                    trace_id=self.snapshot.trace_id,
                ),
            ),
            missing_check_ids=(),
            blocking_reasons=("not_evaluated:check.synthetic-audit",),
            trace_id=self.snapshot.trace_id,
        )

    def test_completed_preflight_appends_minimal_verifiable_metadata(self) -> None:
        preflight = Mock(spec=SafetyPreflight)
        preflight.run.return_value = self.assessment
        ledger = AuditLedger()
        service = SafetyPreflightApplicationService(preflight, ledger)

        returned = service.run(self.snapshot)
        record = ledger.records()[0]
        payload = dict(record.payload)

        self.assertIs(self.assessment, returned)
        self.assertEqual("safety.preflight_completed", record.event_name)
        self.assertEqual("incomplete", payload["status"])
        self.assertEqual("1", payload["expected_check_count"])
        self.assertEqual("false", payload["clinical_execution_allowed"])
        self.assertEqual(self.snapshot.trace_id, record.trace_id)
        self.assertTrue(ledger.verify())
        self.assertFalse(service.clinical_execution_allowed)
        self._assert_no_clinical_values(record)

    def test_preflight_exception_is_audited_without_message_or_values(self) -> None:
        preflight = Mock(spec=SafetyPreflight)
        preflight.run.side_effect = RuntimeError("sensitive synthetic message")
        ledger = AuditLedger()
        service = SafetyPreflightApplicationService(preflight, ledger)

        with self.assertRaises(RuntimeError):
            service.run(self.snapshot)

        record = ledger.records()[0]
        payload = dict(record.payload)
        self.assertEqual("safety.preflight_failed", record.event_name)
        self.assertEqual("RuntimeError", payload["error_type"])
        self.assertNotIn("sensitive synthetic message", str(record))
        self.assertTrue(ledger.verify())
        self._assert_no_clinical_values(record)

    def test_audit_failure_prevents_returning_an_unaudited_assessment(self) -> None:
        preflight = Mock(spec=SafetyPreflight)
        preflight.run.return_value = self.assessment
        service = SafetyPreflightApplicationService(preflight, FailingAuditLedger())

        with self.assertRaises(AuditError) as failure:
            service.run(self.snapshot)

        self.assertEqual("audit.synthetic_failure", failure.exception.code)

    def test_invalid_dependencies_are_rejected(self) -> None:
        preflight = Mock(spec=SafetyPreflight)
        with self.assertRaises(TypeError):
            SafetyPreflightApplicationService(object(), AuditLedger())  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            SafetyPreflightApplicationService(preflight, object())  # type: ignore[arg-type]

    def _assert_no_clinical_values(self, record: object) -> None:
        serialized = str(record)
        self.assertNotIn(str(self.snapshot.subject_reference), serialized)
        self.assertNotIn("observations", serialized)
        self.assertNotIn("patient", serialized.lower())


if __name__ == "__main__":
    unittest.main()
