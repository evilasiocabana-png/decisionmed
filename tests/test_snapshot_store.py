from datetime import datetime, timedelta, timezone
from threading import Thread
import unittest

from decisionmed.domain import (
    ClinicalDataProvenance,
    ClinicalObservation,
    ClinicalSnapshot,
    ClinicalSnapshotSection,
    EntityId,
    SubjectReference,
)
from decisionmed.snapshots import ClinicalSnapshotStore, ClinicalSnapshotStoreError


class ClinicalSnapshotStoreTest(unittest.TestCase):
    def setUp(self) -> None:
        self.time = datetime.now(timezone.utc) - timedelta(minutes=1)
        self.subject = SubjectReference("sub-0123456789abcdef0123456789abcdef")

    def test_revisions_are_append_only_ordered_and_audited(self) -> None:
        store = ClinicalSnapshotStore()
        first = self._snapshot("snapshot-1", "lineage-1")
        second = self._snapshot(
            "snapshot-2",
            "lineage-1",
            previous="snapshot-1",
            captured_at=self.time + timedelta(seconds=1),
        )

        store.append(first)
        store.append(second)

        self.assertEqual((first, second), store.history(first.lineage_id))
        self.assertIs(second, store.latest(first.lineage_id))
        self.assertIs(first, store.get(first.snapshot_id))
        self.assertTrue(store.audit_integrity_valid)
        records = store.audit_records(first.lineage_id)
        self.assertEqual(2, len(records))
        self.assertEqual("clinical-snapshot.recorded", records[-1].event_name)
        self.assertEqual(
            {"snapshot_id", "specialty", "previous_snapshot_id"},
            {key for key, _ in records[-1].payload},
        )
        self.assertNotIn("value", {key for key, _ in records[-1].payload})

    def test_lineage_rejects_duplicate_stale_and_inconsistent_revisions(self) -> None:
        store = ClinicalSnapshotStore()
        first = self._snapshot("snapshot-1", "lineage-1")
        store.append(first)

        invalid = (
            first,
            self._snapshot("snapshot-2", "lineage-1"),
            self._snapshot("snapshot-3", "lineage-1", previous="not-latest"),
            self._snapshot(
                "snapshot-4",
                "lineage-1",
                previous="snapshot-1",
                subject=SubjectReference("sub-abcdef0123456789abcdef0123456789"),
            ),
            self._snapshot(
                "snapshot-5",
                "lineage-1",
                previous="snapshot-1",
                specialty="neurology",
            ),
            self._snapshot(
                "snapshot-6",
                "lineage-1",
                previous="snapshot-1",
                captured_at=self.time - timedelta(seconds=1),
            ),
        )
        for snapshot in invalid:
            with self.subTest(snapshot=snapshot.snapshot_id):
                with self.assertRaises(ClinicalSnapshotStoreError):
                    store.append(snapshot)

        self.assertEqual((first,), store.history(first.lineage_id))

    def test_capacity_is_bounded_and_unknown_ids_fail_closed(self) -> None:
        store = ClinicalSnapshotStore(max_snapshots=1)
        store.append(self._snapshot("snapshot-1", "lineage-1"))

        with self.assertRaises(ClinicalSnapshotStoreError):
            store.append(self._snapshot("snapshot-2", "lineage-2"))
        with self.assertRaises(ClinicalSnapshotStoreError):
            store.get(EntityId("unknown"))
        with self.assertRaises(ClinicalSnapshotStoreError):
            store.history(EntityId("unknown-lineage"))

    def test_concurrent_independent_lineages_remain_isolated(self) -> None:
        store = ClinicalSnapshotStore(max_snapshots=20)
        snapshots = tuple(
            self._snapshot(f"snapshot-{index}", f"lineage-{index}")
            for index in range(10)
        )
        threads = tuple(Thread(target=store.append, args=(item,)) for item in snapshots)

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertTrue(store.audit_integrity_valid)
        for snapshot in snapshots:
            self.assertEqual((snapshot,), store.history(snapshot.lineage_id))

    def _snapshot(
        self,
        snapshot_id: str,
        lineage_id: str,
        *,
        previous: str | None = None,
        captured_at: datetime | None = None,
        subject: SubjectReference | None = None,
        specialty: str = "cardiology",
    ) -> ClinicalSnapshot:
        observed_at = min(captured_at or self.time, self.time)
        return ClinicalSnapshot(
            snapshot_id=EntityId(snapshot_id),
            lineage_id=EntityId(lineage_id),
            previous_snapshot_id=EntityId(previous) if previous else None,
            subject_reference=subject or self.subject,
            session_id=EntityId(f"session-{snapshot_id}"),
            specialty_key=specialty,
            captured_at=captured_at or self.time,
            observations=(
                ClinicalObservation(
                    EntityId(f"observation-{snapshot_id}"),
                    ClinicalSnapshotSection.SYMPTOMS,
                    "symptoms.present",
                    False,
                    ClinicalDataProvenance.CLINICIAN_ENTERED,
                    observed_at,
                ),
            ),
        )


if __name__ == "__main__":
    unittest.main()
