"""Structured citation engine."""

from __future__ import annotations

from evidence_runtime.models import Citation, Evidence


class CitationEngine:
    """Builds citation identifiers and version references without formatting libraries."""

    def build(self, evidence: tuple[Evidence, ...]) -> tuple[Citation, ...]:
        citations = []
        for item in evidence:
            source = item.source
            citations.append(
                Citation(
                    citation_id=f"CIT-{item.evidence_id}",
                    evidence_id=item.evidence_id,
                    source_id=source.source_id if source else "",
                    version=item.metadata.version,
                    source_link=source.uri if source else "",
                )
            )
        return tuple(citations)
