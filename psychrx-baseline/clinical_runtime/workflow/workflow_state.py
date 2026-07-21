"""Structural workflow states for the Clinical Runtime."""

from __future__ import annotations

from enum import Enum


class WorkflowState(str, Enum):
    """Runtime workflow states with no clinical meaning."""

    NOT_STARTED = "not_started"
    READY = "ready"
    RUNNING = "running"
    WAITING = "waiting"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    READ_ONLY = "read_only"

