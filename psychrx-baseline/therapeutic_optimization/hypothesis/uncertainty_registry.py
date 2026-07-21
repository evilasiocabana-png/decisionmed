"""Uncertainty registry."""

from __future__ import annotations

from dataclasses import dataclass, field

from therapeutic_optimization.models import Uncertainty


@dataclass
class UncertaintyRegistry:
    """Registers uncertainty categories with explanations."""

    _items: list[Uncertainty] = field(default_factory=list)

    def register(self, uncertainty: Uncertainty) -> None:
        self._items.append(uncertainty)

    def all(self) -> tuple[Uncertainty, ...]:
        return tuple(self._items)
