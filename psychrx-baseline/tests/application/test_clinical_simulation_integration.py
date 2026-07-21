import unittest

from application.app_service import PsychRxAppService
from clinical_runtime import ClinicalRuntime


class ClinicalSimulationIntegrationTest(unittest.TestCase):
    def test_simulation_is_not_in_runtime_pipeline(self) -> None:
        result = ClinicalRuntime().execute()

        self.assertNotIn("clinical_simulation", result)
        self.assertNotIn("Clinical Simulation", result["result"]["outputs"])
        self.assertEqual(result["prescription"], "not_available")

    def test_app_view_model_exposes_simulation_read_only(self) -> None:
        view_model = PsychRxAppService().get_app_view_model()

        self.assertEqual(view_model.clinical_simulation_status.status, "available_read_only")
        self.assertFalse(view_model.clinical_simulation_status.runtime_connected)
        self.assertFalse(view_model.clinical_simulation_status.production_mutation_allowed)
        self.assertEqual(view_model.clinical_simulation_status.outcome_status, "completed")
        self.assertTrue(view_model.clinical_simulation_status.read_only_mode)

    def test_workspace_contains_simulation_widget_without_prescription(self) -> None:
        payload = str(PsychRxAppService().get_app_view_model().to_dict())

        self.assertIn("Clinical Simulation Platform Status Widget", payload)
        self.assertIn("ClinicalSimulationResult", payload)
        self.assertIn("Runtime mutation: forbidden", payload)
        self.assertIn("Official Twin mutation: forbidden", payload)
        self.assertNotIn("dose recomendada", payload.lower())
        self.assertNotIn("prescrever agora", payload.lower())


if __name__ == "__main__":
    unittest.main()

