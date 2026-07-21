"""Replay protection contract for Question Engine authority decisions."""

from __future__ import annotations

from threading import Lock
from typing import Protocol, runtime_checkable


@runtime_checkable
class QuestionEngineInvocationReplayGuard(Protocol):
    """Reserve one exact authority decision before an engine call."""

    def reserve(self, *, authority_provider: str, decision_reference: str) -> bool: ...


class InMemoryQuestionEngineInvocationReplayGuard:
    """Thread-safe default guard for a local process.

    A production composition must inject a durable shared implementation before
    exposing any Question Engine runtime outside this local reference platform.
    """

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
