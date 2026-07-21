"""Clinical Navigation coordinator."""

from __future__ import annotations

from clinical_navigation.audit import NavigationAudit, NavigationAuditEntry
from clinical_navigation.breadcrumbs import BreadcrumbEngine
from clinical_navigation.history import NavigationHistoryManager
from clinical_navigation.models import ClinicalNavigationState, NavigationRoute


class NavigationCoordinator:
    """Coordinates navigation events without rendering UI or executing engines."""

    def __init__(self) -> None:
        self.history_manager = NavigationHistoryManager()
        self.breadcrumb_engine = BreadcrumbEngine()
        self.audit = NavigationAudit()

    def navigate(
        self,
        state: ClinicalNavigationState | None = None,
        route: NavigationRoute | None = None,
    ) -> ClinicalNavigationState:
        active_state = state or ClinicalNavigationState()
        active_route = route or NavigationRoute("Workspace", "Workspace")
        history = self.history_manager.push(active_state.history, active_route)
        breadcrumbs = self.breadcrumb_engine.build(history.entries)
        new_state = active_state.with_update(
            active_widget=active_route.target,
            history=history,
            breadcrumbs=breadcrumbs,
        )
        self.audit.record(
            NavigationAuditEntry(
                event="NavigationRouteChanged",
                route=f"{active_route.source}->{active_route.target}",
                trace_id=new_state.trace_id,
            )
        )
        return new_state
