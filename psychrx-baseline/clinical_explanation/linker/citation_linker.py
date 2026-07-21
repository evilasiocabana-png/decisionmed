"""Evidence citation linker."""

from __future__ import annotations

from clinical_explanation.models import ExplanationReference


class EvidenceCitationLinker:
    """Links explanation nodes to Evidence Runtime citation metadata."""

    def link(self, citations: tuple[dict[str, object], ...]) -> tuple[ExplanationReference, ...]:
        return tuple(
            ExplanationReference(
                reference_id=str(citation.get("citation_id", "")),
                citation_id=str(citation.get("citation_id", "")),
                evidence_version=str(citation.get("version", "")),
                source_type=str(citation.get("source_id", "")),
                selection_reason="linked from Evidence Runtime",
            )
            for citation in citations
        )
