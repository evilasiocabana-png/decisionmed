import unittest

from application.app_service import PsychRxAppService
from clinical_runtime import ClinicalRuntime


class ScientificValidationIntegrationTest(unittest.TestCase):
    def test_scientific_validation_is_not_in_runtime_pipeline(self) -> None:
        result = ClinicalRuntime().execute()

        self.assertNotIn("scientific_validation", result)
        self.assertNotIn("Scientific Validation", result["result"]["outputs"])
        self.assertEqual(result["prescription"], "not_available")

    def test_app_view_model_exposes_scientific_validation_metadata_read_only(self) -> None:
        view_model = PsychRxAppService().get_app_view_model()

        self.assertEqual(view_model.scientific_validation_status.status, "available_read_only")
        self.assertFalse(view_model.scientific_validation_status.runtime_connected)
        self.assertEqual(view_model.scientific_validation_status.publication_outcome, "publish")
        self.assertEqual(view_model.scientific_validation_status.knowledge_version, "0.1.0")
        self.assertTrue(view_model.scientific_validation_status.read_only_mode)

    def test_workspace_contains_scientific_validation_widget_without_prescription(self) -> None:
        payload = str(PsychRxAppService().get_app_view_model().to_dict())

        self.assertIn("Scientific Validation Framework Status Widget", payload)
        self.assertIn("ScientificValidationResult", payload)
        self.assertIn("Runtime integration: forbidden", payload)
        self.assertNotIn("dose recomendada", payload.lower())
        self.assertNotIn("prescrever agora", payload.lower())


if __name__ == "__main__":
    unittest.main()

