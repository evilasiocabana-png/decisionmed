"""Semantic conflict detector."""

from __future__ import annotations

from knowledge_governance_platform.models import EntityDefinition


class SemanticConflictDetector:
    def detect(self, entities: tuple[EntityDefinition, ...]) -> tuple[str, ...]:
        aliases: dict[str, str] = {}
        conflicts = []
        for entity in entities:
            for alias in entity.aliases:
                if alias in aliases and aliases[alias] != entity.entity_id:
                    conflicts.append(f"ambiguous_mapping:{alias}")
                aliases[alias] = entity.entity_id
        return tuple(conflicts)

