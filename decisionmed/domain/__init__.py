"""DecisionMEd technology-independent Domain Core."""

from .errors import DomainError, DomainInvariantError, ResultAccessError
from .primitives import BaseEntity, DomainEvent, DomainResult, EntityId, ValueObject
from .repositories import Repository

__all__ = [
    "BaseEntity",
    "DomainError",
    "DomainEvent",
    "DomainInvariantError",
    "DomainResult",
    "EntityId",
    "Repository",
    "ResultAccessError",
    "ValueObject",
]
