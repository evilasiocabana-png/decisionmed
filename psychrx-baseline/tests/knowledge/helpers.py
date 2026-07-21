"""Test helpers for the Knowledge Layer."""

from knowledge.core.knowledge_object import KnowledgeObject
from knowledge.core.status import KnowledgeStatus
from knowledge.versioning.version import KnowledgeVersion


def build_knowledge_object(
    identifier: str = "knowledge.test",
    name: str = "Test Knowledge Object",
    origin: str = "test-suite",
    status: KnowledgeStatus = KnowledgeStatus.DRAFT,
    references: tuple[str, ...] = (),
) -> KnowledgeObject:
    return KnowledgeObject(
        identifier=identifier,
        name=name,
        version=KnowledgeVersion(0, 1, 0),
        origin=origin,
        status=status,
        references=references,
        metadata={"fixture": True},
    )
