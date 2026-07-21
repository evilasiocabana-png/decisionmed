"""Immutable models for the Digital Clinical Twin Platform."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, replace
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class TwinVersion:
    major: int = 0
    minor: int = 1
    patch: int = 0
    lineage: tuple[str, ...] = field(default_factory=tuple)
    branch_history: tuple[str, ...] = field(default_factory=tuple)

    def value(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


@dataclass(frozen=True)
class TwinMetadata:
    created_at: str = field(default_factory=_now)
    snapshot_count: int = 0
    timeline_version: str = ""
    knowledge_version: str = ""
    operating_mind_version: str = ""
    builder_version: str = "0.1.0"


@dataclass(frozen=True)
class TwinState:
    state_id: str = field(default_factory=lambda: f"TWIN-STATE-{uuid4()}")
    name: str = "computational_state"
    snapshot_reference: str = ""
    quality_reference: str = ""
    operating_mind_reference: str = ""


@dataclass(frozen=True)
class TwinTransition:
    transition_id: str = field(default_factory=lambda: f"TWIN-TRN-{uuid4()}")
    category: str = "Timeline"
    source_state: str = ""
    target_state: str = ""
    trace_id: str = field(default_factory=lambda: f"TWIN-TRC-{uuid4()}")


@dataclass(frozen=True)
class TwinStatistics:
    snapshot_count: int = 0
    transition_count: int = 0
    quality_events: int = 0
    stability_score: float = 1.0


@dataclass(frozen=True)
class TwinSummary:
    current_state: str = ""
    history: tuple[str, ...] = field(default_factory=tuple)
    major_transitions: tuple[str, ...] = field(default_factory=tuple)
    quality_overview: str = "structural"
    stability_overview: str = "structural"


@dataclass(frozen=True)
class DigitalClinicalTwin:
    twin_id: str = field(default_factory=lambda: f"DCT-{uuid4()}")
    patient_reference: str = "abstract_patient_reference"
    timeline_reference: str = ""
    snapshot_history: tuple[str, ...] = field(default_factory=tuple)
    current_state: TwinState = field(default_factory=TwinState)
    state_transitions: tuple[TwinTransition, ...] = field(default_factory=tuple)
    stability_profile: tuple[str, ...] = field(default_factory=tuple)
    quality_history: tuple[str, ...] = field(default_factory=tuple)
    knowledge_versions: tuple[str, ...] = field(default_factory=tuple)
    metadata: TwinMetadata = field(default_factory=TwinMetadata)
    version: TwinVersion = field(default_factory=TwinVersion)
    trace_id: str = field(default_factory=lambda: f"DCT-TRC-{uuid4()}")
    read_only_mode: bool = True

    def with_update(self, **changes: Any) -> "DigitalClinicalTwin":
        return replace(self, **changes)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

