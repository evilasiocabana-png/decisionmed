"""Scientific audit log."""

from __future__ import annotations


class ScientificAudit:
    def __init__(self) -> None:
        self._events: list[str] = []

    def record(self, event: str) -> None:
        self._events.append(event)

    def snapshot(self) -> tuple[str, ...]:
        return tuple(self._events)

