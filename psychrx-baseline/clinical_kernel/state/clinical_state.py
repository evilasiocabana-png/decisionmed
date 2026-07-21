"""Official structural states for the Clinical Kernel."""

from __future__ import annotations

from enum import Enum


class ClinicalState(str, Enum):
    """Read-only structural states. No clinical transition logic lives here."""

    INITIALIZED = "initialized"
    COLLECTING_INFORMATION = "collecting_information"
    SNAPSHOT_READY = "snapshot_ready"
    SAFETY_PENDING = "safety_pending"
    STRATEGY_BLOCKED = "strategy_blocked"
    MONITORING_PLANNED = "monitoring_planned"
    COMPLETED_READ_ONLY = "completed_read_only"
