"""Twin state manager."""

from __future__ import annotations

from digital_clinical_twin.models import DigitalClinicalTwin, TwinState, TwinTransition


class TwinStateManager:
    def update_state(self, twin: DigitalClinicalTwin, state: TwinState, category: str = "Context") -> DigitalClinicalTwin:
        transition = TwinTransition(category=category, source_state=twin.current_state.state_id, target_state=state.state_id)
        return twin.with_update(current_state=state, state_transitions=twin.state_transitions + (transition,))

