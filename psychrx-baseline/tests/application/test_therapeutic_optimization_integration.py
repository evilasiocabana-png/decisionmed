import unittest

from application.app_service import PsychRxAppService
from clinical_runtime import ClinicalRuntime


class TherapeuticOptimizationIntegrationTest(unittest.TestCase):
    def test_runtime_exposes_optimization_result_after_evidence(self) -> None:
        result = ClinicalRuntime().execute()

        self.assertEqual(result["optimization_result"]["status"], "completed_read_only")
        self.assertIn("Safety", result["result"]["outputs"])
        self.assertIn("Evidence", result["result"]["outputs"])
        self.assertIn("Optimization", result["result"]["outputs"])
        self.assertEqual(result["clinical_decision"], "not_implemented")
        self.assertEqual(result["prescription"], "not_available")

    def test_app_view_model_exposes_optimization_metadata(self) -> None:
        view_model = PsychRxAppService().get_app_view_model()

        self.assertEqual(
            view_model.therapeutic_optimization_status.engine_status,
            "completed_read_only",
        )
        self.assertTrue(view_model.therapeutic_optimization_status.read_only_mode)

    def test_workspace_contains_optimization_widget_without_prescription(self) -> None:
        payload = str(PsychRxAppService().get_app_view_model().to_dict())

        self.assertIn("Therapeutic Optimization Status Widget", payload)
        self.assertIn("TherapeuticOptimizationResult", payload)
        self.assertIn("Strategy Widget", payload)
        self.assertNotIn("dose recomendada", payload.lower())
        self.assertNotIn("prescrever agora", payload.lower())


if __name__ == "__main__":
    unittest.main()
