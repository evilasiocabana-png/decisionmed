import unittest

from application.app_service import PsychRxAppService
from clinical_runtime import ClinicalRuntime


class ClinicalNavigationIntegrationTest(unittest.TestCase):
    def test_runtime_exposes_navigation_state_after_timeline(self) -> None:
        result = ClinicalRuntime().execute()

        self.assertIn("clinical_navigation", result)
        self.assertEqual(result["clinical_navigation"]["active_widget"], "Timeline")
        self.assertIn("Navigation", result["result"]["outputs"])
        self.assertEqual(result["prescription"], "not_available")

    def test_app_view_model_exposes_navigation_metadata(self) -> None:
        view_model = PsychRxAppService().get_app_view_model()

        self.assertEqual(view_model.clinical_navigation_status.status, "available_read_only")
        self.assertTrue(view_model.clinical_navigation_status.read_only_mode)

    def test_workspace_contains_navigation_widget_without_prescription(self) -> None:
        payload = str(PsychRxAppService().get_app_view_model().to_dict())

        self.assertIn("Clinical Navigation Engine Status Widget", payload)
        self.assertIn("ClinicalNavigationState", payload)
        self.assertNotIn("dose recomendada", payload.lower())
        self.assertNotIn("prescrever agora", payload.lower())


if __name__ == "__main__":
    unittest.main()
