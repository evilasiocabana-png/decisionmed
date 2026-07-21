from dataclasses import FrozenInstanceError, replace
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
    clinical_snapshot_fingerprint,
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

    def test_fingerprint_is_deterministic_and_covers_clinical_content(self) -> None:
        observation = self._observation(ClinicalSnapshotSection.SYMPTOMS)
        snapshot = self._snapshot(observations=(observation,))
        changed = self._snapshot(
            observations=(replace(observation, value=True),)
        )

        self.assertRegex(snapshot.content_fingerprint, r"^[0-9a-f]{64}$")
        self.assertEqual(
            clinical_snapshot_fingerprint(snapshot),
            snapshot.content_fingerprint,
        )
        self.assertNotEqual(
            snapshot.content_fingerprint,
            changed.content_fingerprint,
        )

    def test_fingerprint_normalizes_observation_order(self) -> None:
        first = self._observation(ClinicalSnapshotSection.SYMPTOMS, 1)
        second = self._observation(ClinicalSnapshotSection.FUNCTIONING, 2)

        ordered = self._snapshot(observations=(first, second))
        reversed_order = self._snapshot(observations=(second, first))

        self.assertEqual(
            ordered.content_fingerprint,
            reversed_order.content_fingerprint,
        )

    def test_fingerprint_preserves_primitive_value_types(self) -> None:
        observation = self._observation(ClinicalSnapshotSection.SYMPTOMS)
        boolean_snapshot = self._snapshot(
            observations=(replace(observation, value=True),)
        )
        integer_snapshot = self._snapshot(
            observations=(replace(observation, value=1),)
        )

        self.assertNotEqual(
            boolean_snapshot.content_fingerprint,
            integer_snapshot.content_fingerprint,
        )

    def test_fingerprint_normalizes_equivalent_timezone_offsets(self) -> None:
        observation = self._observation(ClinicalSnapshotSection.SYMPTOMS)
        snapshot = self._snapshot(observations=(observation,))
        offset = timezone(timedelta(hours=-3))
        equivalent = replace(
            snapshot,
            captured_at=snapshot.captured_at.astimezone(offset),
            observations=(
                replace(
                    observation,
                    observed_at=observation.observed_at.astimezone(offset),
                ),
            ),
        )

        self.assertEqual(
            snapshot.content_fingerprint,
            equivalent.content_fingerprint,
        )

    def test_fingerprint_rejects_non_snapshot_values(self) -> None:
        with self.assertRaises(TypeError):
            clinical_snapshot_fingerprint(object())  # type: ignore[arg-type]

    def _snapshot(
        self, observations: tuple[ClinicalObservation, ...]
    ) -> ClinicalSnapshot:
        return ClinicalSnapshot(
            snapshot_id=EntityId("snapshot-1"),
            lineage_id=EntityId("lineage-1"),
            subject_reference=SubjectReference("sub-0123456789abcdef0123456789abcdef"),
            session_id=EntityId("session-1"),
            specialty_key="cardiology",
            captured_at=self.now,
            observations=observations,
            trace_id="trace.snapshot-1",
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
