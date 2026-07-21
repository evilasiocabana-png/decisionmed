import unittest
from pathlib import Path

from application.clinical_coverage_matrix import ClinicalCoverageMatrix
from application.clinical_decision_support_service import ClinicalDecisionSupportService
from application.clinical_context_registry import ClinicalContextRegistry
from application.pharmacological_coverage_audit import PharmacologicalCoverageAuditService


ROOT = Path(__file__).resolve().parents[2]


def closed_safety():
    return {
        "suicide": "Negado",
        "aggression": "Negado",
        "mania_or_hypomania": "Negado",
        "substances": "Negado",
        "delirium": "Negado",
        "intoxication": "Negado",
        "withdrawal": "Negado",
        "allergies": "Negado",
        "severe_adverse_reaction": "Negado",
        "interactions": "Negado",
        "qt_risk": "Negado",
        "pregnancy_or_lactation": "Nao aplicavel",
        "metabolic_risk": "Negado",
        "acute_toxicity": "Negado",
        "adherence": "Boa",
        "adverse_effects": "Ausentes",
    }


class Program27CertificationTest(unittest.TestCase):
    def test_priority_documents_exist_before_final_report(self) -> None:
        for number in range(617, 632):
            with self.subTest(number=number):
                self.assertTrue(any((ROOT / "docs").glob(f"{number}_*.md")))

    def test_end_to_end_flow_preserves_patient_first_and_evidence_boundary(self) -> None:
        response = ClinicalDecisionSupportService().build_response(
            {
                "birth_date": "1980-01-01",
                "pregnancy_status": "Nao aplicavel",
                "lactation_status": "Nao aplicavel",
                "postpartum_status": "Nao aplicavel",
                "renal_status": "Preservada",
                "hepatic_status": "Preservada",
                "diagnostic_context": "Transtorno depressivo maior",
                "clinical_context_ids": ["CANNABIS_CONTEXT"],
                "clinical_presentation": "Primeira consulta",
                "symptoms": ["Humor deprimido", "Ansiedade"],
                "impairment_domains": ["Trabalho"],
                "pharmacological_profile": ["Humor: 4", "Ansiedade: 3"],
                "stability": "Sem resposta",
                "safety": closed_safety(),
            }
        )

        self.assertEqual("unresolved", response.status)
        self.assertEqual("structural_only_scientific_review_pending", response.scientific_readiness)
        self.assertIn("MAJOR_DEPRESSIVE_DISORDER", response.coverage_summary[0])
        self.assertIn("Cannabis", response.clinical_context_summary[0])
        self.assertIn("medico permanece responsavel", response.prescription_boundary)

    def test_all_coverage_and_registry_invariants_remain_closed(self) -> None:
        matrix = ClinicalCoverageMatrix()
        report = PharmacologicalCoverageAuditService().run()

        self.assertEqual((), matrix.validation_issues())
        self.assertEqual(51, len(matrix.topics()))
        self.assertTrue(all(not item.treatment_rule_allowed for item in ClinicalContextRegistry().all()))
        self.assertEqual(0, report.disease_use_formally_validated_count)
        self.assertEqual(0, report.motor2_formally_validated_count)

    def test_application_layer_never_depends_on_interface_layer(self) -> None:
        offenders = []
        for path in (ROOT / "application").glob("*.py"):
            source = path.read_text(encoding="utf-8")
            if "from interfaces" in source or "import interfaces" in source:
                offenders.append(path.name)
        self.assertEqual([], offenders)

    def test_no_wemeds_clone_or_apply_to_case_flow_was_added(self) -> None:
        index = (ROOT / "interfaces" / "web" / "static" / "index.html").read_text(encoding="utf-8").lower()
        app = (ROOT / "interfaces" / "web" / "static" / "app.js").read_text(encoding="utf-8").lower()

        self.assertNotIn("aplicar ao caso", index + app)
        self.assertNotIn('id="disease-library"', index)
        self.assertNotIn('id="apply-to-case"', index)
        self.assertIn("auditoria de escopo", index)


if __name__ == "__main__":
    unittest.main()
