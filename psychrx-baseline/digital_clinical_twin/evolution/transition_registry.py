"""Twin transition registry."""

from __future__ import annotations


class TransitionRegistry:
    CATEGORIES = ("Context", "Safety", "Evidence", "Hypothesis", "Quality", "Knowledge", "Timeline")

    def categories(self) -> tuple[str, ...]:
        return self.CATEGORIES

