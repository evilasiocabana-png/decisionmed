"""Audit linker for explanations."""

from __future__ import annotations

from clinical_explanation.models import ClinicalExplanationResult


class AuditLinker:
    """Connects explanation results to runtime audit identifiers."""

    def link(self, result: ClinicalExplanationResult, runtime_trace_id: str) -> dict[str, str]:
        return {"explanation_trace_id": result.trace.trace_id, "runtime_trace_id": runtime_trace_id}
