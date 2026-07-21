"""Migration planner."""

from __future__ import annotations


class MigrationPlanner:
    def plan(
        self,
        affected_entities: tuple[str, ...],
        affected_relationships: tuple[str, ...] = (),
        affected_taxonomy: tuple[str, ...] = (),
    ) -> tuple[str, ...]:
        return (
            *(f"entity:{item}" for item in affected_entities),
            *(f"relationship:{item}" for item in affected_relationships),
            *(f"taxonomy:{item}" for item in affected_taxonomy),
            "automatic_migration:not_allowed",
        )

