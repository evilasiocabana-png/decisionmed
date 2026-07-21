"""Twin builder."""

from __future__ import annotations

from digital_clinical_twin.builder.twin_metadata import TwinMetadataFactory
from digital_clinical_twin.models import DigitalClinicalTwin, TwinState, TwinTransition


class TwinBuilder:
    """Builds a Twin from immutable computational references."""

    def build(
        self,
        timeline_reference: str = "timeline-structural",
        snapshot_ids: tuple[str, ...] = ("snapshot-structural",),
        quality_ids: tuple[str, ...] = ("quality-structural",),
        operating_mind_reference: str = "operating-mind-structural",
        knowledge_versions: tuple[str, ...] = ("0.1.0",),
    ) -> DigitalClinicalTwin:
        current_snapshot = snapshot_ids[-1] if snapshot_ids else ""
        state = TwinState(
            snapshot_reference=current_snapshot,
            quality_reference=quality_ids[-1] if quality_ids else "",
            operating_mind_reference=operating_mind_reference,
        )
        transition = TwinTransition(
            category="Timeline",
            source_state=snapshot_ids[0] if snapshot_ids else "",
            target_state=current_snapshot,
        )
        metadata = TwinMetadataFactory().create(
            snapshot_count=len(snapshot_ids),
            timeline_version="0.1.0",
            knowledge_version=knowledge_versions[-1] if knowledge_versions else "",
            operating_mind_version=operating_mind_reference,
        )
        return DigitalClinicalTwin(
            timeline_reference=timeline_reference,
            snapshot_history=snapshot_ids,
            current_state=state,
            state_transitions=(transition,),
            quality_history=quality_ids,
            knowledge_versions=knowledge_versions,
            metadata=metadata,
        )

