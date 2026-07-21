"""Versioned source registry."""

from __future__ import annotations

from scientific_validation.models import ScientificSource


class SourceRegistry:
    """Catalogs scientific sources without validating clinical use."""

    SUPPORTED_TYPES = (
        "journal",
        "guideline",
        "textbook",
        "systematic_review",
        "meta_analysis",
        "regulatory_agency",
    )

    def __init__(self) -> None:
        self._sources: dict[str, ScientificSource] = {}

    def register(self, source: ScientificSource) -> ScientificSource:
        self._sources[source.source_id] = source
        return source

    def all(self) -> tuple[ScientificSource, ...]:
        return tuple(self._sources.values())

