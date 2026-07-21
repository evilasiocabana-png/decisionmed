"""Immutable runtime context."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, replace
from typing import Any

from clinical_kernel.context import ClinicalContext


@dataclass(frozen=True)
class RuntimeContext:
    """Runtime context with immutable updates."""

    clinical_context: ClinicalContext = field(default_factory=ClinicalContext.empty)
    loaded_widgets: tuple[str, ...] = field(default_factory=tuple)
    loaded_knowledge: tuple[str, ...] = field(default_factory=tuple)
    active_constraints: tuple[str, ...] = field(default_factory=tuple)
    current_hypothesis: str | None = None
    current_snapshot: str | None = None
    execution_status: str = "not_started"
    metadata: dict[str, Any] = field(default_factory=dict)

    def with_update(self, **changes: Any) -> "RuntimeContext":
        """Return an updated context without mutating this instance."""
        return replace(self, **changes)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
