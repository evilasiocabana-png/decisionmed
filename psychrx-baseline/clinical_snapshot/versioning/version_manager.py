"""Snapshot version manager."""

from __future__ import annotations

from clinical_snapshot.models import SnapshotVersion


class SnapshotVersionManager:
    """Creates immutable version values."""

    def next_patch(self, version: SnapshotVersion) -> SnapshotVersion:
        return SnapshotVersion(version.major, version.minor, version.patch + 1, version.lineage_id)

    def next_minor(self, version: SnapshotVersion) -> SnapshotVersion:
        return SnapshotVersion(version.major, version.minor + 1, 0, version.lineage_id)

    def next_major(self, version: SnapshotVersion) -> SnapshotVersion:
        return SnapshotVersion(version.major + 1, 0, 0, version.lineage_id)
