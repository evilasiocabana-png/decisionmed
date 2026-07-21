from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from decisionmed.architecture import (
    PROTECTED_LAYERS,
    BoundaryViolation,
    scan_architecture,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ArchitectureBoundaryTest(unittest.TestCase):
    def test_current_source_respects_layer_boundaries(self) -> None:
        self.assertEqual((), scan_architecture(PROJECT_ROOT / "decisionmed"))

    def test_forbidden_absolute_and_relative_imports_are_reported(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            package_root = self._package_root(Path(temporary_directory))
            self._write(package_root / "domain" / "bad.py", "from decisionmed.app import app_state\n")
            self._write(package_root / "evidence" / "bad.py", "from ..domain import EntityId\n")

            violations = scan_architecture(package_root)

        self.assertEqual(2, len(violations))
        self.assertEqual(
            {("domain", "app"), ("evidence", "domain")},
            {(item.source_layer, item.target_layer) for item in violations},
        )
        self.assertTrue(all(isinstance(item, BoundaryViolation) for item in violations))

    def test_documented_dependencies_and_same_layer_imports_are_allowed(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            package_root = self._package_root(Path(temporary_directory))
            self._write(package_root / "knowledge" / "models.py", "VALUE = 1\n")
            self._write(
                package_root / "knowledge" / "registry.py",
                "from .models import VALUE\n"
                "from decisionmed.domain import EntityId\n"
                "from decisionmed.evidence import EvidenceSource\n",
            )
            self._write(package_root / "audit" / "models.py", "from ..domain import DomainEvent\n")

            violations = scan_architecture(package_root)

        self.assertEqual((), violations)

    def test_future_reasoning_application_and_interface_layers_are_enforced(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            package_root = self._package_root(Path(temporary_directory))
            self._write(
                package_root / "reasoning" / "engine.py",
                "from decisionmed.safety import SafetyAssessment\n",
            )
            self._write(
                package_root / "application" / "service.py",
                "from decisionmed.reasoning import ReasoningResult\n"
                "from decisionmed.audit import AuditLedger\n",
            )
            self._write(
                package_root / "interface" / "view.py",
                "from decisionmed.application import AppService\n",
            )
            self._write(
                package_root / "interface" / "bad.py",
                "from decisionmed.domain import ClinicalSnapshot\n",
            )

            violations = scan_architecture(package_root)

        self.assertEqual(1, len(violations))
        self.assertEqual("interface", violations[0].source_layer)
        self.assertEqual("domain", violations[0].target_layer)

    @staticmethod
    def _package_root(temporary_root: Path) -> Path:
        package_root = temporary_root / "decisionmed"
        for layer in PROTECTED_LAYERS:
            (package_root / layer).mkdir(parents=True)
        return package_root

    @staticmethod
    def _write(path: Path, content: str) -> None:
        path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
