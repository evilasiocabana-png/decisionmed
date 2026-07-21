import unittest
from pathlib import Path

from clinical_navigation import NavigationCoordinator
from clinical_navigation.api import WorkspaceNavigationAPI
from clinical_navigation.audit import NavigationAudit, NavigationAuditEntry, NavigationTrace
from clinical_navigation.context import ContextNavigator, NavigationStateValidator
from clinical_navigation.deeplinks import CrossNavigation, DeepLinkResolver
from clinical_navigation.events import navigation_event_types
from clinical_navigation.history import NavigationReplay
from clinical_navigation.models import ClinicalNavigationState, NavigationContext, NavigationRoute
from clinical_navigation.routing import ReferenceResolver, RouteResolver
from clinical_navigation.widgets import SelectionManager, WidgetSynchronizer


class ClinicalNavigationStructureTest(unittest.TestCase):
    def test_package_structure_exists(self) -> None:
        for dirname in ["coordinator", "context", "routing", "breadcrumbs", "history", "deeplinks", "widgets", "audit", "models", "api", "events", "integration"]:
            with self.subTest(dirname=dirname):
                self.assertTrue((Path("clinical_navigation") / dirname).is_dir())

    def test_coordinator_maintains_immutable_navigation_state(self) -> None:
        original = ClinicalNavigationState()
        route = NavigationRoute("Workspace", "Snapshot", "SNP-1")
        updated = NavigationCoordinator().navigate(original, route)

        self.assertNotEqual(original.navigation_id, "")
        self.assertEqual(original.active_widget, "")
        self.assertEqual(updated.active_widget, "Snapshot")
        self.assertEqual(updated.history.current().artifact_id, "SNP-1")

    def test_context_routing_history_deeplink_selection_and_api_are_structural(self) -> None:
        state = ClinicalNavigationState()
        route = RouteResolver().resolve("Workspace", "Evidence", "EVD-1")
        state = WorkspaceNavigationAPI().navigate(state, route)
        state = ContextNavigator().update_context(state, NavigationContext(snapshot_context="SNP-1"))
        state = SelectionManager().select(state, "Evidence", "EVD-1", ("CIT-1",))

        self.assertTrue(NavigationStateValidator().validate(state).valid)
        self.assertEqual(ReferenceResolver().resolve("Snapshot", "SNP-1").artifact_id, "SNP-1")
        self.assertEqual(DeepLinkResolver().resolve("Evidence", "EVD-1").route.valid, True)
        self.assertIn("Runtime Trace", CrossNavigation().path())
        self.assertIn("Explanation", WidgetSynchronizer().related_widgets("Evidence"))
        self.assertIn("SnapshotSelected", navigation_event_types())
        self.assertEqual(NavigationReplay(state.history).replay(), state.history)

    def test_audit_trace_and_guardrails_are_structural(self) -> None:
        audit = NavigationAudit()
        audit.record(NavigationAuditEntry(event="SnapshotSelected"))
        trace = NavigationTrace(snapshot_id="SNP-1", timeline_id="TML-1")
        payload = str(NavigationCoordinator().navigate().to_dict()).lower()

        self.assertEqual(audit.snapshot()[0].event, "SnapshotSelected")
        self.assertTrue(trace.trace_id.startswith("NAV-TRACE-"))
        self.assertNotIn("dose recomendada", payload)
        self.assertNotIn("prescrever", payload)
        self.assertNotIn("diagnostico definitivo", payload)


if __name__ == "__main__":
    unittest.main()
