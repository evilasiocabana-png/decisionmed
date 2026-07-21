import unittest

from application.app_service import PsychRxAppService
from clinical_runtime import ClinicalRuntime


class ClinicalExplanationIntegrationTest(unittest.TestCase):
    def test_runtime_exposes_explanation_after_optimization(self) -> None:
        result = ClinicalRuntime().execute()

        self.assertEqual(result["explanation_result"]["status"], "completed_read_only")
        self.assertIn("Explanation", result["result"]["outputs"])
        self.assertEqual(result["clinical_decision"], "not_implemented")
        self.assertEqual(result["prescription"], "not_available")

    def test_app_view_model_exposes_explanation_metadata(self) -> None:
        view_model = PsychRxAppService().get_app_view_model()

        self.assertEqual(view_model.clinical_explanation_status.engine_status, "completed_read_only")
        self.assertTrue(view_model.clinical_explanation_status.read_only_mode)

    def test_workspace_contains_explanation_widget_without_prescription(self) -> None:
        payload = str(PsychRxAppService().get_app_view_model().to_dict())

        self.assertIn("Clinical Explanation Engine Status Widget", payload)
        self.assertIn("ClinicalExplanationResult", payload)
        self.assertNotIn("dose recomendada", payload.lower())
        self.assertNotIn("prescrever agora", payload.lower())


if __name__ == "__main__":
    unittest.main()
