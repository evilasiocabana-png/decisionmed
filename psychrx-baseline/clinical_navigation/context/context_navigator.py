"""Context navigator."""

from __future__ import annotations

from clinical_navigation.models import ClinicalNavigationState, NavigationContext


class ContextNavigator:
    """Maintains immutable active context."""

    def update_context(
        self,
        state: ClinicalNavigationState,
        context: NavigationContext,
    ) -> ClinicalNavigationState:
        return state.with_update(current_context=context)
