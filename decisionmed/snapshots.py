"""Append-only in-memory ClinicalSnapshot lineage service."""

from __future__ import annotations

from threading import RLock

from .audit import AuditLedger, AuditRecord
from .domain import ClinicalSnapshot, DomainEvent, EntityId


class ClinicalSnapshotStoreError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


class ClinicalSnapshotStore:
    """Preserve immutable revisions without persistent or clinical authority."""

    def __init__(
        self, audit: AuditLedger | None = None, max_snapshots: int = 1000
    ) -> None:
        if (
            not isinstance(max_snapshots, int)
            or isinstance(max_snapshots, bool)
            or max_snapshots < 1
        ):
            raise ValueError("max_snapshots must be a positive integer")
        self._audit = audit or AuditLedger()
        self._max_snapshots = max_snapshots
        self._snapshots: dict[EntityId, ClinicalSnapshot] = {}
        self._lineages: dict[EntityId, list[ClinicalSnapshot]] = {}
        self._lock = RLock()

    def append(self, snapshot: ClinicalSnapshot) -> None:
        if not isinstance(snapshot, ClinicalSnapshot):
            raise TypeError("snapshot must be a ClinicalSnapshot")
        with self._lock:
            if snapshot.snapshot_id in self._snapshots:
                self._fail("duplicate", "snapshot is already stored")
            if len(self._snapshots) >= self._max_snapshots:
                self._fail("capacity", "in-memory snapshot capacity reached")

            history = self._lineages.get(snapshot.lineage_id, [])
            if not history:
                if snapshot.previous_snapshot_id is not None:
                    self._fail("first_revision", "first revision cannot have a predecessor")
            else:
                latest = history[-1]
                if snapshot.previous_snapshot_id != latest.snapshot_id:
                    self._fail("predecessor", "revision must reference the latest snapshot")
                if snapshot.subject_reference != latest.subject_reference:
                    self._fail("subject", "lineage subject cannot change")
                if snapshot.specialty_key != latest.specialty_key:
                    self._fail("specialty", "lineage specialty cannot change")
                if snapshot.captured_at < latest.captured_at:
                    self._fail("chronology", "revision time cannot move backwards")

            self._snapshots[snapshot.snapshot_id] = snapshot
            self._lineages.setdefault(snapshot.lineage_id, []).append(snapshot)
            self._audit.append(
                DomainEvent(
                    "clinical-snapshot.recorded",
                    str(snapshot.lineage_id),
                    (
                        ("snapshot_id", str(snapshot.snapshot_id)),
                        ("specialty", snapshot.specialty_key),
                        (
                            "previous_snapshot_id",
                            str(snapshot.previous_snapshot_id)
                            if snapshot.previous_snapshot_id is not None
                            else "none",
                        ),
                    ),
                ),
                snapshot.trace_id,
            )

    def get(self, snapshot_id: EntityId) -> ClinicalSnapshot:
        if not isinstance(snapshot_id, EntityId):
            raise TypeError("snapshot_id must be an EntityId")
        with self._lock:
            snapshot = self._snapshots.get(snapshot_id)
            if snapshot is None:
                self._fail("unknown", "snapshot not found")
            return snapshot

    def history(self, lineage_id: EntityId) -> tuple[ClinicalSnapshot, ...]:
        if not isinstance(lineage_id, EntityId):
            raise TypeError("lineage_id must be an EntityId")
        with self._lock:
            history = self._lineages.get(lineage_id)
            if history is None:
                self._fail("unknown_lineage", "snapshot lineage not found")
            return tuple(history)

    def latest(self, lineage_id: EntityId) -> ClinicalSnapshot:
        return self.history(lineage_id)[-1]

    def audit_records(self, lineage_id: EntityId) -> tuple[AuditRecord, ...]:
        with self._lock:
            self.history(lineage_id)
            return tuple(
                record
                for record in self._audit.records()
                if record.aggregate_id == str(lineage_id)
            )

    @property
    def audit_integrity_valid(self) -> bool:
        with self._lock:
            return self._audit.verify()

    @staticmethod
    def _fail(code: str, message: str) -> None:
        raise ClinicalSnapshotStoreError(f"clinical_snapshot_store.{code}", message)
