"""Replay protection contract for safety-review authority decisions."""

from __future__ import annotations

from threading import Lock
from typing import Protocol, runtime_checkable


@runtime_checkable
class SafetyReviewerAuthorityReplayGuard(Protocol):
    """Reserve one exact safety-review authority decision."""

    def reserve(self, *, authority_provider: str, decision_reference: str) -> bool: ...


class InMemorySafetyReviewerAuthorityReplayGuard:
    """Thread-safe local default; production must inject durable storage."""

    def __init__(self) -> None:
        self._reserved: set[tuple[str, str]] = set()
        self._lock = Lock()

    def reserve(self, *, authority_provider: str, decision_reference: str) -> bool:
        key = (authority_provider, decision_reference)
        with self._lock:
            if key in self._reserved:
                return False
            self._reserved.add(key)
            return True
