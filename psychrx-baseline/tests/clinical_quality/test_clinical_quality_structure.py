import unittest
from pathlib import Path

from clinical_quality import (
    CompletenessAnalyzer,
    ConflictDetector,
    ConsistencyAnalyzer,
    ExplainabilityValidator,
    MissingDataAnalyzer,
    PublicationGate,
    QualityCoordinator,
    TraceValidator,
)
from clinical_quality.models import BlockingIssue, QualityMetrics, QualityWarning
from clinical_quality.replay import QualityReplay
from clinical_runtime import ClinicalRuntime


class ClinicalQualityStructureTest(unittest.TestCase):
    def test_package_structure_exists(self) -> None:
        for dirname in [
            "coordinator",
            "completeness",
            "consistency",
            "trace",
            "explainability",
            "missing_data",
            "conflicts",
            "publication",
            "audit",
            "models",
            "integration",
        ]:
            with self.subTest(dirname=dirname):
                expected = Path("clinical_quality") / dirname
                if dirname in {"completeness", "consistency", "trace", "explainability", "missing_data", "conflicts"}:
                    expected = Path("clinical_quality") / "analyzers"
                self.assertTrue(expected.is_dir())

    def test_analyzers_validate_runtime_output_without_interpretation(self) -> None:
        runtime_output = ClinicalRuntime().execute()

        self.assertEqual(CompletenessAnalyzer().analyze(runtime_output).status, "valid")
        self.assertEqual(ConsistencyAnalyzer().analyze(runtime_output).status, "valid")
        self.assertEqual(TraceValidator().validate(runtime_output).status, "valid")
        self.assertEqual(ExplainabilityValidator().validate(runtime_output).status, "valid")
        self.assertIn("optional:patient_context", MissingDataAnalyzer().analyze(runtime_output))
        self.assertEqual(ConflictDetector().detect(runtime_output), ())

    def test_publication_gate_is_explainable_and_non_prescriptive(self) -> None:
        gate = PublicationGate()

        published = gate.decide(QualityMetrics(1.0, 1.0, 1.0, 1.0), (), ())
        warning = gate.decide(
            QualityMetrics(1.0, 1.0, 1.0, 1.0),
            (),
            (QualityWarning(code="optional_context_missing", message="optional"),),
        )
        blocked = gate.decide(
            QualityMetrics(1.0, 1.0, 1.0, 1.0),
            (BlockingIssue(code="trace_mismatch", message="trace", source="test"),),
            (),
        )

        self.assertEqual(published.outcome, "publish")
        self.assertEqual(warning.outcome, "publish_with_warnings")
        self.assertEqual(blocked.outcome, "block_publication")
        self.assertFalse(blocked.publish_allowed)

    def test_quality_coordinator_and_replay_are_read_only(self) -> None:
        runtime_output = ClinicalRuntime().execute()
        result = QualityCoordinator().evaluate(runtime_output)
        replayed = QualityReplay().replay(result)
        payload = str(result.to_dict()).lower()

        self.assertEqual(result.status, "valid")
        self.assertTrue(result.read_only_mode)
        self.assertEqual(replayed, result)
        self.assertEqual(result.publication_decision.outcome, "publish_with_warnings")
        self.assertNotIn("dose recomendada", payload)
        self.assertNotIn("prescrever agora", payload)


if __name__ == "__main__":
    unittest.main()

