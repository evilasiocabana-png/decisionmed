from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timedelta, timezone
import unittest

from decisionmed.safety import (
    SafetyAssessment,
    SafetyCheckOutcome,
    SafetyCheckResult,
    SafetyError,
    SafetyGateStatus,
    SafetyReviewDisposition,
    SafetyReviewRecord,
    safety_assessment_fingerprint,
)


class SafetyReviewRecordTest(unittest.TestCase):
    def setUp(self) -> None:
        self.assessment = self._assessment()
        self.reviewed_at = datetime.now(timezone.utc) - timedelta(seconds=1)

    def test_attestation_is_immutable_and_bound_to_exact_assessment(self) -> None:
        record = self._record(self.assessment)

        self.assertTrue(record.matches(self.assessment))
        self.assertRegex(record.assessment_fingerprint, r"^[0-9a-f]{64}$")
        self.assertEqual(
            safety_assessment_fingerprint(self.assessment),
            record.assessment_fingerprint,
        )
        self.assertFalse(record.reasoning_execution_allowed)
        self.assertFalse(record.clinical_execution_allowed)
        with self.assertRaises(FrozenInstanceError):
            record.rationale = "changed"  # type: ignore[misc]

    def test_changed_result_no_longer_matches_attestation(self) -> None:
        record = self._record(self.assessment)
        changed_result = replace(
            self.assessment.results[0], explanation="Changed synthetic explanation."
        )
        changed = replace(self.assessment, results=(changed_result,))

        self.assertFalse(record.matches(changed))
        self.assertNotEqual(
            record.assessment_fingerprint,
            safety_assessment_fingerprint(changed),
        )

    def test_validation_disposition_cannot_override_non_ready_assessment(self) -> None:
        incomplete = SafetyAssessment(
            status=SafetyGateStatus.INCOMPLETE,
            expected_check_ids=("check.synthetic-review",),
            results=(),
            missing_check_ids=("check.synthetic-review",),
            blocking_reasons=("missing_check:check.synthetic-review",),
            trace_id="trace.synthetic-review",
        )

        with self.assertRaises(SafetyError) as invalid:
            self._record(incomplete)

        self.assertEqual("safety_review.disposition", invalid.exception.code)

    def test_reassessment_disposition_can_record_a_fail_closed_state(self) -> None:
        blocked = SafetyAssessment(
            status=SafetyGateStatus.BLOCKED,
            expected_check_ids=("check.synthetic-review",),
            results=(),
            missing_check_ids=(),
            blocking_reasons=("critical_finding:finding.synthetic",),
            trace_id="trace.synthetic-review",
        )
        record = self._record(
            blocked,
            disposition=SafetyReviewDisposition.REASSESSMENT_REQUIRED,
        )

        self.assertTrue(record.matches(blocked))
        self.assertFalse(record.reasoning_execution_allowed)

    def test_identity_time_and_rationale_are_validated(self) -> None:
        for replacement_values in (
            {"reviewer_id": "Invalid Reviewer"},
            {"authority_reference": "Invalid Authority"},
            {"reviewed_at": datetime.now(timezone.utc) + timedelta(minutes=1)},
            {"rationale": ""},
            {"rationale": "x" * 4001},
        ):
            with self.subTest(replacement_values=replacement_values):
                values = {
                    "reviewer_id": "reviewer.synthetic",
                    "authority_reference": "authority.synthetic-workflow",
                    "reviewed_at": self.reviewed_at,
                    "disposition": (
                        SafetyReviewDisposition.VALIDATED_FOR_REASONING_REVIEW
                    ),
                    "rationale": "Synthetic structural review rationale.",
                    **replacement_values,
                }
                with self.assertRaises((SafetyError, TypeError)):
                    SafetyReviewRecord.create(self.assessment, **values)

    def test_record_does_not_copy_assessment_explanations_or_evidence(self) -> None:
        record = self._record(self.assessment)
        serialized = str(record)

        self.assertNotIn("Synthetic evaluated safety result.", serialized)
        self.assertNotIn("source.synthetic-review", serialized)

    def _record(
        self,
        assessment: SafetyAssessment,
        *,
        disposition: SafetyReviewDisposition = (
            SafetyReviewDisposition.VALIDATED_FOR_REASONING_REVIEW
        ),
    ) -> SafetyReviewRecord:
        return SafetyReviewRecord.create(
            assessment,
            reviewer_id="reviewer.synthetic",
            authority_reference="authority.synthetic-workflow",
            reviewed_at=self.reviewed_at,
            disposition=disposition,
            rationale="Synthetic structural review rationale.",
        )

    @staticmethod
    def _assessment() -> SafetyAssessment:
        return SafetyAssessment(
            status=SafetyGateStatus.READY_FOR_HUMAN_REVIEW,
            expected_check_ids=("check.synthetic-review",),
            results=(
                SafetyCheckResult(
                    check_id="check.synthetic-review",
                    outcome=SafetyCheckOutcome.PASSED,
                    trace_id="trace.synthetic-review",
                    explanation="Synthetic evaluated safety result.",
                    evidence_source_ids=("source.synthetic-review",),
                ),
            ),
            missing_check_ids=(),
            blocking_reasons=(),
            trace_id="trace.synthetic-review",
        )


if __name__ == "__main__":
    unittest.main()
