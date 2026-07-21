"""In-memory Snapshot Index."""

from __future__ import annotations

from dataclasses import dataclass, field

from clinical_snapshot.models import ClinicalSnapshot


@dataclass
class SnapshotIndex:
    snapshots: list[ClinicalSnapshot] = field(default_factory=list)

    def add(self, snapshot: ClinicalSnapshot) -> None:
        self.snapshots.append(snapshot)

    def lookup(self, snapshot_id: str) -> ClinicalSnapshot | None:
        return next((item for item in self.snapshots if item.snapshot_id == snapshot_id), None)

    def latest(self) -> ClinicalSnapshot | None:
        return self.snapshots[-1] if self.snapshots else None

    def history(self) -> tuple[ClinicalSnapshot, ...]:
        return tuple(self.snapshots)

    def by_version(self, label: str) -> tuple[ClinicalSnapshot, ...]:
        return tuple(item for item in self.snapshots if item.version.label() == label)
