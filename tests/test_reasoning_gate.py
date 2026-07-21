from datetime import datetime, timedelta, timezone
import unittest

from decisionmed.domain import (
    ClinicalDataProvenance,
    ClinicalObservation,
    ClinicalSnapshot,
    ClinicalSnapshotSection,
    EntityId,
    SubjectReference,
)
from decisionmed.reasoning import ReasoningError, ReasoningGate, ReasoningGateStatus
from decisionmed.safety import SafetyAssessment, SafetyGateStatus


class ReasoningGateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.now = datetime.now(timezone.utc) - timedelta(seconds=1)

    def test_incomplete_snapshot_blocks_before_safety_state(self) -> None:
        snapshot = self._snapshot(complete=False)
        result = ReasoningGate().assess(
            snapshot, self._safety(snapshot, SafetyGateStatus.BLOCKED)
        )

        self.assertEqual(ReasoningGateStatus.SNAPSHOT_INCOMPLETE, result.status)
        self.assertTrue(
            all(reason.startswith("missing_snapshot_section:") for reason in result.reasons)
        )
        self.assertFalse(result.reasoning_execution_allowed)
        self.assertFalse(result.clinical_execution_allowed)

    def test_safety_states_remain_explicit_and_fail_closed(self) -> None:
        expected = {
            SafetyGateStatus.INCOMPLETE: ReasoningGateStatus.SAFETY_INCOMPLETE,
            SafetyGateStatus.BLOCKED: ReasoningGateStatus.SAFETY_BLOCKED,
            SafetyGateStatus.HUMAN_REVIEW_REQUIRED: (
                ReasoningGateStatus.SAFETY_HUMAN_REVIEW_REQUIRED
            ),
        }
        snapshot = self._snapshot(complete=True)

        for safety_status, gate_status in expected.items():
            with self.subTest(safety_status=safety_status):
                result = ReasoningGate().assess(
                    snapshot, self._safety(snapshot, safety_status)
                )
                self.assertEqual(gate_status, result.status)
                self.assertFalse(result.reasoning_execution_allowed)

    def test_structurally_ready_safety_still_requires_human_validation(self) -> None:
        snapshot = self._snapshot(complete=True)
        result = ReasoningGate().assess(
            snapshot,
            self._safety(snapshot, SafetyGateStatus.READY_FOR_HUMAN_REVIEW),
        )

        self.assertEqual(
            ReasoningGateStatus.AWAITING_HUMAN_SAFETY_VALIDATION,
            result.status,
        )
        self.assertEqual(("human_safety_validation_required",), result.reasons)
        self.assertFalse(result.reasoning_execution_allowed)

    def test_trace_mismatch_is_rejected(self) -> None:
        snapshot = self._snapshot(complete=True)
        safety = self._safety(
            snapshot, SafetyGateStatus.READY_FOR_HUMAN_REVIEW, trace_id="trace.other"
        )

        with self.assertRaises(ReasoningError) as mismatch:
            ReasoningGate().assess(snapshot, safety)

        self.assertEqual("reasoning.trace_mismatch", mismatch.exception.code)

    def _snapshot(self, *, complete: bool) -> ClinicalSnapshot:
        sections = tuple(ClinicalSnapshotSection) if complete else ()
        return ClinicalSnapshot(
            snapshot_id=EntityId(f"snapshot-reasoning-{len(sections)}"),
            lineage_id=EntityId("lineage-reasoning"),
            subject_reference=SubjectReference(
                "sub-0123456789abcdef0123456789abcdef"
            ),
            session_id=EntityId("session-reasoning"),
            specialty_key="cardiology",
            captured_at=self.now,
            observations=tuple(
                ClinicalObservation(
                    observation_id=EntityId(f"observation-{section.value}"),
                    section=section,
                    field_key=f"{section.value}.synthetic",
                    value=False,
                    provenance=ClinicalDataProvenance.CLINICIAN_ENTERED,
                    observed_at=self.now,
                )
                for section in sections
            ),
            trace_id=f"trace.reasoning.{len(sections)}",
        )

    @staticmethod
    def _safety(
        snapshot: ClinicalSnapshot,
        status: SafetyGateStatus,
        *,
        trace_id: str | None = None,
    ) -> SafetyAssessment:
        ready = status is SafetyGateStatus.READY_FOR_HUMAN_REVIEW
        return SafetyAssessment(
            status=status,
            expected_check_ids=("check.synthetic-reasoning-gate",),
            results=(),
            missing_check_ids=("check.synthetic-reasoning-gate",)
            if status is SafetyGateStatus.INCOMPLETE
            else (),
            blocking_reasons=()
            if ready
            else ("synthetic_safety_gate_reason",),
            trace_id=trace_id or snapshot.trace_id,
        )


if __name__ == "__main__":
    unittest.main()
