"""Reference registry and evidence attachment metadata."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class ReferenceEntry:
    reference_id: str = field(default_factory=lambda: f"REF-{uuid4()}")
    reference_type: str = "not_classified"
    pmid: str = ""
    doi: str = ""
    isbn: str = ""
    guideline_id: str = ""
    book_id: str = ""
    journal: str = ""
    regulatory_source: str = ""
    trace_id: str = field(default_factory=lambda: f"REF-TRC-{uuid4()}")
    status: str = "registered"


@dataclass(frozen=True)
class EvidenceAttachment:
    attachment_id: str = field(default_factory=lambda: f"EATT-{uuid4()}")
    evidence_id: str = ""
    target_field: str = ""
    target_entity_id: str = ""
    interpretation: str = "none"
    trace_id: str = field(default_factory=lambda: f"EATT-TRC-{uuid4()}")


class ReferenceRegistry:
    def __init__(self) -> None:
        self._entries: dict[str, ReferenceEntry] = {}

    def register(self, entry: ReferenceEntry) -> None:
        self._entries[entry.reference_id] = entry

    def list_entries(self) -> tuple[ReferenceEntry, ...]:
        return tuple(self._entries.values())

    def find_duplicates(self) -> tuple[str, ...]:
        seen: set[tuple[str, str, str, str]] = set()
        duplicates: list[str] = []
        for entry in self._entries.values():
            key = (entry.pmid, entry.doi, entry.isbn, entry.guideline_id)
            if key in seen and any(key):
                duplicates.append(entry.reference_id)
            seen.add(key)
        return tuple(duplicates)


class ReferenceValidator:
    allowed_types = {"PMID", "DOI", "ISBN", "Guideline", "Book", "Journal", "Regulatory source"}

    def validate(self, entry: ReferenceEntry) -> tuple[str, ...]:
        issues: list[str] = []
        if entry.reference_type not in self.allowed_types:
            issues.append("invalid_reference_type")
        if not any((entry.pmid, entry.doi, entry.isbn, entry.guideline_id, entry.book_id, entry.journal, entry.regulatory_source)):
            issues.append("missing_identifier")
        if not entry.trace_id:
            issues.append("broken_trace")
        return tuple(issues)

