"""Ontology validator."""

from __future__ import annotations

from knowledge_governance_platform.models import EntityDefinition


class OntologyValidator:
    def validate(self, entities: tuple[EntityDefinition, ...]) -> tuple[str, ...]:
        names = [entity.name for entity in entities]
        issues = []
        duplicates = {name for name in names if names.count(name) > 1}
        issues.extend(f"duplicate_entity:{name}" for name in sorted(duplicates))
        issues.extend(f"undefined_entity:{entity.entity_id}" for entity in entities if not entity.name)
        return tuple(issues)

