from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timedelta, timezone
import unittest

from decisionmed.application import (
    SAFETY_REVIEW_ACTION,
    SafetyReviewerAuthority,
    SafetyReviewerAuthorityDecision,
    SafetyReviewerAuthorityStatus,
)


class SyntheticReviewerAuthority:
    provider = "authority-provider.synthetic"

    def __init__(self, decision: SafetyReviewerAuthorityDecision) -> None:
        self._decision = decision

    def verify(
        self,
        *,
        reviewer_id: str,
        authority_reference: str,
        assessment_trace_id: str,
        assessment_fingerprint: str,
    ) -> SafetyReviewerAuthorityDecision:
        return self._decision


class SafetyReviewerAuthorityDecisionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.verified_at = datetime.now(timezone.utc) - timedelta(seconds=1)
        self.fingerprint = "a" * 64

    def test_authorized_decision_is_immutable_and_request_bound(self) -> None:
        decision = self._decision(SafetyReviewerAuthorityStatus.AUTHORIZED)

        self.assertTrue(
            decision.matches_request(
                reviewer_id="reviewer.synthetic",
                authority_reference="authority.synthetic-workflow",
                assessment_trace_id="trace.synthetic-review",
                assessment_fingerprint=self.fingerprint,
            )
        )
        self.assertTrue(decision.review_recording_allowed)
        self.assertFalse(decision.reasoning_execution_allowed)
        self.assertFalse(decision.clinical_execution_allowed)
        with self.assertRaises(FrozenInstanceError):
            decision.status = SafetyReviewerAuthorityStatus.DENIED  # type: ignore[misc]

    def test_denied_decision_remains_fail_closed(self) -> None:
        decision = self._decision(SafetyReviewerAuthorityStatus.DENIED)

        self.assertFalse(decision.review_recording_allowed)
        self.assertFalse(decision.reasoning_execution_allowed)
        self.assertFalse(decision.clinical_execution_allowed)

    def test_changed_request_no_longer_matches_decision(self) -> None:
        decision = self._decision(SafetyReviewerAuthorityStatus.AUTHORIZED)

        self.assertFalse(
            decision.matches_request(
                reviewer_id="reviewer.other",
                authority_reference="authority.synthetic-workflow",
                assessment_trace_id="trace.synthetic-review",
                assessment_fingerprint=self.fingerprint,
            )
        )
        self.assertFalse(
            replace(decision, assessment_fingerprint="b" * 64).matches_request(
                reviewer_id="reviewer.synthetic",
                authority_reference="authority.synthetic-workflow",
                assessment_trace_id="trace.synthetic-review",
                assessment_fingerprint=self.fingerprint,
            )
        )

    def test_contract_rejects_invalid_metadata_and_time(self) -> None:
        for replacement_values in (
            {"reviewer_id": "Invalid Reviewer"},
            {"authority_reference": "Invalid Authority"},
            {"authority_provider": "Invalid Provider"},
            {"action": "other.action"},
            {"assessment_trace_id": ""},
            {"assessment_fingerprint": "not-a-fingerprint"},
            {"decision_reference": "Invalid Decision"},
            {"verified_at": datetime.now(timezone.utc) + timedelta(minutes=1)},
        ):
            with self.subTest(replacement_values=replacement_values):
                values = self._values(
                    SafetyReviewerAuthorityStatus.AUTHORIZED
                ) | replacement_values
                with self.assertRaises((TypeError, ValueError)):
                    SafetyReviewerAuthorityDecision(**values)

    def test_protocol_accepts_only_the_required_runtime_shape(self) -> None:
        adapter = SyntheticReviewerAuthority(
            self._decision(SafetyReviewerAuthorityStatus.AUTHORIZED)
        )

        self.assertIsInstance(adapter, SafetyReviewerAuthority)
        self.assertNotIsInstance(object(), SafetyReviewerAuthority)
        with self.assertRaises(TypeError):
            SafetyReviewerAuthority()  # type: ignore[misc]

    def _decision(
        self, status: SafetyReviewerAuthorityStatus
    ) -> SafetyReviewerAuthorityDecision:
        return SafetyReviewerAuthorityDecision(**self._values(status))

    def _values(
        self, status: SafetyReviewerAuthorityStatus
    ) -> dict[str, object]:
        return {
            "reviewer_id": "reviewer.synthetic",
            "authority_reference": "authority.synthetic-workflow",
            "authority_provider": "authority-provider.synthetic",
            "action": SAFETY_REVIEW_ACTION,
            "assessment_trace_id": "trace.synthetic-review",
            "assessment_fingerprint": self.fingerprint,
            "status": status,
            "decision_reference": "decision.synthetic-review",
            "verified_at": self.verified_at,
        }


if __name__ == "__main__":
    unittest.main()
