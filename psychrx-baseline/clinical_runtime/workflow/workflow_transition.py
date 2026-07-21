"""Workflow transition model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkflowTransition:
    """A structural transition between two workflow nodes."""

    origin: str
    destination: str
    condition: str = "structural_sequence"
    status: str = "available_read_only"
    reason: str = "Runtime workflow order only; no clinical condition."

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-safe representation."""
        return {
            "origin": self.origin,
            "destination": self.destination,
            "condition": self.condition,
            "status": self.status,
            "reason": self.reason,
        }

