"""Technology-independent errors for the DecisionMEd Domain Layer."""

from __future__ import annotations


class DomainError(Exception):
    """Base error with a stable, machine-readable code."""

    def __init__(self, code: str, message: str) -> None:
        if not isinstance(code, str) or not code.strip():
            raise ValueError("domain error code cannot be empty")
        if not isinstance(message, str) or not message.strip():
            raise ValueError("domain error message cannot be empty")
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


class DomainInvariantError(DomainError):
    """Raised when a technical domain invariant is violated."""


class ResultAccessError(DomainError):
    """Raised when a caller reads the unavailable side of a result."""
