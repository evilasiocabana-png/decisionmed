"""Append-only, tamper-evident in-memory audit ledger."""

from __future__ import annotations

from collections.abc import Iterable
from hashlib import sha256
import json
import re

from decisionmed.domain import DomainEvent

from .models import AuditError, AuditRecord


GENESIS_HASH = "0" * 64
_METADATA_KEY = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")


class AuditLedger:
    """Runtime trace only; not persistent or medico-legal storage."""

    def __init__(self) -> None:
        self._records: list[AuditRecord] = []
        self._event_ids: set[str] = set()

    def append(self, event: DomainEvent, trace_id: str) -> AuditRecord:
        if not isinstance(event, DomainEvent):
            raise TypeError("event must be a DomainEvent")
        if not isinstance(trace_id, str) or not trace_id.strip() or len(trace_id) > 200:
            raise AuditError("audit.trace_id", "trace id is invalid")
        if event.event_id in self._event_ids:
            raise AuditError("audit.duplicate_event", "event is already recorded")
        if len(event.aggregate_id) > 200:
            raise AuditError("audit.aggregate_id", "aggregate id is too long")
        payload = _safe_metadata(event.payload)
        sequence = len(self._records) + 1
        previous_hash = self._records[-1].record_hash if self._records else GENESIS_HASH
        record_hash = _calculate_hash(
            sequence=sequence,
            event_id=event.event_id,
            event_name=event.name,
            aggregate_id=event.aggregate_id,
            occurred_at=event.occurred_at.isoformat(),
            payload=payload,
            trace_id=trace_id,
            previous_hash=previous_hash,
        )
        record = AuditRecord(
            sequence=sequence,
            event_id=event.event_id,
            event_name=event.name,
            aggregate_id=event.aggregate_id,
            occurred_at=event.occurred_at,
            payload=payload,
            trace_id=trace_id,
            previous_hash=previous_hash,
            record_hash=record_hash,
        )
        self._records.append(record)
        self._event_ids.add(event.event_id)
        return record

    def records(self) -> tuple[AuditRecord, ...]:
        return tuple(self._records)

    def verify(self) -> bool:
        return verify_chain(self._records)


def verify_chain(records: Iterable[AuditRecord]) -> bool:
    """Verify ordering, links, and content hashes without modifying records."""

    previous_hash = GENESIS_HASH
    for expected_sequence, record in enumerate(records, 1):
        if not isinstance(record, AuditRecord):
            return False
        if record.sequence != expected_sequence or record.previous_hash != previous_hash:
            return False
        expected_hash = _calculate_hash(
            sequence=record.sequence,
            event_id=record.event_id,
            event_name=record.event_name,
            aggregate_id=record.aggregate_id,
            occurred_at=record.occurred_at.isoformat(),
            payload=record.payload,
            trace_id=record.trace_id,
            previous_hash=record.previous_hash,
        )
        if record.record_hash != expected_hash:
            return False
        previous_hash = record.record_hash
    return True


def _safe_metadata(payload: tuple[tuple[str, str], ...]) -> tuple[tuple[str, str], ...]:
    for key, value in payload:
        if not _METADATA_KEY.fullmatch(key):
            raise AuditError("audit.metadata_key", "metadata keys must be canonical")
        if not value or len(value) > 200:
            raise AuditError(
                "audit.metadata_value", "metadata values must contain 1 to 200 characters"
            )
    return tuple(payload)


def _calculate_hash(**values: object) -> str:
    canonical = json.dumps(
        values, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256(canonical).hexdigest()
