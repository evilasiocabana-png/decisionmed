import csv
import unittest
from pathlib import Path

from application.clinical_decision_support_contract import CurrentMedicationPayload
from application.monitoring_governance import MonitoringGovernanceService
from application.pharmacological_coverage_audit import PharmacologicalCoverageAuditService


ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "knowledge_base" / "decision_support_engine" / "tables"


class Program28ScientificPromotionTest(unittest.TestCase):
    def test_governance_precedes_runtime_publication(self) -> None:
        adr = ROOT / "governance" / "adr" / "docs_adr" / "0051_SOURCE_GOVERNED_MONITORING_PLANS.md"
        self.assertTrue(adr.exists())
        text = adr.read_text(encoding="utf-8")
        self.assertIn("Accepted for implementation", text)
        self.assertIn("It may not", text)

    def test_all_published_rows_have_complete_official_source_gates(self) -> None:
        with (TABLES / "monitoring_runtime_rules.csv").open(
            "r", encoding="utf-8-sig", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))

        self.assertEqual(4, len(rows))
        for row in rows:
            self.assertTrue(row["official_source_id"].startswith("NICE-"))
            self.assertTrue(row["official_source_url"].startswith("https://www.nice.org.uk/"))
            self.assertEqual("verified_against_official_guideline", row["scientific_review_status"])
            self.assertEqual("approved_for_non_prescriptive_runtime", row["editorial_review_status"])
            self.assertEqual("published_monitoring_knowledge_object", row["publication_status"])
            self.assertEqual("true", row["runtime_eligible"])
            self.assertTrue(row["boundary"].startswith("nao "))

    def test_runtime_activation_is_patient_state_specific(self) -> None:
        service = MonitoringGovernanceService()
        unrelated = service.assess(
            symptoms=(), medications=(CurrentMedicationPayload(name="Acamprosato"),)
        )
        antipsychotic = service.assess(
            symptoms=(), medications=(CurrentMedicationPayload(name="Risperidona"),)
        )

        self.assertEqual((), unrelated.activated_rule_ids)
        self.assertEqual(("TPC-014", "TPC-015"), antipsychotic.activated_rule_ids)

    def test_final_audit_reproduces_all_quoted_backlog_totals(self) -> None:
        report = PharmacologicalCoverageAuditService().run()

        self.assertEqual(44, report.interaction_gap_count)
        self.assertEqual(347, report.disease_use_row_count)
        self.assertEqual(1444, report.motor2_row_count)
        self.assertEqual(436, report.motor2_missing_condition_range_count)
        self.assertEqual(4, report.monitoring_runtime_eligible_count)


if __name__ == "__main__":
    unittest.main()
