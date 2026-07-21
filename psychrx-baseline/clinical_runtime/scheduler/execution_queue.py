"""Runtime execution queue."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

from clinical_runtime.scheduler.runtime_scheduler import ScheduledItem


@dataclass
class ExecutionQueue:
    """FIFO queue for structural execution."""

    _items: deque[ScheduledItem] = field(default_factory=deque)

    def push(self, item: ScheduledItem) -> None:
        self._items.append(item)

    def pop(self) -> ScheduledItem | None:
        if not self._items:
            return None
        return self._items.popleft()

    def snapshot(self) -> tuple[ScheduledItem, ...]:
        return tuple(self._items)
