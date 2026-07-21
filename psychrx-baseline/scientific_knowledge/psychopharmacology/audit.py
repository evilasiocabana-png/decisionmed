"""Audit and replay support for psychopharmacology metadata packages."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class DrugAuditEvent:
    event_id: str = field(default_factory=lambda: f"DAUD-{uuid4()}")
    package_id: str = ""
    event_type: str = "registration"
    trace_id: str = field(default_factory=lambda: f"DAUD-TRC-{uuid4()}")
    timestamp: str = field(default_factory=_now)
    read_only_mode: bool = True


class DrugAuditLog:
    def __init__(self) -> None:
        self._events: list[DrugAuditEvent] = []

    def record(self, event: DrugAuditEvent) -> None:
        self._events.append(event)

    def list_events(self) -> tuple[DrugAuditEvent, ...]:
        return tuple(self._events)


class DrugReplaySupport:
    def replay(self, events: tuple[DrugAuditEvent, ...]) -> tuple[str, ...]:
        return tuple(f"{event.timestamp}:{event.package_id}:{event.event_type}:{event.trace_id}" for event in events)

