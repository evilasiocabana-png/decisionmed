import unittest

from application.app_service import PsychRxAppService
from clinical_runtime import ClinicalRuntime


class ClinicalQualityIntegrationTest(unittest.TestCase):
    def test_runtime_exposes_quality_after_operating_mind(self) -> None:
        result = ClinicalRuntime().execute()

        self.assertIn("clinical_quality", result)
        self.assertEqual(result["clinical_quality"]["status"], "valid")
        self.assertIn("Quality", result["result"]["outputs"])
        self.assertEqual(result["clinical_decision"], "not_implemented")
        self.assertEqual(result["prescription"], "not_available")

    def test_app_view_model_exposes_quality_metadata(self) -> None:
        view_model = PsychRxAppService().get_app_view_model()

        self.assertEqual(view_model.clinical_quality_status.status, "valid")
        self.assertGreaterEqual(view_model.clinical_quality_status.quality_score, 0.75)
        self.assertEqual(view_model.clinical_quality_status.publication_outcome, "publish_with_warnings")
        self.assertTrue(view_model.clinical_quality_status.publish_allowed)
        self.assertTrue(view_model.clinical_quality_status.read_only_mode)

    def test_workspace_contains_quality_widget_without_prescription(self) -> None:
        payload = str(PsychRxAppService().get_app_view_model().to_dict())

        self.assertIn("Clinical Quality Engine Status Widget", payload)
        self.assertIn("ClinicalQualityResult", payload)
        self.assertIn("Publication Gate", payload)
        self.assertNotIn("dose recomendada", payload.lower())
        self.assertNotIn("prescrever agora", payload.lower())


if __name__ == "__main__":
    unittest.main()

