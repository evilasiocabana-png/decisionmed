"""Typed Clinical Timeline models."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class TimelineMetadata:
    creation_date: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    snapshot_count: int = 0
    knowledge_versions: tuple[str, ...] = field(default_factory=tuple)
    runtime_versions: tuple[str, ...] = field(default_factory=tuple)
    timeline_version: str = "0.1-structural"


@dataclass(frozen=True)
class TimelineNode:
    snapshot_id: str
    timestamp: str
    version: str
    trace_id: str
    snapshot: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TimelineTransition:
    from_snapshot: str
    to_snapshot: str
    category: str = "Metadata"
    change_type: str = "unchanged"
    summary: str = "Structural transition only."


@dataclass(frozen=True)
class TimelineEvent:
    event_id: str
    event_type: str
    snapshot_id: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass(frozen=True)
class TimelineStatistics:
    snapshot_count: int = 0
    transition_count: int = 0
    event_count: int = 0


@dataclass(frozen=True)
class TimelineSummary:
    text: str = "Timeline summary is descriptive and non-interpretive."
    transition_summaries: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ClinicalTimeline:
    timeline_id: str = field(default_factory=lambda: f"TML-{uuid4()}")
    patient_id: str = "not_bound"
    snapshots: tuple[TimelineNode, ...] = field(default_factory=tuple)
    transitions: tuple[TimelineTransition, ...] = field(default_factory=tuple)
    events: tuple[TimelineEvent, ...] = field(default_factory=tuple)
    metadata: TimelineMetadata = field(default_factory=TimelineMetadata)
    statistics: TimelineStatistics = field(default_factory=TimelineStatistics)
    current_snapshot: str = ""
    version: str = "0.1-structural"
    trace_id: str = field(default_factory=lambda: f"TML-TRC-{uuid4()}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
