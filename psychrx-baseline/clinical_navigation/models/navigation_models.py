"""Typed models for immutable Clinical Navigation state."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, replace
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class NavigationContext:
    patient_context: str = ""
    snapshot_context: str = ""
    timeline_context: str = ""
    runtime_context: str = ""
    selection_context: str = ""


@dataclass(frozen=True)
class NavigationRoute:
    source: str
    target: str
    artifact_id: str = ""
    valid: bool = True


@dataclass(frozen=True)
class Breadcrumb:
    label: str
    route: NavigationRoute


@dataclass(frozen=True)
class DeepLink:
    target_type: str
    target_id: str
    route: NavigationRoute


@dataclass(frozen=True)
class NavigationEvent:
    event_type: str
    target_id: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    trace_id: str = field(default_factory=lambda: f"NAV-EVT-{uuid4()}")


@dataclass(frozen=True)
class NavigationHistory:
    entries: tuple[NavigationRoute, ...] = field(default_factory=tuple)
    cursor: int = -1

    def push(self, route: NavigationRoute) -> "NavigationHistory":
        entries = self.entries[: self.cursor + 1] + (route,)
        return NavigationHistory(entries=entries, cursor=len(entries) - 1)

    def back(self) -> "NavigationHistory":
        return replace(self, cursor=max(-1, self.cursor - 1))

    def forward(self) -> "NavigationHistory":
        return replace(self, cursor=min(len(self.entries) - 1, self.cursor + 1))

    def current(self) -> NavigationRoute | None:
        if 0 <= self.cursor < len(self.entries):
            return self.entries[self.cursor]
        return None


@dataclass(frozen=True)
class ClinicalNavigationState:
    navigation_id: str = field(default_factory=lambda: f"NAV-{uuid4()}")
    current_context: NavigationContext = field(default_factory=NavigationContext)
    active_snapshot: str = ""
    active_timeline_node: str = ""
    active_widget: str = ""
    selected_hypothesis: str = ""
    selected_evidence: str = ""
    selected_alert: str = ""
    selected_explanation: str = ""
    breadcrumbs: tuple[Breadcrumb, ...] = field(default_factory=tuple)
    history: NavigationHistory = field(default_factory=NavigationHistory)
    highlighted_references: tuple[str, ...] = field(default_factory=tuple)
    trace_id: str = field(default_factory=lambda: f"NAV-TRC-{uuid4()}")

    def with_update(self, **changes: Any) -> "ClinicalNavigationState":
        return replace(self, **changes)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
