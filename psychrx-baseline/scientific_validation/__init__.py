"""Scientific Validation Framework package."""

from scientific_validation.coordinator import ValidationCoordinator
from scientific_validation.editorial import EditorialReviewEngine
from scientific_validation.governance import ConflictResolutionEngine, GuidelineRegistry
from scientific_validation.models import (
    EditorialDecision,
    GuidelineReference,
    PublicationDecision,
    QualityAssessment,
    ScientificEvidence,
    ScientificSource,
    ScientificValidationResult,
)
from scientific_validation.publication import KnowledgeVersionManager, PublicationGate
from scientific_validation.quality import EvidenceQualityEvaluator, EvidenceSummaryGenerator, HierarchyEngine
from scientific_validation.sources import SourceLifecycle, SourceMetadataFactory, SourceRegistry

__all__ = [
    "ConflictResolutionEngine",
    "EditorialDecision",
    "EditorialReviewEngine",
    "EvidenceQualityEvaluator",
    "EvidenceSummaryGenerator",
    "GuidelineReference",
    "GuidelineRegistry",
    "HierarchyEngine",
    "KnowledgeVersionManager",
    "PublicationDecision",
    "PublicationGate",
    "QualityAssessment",
    "ScientificEvidence",
    "ScientificSource",
    "ScientificValidationResult",
    "SourceLifecycle",
    "SourceMetadataFactory",
    "SourceRegistry",
    "ValidationCoordinator",
]

