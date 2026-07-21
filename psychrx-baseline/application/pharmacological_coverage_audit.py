"""Read-only governance audit for PsychRx pharmacological tables."""

from __future__ import annotations

import csv
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

from application.medication_interaction_table import MedicationInteractionTable
from application.monitoring_governance import MonitoringGovernanceService


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TABLES = PROJECT_ROOT / "knowledge_base" / "decision_support_engine" / "tables"


@dataclass(frozen=True)
class PharmacologicalCoverageReport:
    medication_count: int
    interaction_profile_count: int
    interaction_alias_count: int
    interaction_covered_medication_count: int
    interaction_gap_count: int
    interaction_gap_medications: tuple[str, ...]
    interaction_gap_official_excerpt_candidate_count: int
    interaction_gap_source_or_anchor_required_count: int
    disease_use_row_count: int
    disease_use_pending_formal_review_count: int
    disease_use_formally_validated_count: int
    motor2_row_count: int
    motor2_pending_formal_review_count: int
    motor2_pending_condition_research_count: int
    motor2_selected_official_range_count: int
    motor2_formally_validated_count: int
    motor2_missing_condition_range_count: int
    theory_to_practice_rule_count: int
    monitoring_related_rule_count: int
    monitoring_runtime_eligible_count: int
    monitoring_runtime_eligible_rule_ids: tuple[str, ...]
    official_claim_anchor_count: int
    official_claim_unresolved_count: int
    disease_use_official_label_match_count: int
    disease_use_guideline_or_off_label_review_count: int
    disease_use_official_source_missing_count: int
    motor2_official_indication_match_count: int
    motor2_range_off_label_review_count: int
    motor2_range_do_not_invent_count: int
    scientific_runtime_readiness: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class PharmacologicalCoverageAuditService:
    """Measure coverage without mutating or promoting scientific content."""

    def run(self) -> PharmacologicalCoverageReport:
        medications = self._rows("pharmacological_decision_matrix.csv")
        disease_uses = self._rows("medication_disease_use_matrix.csv")
        motor2 = self._rows("motor2_strategy_matrix.csv")
        theory = self._rows("theory_to_practice_matrix.csv")
        official_claims = self._rows("medication_official_claims.csv")
        disease_review = self._rows("medication_disease_use_evidence_review.csv")
        motor2_resolution = self._rows("motor2_gap_resolution_matrix.csv")
        interaction_table = MedicationInteractionTable()
        monitoring_assessment = MonitoringGovernanceService().assess(symptoms=())

        medication_names = tuple(
            row.get("drug_name", "").strip()
            for row in medications
            if row.get("drug_name", "").strip()
        )
        interaction_gaps = tuple(
            name for name in medication_names if interaction_table.profile_for(name) is None
        )
        claims_by_name = {
            row.get("medication_name", ""): row for row in official_claims
        }
        interaction_gap_excerpt_candidates = tuple(
            name
            for name in interaction_gaps
            if claims_by_name.get(name, {}).get("extraction_status")
            == "official_claim_anchors_extracted"
            and claims_by_name.get(name, {}).get("interactions_anchor", "").strip()
            and claims_by_name.get(name, {}).get("interactions_excerpt", "").strip()
        )
        disease_statuses = Counter(
            row.get("review_status", "").strip().lower() for row in disease_uses
        )
        motor_statuses = Counter(
            row.get("evidence_status", "").strip().lower() for row in motor2
        )
        monitoring = tuple(
            row for row in theory if "monitor" in " ".join(row.values()).lower()
        )

        disease_validated = sum(
            count
            for status, count in disease_statuses.items()
            if self._is_formally_validated(status)
        )
        motor_validated = sum(
            count
            for status, count in motor_statuses.items()
            if self._is_formally_validated(status)
        )
        readiness = (
            "scientifically_runtime_eligible"
            if disease_validated and motor_validated
            else "structural_only_scientific_review_pending"
        )

        return PharmacologicalCoverageReport(
            medication_count=len(medication_names),
            interaction_profile_count=len(interaction_table.profiles()),
            interaction_alias_count=len(interaction_table.aliases()),
            interaction_covered_medication_count=len(medication_names) - len(interaction_gaps),
            interaction_gap_count=len(interaction_gaps),
            interaction_gap_medications=interaction_gaps,
            interaction_gap_official_excerpt_candidate_count=len(
                interaction_gap_excerpt_candidates
            ),
            interaction_gap_source_or_anchor_required_count=(
                len(interaction_gaps) - len(interaction_gap_excerpt_candidates)
            ),
            disease_use_row_count=len(disease_uses),
            disease_use_pending_formal_review_count=sum(
                count for status, count in disease_statuses.items() if "pendente" in status
            ),
            disease_use_formally_validated_count=disease_validated,
            motor2_row_count=len(motor2),
            motor2_pending_formal_review_count=sum(
                count
                for status, count in motor_statuses.items()
                if "pending_formal_review" in status or status == "source_located_pending_review"
            ),
            motor2_pending_condition_research_count=motor_statuses.get(
                "pending_condition_range_research", 0
            ),
            motor2_selected_official_range_count=motor_statuses.get(
                "official_source_mapped_for_selected_ranges", 0
            ),
            motor2_formally_validated_count=motor_validated,
            motor2_missing_condition_range_count=sum(
                not row.get("condition_range", "").strip()
                or row.get("condition_range", "").strip().lower() == "nao cadastrado"
                for row in motor2
            ),
            theory_to_practice_rule_count=len(theory),
            monitoring_related_rule_count=len(monitoring),
            monitoring_runtime_eligible_count=len(
                monitoring_assessment.runtime_eligible_rule_ids
            ),
            monitoring_runtime_eligible_rule_ids=(
                monitoring_assessment.runtime_eligible_rule_ids
            ),
            official_claim_anchor_count=sum(
                row.get("extraction_status", "") == "official_claim_anchors_extracted"
                for row in official_claims
            ),
            official_claim_unresolved_count=sum(
                row.get("extraction_status", "") != "official_claim_anchors_extracted"
                for row in official_claims
            ),
            disease_use_official_label_match_count=sum(
                row.get("evidence_review_status", "") == "official_label_indication_match"
                for row in disease_review
            ),
            disease_use_guideline_or_off_label_review_count=sum(
                row.get("evidence_review_status", "")
                == "no_direct_label_match_guideline_or_off_label_review_required"
                for row in disease_review
            ),
            disease_use_official_source_missing_count=sum(
                row.get("evidence_review_status", "")
                == "official_indication_source_missing"
                for row in disease_review
            ),
            motor2_official_indication_match_count=sum(
                row.get("official_indication_match", "").strip().lower() == "true"
                for row in motor2_resolution
            ),
            motor2_range_off_label_review_count=sum(
                row.get("range_resolution_status", "")
                == "guideline_or_off_label_range_review_required"
                for row in motor2_resolution
            ),
            motor2_range_do_not_invent_count=sum(
                row.get("range_resolution_status", "")
                == "no_supported_relationship_registered_do_not_invent_range"
                for row in motor2_resolution
            ),
            scientific_runtime_readiness=readiness,
        )

    @staticmethod
    def _is_formally_validated(status: str) -> bool:
        normalized = str(status or "").lower()
        return (
            ("validated" in normalized or "aprovad" in normalized)
            and "pending" not in normalized
            and "pendente" not in normalized
        )

    @staticmethod
    def _rows(filename: str) -> list[dict[str, str]]:
        path = TABLES / filename
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
