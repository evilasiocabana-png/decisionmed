import unittest
from pathlib import Path

from clinical_explanation import ExplanationCoordinator
from clinical_explanation.audit import ExplanationAudit, ExplanationAuditEntry
from clinical_explanation.composer import WhyExplanationEngine
from clinical_explanation.formatter import ExplanationFormatter
from clinical_explanation.guardrails import LanguageGuardrails
from clinical_explanation.linker import AuditLinker, EvidenceCitationLinker, ExplainabilityNavigation
from clinical_explanation.widget import ExplanationWidgetContract


class ClinicalExplanationStructureTest(unittest.TestCase):
    def test_package_structure_exists(self) -> None:
        required_dirs = [
            "coordinator",
            "sources",
            "mapper",
            "composer",
            "trace",
            "linker",
            "formatter",
            "audit",
            "models",
            "widget",
            "integration",
        ]
        for dirname in required_dirs:
            with self.subTest(dirname=dirname):
                self.assertTrue((Path("clinical_explanation") / dirname).exists())

    def test_coordinator_returns_safe_explanation(self) -> None:
        result = ExplanationCoordinator().execute(
            runtime_result={"result": {"outputs": {"Safety": "structural"}}},
            safety_result={"blocking_decision": {"status": "allow"}, "snapshot": {"alert_count": 0}},
            evidence_result={"snapshot": {"selected_count": 0}, "citations": ()},
            optimization_result={"hypotheses": (), "uncertainties": ()},
        )

        self.assertEqual(result.status, "completed_read_only")
        self.assertGreater(len(result.sections), 0)
        self.assertIn("requires clinical judgment", result.readable_text)

    def test_guardrails_linkers_formatter_widget_and_audit_are_structural(self) -> None:
        guardrails = LanguageGuardrails()
        result = ExplanationCoordinator().execute({}, {}, {"citations": ()}, {})
        formatter = ExplanationFormatter()
        audit = ExplanationAudit()

        audit.record(ExplanationAuditEntry(event="ClinicalExplanationFinished"))

        self.assertFalse(guardrails.is_safe("must prescribe"))
        self.assertIn("requires clinical judgment", WhyExplanationEngine().explain_included())
        self.assertEqual(EvidenceCitationLinker().link(()), ())
        self.assertIn("Runtime Trace", ExplainabilityNavigation().links())
        self.assertIn("structured", formatter.to_workspace(result))
        self.assertEqual(ExplanationWidgetContract().to_dict()["state"], "read-only")
        self.assertEqual(audit.snapshot()[0].event, "ClinicalExplanationFinished")
        self.assertIn("explanation_trace_id", AuditLinker().link(result, "runtime"))

    def test_explanation_does_not_recommend_or_prescribe(self) -> None:
        payload = str(ExplanationCoordinator().execute({}, {}, {"citations": ()}, {}).to_dict()).lower()

        self.assertNotIn("best medication", payload)
        self.assertNotIn("recommended prescription", payload)
        self.assertNotIn("dose recomendada", payload)
        self.assertNotIn("automatic treatment", payload)


if __name__ == "__main__":
    unittest.main()
