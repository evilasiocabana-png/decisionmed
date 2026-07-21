"""Internal navigation API for workspace consumers."""

from __future__ import annotations

from clinical_navigation.coordinator import NavigationCoordinator
from clinical_navigation.models import ClinicalNavigationState, NavigationRoute


class WorkspaceNavigationAPI:
    def __init__(self, coordinator: NavigationCoordinator | None = None) -> None:
        self._coordinator = coordinator or NavigationCoordinator()

    def navigate(self, state: ClinicalNavigationState, route: NavigationRoute) -> ClinicalNavigationState:
        return self._coordinator.navigate(state, route)

    def goBack(self, state: ClinicalNavigationState) -> ClinicalNavigationState:
        return state.with_update(history=state.history.back())

    def goForward(self, state: ClinicalNavigationState) -> ClinicalNavigationState:
        return state.with_update(history=state.history.forward())

    def jump(self, state: ClinicalNavigationState, cursor: int) -> ClinicalNavigationState:
        from clinical_navigation.history import NavigationHistoryManager

        return state.with_update(history=NavigationHistoryManager().jump(state.history, cursor))

    def restore(self, entries: tuple[NavigationRoute, ...]) -> ClinicalNavigationState:
        from clinical_navigation.history import NavigationHistoryManager

        return ClinicalNavigationState(history=NavigationHistoryManager().restore(entries))

    def resolve(self, source: str, target: str, artifact_id: str = "") -> NavigationRoute:
        from clinical_navigation.routing import RouteResolver

        return RouteResolver().resolve(source, target, artifact_id)
