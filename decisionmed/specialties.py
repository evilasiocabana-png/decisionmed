"""Specialty composition contracts for DecisionMEd.

This module describes how a specialty identifies the contracts it needs. It
does not contain clinical knowledge, therapeutic rules, or prescribing logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re
from typing import Iterable


_IDENTIFIER_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_SEMANTIC_VERSION_PATTERN = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)


class SpecialtyPackStatus(str, Enum):
    """Lifecycle states for a specialty composition manifest."""

    REFERENCE_ONLY = "reference_only"
    ACTIVE = "active"
    RETIRED = "retired"


class SpecialtyPackRegistryError(ValueError):
    """Base error for registry contract violations."""


class DuplicateSpecialtyPackError(SpecialtyPackRegistryError):
    """Raised when a specialty key is registered more than once."""


class UnknownSpecialtyPackError(SpecialtyPackRegistryError):
    """Raised when a required specialty key is not registered."""


@dataclass(frozen=True, slots=True)
class SpecialtyPack:
    """Immutable composition manifest for one medical specialty.

    The identifiers point to independently governed workflow, safety,
    evidence, knowledge, and audit contracts. They are references only; a pack
    cannot execute clinical decisions.
    """

    key: str
    display_name: str
    version: str
    workflow_contract: str
    safety_contract: str
    evidence_policy: str
    knowledge_namespace: str
    audit_namespace: str
    required_capabilities: tuple[str, ...]
    status: SpecialtyPackStatus = SpecialtyPackStatus.REFERENCE_ONLY

    def __post_init__(self) -> None:
        self._validate_identifier("key", self.key)
        self._validate_text("display_name", self.display_name)

        if not isinstance(self.version, str) or not _SEMANTIC_VERSION_PATTERN.fullmatch(
            self.version
        ):
            raise ValueError("version must use semantic versioning")

        for field_name in (
            "workflow_contract",
            "safety_contract",
            "evidence_policy",
            "knowledge_namespace",
            "audit_namespace",
        ):
            self._validate_identifier(field_name, getattr(self, field_name))

        if isinstance(self.required_capabilities, (str, bytes)):
            raise TypeError("required_capabilities must be an iterable of identifiers")

        capabilities = tuple(self.required_capabilities)
        if not capabilities:
            raise ValueError("required_capabilities cannot be empty")
        for capability in capabilities:
            self._validate_identifier("required_capability", capability)
        if len(set(capabilities)) != len(capabilities):
            raise ValueError("required_capabilities cannot contain duplicates")
        object.__setattr__(self, "required_capabilities", capabilities)

        if not isinstance(self.status, SpecialtyPackStatus):
            raise TypeError("status must be a SpecialtyPackStatus")

    @staticmethod
    def _validate_identifier(field_name: str, value: object) -> None:
        if not isinstance(value, str) or not _IDENTIFIER_PATTERN.fullmatch(value):
            raise ValueError(f"{field_name} must be a canonical lowercase identifier")

    @staticmethod
    def _validate_text(field_name: str, value: object) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} cannot be empty")

    @property
    def is_clinically_active(self) -> bool:
        """Return whether this manifest is cleared for application composition."""

        return self.status is SpecialtyPackStatus.ACTIVE


class SpecialtyPackRegistry:
    """Deterministic registry for specialty composition manifests."""

    def __init__(self, packs: Iterable[SpecialtyPack] = ()) -> None:
        self._packs: dict[str, SpecialtyPack] = {}
        for pack in packs:
            self.register(pack)

    def register(self, pack: SpecialtyPack) -> SpecialtyPack:
        if not isinstance(pack, SpecialtyPack):
            raise TypeError("pack must be a SpecialtyPack")
        if pack.key in self._packs:
            raise DuplicateSpecialtyPackError(
                f"specialty pack already registered: {pack.key}"
            )
        self._packs[pack.key] = pack
        return pack

    def get(self, key: str) -> SpecialtyPack | None:
        return self._packs.get(key)

    def require(self, key: str) -> SpecialtyPack:
        pack = self.get(key)
        if pack is None:
            raise UnknownSpecialtyPackError(f"specialty pack not registered: {key}")
        return pack

    def all(self) -> tuple[SpecialtyPack, ...]:
        return tuple(self._packs[key] for key in sorted(self._packs))


PSYCHIATRY_PACK = SpecialtyPack(
    key="psychiatry",
    display_name="Psiquiatria",
    version="0.1.0",
    workflow_contract="psychrx.clinical-decision.v1",
    safety_contract="psychrx.safety-first.v1",
    evidence_policy="psychrx.evidence-traceability.v1",
    knowledge_namespace="psychrx",
    audit_namespace="decisionmed.psychiatry",
    required_capabilities=(
        "clinical-snapshot",
        "safety",
        "evidence",
        "reasoning",
        "explanation",
        "monitoring",
        "audit",
    ),
    status=SpecialtyPackStatus.REFERENCE_ONLY,
)

def _planned_specialty_pack(key: str, display_name: str) -> SpecialtyPack:
    """Create a structural placeholder with no bound clinical providers."""

    return SpecialtyPack(
        key=key,
        display_name=display_name,
        version="0.1.0",
        workflow_contract=f"decisionmed.{key}.workflow.v1",
        safety_contract=f"decisionmed.{key}.safety.v1",
        evidence_policy="decisionmed.evidence-traceability.v1",
        knowledge_namespace=f"decisionmed.{key}",
        audit_namespace=f"decisionmed.{key}",
        required_capabilities=(
            f"{key}.clinical-snapshot",
            f"{key}.safety",
            f"{key}.evidence",
            f"{key}.reasoning",
            f"{key}.explanation",
            f"{key}.monitoring",
            f"{key}.audit",
        ),
        status=SpecialtyPackStatus.REFERENCE_ONLY,
    )


INTERNAL_MEDICINE_PACK = _planned_specialty_pack(
    "internal-medicine", "Clínica Médica"
)
CARDIOLOGY_PACK = _planned_specialty_pack("cardiology", "Cardiologia")
PEDIATRICS_PACK = _planned_specialty_pack("pediatrics", "Pediatria")
NEUROLOGY_PACK = _planned_specialty_pack("neurology", "Neurologia")
EMERGENCY_PACK = _planned_specialty_pack("emergency", "Emergência")

DEFAULT_SPECIALTY_PACKS = (
    PSYCHIATRY_PACK,
    INTERNAL_MEDICINE_PACK,
    CARDIOLOGY_PACK,
    PEDIATRICS_PACK,
    NEUROLOGY_PACK,
    EMERGENCY_PACK,
)


def build_default_specialty_registry() -> SpecialtyPackRegistry:
    """Build a fresh registry containing the governed default manifests."""

    return SpecialtyPackRegistry(DEFAULT_SPECIALTY_PACKS)
