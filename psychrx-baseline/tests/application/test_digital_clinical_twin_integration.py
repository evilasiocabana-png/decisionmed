import unittest

from application.app_service import PsychRxAppService
from clinical_runtime import ClinicalRuntime


class DigitalClinicalTwinIntegrationTest(unittest.TestCase):
    def test_digital_twin_is_not_in_runtime_pipeline(self) -> None:
        result = ClinicalRuntime().execute()

        self.assertNotIn("digital_clinical_twin", result)
        self.assertNotIn("Digital Clinical Twin", result["result"]["outputs"])
        self.assertEqual(result["prescription"], "not_available")

    def test_app_view_model_exposes_digital_twin_read_only(self) -> None:
        view_model = PsychRxAppService().get_app_view_model()

        self.assertEqual(view_model.digital_clinical_twin_status.status, "available_read_only")
        self.assertFalse(view_model.digital_clinical_twin_status.runtime_connected)
        self.assertEqual(view_model.digital_clinical_twin_status.snapshot_count, 1)
        self.assertEqual(view_model.digital_clinical_twin_status.version, "0.1.0")
        self.assertTrue(view_model.digital_clinical_twin_status.read_only_mode)

    def test_workspace_contains_twin_widget_without_prescription(self) -> None:
        payload = str(PsychRxAppService().get_app_view_model().to_dict())

        self.assertIn("Digital Clinical Twin Platform Status Widget", payload)
        self.assertIn("DigitalClinicalTwin", payload)
        self.assertIn("Runtime execution: forbidden", payload)
        self.assertIn("Patient reality: not represented", payload)
        self.assertNotIn("dose recomendada", payload.lower())
        self.assertNotIn("prescrever agora", payload.lower())


if __name__ == "__main__":
    unittest.main()

