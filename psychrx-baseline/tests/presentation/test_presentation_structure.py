from pathlib import Path
import unittest


class PresentationStructureTest(unittest.TestCase):
    def setUp(self) -> None:
        self.project_root = Path(__file__).resolve().parents[2]
        self.presentation_root = self.project_root / "presentation"
        self.workspace_root = self.presentation_root / "clinical_workspace"

    def test_presentation_workspace_structure_exists(self) -> None:
        self.assertTrue((self.presentation_root / "README.md").is_file())
        self.assertTrue((self.workspace_root / "README.md").is_file())

    def test_required_workspace_sections_exist(self) -> None:
        sections = [
            "widgets",
            "layouts",
            "workspace",
            "investigation",
            "timeline",
            "strategy",
            "monitoring",
            "patient",
            "shared",
        ]

        for section in sections:
            with self.subTest(section=section):
                path = self.workspace_root / section
                self.assertTrue(path.is_dir())
                self.assertTrue((path / "README.md").is_file())

    def test_clinical_widget_specification_exists(self) -> None:
        spec = self.project_root / "docs" / "CLINICAL_WIDGET_SPECIFICATION.md"
        content = spec.read_text(encoding="utf-8")

        self.assertIn("Clinical Widget", content)
        self.assertIn("id", content)
        self.assertIn("permissions", content)
        self.assertIn("nao prescreve", content.lower())


if __name__ == "__main__":
    unittest.main()
