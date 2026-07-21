"""Official lifecycle status values for structured knowledge."""

from enum import StrEnum


class KnowledgeStatus(StrEnum):
    """Lifecycle status for a knowledge object."""

    DRAFT = "draft"
    AWAITING_VALIDATION = "awaiting_validation"
    VALIDATED = "validated"
    CONFLICTING_EVIDENCE = "conflicting_evidence"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"
