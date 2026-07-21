from dataclasses import replace
from datetime import datetime, timedelta, timezone
import unittest

from decisionmed.application import (
    SAFETY_REVIEW_ACTION,
    SafetyReviewerAuthorityDecision,
    SafetyReviewerAuthorityStatus,
    SafetyReviewApplicationError,
    SafetyReviewApplicationService,
)
from decisionmed.audit import AuditError, AuditLedger
from decisionmed.safety import (
    SafetyAssessment,
    SafetyCheckOutcome,
    SafetyCheckResult,
    SafetyError,
    SafetyGateStatus,
    SafetyReviewDisposition,
    safety_assessment_fingerprint,
)


class SyntheticAuthority:
    provider = "authority-provider.synthetic"

    def __init__(self, decision: object) -> None:
        self.decision = decision

    def verify(self, **kwargs: object) -> object:
        return self.decision


class FailingAuthority(SyntheticAuthority):
    def verify(self, **kwargs: object) -> object:
        raise RuntimeError("sensitive synthetic authority message")


class FailingAuditLedger(AuditLedger):
    def append(self, event, trace_id):  # type: ignore[no-untyped-def]
        raise AuditError("audit.synthetic_failure", "synthetic audit failure")


class SafetyReviewApplicationServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.assessment = SafetyAssessment(
            status=SafetyGateStatus.READY_FOR_HUMAN_REVIEW,
            expected_check_ids=("check.synthetic-review",),
            results=(
                SafetyCheckResult(
                    check_id="check.synthetic-review",
                    outcome=SafetyCheckOutcome.PASSED,
                    trace_id="trace.synthetic-review",
                    explanation="Sensitive synthetic clinical explanation.",
                    evidence_source_ids=("source.synthetic-review",),
                ),
            ),
            missing_check_ids=(),
            blocking_reasons=(),
            trace_id="trace.synthetic-review",
        )
        self.reviewed_at = datetime.now(timezone.utc) - timedelta(seconds=1)

    def test_authorized_review_is_returned_only_after_minimal_audit(self) -> None:
        ledger = AuditLedger()
        service = self._service(self._decision(), ledger)

        record = self._record(service)
        audit_record = ledger.records()[0]
        payload = dict(audit_record.payload)

        self.assertTrue(record.matches(self.assessment))
        self.assertEqual("safety.review_recorded", audit_record.event_name)
        self.assertEqual(
            record.assessment_fingerprint, payload["assessment_fingerprint"]
        )
        self.assertEqual("validated_for_reasoning_review", payload["disposition"])
        self.assertEqual("false", payload["reasoning_execution_allowed"])
        self.assertEqual("false", payload["clinical_execution_allowed"])
        self.assertTrue(ledger.verify())
        self.assertFalse(service.reasoning_execution_allowed)
        self.assertFalse(service.clinical_execution_allowed)
        self._assert_sensitive_content_absent(audit_record)

    def test_denied_decision_is_audited_and_rejected(self) -> None:
        ledger = AuditLedger()
        service = self._service(
            self._decision(SafetyReviewerAuthorityStatus.DENIED), ledger
        )

        with self.assertRaises(SafetyReviewApplicationError) as denied:
            self._record(service)

        self.assertEqual("safety_review.authority_denied", denied.exception.code)
        self.assertEqual("safety.review_authority_denied", ledger.records()[0].event_name)
        self._assert_sensitive_content_absent(ledger.records()[0])

    def test_mismatched_decision_is_audited_and_rejected(self) -> None:
        decision = replace(
            self._decision(),
            assessment_fingerprint="b" * 64,
        )
        ledger = AuditLedger()
        service = self._service(decision, ledger)

        with self.assertRaises(SafetyReviewApplicationError) as mismatch:
            self._record(service)

        self.assertEqual(
            "safety_review.authority_decision_mismatch", mismatch.exception.code
        )
        self.assertEqual("safety.review_authority_invalid", ledger.records()[0].event_name)

    def test_authority_failure_is_audited_without_exception_message(self) -> None:
        ledger = AuditLedger()
        service = SafetyReviewApplicationService(
            FailingAuthority(self._decision()), ledger
        )

        with self.assertRaises(RuntimeError):
            self._record(service)

        audit_record = ledger.records()[0]
        self.assertEqual("safety.review_authority_failed", audit_record.event_name)
        self.assertEqual("RuntimeError", dict(audit_record.payload)["error_type"])
        self.assertNotIn("sensitive synthetic authority message", str(audit_record))

    def test_invalid_review_is_audited_without_rationale(self) -> None:
        ledger = AuditLedger()
        service = self._service(self._decision(), ledger)

        with self.assertRaises(SafetyError):
            self._record(service, rationale="sensitive invalid rationale", reviewed_at=(
                datetime.now(timezone.utc) + timedelta(minutes=1)
            ))

        audit_record = ledger.records()[0]
        self.assertEqual("safety.review_record_rejected", audit_record.event_name)
        self.assertNotIn("sensitive invalid rationale", str(audit_record))

    def test_audit_failure_prevents_returning_a_review(self) -> None:
        service = self._service(self._decision(), FailingAuditLedger())

        with self.assertRaises(AuditError) as failure:
            self._record(service)

        self.assertEqual("audit.synthetic_failure", failure.exception.code)

    def test_invalid_dependencies_are_rejected(self) -> None:
        with self.assertRaises(TypeError):
            SafetyReviewApplicationService(object(), AuditLedger())  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            SafetyReviewApplicationService(
                SyntheticAuthority(self._decision()), object()  # type: ignore[arg-type]
            )

    def _service(
        self, decision: SafetyReviewerAuthorityDecision, ledger: AuditLedger
    ) -> SafetyReviewApplicationService:
        return SafetyReviewApplicationService(SyntheticAuthority(decision), ledger)

    def _record(
        self,
        service: SafetyReviewApplicationService,
        *,
        rationale: str = "Synthetic structural review rationale.",
        reviewed_at: datetime | None = None,
    ):
        return service.record(
            self.assessment,
            reviewer_id="reviewer.synthetic",
            authority_reference="authority.synthetic-workflow",
            reviewed_at=reviewed_at or self.reviewed_at,
            disposition=SafetyReviewDisposition.VALIDATED_FOR_REASONING_REVIEW,
            rationale=rationale,
        )

    def _decision(
        self,
        status: SafetyReviewerAuthorityStatus = (
            SafetyReviewerAuthorityStatus.AUTHORIZED
        ),
    ) -> SafetyReviewerAuthorityDecision:
        return SafetyReviewerAuthorityDecision(
            reviewer_id="reviewer.synthetic",
            authority_reference="authority.synthetic-workflow",
            authority_provider="authority-provider.synthetic",
            action=SAFETY_REVIEW_ACTION,
            assessment_trace_id=self.assessment.trace_id,
            assessment_fingerprint=safety_assessment_fingerprint(self.assessment),
            status=status,
            decision_reference="decision.synthetic-review",
            verified_at=self.reviewed_at,
        )

    def _assert_sensitive_content_absent(self, record: object) -> None:
        serialized = str(record)
        self.assertNotIn("Sensitive synthetic clinical explanation.", serialized)
        self.assertNotIn("source.synthetic-review", serialized)


if __name__ == "__main__":
    unittest.main()
