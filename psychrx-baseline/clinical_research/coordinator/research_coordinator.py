"""Clinical Research Platform coordinator."""

from __future__ import annotations

from clinical_research.audit import ResearchAudit
from clinical_research.benchmark import BenchmarkEngine, ComparisonEngine, MetricsEngine
from clinical_research.experiments import ExperimentManager
from clinical_research.governance import PromotionPipeline, ResearchGovernance
from clinical_research.models import ClinicalResearchResult, PromotionDecision, ResearchExperiment
from clinical_research.validation import ValidationEngine


class ResearchCoordinator:
    """Coordinates research workflows without Clinical Runtime integration."""

    def __init__(self) -> None:
        self.experiments = ExperimentManager()
        self.benchmarks = BenchmarkEngine()
        self.metrics = MetricsEngine()
        self.comparison = ComparisonEngine()
        self.validation = ValidationEngine()
        self.governance = ResearchGovernance()
        self.promotion = PromotionPipeline()
        self.audit = ResearchAudit()

    def run_structural_experiment(self, experiment: ResearchExperiment | None = None) -> ClinicalResearchResult:
        active = self.experiments.register(experiment or ResearchExperiment(status="configured"))
        metrics = self.metrics.compute()
        benchmark = self.benchmarks.run()
        validation = self.validation.validate()
        comparison = self.comparison.compare("operating-mind-current", "operating-mind-current")
        self.audit.record("ResearchExperimentEvaluated")
        return ClinicalResearchResult(
            experiment_id=active.experiment_id,
            metrics=metrics,
            benchmark_results=(benchmark,),
            validation_results=(validation,),
            comparison_results=comparison,
            promotion_decision=PromotionDecision(
                state="Approved for Experimental Branch",
                governance_required=True,
                reason="governance_review_required_before_integration",
            ),
            audit=self.audit.snapshot(),
        )

