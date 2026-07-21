"""Version-aware snapshot cache."""

from __future__ import annotations

from dataclasses import dataclass, field

from clinical_snapshot.models import ClinicalSnapshot


@dataclass
class SnapshotCache:
    items: dict[str, ClinicalSnapshot] = field(default_factory=dict)

    def key(self, snapshot: ClinicalSnapshot) -> str:
        return f"{snapshot.snapshot_id}:{snapshot.version.label()}"

    def put(self, snapshot: ClinicalSnapshot) -> None:
        self.items[self.key(snapshot)] = snapshot

    def get(self, snapshot_id: str, version: str) -> ClinicalSnapshot | None:
        return self.items.get(f"{snapshot_id}:{version}")
