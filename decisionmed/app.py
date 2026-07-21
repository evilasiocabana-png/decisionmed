"""Read-only application service for the DecisionMEd MVP shell."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .composition import SpecialtyPackResolver, build_reference_resolver
from .specialties import SpecialtyPackRegistry, build_default_specialty_registry


@dataclass(frozen=True, slots=True)
class SpecialtyView:
    key: str
    display_name: str
    version: str
    pack_status: str
    load_status: str
    execution_allowed: bool
    missing_capabilities: tuple[str, ...]
    blocking_reasons: tuple[str, ...]
    trace_id: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "display_name": self.display_name,
            "version": self.version,
            "pack_status": self.pack_status,
            "load_status": self.load_status,
            "execution_allowed": self.execution_allowed,
            "missing_capabilities": list(self.missing_capabilities),
            "blocking_reasons": list(self.blocking_reasons),
            "trace_id": self.trace_id,
        }


class DecisionMedAppService:
    """Expose composition state without running clinical capabilities."""

    def __init__(
        self,
        registry: SpecialtyPackRegistry | None = None,
        resolver: SpecialtyPackResolver | None = None,
    ) -> None:
        self._registry = registry or build_default_specialty_registry()
        self._resolver = resolver or build_reference_resolver()

    def specialties(self) -> tuple[SpecialtyView, ...]:
        views: list[SpecialtyView] = []
        for pack in self._registry.all():
            result = self._resolver.resolve(pack)
            views.append(
                SpecialtyView(
                    key=pack.key,
                    display_name=pack.display_name,
                    version=pack.version,
                    pack_status=pack.status.value,
                    load_status=result.status.value,
                    execution_allowed=result.clinical_execution_allowed,
                    missing_capabilities=result.missing_capabilities,
                    blocking_reasons=result.blocking_reasons,
                    trace_id=result.trace_id,
                )
            )
        return tuple(views)

    def get_app_state(self) -> dict[str, Any]:
        specialties = self.specialties()
        return {
            "product": "DecisionMEd",
            "mode": "read-only",
            "clinical_execution_allowed": False,
            "specialties": [item.to_dict() for item in specialties],
        }
