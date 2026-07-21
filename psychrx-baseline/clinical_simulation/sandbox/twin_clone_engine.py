"""Twin clone engine."""

from __future__ import annotations

from digital_clinical_twin.models import DigitalClinicalTwin
from clinical_simulation.models import TwinClone


class TwinCloneEngine:
    def clone(self, twin: DigitalClinicalTwin) -> TwinClone:
        return TwinClone(
            source_twin_id=twin.twin_id,
            snapshot_refs=twin.snapshot_history,
            timeline_ref=twin.timeline_reference,
            knowledge_version=twin.knowledge_versions[-1] if twin.knowledge_versions else "",
            operating_mind_version=twin.current_state.operating_mind_reference,
            quality_refs=twin.quality_history,
            shared_mutable_state=False,
        )

