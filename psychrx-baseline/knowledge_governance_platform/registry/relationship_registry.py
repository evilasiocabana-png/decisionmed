"""Relationship registry."""

from __future__ import annotations

from knowledge_governance_platform.models import RelationshipDefinition


class RelationshipRegistry:
    def __init__(self) -> None:
        self._relationships: dict[str, RelationshipDefinition] = {}

    def register(self, relationship: RelationshipDefinition) -> RelationshipDefinition:
        self._relationships[relationship.relationship_id] = relationship
        return relationship

    def all(self) -> tuple[RelationshipDefinition, ...]:
        return tuple(self._relationships.values())

