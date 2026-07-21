"""Navigation state validation."""

from __future__ import annotations

from dataclasses import dataclass, field

from clinical_navigation.models import ClinicalNavigationState


@dataclass(frozen=True)
class NavigationStateValidation:
    broken_routes: tuple[str, ...] = field(default_factory=tuple)
    missing_references: tuple[str, ...] = field(default_factory=tuple)
    invalid_context: tuple[str, ...] = field(default_factory=tuple)

    @property
    def valid(self) -> bool:
        return not (self.broken_routes or self.missing_references or self.invalid_context)


class NavigationStateValidator:
    def validate(self, state: ClinicalNavigationState) -> NavigationStateValidation:
        broken = tuple(route.target for route in state.history.entries if not route.valid)
        return NavigationStateValidation(broken_routes=broken)
