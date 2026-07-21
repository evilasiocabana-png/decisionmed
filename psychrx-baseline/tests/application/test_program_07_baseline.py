import unittest
from pathlib import Path

from application.app_service import PsychRxAppService


class Program07BaselineTest(unittest.TestCase):
    def test_program_07_docs_exist(self) -> None:
        required_docs = [
            "151_STRATEGY_WIDGET.md",
            "152_MONITORING_WIDGET.md",
            "153_CONSULTATION_WORKSPACE_BASELINE.md",
            "154_INVESTIGATION_WORKFLOW.md",
            "155_CLINICAL_COMPASS.md",
            "156_MISSING_INFORMATION_WIDGET.md",
            "157_CONSULTATION_PROGRESS_WIDGET.md",
            "158_DYNAMIC_QUESTION_STATES.md",
            "159_DYNAMIC_INVESTIGATION_BASELINE.md",
            "160_CLINICAL_WIDGET_FRAMEWORK.md",
            "161_WIDGET_REGISTRY.md",
            "162_WIDGET_STATE_MODEL.md",
            "163_WIDGET_VISIBILITY_RULES.md",
            "164_WIDGET_DOCUMENTATION_STANDARD.md",
            "165_CLINICAL_WIDGET_BASELINE.md",
            "166_CONSULTATION_TIMELINE.md",
            "167_CLINICAL_TIMELINE.md",
            "168_MEDICATION_TIMELINE.md",
            "169_SYMPTOM_TIMELINE.md",
            "170_RESPONSE_TIMELINE.md",
            "171_TIMELINE_BASELINE.md",
            "172_DESKTOP_REVIEW.md",
            "173_TABLET_REVIEW.md",
            "174_MOBILE_REVIEW.md",
            "175_ACCESSIBILITY_REVIEW.md",
            "176_WORKSPACE_REGRESSION_TESTS.md",
            "177_PROGRAM_07_BASELINE.md",
            "PROGRAM_07_BASELINE.md",
        ]

        for filename in required_docs:
            with self.subTest(filename=filename):
                self.assertTrue((Path("docs") / filename).is_file())

    def test_workspace_contains_program_07_widgets(self) -> None:
        payload = str(PsychRxAppService().get_app_view_model().to_dict())

        expected_terms = [
            "Strategy Widget",
            "Monitoring Widget",
            "Investigation Workflow",
            "Clinical Compass",
            "Missing Information Widget",
            "Consultation Progress Widget",
            "Dynamic Question States",
            "Clinical Widget Framework",
            "Widget Registry",
            "Widget State Model",
            "Widget Visibility Rules",
            "Consultation Timeline",
            "Clinical Timeline",
            "Medication Timeline",
            "Symptom Timeline",
            "Response Timeline",
        ]

        for term in expected_terms:
            with self.subTest(term=term):
                self.assertIn(term, payload)

    def test_program_07_preserves_read_only_safety(self) -> None:
        payload = str(PsychRxAppService().get_app_view_model().to_dict()).lower()

        self.assertIn("read-only", payload)
        self.assertIn("estrategias terapeuticas ainda nao disponiveis", payload)
        forbidden_terms = [
            "prescrever agora",
            "dose recomendada",
            "iniciar medicamento",
            "aumentar dose",
            "trocar para",
        ]
        for term in forbidden_terms:
            with self.subTest(term=term):
                self.assertNotIn(term, payload)


if __name__ == "__main__":
    unittest.main()
