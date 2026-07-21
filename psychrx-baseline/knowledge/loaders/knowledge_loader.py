"""Loader contracts for structured knowledge."""

from __future__ import annotations

from typing import Protocol

from knowledge.core.knowledge_object import KnowledgeObject


class KnowledgeLoader(Protocol):
    """Contract for loading already-structured knowledge.

    This contract does not import PDFs, parse free text, call AI systems, or
    persist data.
    """

    def load(self) -> tuple[KnowledgeObject, ...]:
        """Return structured knowledge objects from an implementation adapter."""
