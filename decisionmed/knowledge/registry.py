"""Knowledge catalog that enforces EvidenceSource references."""

from __future__ import annotations

from collections.abc import Iterable

from decisionmed.evidence import EvidenceRegistry, EvidenceStatus

from .models import KnowledgeError, KnowledgeObject, KnowledgeStatus


class KnowledgeRegistry:
    def __init__(
        self,
        evidence: EvidenceRegistry,
        objects: Iterable[KnowledgeObject] = (),
    ) -> None:
        if not isinstance(evidence, EvidenceRegistry):
            raise TypeError("evidence must be an EvidenceRegistry")
        self._evidence = evidence
        self._objects: dict[str, KnowledgeObject] = {}
        for item in objects:
            self.register(item)

    def register(self, item: KnowledgeObject) -> KnowledgeObject:
        if not isinstance(item, KnowledgeObject):
            raise TypeError("item must be a KnowledgeObject")
        if item.object_id in self._objects:
            raise KnowledgeError(
                "knowledge_registry.duplicate",
                f"knowledge object already registered: {item.object_id}",
            )

        sources = tuple(
            self._evidence.get(source_id) for source_id in item.evidence_source_ids
        )
        missing = tuple(
            source_id
            for source_id, source in zip(item.evidence_source_ids, sources)
            if source is None
        )
        if missing:
            raise KnowledgeError(
                "knowledge_registry.unknown_evidence",
                f"unknown evidence sources: {', '.join(missing)}",
            )
        if item.status is KnowledgeStatus.VALIDATED and any(
            source.status is not EvidenceStatus.VALIDATED
            for source in sources
            if source is not None
        ):
            raise KnowledgeError(
                "knowledge_registry.unvalidated_evidence",
                "validated knowledge requires validated evidence metadata",
            )

        self._objects[item.object_id] = item
        return item

    def get(self, object_id: str) -> KnowledgeObject | None:
        return self._objects.get(object_id)

    def require(self, object_id: str) -> KnowledgeObject:
        item = self.get(object_id)
        if item is None:
            raise KnowledgeError(
                "knowledge_registry.unknown",
                f"knowledge object not registered: {object_id}",
            )
        return item

    def all(self) -> tuple[KnowledgeObject, ...]:
        return tuple(self._objects[key] for key in sorted(self._objects))
