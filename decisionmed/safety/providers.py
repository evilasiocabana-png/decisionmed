"""Technical provider bindings for governed safety-check specifications."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import re

from .definitions import SafetyCheckStatus
from .models import SafetyError
from .registry import SafetyCheckRegistry


_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_VERSION = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


@dataclass(frozen=True, slots=True)
class SafetyCheckProviderBinding:
    """Descriptor for a technical provider; it does not execute the provider."""

    check_id: str
    provider: str
    version: str

    def __post_init__(self) -> None:
        _identifier("check_id", self.check_id)
        _identifier("provider", self.provider)
        if not isinstance(self.version, str) or not _VERSION.fullmatch(self.version):
            _fail("version", "version must use semantic versioning")

    @property
    def clinical_execution_allowed(self) -> bool:
        return False


@dataclass(frozen=True, slots=True)
class SafetyImplementationCoverage:
    """Fail-closed comparison between governed specifications and providers."""

    specification_ids: tuple[str, ...]
    bound_check_ids: tuple[str, ...]
    missing_check_ids: tuple[str, ...]
    incompatible_check_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        specifications = _identifiers(
            "specification_ids", self.specification_ids, allow_empty=True
        )
        bound = _identifiers("bound_check_ids", self.bound_check_ids, allow_empty=True)
        missing = _identifiers(
            "missing_check_ids", self.missing_check_ids, allow_empty=True
        )
        incompatible = _identifiers(
            "incompatible_check_ids",
            self.incompatible_check_ids,
            allow_empty=True,
        )
        specification_set = set(specifications)
        partitions = (set(bound), set(missing), set(incompatible))
        if any(not partition.issubset(specification_set) for partition in partitions):
            _fail("coverage", "coverage entries must reference specifications")
        if any(
            left.intersection(right)
            for index, left in enumerate(partitions)
            for right in partitions[index + 1 :]
        ):
            _fail("coverage", "coverage states must be disjoint")
        if set().union(*partitions) != specification_set:
            _fail("coverage", "every specification requires one coverage state")
        object.__setattr__(self, "specification_ids", specifications)
        object.__setattr__(self, "bound_check_ids", bound)
        object.__setattr__(self, "missing_check_ids", missing)
        object.__setattr__(self, "incompatible_check_ids", incompatible)

    @property
    def complete(self) -> bool:
        return bool(self.specification_ids) and not (
            self.missing_check_ids or self.incompatible_check_ids
        )

    @property
    def clinical_execution_allowed(self) -> bool:
        return False


class SafetyCheckProviderRegistry:
    """Bind provider metadata only to validated governed specifications."""

    def __init__(
        self,
        specifications: SafetyCheckRegistry,
        bindings: Iterable[SafetyCheckProviderBinding] = (),
    ) -> None:
        if not isinstance(specifications, SafetyCheckRegistry):
            raise TypeError("specifications must be a SafetyCheckRegistry")
        self._specifications = specifications
        self._bindings: dict[str, SafetyCheckProviderBinding] = {}
        for binding in bindings:
            self.register(binding)

    def register(
        self, binding: SafetyCheckProviderBinding
    ) -> SafetyCheckProviderBinding:
        if not isinstance(binding, SafetyCheckProviderBinding):
            raise TypeError("binding must be a SafetyCheckProviderBinding")
        specification = self._specifications.get(binding.check_id)
        if specification is None:
            raise SafetyError(
                "safety_provider_registry.unknown_specification",
                f"check not registered: {binding.check_id}",
            )
        if specification.status is not SafetyCheckStatus.VALIDATED:
            raise SafetyError(
                "safety_provider_registry.unvalidated_specification",
                "provider binding requires a validated specification",
            )
        if binding.check_id in self._bindings:
            raise SafetyError(
                "safety_provider_registry.duplicate",
                f"provider already registered: {binding.check_id}",
            )
        self._bindings[binding.check_id] = binding
        return binding

    def get(self, check_id: str) -> SafetyCheckProviderBinding | None:
        return self._bindings.get(check_id)

    def all(self) -> tuple[SafetyCheckProviderBinding, ...]:
        return tuple(self._bindings[key] for key in sorted(self._bindings))

    @property
    def specifications(self) -> SafetyCheckRegistry:
        """Return the governed specifications behind these descriptors."""

        return self._specifications

    def coverage(self) -> SafetyImplementationCoverage:
        specifications = self._specifications.all()
        compatible: list[str] = []
        missing: list[str] = []
        incompatible: list[str] = []
        for specification in specifications:
            binding = self.get(specification.check_id)
            if binding is None:
                missing.append(specification.check_id)
            elif binding.version != specification.version:
                incompatible.append(specification.check_id)
            else:
                compatible.append(specification.check_id)
        return SafetyImplementationCoverage(
            specification_ids=tuple(item.check_id for item in specifications),
            bound_check_ids=tuple(compatible),
            missing_check_ids=tuple(missing),
            incompatible_check_ids=tuple(incompatible),
        )


def _identifier(field_name: str, value: object) -> None:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
        _fail(field_name, f"{field_name} must be canonical")


def _identifiers(
    field_name: str, values: object, *, allow_empty: bool
) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        _fail(field_name, f"{field_name} must be a collection")
    items = tuple(values)  # type: ignore[arg-type]
    if not allow_empty and not items:
        _fail(field_name, f"{field_name} cannot be empty")
    for item in items:
        _identifier(field_name, item)
    if len(set(items)) != len(items):
        _fail(field_name, f"{field_name} must be unique")
    return items


def _fail(field_name: str, message: str) -> None:
    raise SafetyError(f"safety_provider.{field_name}", message)
