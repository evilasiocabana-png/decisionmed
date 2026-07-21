"""Evidence request resolver."""

from __future__ import annotations

from evidence_runtime.models import Evidence, EvidenceRequest
from evidence_runtime.registry import EvidenceRegistry


class EvidenceResolver:
    """Returns candidate evidence without ranking or interpretation."""

    def __init__(self, registry: EvidenceRegistry | None = None) -> None:
        self._registry = registry or EvidenceRegistry()

    def resolve(self, request: EvidenceRequest) -> tuple[Evidence, ...]:
        if request.category:
            return self._registry.by_category(request.category)
        return self._registry.all()
