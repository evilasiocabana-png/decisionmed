import unittest

from application.app_service import PsychRxAppService
from clinical_runtime import ClinicalRuntime


class ClinicalSnapshotIntegrationTest(unittest.TestCase):
    def test_runtime_exposes_clinical_snapshot_after_explanation(self) -> None:
        result = ClinicalRuntime().execute()

        self.assertIn("clinical_snapshot", result)
        self.assertEqual(result["clinical_snapshot"]["runtime_id"], result["session"]["session_id"])
        self.assertIn("Snapshot", result["result"]["outputs"])
        self.assertEqual(result["prescription"], "not_available")

    def test_app_view_model_exposes_snapshot_metadata(self) -> None:
        view_model = PsychRxAppService().get_app_view_model()

        self.assertEqual(view_model.clinical_snapshot_status.status, "available_read_only")
        self.assertTrue(view_model.clinical_snapshot_status.read_only_mode)

    def test_workspace_contains_snapshot_widget_without_prescription(self) -> None:
        payload = str(PsychRxAppService().get_app_view_model().to_dict())

        self.assertIn("Clinical Snapshot Engine Status Widget", payload)
        self.assertIn("ClinicalSnapshot", payload)
        self.assertNotIn("dose recomendada", payload.lower())
        self.assertNotIn("prescrever agora", payload.lower())


if __name__ == "__main__":
    unittest.main()
