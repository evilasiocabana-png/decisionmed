"""Dependency analyzer."""

from __future__ import annotations

from knowledge_governance_platform.models import DependencyGraph, EntityDefinition, RelationshipDefinition


class DependencyAnalyzer:
    def analyze(
        self,
        entities: tuple[EntityDefinition, ...],
        relationships: tuple[RelationshipDefinition, ...],
    ) -> DependencyGraph:
        entity_ids = {entity.entity_id for entity in entities}
        issues = []
        for relationship in relationships:
            if relationship.source not in entity_ids:
                issues.append(f"broken_reference:{relationship.source}")
            if relationship.target not in entity_ids:
                issues.append(f"broken_reference:{relationship.target}")
            if relationship.source == relationship.target:
                issues.append(f"cycle:{relationship.source}")
        return DependencyGraph(
            nodes=tuple(sorted(entity_ids)),
            edges=tuple((item.source, item.target) for item in relationships),
            issues=tuple(issues),
        )

