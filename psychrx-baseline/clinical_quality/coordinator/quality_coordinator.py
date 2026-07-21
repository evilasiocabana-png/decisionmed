"""Coordinator for Clinical Quality & Error Reduction Engine."""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy

from clinical_quality.analyzers import (
    CompletenessAnalyzer,
    ConflictDetector,
    ConsistencyAnalyzer,
    EvidenceReferenceValidator,
    ExplainabilityValidator,
    ImmutabilityValidator,
    MissingDataAnalyzer,
    TraceValidator,
)
from clinical_quality.audit import QualityAuditLog
from clinical_quality.audit.quality_audit import QualityAuditEntry
from clinical_quality.models import (
    BlockingIssue,
    ClinicalQualityResult,
    QualityMetrics,
    QualityWarning,
)
from clinical_quality.publication import PublicationGate


class QualityCoordinator:
    """Coordinates structural quality evaluation without mutating inputs."""

    def __init__(self) -> None:
        self.completeness = CompletenessAnalyzer()
        self.consistency = ConsistencyAnalyzer()
        self.trace = TraceValidator()
        self.explainability = ExplainabilityValidator()
        self.missing_data = MissingDataAnalyzer()
        self.conflicts = ConflictDetector()
        self.evidence_references = EvidenceReferenceValidator()
        self.immutability = ImmutabilityValidator()
        self.publication = PublicationGate()
        self.audit = QualityAuditLog()

    def evaluate(self, runtime_output: Mapping[str, object]) -> ClinicalQualityResult:
        before = deepcopy(dict(runtime_output))
        completeness = self.completeness.analyze(runtime_output)
        consistency = self.consistency.analyze(runtime_output)
        traceability = self.trace.validate(runtime_output)
        explainability = self.explainability.validate(runtime_output)
        missing = self.missing_data.analyze(runtime_output)
        conflicts = self.conflicts.detect(runtime_output)
        evidence_errors = self.evidence_references.validate(runtime_output)
        mutation_errors = self.immutability.validate(before, dict(runtime_output))
        blocking = tuple(
            BlockingIssue(code=code, message=code, source="ClinicalQuality")
            for code in conflicts + evidence_errors + mutation_errors
        )
        warnings = tuple(
            QualityWarning(code=item, message=item)
            for item in missing
            if item.startswith("optional:")
        )
        metrics = QualityMetrics(
            completeness=completeness.score,
            consistency=consistency.score,
            traceability=traceability.score,
            explainability=explainability.score,
        )
        decision = self.publication.decide(metrics, blocking, warnings)
        self.audit.record(QualityAuditEntry(event="QualityEvaluated", decision=decision.outcome))
        return ClinicalQualityResult(
            status="valid" if decision.publish_allowed else "blocked",
            quality_score=metrics.average(),
            completeness=completeness,
            consistency=consistency,
            traceability=traceability,
            explainability=explainability,
            missing_data=missing,
            conflicts=conflicts,
            blocking_issues=blocking,
            warnings=warnings,
            publication_decision=decision,
        )

