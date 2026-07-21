"""Comparison engine."""

from __future__ import annotations


class ComparisonEngine:
    """Compares architecture versions structurally."""

    def compare(self, left: str, right: str) -> tuple[str, ...]:
        if left == right:
            return ("no_structural_difference",)
        return (f"comparison:{left}->{right}",)

