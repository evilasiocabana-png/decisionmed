"""Navigation trace."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class NavigationTrace:
    trace_id: str = field(default_factory=lambda: f"NAV-TRACE-{uuid4()}")
    snapshot_id: str = ""
    timeline_id: str = ""
    runtime_trace: str = ""
    workspace_session: str = ""
    navigation_session: str = ""
