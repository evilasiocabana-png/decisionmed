"""Twin audit."""

from __future__ import annotations


class TwinAudit:
    def __init__(self) -> None:
        self._events: list[str] = []

    def record(self, event: str) -> None:
        self._events.append(event)

    def snapshot(self) -> tuple[str, ...]:
        return tuple(self._events)

