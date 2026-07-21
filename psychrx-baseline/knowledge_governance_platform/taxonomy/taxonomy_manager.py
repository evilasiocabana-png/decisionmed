"""Taxonomy manager."""

from __future__ import annotations

from knowledge_governance_platform.models import TaxonomyDefinition


class TaxonomyManager:
    def build(self, categories: tuple[str, ...]) -> TaxonomyDefinition:
        return TaxonomyDefinition(categories=categories)

