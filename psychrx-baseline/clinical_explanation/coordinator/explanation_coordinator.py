"""Clinical Explanation coordinator."""

from __future__ import annotations

from typing import Any

from clinical_explanation.audit import ExplanationAudit, ExplanationAuditEntry
from clinical_explanation.composer import ExplanationComposer, UncertaintyExplanationBuilder
from clinical_explanation.guardrails import LanguageGuardrails
from clinical_explanation.mapper import (
    EvidenceExplanationMapper,
    RuntimeExplanationMapper,
    SafetyExplanationMapper,
    TherapeuticHypothesisMapper,
)
from clinical_explanation.models import ClinicalExplanationResult


class ExplanationCoordinator:
    """Organizes explanation data without changing clinical results."""

    def __init__(self) -> None:
        self.runtime_mapper = RuntimeExplanationMapper()
        self.safety_mapper = SafetyExplanationMapper()
        self.evidence_mapper = EvidenceExplanationMapper()
        self.hypothesis_mapper = TherapeuticHypothesisMapper()
        self.composer = ExplanationComposer()
        self.guardrails = LanguageGuardrails()
        self.uncertainty_builder = UncertaintyExplanationBuilder()
        self.audit = ExplanationAudit()

    def execute(
        self,
        runtime_result: dict[str, Any],
        safety_result: dict[str, Any],
        evidence_result: dict[str, Any],
        optimization_result: dict[str, Any],
        clinical_snapshot: dict[str, Any] | None = None,
    ) -> ClinicalExplanationResult:
        _ = clinical_snapshot or {}
        nodes = (
            *self.runtime_mapper.map(runtime_result),
            *self.safety_mapper.map(safety_result),
            *self.evidence_mapper.map(evidence_result),
            *self.hypothesis_mapper.map(optimization_result),
        )
        sections = self.composer.compose(nodes)
        warning = self.uncertainty_builder.build("incomplete knowledge", "Clinical Explanation Engine")
        readable = (
            "Clinical explanation hypothesis based on available data; "
            "requires clinical judgment and preserves uncertainty when applicable."
        )
        violations = self.guardrails.violations(readable)
        warnings = (warning,) if not violations else (
            warning,
            self.uncertainty_builder.build("language guardrail", "Clinical Explanation Engine"),
        )
        result = ClinicalExplanationResult(
            status="completed_read_only",
            sections=sections,
            warnings=warnings,
            readable_text=readable,
        )
        self.audit.record(
            ExplanationAuditEntry(
                event="ClinicalExplanationFinished",
                explanation_trace_id=result.trace.trace_id,
                runtime_trace_id=str(runtime_result.get("result", {}).get("trace_id", "")),
            )
        )
        return result
