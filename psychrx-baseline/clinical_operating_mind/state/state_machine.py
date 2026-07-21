"""Explicit state machine for Clinical Operating Mind."""

from __future__ import annotations


class OperatingMindStateMachine:
    """Allows only explicit structural transitions."""

    ALLOWED: dict[str, tuple[str, ...]] = {
        "idle": ("context_loaded", "error"),
        "context_loaded": ("safety_checked", "blocked", "error"),
        "safety_checked": ("evidence_resolved", "blocked", "error"),
        "evidence_resolved": ("hypotheses_generated", "blocked", "error"),
        "hypotheses_generated": ("explained", "blocked", "error"),
        "explained": ("snapshot_created", "blocked", "error"),
        "snapshot_created": ("timeline_updated", "blocked", "error"),
        "timeline_updated": ("navigation_ready", "blocked", "error"),
        "navigation_ready": ("navigation_ready",),
        "blocked": ("explained", "snapshot_created", "timeline_updated", "navigation_ready"),
        "error": ("error",),
    }

    def can_transition(self, source: str, target: str) -> bool:
        return target in self.ALLOWED.get(source, ())

    def transition(self, source: str, target: str) -> str:
        if not self.can_transition(source, target):
            raise ValueError(f"Invalid Clinical Operating Mind transition: {source}->{target}")
        return target

