import unittest

from application.app_service import PsychRxAppService
from clinical_runtime import ClinicalRuntime


class ClinicalResearchIntegrationTest(unittest.TestCase):
    def test_research_platform_is_not_in_runtime_pipeline(self) -> None:
        result = ClinicalRuntime().execute()

        self.assertNotIn("clinical_research", result)
        self.assertNotIn("Clinical Research", result["result"]["outputs"])
        self.assertEqual(result["prescription"], "not_available")

    def test_app_view_model_exposes_research_metadata_read_only(self) -> None:
        view_model = PsychRxAppService().get_app_view_model()

        self.assertEqual(view_model.clinical_research_status.status, "available_read_only")
        self.assertFalse(view_model.clinical_research_status.runtime_connected)
        self.assertEqual(
            view_model.clinical_research_status.promotion_state,
            "Approved for Experimental Branch",
        )
        self.assertTrue(view_model.clinical_research_status.read_only_mode)

    def test_workspace_contains_research_widget_without_prescription(self) -> None:
        payload = str(PsychRxAppService().get_app_view_model().to_dict())

        self.assertIn("Clinical Research Platform Status Widget", payload)
        self.assertIn("ClinicalResearchResult", payload)
        self.assertIn("Runtime integration: forbidden", payload)
        self.assertNotIn("dose recomendada", payload.lower())
        self.assertNotIn("prescrever agora", payload.lower())


if __name__ == "__main__":
    unittest.main()

