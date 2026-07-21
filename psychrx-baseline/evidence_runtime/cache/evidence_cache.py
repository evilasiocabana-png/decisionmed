"""Version-aware read-only cache abstraction."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvidenceCache:
    """In-memory cache placeholder for future pluggable stores."""

    _items: dict[str, Any] = field(default_factory=dict)

    def key(self, evidence_id: str, version: str) -> str:
        return f"{evidence_id}:{version}"

    def get(self, evidence_id: str, version: str) -> Any:
        return self._items.get(self.key(evidence_id, version))

    def put(self, evidence_id: str, version: str, value: Any) -> None:
        self._items[self.key(evidence_id, version)] = value
