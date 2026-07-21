import unittest

from application.app_service import PsychRxAppService
from clinical_runtime import ClinicalRuntime


class ClinicalIntelligenceIntegrationTest(unittest.TestCase):
    def test_intelligence_is_not_in_runtime_pipeline(self) -> None:
        result = ClinicalRuntime().execute()

        self.assertNotIn("clinical_intelligence", result)
        self.assertNotIn("Clinical Intelligence", result["result"]["outputs"])
        self.assertEqual(result["prescription"], "not_available")

    def test_app_view_model_exposes_intelligence_read_only(self) -> None:
        view_model = PsychRxAppService().get_app_view_model()

        self.assertEqual(view_model.clinical_intelligence_status.status, "available_read_only")
        self.assertFalse(view_model.clinical_intelligence_status.runtime_connected)
        self.assertFalse(view_model.clinical_intelligence_status.autonomous_decision_allowed)
        self.assertEqual(view_model.clinical_intelligence_status.governance_outcome, "approved_read_only")
        self.assertTrue(view_model.clinical_intelligence_status.read_only_mode)

    def test_workspace_contains_intelligence_widget_without_prescription(self) -> None:
        payload = str(PsychRxAppService().get_app_view_model().to_dict())

        self.assertIn("Clinical Intelligence Platform Status Widget", payload)
        self.assertIn("ClinicalIntelligenceResult", payload)
        self.assertIn("AI implementation: none", payload)
        self.assertIn("Autonomous decision: forbidden", payload)
        self.assertNotIn("dose recomendada", payload.lower())
        self.assertNotIn("prescrever agora", payload.lower())


if __name__ == "__main__":
    unittest.main()

