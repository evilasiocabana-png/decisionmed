from pathlib import Path
import importlib
import unittest


class DomainPackageStructureTest(unittest.TestCase):
    def setUp(self) -> None:
        self.project_root = Path(__file__).resolve().parents[2]
        self.domain_root = self.project_root / "domain"

    def test_domain_package_exists(self) -> None:
        self.assertTrue(self.domain_root.is_dir())
        self.assertTrue((self.domain_root / "__init__.py").is_file())

    def test_required_domain_subpackages_exist(self) -> None:
        required_subpackages = [
            "entities",
            "value_objects",
            "events",
            "services",
            "exceptions",
            "repositories",
        ]

        for subpackage in required_subpackages:
            with self.subTest(subpackage=subpackage):
                path = self.domain_root / subpackage
                self.assertTrue(path.is_dir())
                self.assertTrue((path / "__init__.py").is_file())

    def test_domain_package_imports_without_side_effects(self) -> None:
        domain = importlib.import_module("domain")

        self.assertEqual(
            sorted(domain.__all__),
            [
                "entities",
                "events",
                "exceptions",
                "repositories",
                "services",
                "value_objects",
            ],
        )

    def test_domain_readme_documents_current_limits(self) -> None:
        readme = self.domain_root / "README.md"

        self.assertTrue(readme.is_file())
        content = readme.read_text(encoding="utf-8")
        self.assertIn("Mission 051 creates structure only", content)
        self.assertIn("does not implement", content)
        self.assertIn("clinical entities", content)
        self.assertIn("database access", content)
        self.assertIn("framework integrations", content)


if __name__ == "__main__":
    unittest.main()
