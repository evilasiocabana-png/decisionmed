"""Twin metadata factory."""

from __future__ import annotations

from digital_clinical_twin.models import TwinMetadata


class TwinMetadataFactory:
    def create(
        self,
        snapshot_count: int,
        timeline_version: str,
        knowledge_version: str,
        operating_mind_version: str,
    ) -> TwinMetadata:
        return TwinMetadata(
            snapshot_count=snapshot_count,
            timeline_version=timeline_version,
            knowledge_version=knowledge_version,
            operating_mind_version=operating_mind_version,
        )

