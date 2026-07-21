"""Runtime scheduler."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, order=True)
class ScheduledItem:
    priority: int
    name: str = field(compare=False)
    dependencies: tuple[str, ...] = field(default_factory=tuple, compare=False)
    blocked: bool = field(default=False, compare=False)


class RuntimeScheduler:
    """Schedules structural execution by priority and dependencies."""

    def order(self, items: tuple[ScheduledItem, ...]) -> tuple[ScheduledItem, ...]:
        return tuple(sorted(items))
