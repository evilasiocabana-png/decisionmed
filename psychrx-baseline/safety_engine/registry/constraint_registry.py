"""Versioned constraint registry without executable clinical rules."""

from __future__ import annotations

from dataclasses import dataclass, field

from safety_engine.models import Constraint


@dataclass
class ConstraintRegistry:
    """Stores structural constraint definitions from validated knowledge."""

    version: str = "0.1-structural"
    _constraints: list[Constraint] = field(default_factory=list)

    def register(self, constraint: Constraint) -> None:
        self._constraints.append(constraint)

    def all(self) -> tuple[Constraint, ...]:
        return tuple(self._constraints)

    def lookup(self, constraint_id: str) -> Constraint | None:
        return next(
            (
                constraint
                for constraint in self._constraints
                if constraint.constraint_id == constraint_id
            ),
            None,
        )

    def categories(self) -> tuple[str, ...]:
        return tuple(sorted({constraint.category for constraint in self._constraints}))
