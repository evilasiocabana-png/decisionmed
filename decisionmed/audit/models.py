"""Immutable audit records for metadata-only trace reconstruction."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import re

from decisionmed.domain import DomainError


_HASH = re.compile(r"^[0-9a-f]{64}$")


class AuditError(DomainError):
    pass


@dataclass(frozen=True, slots=True)
class AuditRecord:
    sequence: int
    event_id: str
    event_name: str
    aggregate_id: str
    occurred_at: datetime
    payload: tuple[tuple[str, str], ...]
    trace_id: str
    previous_hash: str
    record_hash: str

    def __post_init__(self) -> None:
        if not isinstance(self.sequence, int) or self.sequence < 1:
            raise AuditError("audit.invalid_sequence", "sequence must be positive")
        for field_name in ("event_id", "event_name", "aggregate_id", "trace_id"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise AuditError(f"audit.{field_name}", f"{field_name} cannot be empty")
        if self.occurred_at.tzinfo is None or self.occurred_at.utcoffset() is None:
            raise AuditError("audit.naive_time", "occurred_at must include a timezone")
        payload = tuple(self.payload)
        if not all(
            isinstance(item, tuple)
            and len(item) == 2
            and all(isinstance(value, str) for value in item)
            for item in payload
        ):
            raise AuditError("audit.invalid_payload", "payload must contain string pairs")
        if not _HASH.fullmatch(self.previous_hash):
            raise AuditError("audit.previous_hash", "previous hash must be SHA-256")
        if not _HASH.fullmatch(self.record_hash):
            raise AuditError("audit.record_hash", "record hash must be SHA-256")
        object.__setattr__(self, "payload", payload)
