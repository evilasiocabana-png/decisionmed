"""Selection manager."""

from __future__ import annotations

from clinical_navigation.models import ClinicalNavigationState


class SelectionManager:
    """Maintains a single active selection with optional highlights."""

    def select(
        self,
        state: ClinicalNavigationState,
        widget: str,
        selected_id: str,
        highlights: tuple[str, ...] = (),
    ) -> ClinicalNavigationState:
        return state.with_update(
            active_widget=widget,
            selected_hypothesis=selected_id if widget == "Hypotheses" else state.selected_hypothesis,
            selected_evidence=selected_id if widget == "Evidence" else state.selected_evidence,
            selected_alert=selected_id if widget == "Safety" else state.selected_alert,
            selected_explanation=selected_id if widget == "Explanation" else state.selected_explanation,
            highlighted_references=highlights,
        )
