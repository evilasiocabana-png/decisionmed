"""Internal API for Evidence Runtime. No REST."""

from __future__ import annotations

from evidence_runtime.coordinator import EvidenceCoordinator
from evidence_runtime.models import EvidenceRequest, EvidenceResult


class EvidenceRuntimeAPI:
    """Small internal facade for future runtime consumers."""

    def __init__(self, coordinator: EvidenceCoordinator | None = None) -> None:
        self._coordinator = coordinator or EvidenceCoordinator()

    def find(self, request: EvidenceRequest | None = None) -> EvidenceResult:
        return self._coordinator.execute(request)

    def resolve(self, request: EvidenceRequest | None = None) -> EvidenceResult:
        return self._coordinator.execute(request)

    def rank(self, request: EvidenceRequest | None = None) -> tuple[str, ...]:
        return self._coordinator.execute(request).ranking

    def snapshot(self, request: EvidenceRequest | None = None) -> dict[str, object]:
        return self._coordinator.execute(request).snapshot.to_dict()

    def citations(self, request: EvidenceRequest | None = None) -> tuple[dict[str, object], ...]:
        return tuple(citation.to_dict() for citation in self._coordinator.execute(request).citations)
