"""Format ClinicalExplanationResult for read-only surfaces."""

from __future__ import annotations

from clinical_explanation.models import ClinicalExplanationResult


class ExplanationFormatter:
    """Returns structured JSON plus readable text."""

    def to_workspace(self, result: ClinicalExplanationResult) -> dict[str, object]:
        return {"structured": result.to_dict(), "text": result.readable_text}

    def to_widget(self, result: ClinicalExplanationResult) -> dict[str, object]:
        return {"title": "Clinical Explanation", "summary": result.readable_text}

    def to_audit(self, result: ClinicalExplanationResult) -> dict[str, object]:
        return result.to_dict()

    def to_developer_console(self, result: ClinicalExplanationResult) -> dict[str, object]:
        return {"trace": result.trace.to_dict(), "sections": len(result.sections)}
