"""PsychRx Knowledge Layer.

This package contains the technology-independent platform infrastructure for
structured clinical knowledge.

Sprint 8 defines contracts, base objects, validation, versioning, schemas, and
test infrastructure only. Real scientific content belongs in psychrx-knowledge.

No populated guidelines, evidence content, clinical rules, recommendation logic,
parsing, AI loading, persistence, database access, or framework integrations
belong here at this stage.
"""

__all__ = [
    "core",
    "loaders",
    "models",
    "repositories",
    "validators",
    "versioning",
]
