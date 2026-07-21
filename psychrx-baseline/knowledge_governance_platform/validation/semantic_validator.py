"""Semantic validator."""

from __future__ import annotations

from knowledge_governance_platform.models import EntityDefinition, RelationshipDefinition, TaxonomyDefinition


class SemanticValidator:
    def validate(
        self,
        entities: tuple[EntityDefinition, ...],
        relationships: tuple[RelationshipDefinition, ...],
        taxonomy: TaxonomyDefinition,
    ) -> tuple[str, ...]:
        issues = []
        if not entities:
            issues.append("missing_entities")
        if not taxonomy.categories:
            issues.append("missing_taxonomy_categories")
        if relationships and not entities:
            issues.append("relationships_without_entities")
        return tuple(issues)

