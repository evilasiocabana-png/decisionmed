"""Evidence explanation mapper."""

from __future__ import annotations

from typing import Any

from clinical_explanation.models import ExplanationNode, ExplanationReference, ExplanationSource


class EvidenceExplanationMapper:
    """Maps EvidenceResult into explanation nodes without interpreting evidence."""

    def map(self, evidence_result: dict[str, Any]) -> tuple[ExplanationNode, ...]:
        citations = evidence_result.get("citations", ())
        references = tuple(
            ExplanationReference(
                reference_id=str(citation.get("citation_id", "")),
                citation_id=str(citation.get("citation_id", "")),
                evidence_version=str(citation.get("version", "")),
                source_type=str(citation.get("source_id", "")),
                selection_reason="selected by Evidence Runtime contract",
            )
            for citation in citations
            if isinstance(citation, dict)
        )
        selected = evidence_result.get("snapshot", {}).get("selected_count", 0)
        return (
            ExplanationNode(
                node_id="evidence-summary",
                title="Evidence used",
                text=f"EvidenceResult supplied {selected} selected evidence records.",
                source=ExplanationSource("evidence", "evidence_result"),
                references=references,
            ),
        )
