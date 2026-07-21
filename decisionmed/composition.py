"""Safe application composition for DecisionMEd specialty packs.

The resolver binds structural capability identifiers to provider descriptors.
It never calls clinical engines and cannot authorize clinical execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re
from typing import Iterable

from .specialties import (
    SpecialtyPack,
    SpecialtyPackRegistry,
    SpecialtyPackStatus,
)


_IDENTIFIER_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_SEMANTIC_VERSION_PATTERN = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)


class SpecialtyLoadStatus(str, Enum):
    """Non-clinical states produced by the composition resolver."""

    BLOCKED = "blocked"
    REFERENCE_ONLY = "reference_only"
    READY_FOR_VALIDATION = "ready_for_validation"


class DuplicateCapabilityBindingError(ValueError):
    """Raised when two providers claim the same capability identifier."""


@dataclass(frozen=True, slots=True)
class CapabilityBinding:
    """Versioned descriptor for one structural platform capability."""

    capability: str
    provider: str
    version: str

    def __post_init__(self) -> None:
        for field_name in ("capability", "provider"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not _IDENTIFIER_PATTERN.fullmatch(value):
                raise ValueError(
                    f"{field_name} must be a canonical lowercase identifier"
                )
        if not isinstance(self.version, str) or not _SEMANTIC_VERSION_PATTERN.fullmatch(
            self.version
        ):
            raise ValueError("version must use semantic versioning")


@dataclass(frozen=True, slots=True)
class SpecialtyLoadResult:
    """Auditable result of resolving a pack without executing it."""

    pack: SpecialtyPack
    status: SpecialtyLoadStatus
    bindings: tuple[CapabilityBinding, ...]
    missing_capabilities: tuple[str, ...]
    incompatible_capabilities: tuple[str, ...]
    blocking_reasons: tuple[str, ...]
    trace_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.pack, SpecialtyPack):
            raise TypeError("pack must be a SpecialtyPack")
        if not isinstance(self.status, SpecialtyLoadStatus):
            raise TypeError("status must be a SpecialtyLoadStatus")

        bindings = tuple(self.bindings)
        missing = tuple(self.missing_capabilities)
        incompatible = tuple(self.incompatible_capabilities)
        reasons = tuple(self.blocking_reasons)
        if not all(isinstance(binding, CapabilityBinding) for binding in bindings):
            raise TypeError("bindings must contain only CapabilityBinding values")
        if len({binding.capability for binding in bindings}) != len(bindings):
            raise ValueError("bindings cannot contain duplicate capabilities")
        for capability in missing + incompatible:
            if not isinstance(capability, str) or not _IDENTIFIER_PATTERN.fullmatch(
                capability
            ):
                raise ValueError(
                    "capability failures must contain canonical identifiers"
                )
        if set(missing).intersection(incompatible):
            raise ValueError("a capability cannot be both missing and incompatible")
        if {binding.capability for binding in bindings}.intersection(
            set(missing) | set(incompatible)
        ):
            raise ValueError("a failed capability cannot be bound")
        if (missing or incompatible) and self.status is not SpecialtyLoadStatus.BLOCKED:
            raise ValueError("capability failures require blocked status")
        if self.status is SpecialtyLoadStatus.BLOCKED and not reasons:
            raise ValueError("blocked status requires at least one reason")
        if not all(isinstance(reason, str) and reason for reason in reasons):
            raise ValueError("blocking_reasons must contain non-empty strings")
        if not isinstance(self.trace_id, str) or not self.trace_id:
            raise ValueError("trace_id cannot be empty")

        object.__setattr__(self, "bindings", bindings)
        object.__setattr__(self, "missing_capabilities", missing)
        object.__setattr__(self, "incompatible_capabilities", incompatible)
        object.__setattr__(self, "blocking_reasons", reasons)

    @property
    def clinical_execution_allowed(self) -> bool:
        """DM-002 never authorizes a clinical execution path."""

        return False


class SpecialtyPackResolver:
    """Resolve a registered pack against versioned capability descriptors."""

    def __init__(self, bindings: Iterable[CapabilityBinding]) -> None:
        self._bindings: dict[str, CapabilityBinding] = {}
        for binding in bindings:
            if not isinstance(binding, CapabilityBinding):
                raise TypeError("binding must be a CapabilityBinding")
            if binding.capability in self._bindings:
                raise DuplicateCapabilityBindingError(
                    f"capability already bound: {binding.capability}"
                )
            self._bindings[binding.capability] = binding

    def load(
        self, registry: SpecialtyPackRegistry, specialty_key: str
    ) -> SpecialtyLoadResult:
        """Load and resolve a registered specialty by canonical key."""

        if not isinstance(registry, SpecialtyPackRegistry):
            raise TypeError("registry must be a SpecialtyPackRegistry")
        return self.resolve(registry.require(specialty_key))

    def resolve(self, pack: SpecialtyPack) -> SpecialtyLoadResult:
        """Resolve provider metadata and return explicit safety gates."""

        if not isinstance(pack, SpecialtyPack):
            raise TypeError("pack must be a SpecialtyPack")

        missing = tuple(
            requirement.capability
            for requirement in pack.capability_requirements
            if requirement.capability not in self._bindings
        )
        incompatible = tuple(
            requirement.capability
            for requirement in pack.capability_requirements
            if requirement.capability in self._bindings
            and self._bindings[requirement.capability].version
            != requirement.required_version
        )
        bindings = tuple(
            self._bindings[requirement.capability]
            for requirement in pack.capability_requirements
            if requirement.capability in self._bindings
            and self._bindings[requirement.capability].version
            == requirement.required_version
        )
        trace_id = f"{pack.audit_namespace}:{pack.key}:{pack.version}"

        if missing or incompatible:
            status = SpecialtyLoadStatus.BLOCKED
            missing_reasons = tuple(f"missing_capability:{item}" for item in missing)
            incompatible_reasons = tuple(
                "incompatible_capability:"
                f"{requirement.capability}:required={requirement.required_version}:"
                f"found={self._bindings[requirement.capability].version}"
                for requirement in pack.capability_requirements
                if requirement.capability in incompatible
            )
            reasons = missing_reasons + incompatible_reasons
        elif pack.status is SpecialtyPackStatus.RETIRED:
            status = SpecialtyLoadStatus.BLOCKED
            reasons = ("pack_status:retired",)
        elif pack.status is SpecialtyPackStatus.REFERENCE_ONLY:
            status = SpecialtyLoadStatus.REFERENCE_ONLY
            reasons = ("pack_status:reference_only",)
        else:
            status = SpecialtyLoadStatus.READY_FOR_VALIDATION
            reasons = ("clinical_activation_gate:not_implemented",)

        return SpecialtyLoadResult(
            pack=pack,
            status=status,
            bindings=bindings,
            missing_capabilities=missing,
            incompatible_capabilities=incompatible,
            blocking_reasons=reasons,
            trace_id=trace_id,
        )


REFERENCE_CAPABILITY_BINDINGS = (
    CapabilityBinding("clinical-snapshot", "psychrx-baseline.snapshot", "0.1.0"),
    CapabilityBinding("safety", "psychrx-baseline.safety", "0.1.0"),
    CapabilityBinding("evidence", "psychrx-baseline.evidence", "0.1.0"),
    CapabilityBinding("reasoning", "psychrx-baseline.reasoning", "0.1.0"),
    CapabilityBinding("explanation", "psychrx-baseline.explanation", "0.1.0"),
    CapabilityBinding("monitoring", "psychrx-baseline.monitoring", "0.1.0"),
    CapabilityBinding("audit", "psychrx-baseline.audit", "0.1.0"),
)


def build_reference_resolver(
    catalog_specialty_keys: Iterable[str] = (),
    *,
    platform_specialty_keys: Iterable[str] = (),
) -> SpecialtyPackResolver:
    """Build a read-only resolver from verified structural providers."""

    catalog_keys = _canonical_specialty_keys(
        catalog_specialty_keys, "catalog_specialty_keys"
    )
    platform_keys = _canonical_specialty_keys(
        platform_specialty_keys, "platform_specialty_keys"
    )
    bindings = list(REFERENCE_CAPABILITY_BINDINGS)
    bindings.extend(
        CapabilityBinding(
            f"{key}.evidence",
            "decisionmed.catalog.evidence",
            "0.1.0",
        )
        for key in catalog_keys
    )
    bindings.extend(
        CapabilityBinding(f"{key}.{capability}", provider, "0.1.0")
        for key in platform_keys
        for capability, provider in (
            ("clinical-snapshot", "decisionmed.domain.clinical-snapshot"),
            ("audit", "decisionmed.audit.ledger"),
        )
    )
    return SpecialtyPackResolver(bindings)


def _canonical_specialty_keys(values: Iterable[str], field_name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise TypeError(f"{field_name} must be an iterable of identifiers")
    keys = tuple(values)
    if any(
        not isinstance(key, str) or not _IDENTIFIER_PATTERN.fullmatch(key)
        for key in keys
    ):
        raise ValueError(f"{field_name} must contain canonical identifiers")
    return tuple(sorted(set(keys)))
