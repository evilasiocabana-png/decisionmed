from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone
import math
import unittest

from decisionmed.domain import (
    REQUIRED_SNAPSHOT_SECTIONS,
    ClinicalDataProvenance,
    ClinicalObservation,
    ClinicalSnapshot,
    ClinicalSnapshotSection,
    ClinicalSnapshotStatus,
    DomainInvariantError,
    EntityId,
    SubjectReference,
)


class ClinicalSnapshotContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.now = datetime.now(timezone.utc) - timedelta(seconds=1)

    def test_incomplete_snapshot_declares_every_missing_section(self) -> None:
        snapshot = self._snapshot(
            observations=(self._observation(ClinicalSnapshotSection.SYMPTOMS),)
        )

        self.assertEqual(ClinicalSnapshotStatus.INCOMPLETE, snapshot.status)
        self.assertNotIn(ClinicalSnapshotSection.SYMPTOMS, snapshot.missing_sections)
        self.assertEqual(
            REQUIRED_SNAPSHOT_SECTIONS - {ClinicalSnapshotSection.SYMPTOMS},
            set(snapshot.missing_sections),
        )
        self.assertFalse(snapshot.clinical_execution_allowed)

    def test_complete_structure_still_waits_for_human_validation(self) -> None:
        observations = tuple(
            self._observation(section, index)
            for index, section in enumerate(ClinicalSnapshotSection)
        )

        snapshot = self._snapshot(observations=observations)

        self.assertTrue(snapshot.structurally_complete)
        self.assertEqual((), snapshot.missing_sections)
        self.assertEqual(
            ClinicalSnapshotStatus.AWAITING_HUMAN_VALIDATION, snapshot.status
        )
        self.assertFalse(snapshot.clinical_execution_allowed)

    def test_snapshot_and_observations_are_immutable(self) -> None:
        observation = self._observation(ClinicalSnapshotSection.SYMPTOMS)
        snapshot = self._snapshot(observations=(observation,))

        with self.assertRaises(FrozenInstanceError):
            snapshot.version = "1.0.0"  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            observation.value = "changed"  # type: ignore[misc]

    def test_duplicate_observations_and_future_times_are_rejected(self) -> None:
        observation = self._observation(ClinicalSnapshotSection.SYMPTOMS)
        with self.assertRaises(DomainInvariantError):
            self._snapshot(observations=(observation, observation))
        with self.assertRaises(DomainInvariantError):
            self._snapshot(
                observations=(
                    ClinicalObservation(
                        EntityId("future"),
                        ClinicalSnapshotSection.SYMPTOMS,
                        "symptom_presence",
                        True,
                        ClinicalDataProvenance.CLINICIAN_ENTERED,
                        datetime.now(timezone.utc) + timedelta(minutes=1),
                    ),
                )
            )

    def test_values_are_bounded_finite_primitives(self) -> None:
        for invalid_value in ("", "x" * 2001, math.inf, math.nan, {"unsafe": True}):
            with self.subTest(value=invalid_value):
                with self.assertRaises(DomainInvariantError):
                    ClinicalObservation(
                        EntityId("invalid"),
                        ClinicalSnapshotSection.SYMPTOMS,
                        "symptom_presence",
                        invalid_value,  # type: ignore[arg-type]
                        ClinicalDataProvenance.UNKNOWN,
                        self.now,
                    )

    def test_subject_reference_rejects_direct_identifiers(self) -> None:
        self.assertRegex(str(SubjectReference()), r"^sub-[0-9a-f]{32}$")
        for direct_identifier in ("Maria Silva", "12345678900", "maria@example.com"):
            with self.subTest(value=direct_identifier):
                with self.assertRaises(DomainInvariantError):
                    SubjectReference(direct_identifier)

    def _snapshot(
        self, observations: tuple[ClinicalObservation, ...]
    ) -> ClinicalSnapshot:
        return ClinicalSnapshot(
            snapshot_id=EntityId("snapshot-1"),
            subject_reference=SubjectReference("sub-0123456789abcdef0123456789abcdef"),
            session_id=EntityId("session-1"),
            specialty_key="cardiology",
            captured_at=self.now,
            observations=observations,
        )

    def _observation(
        self, section: ClinicalSnapshotSection, index: int = 0
    ) -> ClinicalObservation:
        return ClinicalObservation(
            observation_id=EntityId(f"observation-{section.value}-{index}"),
            section=section,
            field_key=f"{section.value}.presence",
            value=False,
            provenance=ClinicalDataProvenance.CLINICIAN_ENTERED,
            observed_at=self.now,
        )


if __name__ == "__main__":
    unittest.main()
