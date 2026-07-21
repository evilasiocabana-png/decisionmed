"""Coordinator for Scientific Validation Framework."""

from __future__ import annotations

from scientific_validation.audit import ScientificAudit
from scientific_validation.editorial import EditorialReviewEngine
from scientific_validation.models import ScientificEvidence, ScientificSource, ScientificValidationResult
from scientific_validation.publication import KnowledgeVersionManager, PublicationGate
from scientific_validation.quality import EvidenceQualityEvaluator
from scientific_validation.sources import SourceRegistry


class ValidationCoordinator:
    """Coordinates scientific validation without medical inference or Runtime access."""

    def __init__(self) -> None:
        self.sources = SourceRegistry()
        self.quality = EvidenceQualityEvaluator()
        self.editorial = EditorialReviewEngine()
        self.versioning = KnowledgeVersionManager()
        self.publication = PublicationGate()
        self.audit = ScientificAudit()

    def validate_candidate(
        self,
        candidate: str = "knowledge_candidate",
        source: ScientificSource | None = None,
        evidence: ScientificEvidence | None = None,
        reviewers: tuple[str, ...] = ("scientific-reviewer",),
    ) -> ScientificValidationResult:
        active_source = self.sources.register(source or ScientificSource(title="Structured source candidate"))
        active_evidence = evidence or ScientificEvidence(study_design="systematic_review", references=(active_source.source_id,))
        quality = self.quality.evaluate(active_evidence)
        editorial = self.editorial.decide(reviewers, "structured scientific review", approved=True)
        version = self.versioning.assign()
        publication = self.publication.decide(quality, editorial, trace_valid=True, version=version)
        self.audit.record("ScientificValidationCompleted")
        return ScientificValidationResult(
            knowledge_candidate=candidate,
            scientific_sources=(active_source,),
            quality_assessment=quality,
            guideline_assessment=(),
            conflicts=(),
            editorial_review=editorial,
            publication_decision=publication,
            knowledge_version=version,
            audit=self.audit.snapshot(),
        )

