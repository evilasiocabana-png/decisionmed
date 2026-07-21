"""Twin migration planner."""

from __future__ import annotations


class TwinMigrationPlanner:
    def plan(self, schema_updates: tuple[str, ...], knowledge_updates: tuple[str, ...], version_upgrades: tuple[str, ...]) -> tuple[str, ...]:
        return (
            *(f"schema:{item}" for item in schema_updates),
            *(f"knowledge:{item}" for item in knowledge_updates),
            *(f"version:{item}" for item in version_upgrades),
            "automatic_migration:not_allowed",
        )

