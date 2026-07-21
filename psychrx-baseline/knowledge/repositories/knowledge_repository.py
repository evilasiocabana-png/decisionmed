"""Repository contracts for structured knowledge."""

from __future__ import annotations

from typing import Protocol

from knowledge.core.knowledge_object import KnowledgeObject
from knowledge.core.status import KnowledgeStatus


class KnowledgeRepository(Protocol):
    """Technology-independent repository contract.

    Implementations must not be placed in the Knowledge Layer unless a future
    mission explicitly authorizes persistence technology.
    """

    def add(self, knowledge_object: KnowledgeObject) -> None:
        """Store a knowledge object through an implementation-specific adapter."""

    def get(self, identifier: str) -> KnowledgeObject | None:
        """Return a knowledge object by identifier, or None when absent."""

    def list(self) -> tuple[KnowledgeObject, ...]:
        """Return all available knowledge objects."""

    def find_by_status(self, status: KnowledgeStatus) -> tuple[KnowledgeObject, ...]:
        """Return knowledge objects with the requested lifecycle status."""
