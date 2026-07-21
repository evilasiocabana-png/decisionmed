import unittest

from application.app_service import PsychRxAppService
from clinical_runtime import ClinicalRuntime


class ClinicalOperatingMindIntegrationTest(unittest.TestCase):
    def test_runtime_exposes_operating_mind_after_navigation(self) -> None:
        result = ClinicalRuntime().execute()

        self.assertIn("clinical_operating_mind", result)
        self.assertEqual(result["clinical_operating_mind"]["state"]["status"], "navigation_ready")
        self.assertIn("Operating Mind", result["result"]["outputs"])
        self.assertEqual(result["clinical_decision"], "not_implemented")
        self.assertEqual(result["prescription"], "not_available")

    def test_app_view_model_exposes_operating_mind_metadata(self) -> None:
        view_model = PsychRxAppService().get_app_view_model()

        self.assertEqual(view_model.clinical_operating_mind_status.status, "navigation_ready")
        self.assertEqual(view_model.clinical_operating_mind_status.completed_phase_count, 8)
        self.assertEqual(view_model.clinical_operating_mind_status.contract_count, 8)
        self.assertTrue(view_model.clinical_operating_mind_status.trace_complete)
        self.assertTrue(view_model.clinical_operating_mind_status.read_only_mode)

    def test_workspace_contains_operating_mind_widget_without_prescription(self) -> None:
        payload = str(PsychRxAppService().get_app_view_model().to_dict())

        self.assertIn("Clinical Operating Mind Status Widget", payload)
        self.assertIn("ClinicalOperatingMind", payload)
        self.assertIn("Safety before Optimization", payload)
        self.assertNotIn("dose recomendada", payload.lower())
        self.assertNotIn("prescrever agora", payload.lower())


if __name__ == "__main__":
    unittest.main()

