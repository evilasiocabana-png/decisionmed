"""Deterministic in-memory catalog for EvidenceSource metadata."""

from __future__ import annotations

from collections.abc import Iterable

from .models import EvidenceError, EvidenceSource


class EvidenceRegistryError(EvidenceError):
    pass


class EvidenceRegistry:
    """Catalog metadata without loading source content or clinical claims."""

    def __init__(self, sources: Iterable[EvidenceSource] = ()) -> None:
        self._sources: dict[str, EvidenceSource] = {}
        for source in sources:
            self.register(source)

    def register(self, source: EvidenceSource) -> EvidenceSource:
        if not isinstance(source, EvidenceSource):
            raise TypeError("source must be an EvidenceSource")
        if source.source_id in self._sources:
            raise EvidenceRegistryError(
                "evidence_registry.duplicate",
                f"source already registered: {source.source_id}",
            )
        self._sources[source.source_id] = source
        return source

    def get(self, source_id: str) -> EvidenceSource | None:
        return self._sources.get(source_id)

    def require(self, source_id: str) -> EvidenceSource:
        source = self.get(source_id)
        if source is None:
            raise EvidenceRegistryError(
                "evidence_registry.unknown", f"source not registered: {source_id}"
            )
        return source

    def all(self) -> tuple[EvidenceSource, ...]:
        return tuple(self._sources[key] for key in sorted(self._sources))
