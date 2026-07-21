"""Cross artifact navigation."""

from __future__ import annotations


class CrossNavigation:
    """Read-only related-object navigation map."""

    def path(self) -> tuple[str, ...]:
        return ("Hypothesis", "Evidence", "Safety", "Explanation", "Runtime Trace")
