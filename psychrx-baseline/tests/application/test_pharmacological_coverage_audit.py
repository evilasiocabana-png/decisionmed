import unittest

from application.pharmacological_coverage_audit import PharmacologicalCoverageAuditService


class PharmacologicalCoverageAuditServiceTest(unittest.TestCase):
    def test_report_reconciles_current_tables(self) -> None:
        report = PharmacologicalCoverageAuditService().run()

        self.assertEqual(83, report.medication_count)
        self.assertEqual(38, report.interaction_profile_count)
        self.assertEqual(347, report.disease_use_row_count)
        self.assertEqual(347, report.disease_use_pending_formal_review_count)
        self.assertEqual(0, report.disease_use_formally_validated_count)
        self.assertEqual(1444, report.motor2_row_count)
        self.assertEqual(1398, report.motor2_pending_formal_review_count)
        self.assertEqual(23, report.motor2_pending_condition_research_count)
        self.assertEqual(23, report.motor2_selected_official_range_count)
        self.assertEqual(0, report.motor2_formally_validated_count)
        self.assertEqual(436, report.motor2_missing_condition_range_count)
        self.assertEqual(32, report.interaction_gap_official_excerpt_candidate_count)
        self.assertEqual(12, report.interaction_gap_source_or_anchor_required_count)

    def test_four_monitoring_rules_pass_the_dual_publication_gate(self) -> None:
        report = PharmacologicalCoverageAuditService().run()

        self.assertEqual(16, report.theory_to_practice_rule_count)
        self.assertEqual(4, report.monitoring_related_rule_count)
        self.assertEqual(4, report.monitoring_runtime_eligible_count)
        self.assertEqual(
            ("TPC-005", "TPC-012", "TPC-014", "TPC-015"),
            report.monitoring_runtime_eligible_rule_ids,
        )
        self.assertEqual("structural_only_scientific_review_pending", report.scientific_runtime_readiness)

    def test_scientific_backlog_is_reconciled_by_source_state(self) -> None:
        report = PharmacologicalCoverageAuditService().run()

        self.assertEqual(76, report.official_claim_anchor_count)
        self.assertEqual(7, report.official_claim_unresolved_count)
        self.assertEqual(68, report.disease_use_official_label_match_count)
        self.assertEqual(259, report.disease_use_guideline_or_off_label_review_count)
        self.assertEqual(20, report.disease_use_official_source_missing_count)
        self.assertEqual(95, report.motor2_official_indication_match_count)
        self.assertEqual(359, report.motor2_range_off_label_review_count)
        self.assertEqual(8, report.motor2_range_do_not_invent_count)

    def test_interaction_gaps_are_named_not_silently_closed(self) -> None:
        report = PharmacologicalCoverageAuditService().run()

        self.assertEqual(report.medication_count, report.interaction_covered_medication_count + report.interaction_gap_count)
        self.assertEqual(report.interaction_gap_count, len(report.interaction_gap_medications))
        self.assertGreater(report.interaction_gap_count, 0)


if __name__ == "__main__":
    unittest.main()
