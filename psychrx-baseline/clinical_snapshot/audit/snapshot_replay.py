"""Snapshot replay."""

from __future__ import annotations

from clinical_snapshot.models import ClinicalSnapshot


class SnapshotReplay:
    """Returns stored snapshot without recalculation."""

    def __init__(self, snapshot: ClinicalSnapshot) -> None:
        self._snapshot = snapshot

    def replay(self) -> ClinicalSnapshot:
        return self._snapshot
