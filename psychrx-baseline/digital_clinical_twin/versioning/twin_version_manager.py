"""Twin version manager."""

from __future__ import annotations

from digital_clinical_twin.models import TwinVersion


class TwinVersionManager:
    def create(self, major: int = 0, minor: int = 1, patch: int = 0, lineage: tuple[str, ...] = ()) -> TwinVersion:
        return TwinVersion(major=major, minor=minor, patch=patch, lineage=lineage)

