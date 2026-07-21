"""Base object for structured scientific knowledge."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any, Mapping

from knowledge.core.status import KnowledgeStatus
from knowledge.versioning.version import KnowledgeVersion


def _require_text(value: str, field_name: str) -> None:
    if not value.strip():
        raise ValueError(f"{field_name} is required")


@dataclass(frozen=True)
class KnowledgeObject:
    """Technology-independent base for scientific knowledge objects.

    This base stores structural metadata only. It does not contain clinical
    decision logic, therapeutic recommendations, parsing, persistence, or AI.
    """

    identifier: str
    name: str
    version: KnowledgeVersion
    origin: str
    status: KnowledgeStatus = KnowledgeStatus.DRAFT
    metadata: Mapping[str, Any] = field(default_factory=dict)
    references: tuple[str, ...] = ()
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        _require_text(self.identifier, "identifier")
        _require_text(self.name, "name")
        _require_text(self.origin, "origin")
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))
        object.__setattr__(self, "references", tuple(self.references))

    @property
    def is_active(self) -> bool:
        return self.status in {
            KnowledgeStatus.AWAITING_VALIDATION,
            KnowledgeStatus.VALIDATED,
            KnowledgeStatus.CONFLICTING_EVIDENCE,
        }
