"""DecisionMEd technology-independent Domain Core."""

from .clinical_snapshot import (
    REQUIRED_SNAPSHOT_SECTIONS,
    ClinicalDataProvenance,
    ClinicalObservation,
    ClinicalSnapshot,
    ClinicalSnapshotSection,
    ClinicalSnapshotStatus,
    SubjectReference,
    clinical_snapshot_fingerprint,
)
from .errors import DomainError, DomainInvariantError, ResultAccessError
from .primitives import BaseEntity, DomainEvent, DomainResult, EntityId, ValueObject
from .repositories import Repository

__all__ = [
    "BaseEntity",
    "ClinicalDataProvenance",
    "ClinicalObservation",
    "ClinicalSnapshot",
    "ClinicalSnapshotSection",
    "ClinicalSnapshotStatus",
    "clinical_snapshot_fingerprint",
    "DomainError",
    "DomainEvent",
    "DomainInvariantError",
    "DomainResult",
    "EntityId",
    "Repository",
    "REQUIRED_SNAPSHOT_SECTIONS",
    "ResultAccessError",
    "SubjectReference",
    "ValueObject",
]
