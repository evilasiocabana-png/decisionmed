"""Entity registry."""

from __future__ import annotations

from knowledge_governance_platform.models import EntityDefinition


class EntityRegistry:
    def __init__(self) -> None:
        self._entities: dict[str, EntityDefinition] = {}

    def register(self, entity: EntityDefinition) -> EntityDefinition:
        self._entities[entity.entity_id] = entity
        return entity

    def all(self) -> tuple[EntityDefinition, ...]:
        return tuple(self._entities.values())

