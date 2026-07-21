"""Composition of exact clinical and governed knowledge reasoning inputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
import json
import re

from .gate import ReasoningError
from .input import ReasoningInputEnvelope
from .knowledge_binding import ReasoningKnowledgeBinding


_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_VERSION = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


@dataclass(frozen=True, slots=True)
class GovernedReasoningInput:
    """Complete governed input identity, still lacking an executable engine."""

    input_id: str
    contract_version: str
    assembled_at: datetime
    envelope: ReasoningInputEnvelope = field(repr=False)
    knowledge_binding: ReasoningKnowledgeBinding = field(repr=False)
    content_fingerprint: str = field(init=False)

    def __post_init__(self) -> None:
        if not isinstance(self.input_id, str) or not _IDENTIFIER.fullmatch(
            self.input_id
        ):
            _fail("input_id", "input id must be canonical")
        if (
            not isinstance(self.contract_version, str)
            or not _VERSION.fullmatch(self.contract_version)
        ):
            _fail("contract_version", "contract version must use semantic versioning")
        if not isinstance(self.envelope, ReasoningInputEnvelope):
            raise TypeError("envelope must be a ReasoningInputEnvelope")
        if not isinstance(self.knowledge_binding, ReasoningKnowledgeBinding):
            raise TypeError("knowledge_binding must be a ReasoningKnowledgeBinding")
        if (
            not isinstance(self.assembled_at, datetime)
            or self.assembled_at.tzinfo is None
            or self.assembled_at.utcoffset() is None
        ):
            raise TypeError("assembled_at must be a timezone-aware datetime")
        if self.assembled_at > datetime.now(timezone.utc):
            _fail("assembled_at", "assembly time cannot be in the future")
        if self.assembled_at < self.envelope.prepared_at:
            _fail("assembled_at", "assembly cannot predate the clinical envelope")
        if self.assembled_at < self.knowledge_binding.bound_at:
            _fail("assembled_at", "assembly cannot predate the knowledge binding")
        if (
            self.envelope.snapshot.specialty_key
            != self.knowledge_binding.specialty_key
        ):
            _fail(
                "specialty_mismatch",
                "clinical and knowledge inputs must share a specialty",
            )
        if not self.knowledge_binding.knowledge_binding_complete:
            _fail(
                "knowledge_expired",
                "knowledge and evidence review must remain current at assembly",
            )
        object.__setattr__(self, "content_fingerprint", self._fingerprint())

    @property
    def trace_id(self) -> str:
        return self.envelope.trace_id

    @property
    def specialty_key(self) -> str:
        return self.envelope.snapshot.specialty_key

    @property
    def snapshot_fingerprint(self) -> str:
        return self.envelope.snapshot_fingerprint

    @property
    def safety_assessment_fingerprint(self) -> str:
        return self.envelope.safety_assessment_fingerprint

    @property
    def knowledge_binding_fingerprint(self) -> str:
        return self.knowledge_binding.content_fingerprint

    @property
    def knowledge_binding_complete(self) -> bool:
        return self.knowledge_binding.knowledge_binding_complete

    @property
    def engine_contract_present(self) -> bool:
        return False

    @property
    def engine_invocation_allowed(self) -> bool:
        return False

    @property
    def reasoning_execution_allowed(self) -> bool:
        return False

    @property
    def clinical_execution_allowed(self) -> bool:
        return False

    def _fingerprint(self) -> str:
        payload = {
            "input_id": self.input_id,
            "contract_version": self.contract_version,
            "envelope_id": self.envelope.envelope_id,
            "envelope_contract_version": self.envelope.contract_version,
            "producer": self.envelope.producer,
            "trace_id": self.envelope.trace_id,
            "snapshot_fingerprint": self.envelope.snapshot_fingerprint,
            "safety_assessment_fingerprint": (
                self.envelope.safety_assessment_fingerprint
            ),
            "safety_review_fingerprint": (
                self.envelope.safety_review.assessment_fingerprint
            ),
            "gate_status": self.envelope.gate_result.status.value,
            "knowledge_binding_fingerprint": (
                self.knowledge_binding.content_fingerprint
            ),
            "catalog_id": self.knowledge_binding.catalog_id,
            "catalog_version": self.knowledge_binding.catalog_version,
            "specialty_key": self.knowledge_binding.specialty_key,
        }
        canonical = json.dumps(
            payload,
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return sha256(canonical).hexdigest()


def _fail(field_name: str, message: str) -> None:
    raise ReasoningError(f"governed_reasoning_input.{field_name}", message)
