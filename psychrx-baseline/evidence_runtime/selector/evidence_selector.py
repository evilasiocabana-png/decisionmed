"""Evidence selector."""

from __future__ import annotations

from evidence_runtime.models import Evidence, EvidenceRequest


class EvidenceSelector:
    """Filters evidence by structural metadata only."""

    def select(
        self,
        candidates: tuple[Evidence, ...],
        request: EvidenceRequest,
    ) -> tuple[Evidence, ...]:
        selected = candidates
        if request.status:
            selected = tuple(
                item for item in selected if item.metadata.status == request.status
            )
        if request.scope:
            selected = tuple(item for item in selected if item.scope == request.scope)
        return selected
