"""Structural ClinicalContext for the future Clinical Kernel."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class ClinicalContext:
    """Shared structural state between application, workspace, and future engines."""

    patient_context: dict[str, Any] = field(default_factory=dict)
    clinical_snapshot: dict[str, Any] = field(default_factory=dict)
    medications: tuple[str, ...] = field(default_factory=tuple)
    investigation: dict[str, Any] = field(default_factory=dict)
    risks: dict[str, Any] = field(default_factory=dict)
    objectives: tuple[str, ...] = field(default_factory=tuple)
    strategies: tuple[str, ...] = field(default_factory=tuple)
    monitoring: dict[str, Any] = field(default_factory=dict)
    explanations: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-safe structural representation."""
        return asdict(self)

    @classmethod
    def empty(cls) -> "ClinicalContext":
        """Return an empty read-only context."""
        return cls(metadata={"mode": "read-only", "clinical_logic": "not_implemented"})
