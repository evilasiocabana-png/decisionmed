"""Evidence quality evaluator."""

from __future__ import annotations

from scientific_validation.models import QualityAssessment, ScientificEvidence


class EvidenceQualityEvaluator:
    """Evaluates methodology metadata without clinical applicability interpretation."""

    def evaluate(self, evidence: ScientificEvidence) -> QualityAssessment:
        level = "structured"
        rank = 4
        if evidence.study_design in {"clinical_guideline", "systematic_review", "meta_analysis"}:
            level = "high_structural_priority"
            rank = 1
        return QualityAssessment(
            status="evaluated",
            quality_level=level,
            hierarchy_rank=rank,
            limitations=("no_clinical_applicability_interpretation",),
        )

