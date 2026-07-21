import unittest

from application.app_service import PsychRxAppService
from clinical_runtime import ClinicalRuntime


class SafetyEngineIntegrationTest(unittest.TestCase):
    def test_runtime_exposes_safety_result_before_downstream_steps(self) -> None:
        result = ClinicalRuntime().execute()

        self.assertEqual(result["safety_result"]["status"], "completed_read_only")
        self.assertEqual(result["safety_result"]["blocking_decision"]["status"], "allow")
        self.assertIn("Safety", result["result"]["outputs"])
        self.assertEqual(result["clinical_decision"], "not_implemented")
        self.assertEqual(result["prescription"], "not_available")

    def test_app_view_model_exposes_safety_engine_metadata(self) -> None:
        view_model = PsychRxAppService().get_app_view_model()

        self.assertEqual(view_model.safety_engine_status.engine_status, "completed_read_only")
        self.assertEqual(view_model.safety_engine_status.blocking_status, "allow")
        self.assertTrue(view_model.safety_engine_status.read_only_mode)

    def test_workspace_contains_safety_engine_widget_without_unlocking_strategy(self) -> None:
        payload = str(PsychRxAppService().get_app_view_model().to_dict())

        self.assertIn("Safety Engine Status Widget", payload)
        self.assertIn("SafetyResult", payload)
        self.assertIn("Strategy Widget", payload)
        self.assertIn("locked", payload)
        self.assertNotIn("dose recomendada", payload.lower())
        self.assertNotIn("prescrever agora", payload.lower())


if __name__ == "__main__":
    unittest.main()
