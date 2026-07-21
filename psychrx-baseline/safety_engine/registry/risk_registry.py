"""Versioned risk registry without executable clinical rules."""

from __future__ import annotations

from dataclasses import dataclass, field

from safety_engine.models import Risk


@dataclass
class RiskRegistry:
    """Stores structural risk definitions from validated knowledge."""

    version: str = "0.1-structural"
    _risks: list[Risk] = field(default_factory=list)

    def register(self, risk: Risk) -> None:
        self._risks.append(risk)

    def all(self) -> tuple[Risk, ...]:
        return tuple(self._risks)

    def lookup(self, risk_id: str) -> Risk | None:
        return next((risk for risk in self._risks if risk.risk_id == risk_id), None)

    def categories(self) -> tuple[str, ...]:
        return tuple(sorted({risk.category for risk in self._risks}))
