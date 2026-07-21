"""Runtime adapter for Clinical Navigation Engine."""

from __future__ import annotations

from clinical_navigation.coordinator import NavigationCoordinator
from clinical_navigation.models import ClinicalNavigationState, NavigationRoute


class RuntimeNavigationAdapter:
    def __init__(self, coordinator: NavigationCoordinator | None = None) -> None:
        self._coordinator = coordinator or NavigationCoordinator()

    def build_state(self) -> ClinicalNavigationState:
        return self._coordinator.navigate(
            ClinicalNavigationState(),
            NavigationRoute("Workspace", "Timeline"),
        )
