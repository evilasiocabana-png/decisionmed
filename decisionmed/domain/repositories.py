"""Persistence-independent repository contracts for the Domain Layer."""

from __future__ import annotations

from typing import Protocol, TypeVar, runtime_checkable

from .primitives import BaseEntity


IdentifierT = TypeVar("IdentifierT")
EntityT = TypeVar("EntityT", bound=BaseEntity[object])


@runtime_checkable
class Repository(Protocol[IdentifierT, EntityT]):
    """Minimum collection-like contract; concrete storage lives elsewhere."""

    def get(self, entity_id: IdentifierT) -> EntityT | None: ...

    def add(self, entity: EntityT) -> None: ...
