"""Immutable models for Clinical Research Platform."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ResearchScenario:
    scenario_id: str
    scenario_type: str = "reference"
    description: str = ""


@dataclass(frozen=True)
class ResearchExperiment:
    experiment_id: str = field(default_factory=lambda: f"EXP-{uuid4()}")
    name: str = "Structural Research Experiment"
    status: str = "draft"
    metadata: tuple[str, ...] = field(default_factory=tuple)
    version: str = "0.1"


@dataclass(frozen=True)
class BenchmarkResult:
    benchmark_id: str = field(default_factory=lambda: f"BM-{uuid4()}")
    status: str = "completed"
    measured_items: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ValidationResult:
    validation_id: str = field(default_factory=lambda: f"VAL-{uuid4()}")
    status: str = "valid"
    checks: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class PromotionDecision:
    state: str = "Needs Revision"
    governance_required: bool = True
    reason: str = "architecture_review_required"


@dataclass(frozen=True)
class ResearchMetrics:
    execution_time: float = 0.0
    trace_completeness: float = 1.0
    quality_coverage: float = 1.0
    reproducibility: float = 1.0
    contract_compliance: float = 1.0

    def average(self) -> float:
        return round(
            (
                self.trace_completeness
                + self.quality_coverage
                + self.reproducibility
                + self.contract_compliance
            )
            / 4,
            3,
        )


@dataclass(frozen=True)
class ResearchReport:
    report_id: str = field(default_factory=lambda: f"RPT-{uuid4()}")
    metrics: ResearchMetrics = field(default_factory=ResearchMetrics)
    limitations: tuple[str, ...] = field(default_factory=tuple)
    known_issues: tuple[str, ...] = field(default_factory=tuple)
    promotion_recommendation: str = "governance_review_required"


@dataclass(frozen=True)
class ClinicalResearchResult:
    research_id: str = field(default_factory=lambda: f"CRP-{uuid4()}")
    experiment_id: str = ""
    architecture_version: str = "structural"
    knowledge_version: str = "structural"
    runtime_version: str = "not_connected"
    metrics: ResearchMetrics = field(default_factory=ResearchMetrics)
    benchmark_results: tuple[BenchmarkResult, ...] = field(default_factory=tuple)
    validation_results: tuple[ValidationResult, ...] = field(default_factory=tuple)
    comparison_results: tuple[str, ...] = field(default_factory=tuple)
    promotion_decision: PromotionDecision = field(default_factory=PromotionDecision)
    audit: tuple[str, ...] = field(default_factory=tuple)
    trace_id: str = field(default_factory=lambda: f"CRP-TRC-{uuid4()}")
    timestamp: str = field(default_factory=_now)
    read_only_mode: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

