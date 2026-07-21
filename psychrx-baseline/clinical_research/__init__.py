"""Clinical Research Platform package."""

from clinical_research.benchmark import BenchmarkEngine, ComparisonEngine, MetricsEngine
from clinical_research.coordinator import ResearchCoordinator
from clinical_research.experiments import ExperimentLifecycle, ExperimentManager, ScenarioRegistry
from clinical_research.governance import AdrRequirementValidator, PromotionPipeline, ResearchGovernance
from clinical_research.models import (
    BenchmarkResult,
    ClinicalResearchResult,
    PromotionDecision,
    ResearchExperiment,
    ResearchMetrics,
    ResearchReport,
    ResearchScenario,
    ValidationResult,
)
from clinical_research.validation import ResearchReportGenerator, ValidationEngine

__all__ = [
    "AdrRequirementValidator",
    "BenchmarkEngine",
    "BenchmarkResult",
    "ClinicalResearchResult",
    "ComparisonEngine",
    "ExperimentLifecycle",
    "ExperimentManager",
    "MetricsEngine",
    "PromotionDecision",
    "PromotionPipeline",
    "ResearchCoordinator",
    "ResearchExperiment",
    "ResearchGovernance",
    "ResearchMetrics",
    "ResearchReport",
    "ResearchReportGenerator",
    "ResearchScenario",
    "ScenarioRegistry",
    "ValidationEngine",
    "ValidationResult",
]

