"""Ontology registry."""

from __future__ import annotations

from knowledge_governance_platform.models import OntologyDefinition


class OntologyRegistry:
    def __init__(self) -> None:
        self._items: dict[str, OntologyDefinition] = {}
        self._history: list[OntologyDefinition] = []

    def register(self, ontology: OntologyDefinition) -> OntologyDefinition:
        self._items[ontology.ontology_id] = ontology
        self._history.append(ontology)
        return ontology

    def all(self) -> tuple[OntologyDefinition, ...]:
        return tuple(self._items.values())

    def history(self) -> tuple[OntologyDefinition, ...]:
        return tuple(self._history)

