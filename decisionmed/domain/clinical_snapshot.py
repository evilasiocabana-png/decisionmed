"""Immutable ClinicalSnapshot contracts without clinical reasoning rules."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
import json
import math
import re
from uuid import uuid4

from .errors import DomainInvariantError
from .primitives import EntityId


_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_SUBJECT_REFERENCE = re.compile(r"^sub-[0-9a-f]{32}$")
_VERSION = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


class ClinicalSnapshotSection(str, Enum):
    SYMPTOMS = "symptoms"
    SYNDROMES = "syndromes"
    FUNCTIONING = "functioning"
    QUALITY_OF_LIFE = "quality_of_life"
    CURRENT_MEDICATIONS = "current_medications"
    TREATMENT_HISTORY = "treatment_history"
    ADVERSE_EFFECTS = "adverse_effects"
    COMORBIDITIES = "comorbidities"
    RISK_FACTORS = "risk_factors"
    THERAPEUTIC_CONSTRAINTS = "therapeutic_constraints"
    DIAGNOSTIC_HYPOTHESES = "diagnostic_hypotheses"
    THERAPEUTIC_OBJECTIVES = "therapeutic_objectives"
    SAFETY_ALERTS = "safety_alerts"
    UNCERTAINTIES = "uncertainties"


REQUIRED_SNAPSHOT_SECTIONS = frozenset(ClinicalSnapshotSection)


class ClinicalDataProvenance(str, Enum):
    CLINICIAN_ENTERED = "clinician_entered"
    PATIENT_REPORTED = "patient_reported"
    RECORD_IMPORT = "record_import"
    DEVICE_REPORTED = "device_reported"
    UNKNOWN = "unknown"


class ClinicalSnapshotStatus(str, Enum):
    INCOMPLETE = "incomplete"
    AWAITING_HUMAN_VALIDATION = "awaiting_human_validation"


@dataclass(frozen=True, slots=True)
class SubjectReference:
    """Generated pseudonymous reference; never a name, CPF, email, or record id."""

    value: str = field(default_factory=lambda: f"sub-{uuid4().hex}")

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or not _SUBJECT_REFERENCE.fullmatch(
            self.value
        ):
            raise DomainInvariantError(
                "clinical_snapshot.subject_reference",
                "subject reference must be a generated pseudonymous identifier",
            )

    def __str__(self) -> str:
        return self.value


ClinicalValue = str | int | float | bool


@dataclass(frozen=True, slots=True)
class ClinicalObservation:
    """One sourced value; its meaning is supplied by validated specialty knowledge."""

    observation_id: EntityId
    section: ClinicalSnapshotSection
    field_key: str
    value: ClinicalValue
    provenance: ClinicalDataProvenance
    observed_at: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.observation_id, EntityId):
            raise TypeError("observation_id must be an EntityId")
        if not isinstance(self.section, ClinicalSnapshotSection):
            raise TypeError("section must be a ClinicalSnapshotSection")
        if not isinstance(self.field_key, str) or not _IDENTIFIER.fullmatch(
            self.field_key
        ):
            _fail("field_key", "field key must be canonical")
        if not isinstance(self.provenance, ClinicalDataProvenance):
            raise TypeError("provenance must be a ClinicalDataProvenance")
        _aware_datetime("observed_at", self.observed_at)
        _clinical_value(self.value)


@dataclass(frozen=True, slots=True)
class ClinicalSnapshot:
    """Read-only state at one instant; not a medical record or clinical decision."""

    snapshot_id: EntityId
    lineage_id: EntityId
    subject_reference: SubjectReference
    session_id: EntityId
    specialty_key: str
    captured_at: datetime
    observations: tuple[ClinicalObservation, ...] = ()
    previous_snapshot_id: EntityId | None = None
    trace_id: str = field(default_factory=lambda: f"clinical-snapshot:{uuid4()}")
    version: str = "0.1.0"

    def __post_init__(self) -> None:
        for field_name in ("snapshot_id", "lineage_id", "session_id"):
            if not isinstance(getattr(self, field_name), EntityId):
                raise TypeError(f"{field_name} must be an EntityId")
        if self.previous_snapshot_id is not None and not isinstance(
            self.previous_snapshot_id, EntityId
        ):
            raise TypeError("previous_snapshot_id must be an EntityId or None")
        if self.previous_snapshot_id == self.snapshot_id:
            _fail("previous_snapshot_id", "snapshot cannot reference itself")
        if not isinstance(self.subject_reference, SubjectReference):
            raise TypeError("subject_reference must be a SubjectReference")
        if not isinstance(self.specialty_key, str) or not _IDENTIFIER.fullmatch(
            self.specialty_key
        ):
            _fail("specialty_key", "specialty key must be canonical")
        _aware_datetime("captured_at", self.captured_at)
        if not isinstance(self.trace_id, str) or not self.trace_id.strip():
            _fail("trace_id", "trace id cannot be empty")
        if not isinstance(self.version, str) or not _VERSION.fullmatch(self.version):
            _fail("version", "version must use semantic versioning")

        observations = tuple(self.observations)
        if not all(isinstance(item, ClinicalObservation) for item in observations):
            raise TypeError("observations must contain only ClinicalObservation values")
        observation_ids = tuple(item.observation_id for item in observations)
        if len(set(observation_ids)) != len(observation_ids):
            _fail("observations", "observation ids must be unique")
        if any(item.observed_at > self.captured_at for item in observations):
            _fail("observations", "an observation cannot be newer than its snapshot")
        object.__setattr__(self, "observations", observations)

    @property
    def missing_sections(self) -> tuple[ClinicalSnapshotSection, ...]:
        present = {item.section for item in self.observations}
        return tuple(
            section
            for section in ClinicalSnapshotSection
            if section not in present
        )

    @property
    def structurally_complete(self) -> bool:
        return not self.missing_sections

    @property
    def status(self) -> ClinicalSnapshotStatus:
        if self.structurally_complete:
            return ClinicalSnapshotStatus.AWAITING_HUMAN_VALIDATION
        return ClinicalSnapshotStatus.INCOMPLETE

    @property
    def clinical_execution_allowed(self) -> bool:
        return False

    @property
    def content_fingerprint(self) -> str:
        return clinical_snapshot_fingerprint(self)


def clinical_snapshot_fingerprint(snapshot: ClinicalSnapshot) -> str:
    """Return a deterministic digest of the complete pseudonymous snapshot."""

    if not isinstance(snapshot, ClinicalSnapshot):
        raise TypeError("snapshot must be a ClinicalSnapshot")
    payload = {
        "snapshot_id": str(snapshot.snapshot_id),
        "lineage_id": str(snapshot.lineage_id),
        "subject_reference": str(snapshot.subject_reference),
        "session_id": str(snapshot.session_id),
        "specialty_key": snapshot.specialty_key,
        "captured_at": _canonical_datetime(snapshot.captured_at),
        "observations": [
            {
                "observation_id": str(observation.observation_id),
                "section": observation.section.value,
                "field_key": observation.field_key,
                "value": _canonical_value(observation.value),
                "provenance": observation.provenance.value,
                "observed_at": _canonical_datetime(observation.observed_at),
            }
            for observation in sorted(
                snapshot.observations,
                key=lambda item: str(item.observation_id),
            )
        ],
        "previous_snapshot_id": (
            str(snapshot.previous_snapshot_id)
            if snapshot.previous_snapshot_id is not None
            else None
        ),
        "trace_id": snapshot.trace_id,
        "version": snapshot.version,
    }
    canonical = json.dumps(
        payload,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return sha256(canonical).hexdigest()


def _canonical_datetime(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds")


def _canonical_value(value: ClinicalValue) -> dict[str, ClinicalValue]:
    if isinstance(value, bool):
        value_type = "boolean"
    elif isinstance(value, int):
        value_type = "integer"
    elif isinstance(value, float):
        value_type = "number"
    else:
        value_type = "text"
    return {"type": value_type, "value": value}


def _clinical_value(value: object) -> None:
    if isinstance(value, str):
        if not value.strip() or len(value) > 2000:
            _fail("value", "text values must contain 1 to 2000 characters")
        return
    if isinstance(value, bool):
        return
    if isinstance(value, int):
        return
    if isinstance(value, float) and math.isfinite(value):
        return
    _fail("value", "value must be finite text, integer, number, or boolean")


def _aware_datetime(field_name: str, value: object) -> None:
    if (
        not isinstance(value, datetime)
        or value.tzinfo is None
        or value.utcoffset() is None
    ):
        _fail(field_name, f"{field_name} must include a timezone")
    if value > datetime.now(timezone.utc):
        _fail(field_name, f"{field_name} cannot be in the future")


def _fail(field_name: str, message: str) -> None:
    raise DomainInvariantError(f"clinical_snapshot.{field_name}", message)
