from pathlib import Path
import importlib
import unittest


class KnowledgePackageStructureTest(unittest.TestCase):
    def setUp(self) -> None:
        self.project_root = Path(__file__).resolve().parents[2]
        self.knowledge_root = self.project_root / "knowledge"

    def test_knowledge_package_exists(self) -> None:
        self.assertTrue(self.knowledge_root.is_dir())
        self.assertTrue((self.knowledge_root / "__init__.py").is_file())

    def test_required_knowledge_subpackages_exist(self) -> None:
        required_subpackages = [
            "core",
            "models",
            "repositories",
            "loaders",
            "validators",
            "versioning",
        ]

        for subpackage in required_subpackages:
            with self.subTest(subpackage=subpackage):
                path = self.knowledge_root / subpackage
                self.assertTrue(path.is_dir())
                self.assertTrue((path / "__init__.py").is_file())

    def test_knowledge_package_imports_without_side_effects(self) -> None:
        knowledge = importlib.import_module("knowledge")

        self.assertEqual(
            sorted(knowledge.__all__),
            [
                "core",
                "loaders",
                "models",
                "repositories",
                "validators",
                "versioning",
            ],
        )

    def test_knowledge_readme_documents_current_limits(self) -> None:
        readme = self.knowledge_root / "README.md"

        self.assertTrue(readme.is_file())
        content = readme.read_text(encoding="utf-8")
        self.assertIn("Missions 061-070", content)
        self.assertIn("does not implement", content)
        self.assertIn("clinical engines", content)
        self.assertIn("guideline schema without content", content)
        self.assertIn("AI loading", content)
        self.assertIn("parsing", content)
        self.assertIn("database access", content)


if __name__ == "__main__":
    unittest.main()
