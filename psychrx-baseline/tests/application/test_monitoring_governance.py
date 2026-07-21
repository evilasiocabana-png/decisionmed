import csv
import tempfile
import unittest
from pathlib import Path

from application.clinical_decision_support_contract import CurrentMedicationPayload
from application.monitoring_governance import MonitoringGovernanceService


class MonitoringGovernanceServiceTest(unittest.TestCase):
    def test_four_rules_are_published_but_only_context_matches_activate(self) -> None:
        result = MonitoringGovernanceService().assess(
            symptoms=("Ansiedade", "Insonia inicial")
        )

        self.assertIn("ansiedade", result.generic_targets)
        self.assertIn("sono", result.generic_targets)
        self.assertEqual(("TPC-005", "TPC-012", "TPC-014", "TPC-015"), result.runtime_eligible_rule_ids)
        self.assertEqual((), result.activated_rule_ids)
        self.assertEqual((), result.pending_runtime_rule_ids)
        self.assertTrue(any("publicadas: 4" in line for line in result.display_lines()))

    def test_antidepressant_withdrawal_rule_requires_action_and_class(self) -> None:
        service = MonitoringGovernanceService()
        medication = (CurrentMedicationPayload(name="Sertralina"),)

        inactive = service.assess(symptoms=(), medications=medication)
        active = service.assess(
            symptoms=(), action="taper_or_withdraw", medications=medication
        )

        self.assertNotIn("TPC-005", inactive.activated_rule_ids)
        self.assertEqual(("TPC-005",), active.activated_rule_ids)
        self.assertTrue(any("sintomas de retirada" in item for item in active.targets))
        self.assertEqual("NICE-NG222-1.4.12-1.4.21", active.evidence[0].source_id)

    def test_lithium_rule_activates_from_current_medication(self) -> None:
        result = MonitoringGovernanceService().assess(
            symptoms=(), medications=(CurrentMedicationPayload(name="Lítio"),)
        )

        self.assertEqual(("TPC-012",), result.activated_rule_ids)
        self.assertTrue(any("nivel plasmatico" in item for item in result.targets))
        self.assertTrue(result.evidence[0].url.startswith("https://www.nice.org.uk/"))

    def test_antipsychotic_activates_movement_and_metabolic_rules(self) -> None:
        result = MonitoringGovernanceService().assess(
            symptoms=(), medications=(CurrentMedicationPayload(name="Risperidona"),)
        )

        self.assertEqual(("TPC-014", "TPC-015"), result.activated_rule_ids)
        self.assertTrue(any("transtornos do movimento" in item for item in result.targets))
        self.assertTrue(any("HbA1c" in item for item in result.targets))
        self.assertTrue(all("nao " in item.boundary for item in result.evidence))

    def test_dual_gate_failure_keeps_rule_out_of_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            runtime_path = Path(directory) / "monitoring.csv"
            source = Path(
                "knowledge_base/decision_support_engine/tables/monitoring_runtime_rules.csv"
            )
            with source.open("r", encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
                fieldnames = list(rows[0])
            rows[1]["editorial_review_status"] = "pending_formal_review"
            with runtime_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            result = MonitoringGovernanceService(runtime_path=runtime_path).assess(
                symptoms=(), medications=(CurrentMedicationPayload(name="Litio"),)
            )

        self.assertNotIn("TPC-012", result.runtime_eligible_rule_ids)
        self.assertIn("TPC-012", result.pending_runtime_rule_ids)
        self.assertEqual((), result.activated_rule_ids)


if __name__ == "__main__":
    unittest.main()
