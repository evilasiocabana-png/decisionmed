"""Structural primitives for the technology-independent Domain Layer.

This module contains no clinical entity, knowledge, recommendation, or rule.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
import re
from typing import Generic, TypeVar, cast
from uuid import uuid4

from .errors import DomainError, DomainInvariantError, ResultAccessError


_EVENT_NAME = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_MISSING = object()
IdentifierT = TypeVar("IdentifierT")
ValueT = TypeVar("ValueT")


@dataclass(frozen=True, slots=True)
class EntityId:
    """Opaque, immutable identifier without persistence assumptions."""

    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or not self.value.strip():
            raise DomainInvariantError("entity_id.empty", "entity id cannot be empty")
        if len(self.value) > 200:
            raise DomainInvariantError("entity_id.too_long", "entity id is too long")

    def __str__(self) -> str:
        return self.value


class BaseEntity(Generic[IdentifierT]):
    """Entity equality is based on concrete type and stable identity."""

    __slots__ = ("_id",)

    def __init__(self, entity_id: IdentifierT) -> None:
        if entity_id is None:
            raise DomainInvariantError("entity.id_missing", "entity id is required")
        object.__setattr__(self, "_id", entity_id)

    @property
    def id(self) -> IdentifierT:
        return self._id

    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and self.id == cast(BaseEntity[object], other).id

    def __hash__(self) -> int:
        return hash((type(self), self.id))


class ValueObject(ABC):
    """Base equality contract for immutable structural value objects."""

    __slots__ = ()

    @property
    @abstractmethod
    def components(self) -> tuple[object, ...]:
        """Return immutable components that define value equality."""

    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and self.components == cast(
            ValueObject, other
        ).components

    def __hash__(self) -> int:
        return hash((type(self), self.components))


@dataclass(frozen=True, slots=True)
class DomainEvent:
    """Immutable, metadata-only fact emitted by the domain."""

    name: str
    aggregate_id: str
    payload: tuple[tuple[str, str], ...] = ()
    event_id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not _EVENT_NAME.fullmatch(self.name):
            raise DomainInvariantError(
                "domain_event.invalid_name", "event name must be canonical"
            )
        if not isinstance(self.aggregate_id, str) or not self.aggregate_id.strip():
            raise DomainInvariantError(
                "domain_event.aggregate_missing", "aggregate id is required"
            )
        payload = tuple(self.payload)
        if any(
            not isinstance(item, tuple)
            or len(item) != 2
            or not all(isinstance(value, str) for value in item)
            for item in payload
        ):
            raise DomainInvariantError(
                "domain_event.invalid_payload", "payload must contain string pairs"
            )
        if len({key for key, _ in payload}) != len(payload):
            raise DomainInvariantError(
                "domain_event.duplicate_payload_key", "payload keys must be unique"
            )
        if not isinstance(self.event_id, str) or not self.event_id.strip():
            raise DomainInvariantError(
                "domain_event.id_missing", "event id is required"
            )
        if self.occurred_at.tzinfo is None or self.occurred_at.utcoffset() is None:
            raise DomainInvariantError(
                "domain_event.naive_time", "event time must include a timezone"
            )
        object.__setattr__(self, "payload", payload)


@dataclass(frozen=True, slots=True)
class DomainResult(Generic[ValueT]):
    """Explicit success/failure result without hidden fallback behavior."""

    _value: object = _MISSING
    _error: DomainError | None = None

    def __post_init__(self) -> None:
        has_value = self._value is not _MISSING
        has_error = self._error is not None
        if has_value == has_error:
            raise DomainInvariantError(
                "result.invalid_state", "result must contain value or error, exclusively"
            )
        if has_error and not isinstance(self._error, DomainError):
            raise TypeError("error must be a DomainError")

    @classmethod
    def success(cls, value: ValueT) -> DomainResult[ValueT]:
        return cls(_value=value)

    @classmethod
    def failure(cls, error: DomainError) -> DomainResult[ValueT]:
        if not isinstance(error, DomainError):
            raise TypeError("error must be a DomainError")
        return cls(_error=error)

    @property
    def is_success(self) -> bool:
        return self._error is None

    @property
    def is_failure(self) -> bool:
        return not self.is_success

    @property
    def value(self) -> ValueT:
        if self.is_failure:
            raise ResultAccessError(
                "result.value_unavailable", "failed result has no value"
            )
        return cast(ValueT, self._value)

    @property
    def error(self) -> DomainError:
        if self.is_success:
            raise ResultAccessError(
                "result.error_unavailable", "successful result has no error"
            )
        return cast(DomainError, self._error)
