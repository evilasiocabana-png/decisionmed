from pathlib import Path
import unittest


class ClinicalExperienceStructureTest(unittest.TestCase):
    def setUp(self) -> None:
        self.project_root = Path(__file__).resolve().parents[2]
        self.layer_root = self.project_root / "clinical_experience"

    def test_clinical_experience_layer_exists(self) -> None:
        self.assertTrue(self.layer_root.is_dir())
        self.assertTrue((self.layer_root / "README.md").is_file())

    def test_required_components_exist(self) -> None:
        components = [
            "consultation_room",
            "clinical_card_stack",
            "guided_anamnesis",
            "live_question_panel",
            "symptom_capture",
            "strategy_panel",
            "risk_panel",
            "monitoring_timeline",
            "evidence_summary",
            "patient_friendly_mode",
        ]

        for component in components:
            with self.subTest(component=component):
                path = self.layer_root / component
                self.assertTrue(path.is_dir())
                self.assertTrue((path / "README.md").is_file())

    def test_layer_documents_no_prescription_boundary(self) -> None:
        readme = (self.layer_root / "README.md").read_text(encoding="utf-8")

        self.assertIn("nao decide conduta", readme.lower())
        self.assertIn("nao prescreve", readme.lower())

    def test_interface_views_exist(self) -> None:
        interfaces_root = self.project_root / "interfaces"

        for view in ["desktop_dashboard", "tablet_view", "mobile_view"]:
            with self.subTest(view=view):
                self.assertTrue((interfaces_root / view / "README.md").is_file())


if __name__ == "__main__":
    unittest.main()
