"""Typed runtime event bus."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable
from uuid import uuid4


@dataclass(frozen=True)
class RuntimeEvent:
    name: str
    payload: dict[str, object] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: f"EVT-{uuid4()}")


Subscriber = Callable[[RuntimeEvent], None]


class RuntimeEventBus:
    """In-process event bus with no external libraries."""

    def __init__(self) -> None:
        self._subscribers: dict[str, list[Subscriber]] = {}

    def subscribe(self, event_name: str, subscriber: Subscriber) -> None:
        self._subscribers.setdefault(event_name, []).append(subscriber)

    def unsubscribe(self, event_name: str, subscriber: Subscriber) -> None:
        subscribers = self._subscribers.get(event_name, [])
        if subscriber in subscribers:
            subscribers.remove(subscriber)

    def publish(self, event: RuntimeEvent) -> None:
        for subscriber in tuple(self._subscribers.get(event.name, [])):
            subscriber(event)
