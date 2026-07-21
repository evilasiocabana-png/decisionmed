"""Research governance rules."""

from __future__ import annotations


class ResearchGovernance:
    RULES = (
        "Research cannot modify production",
        "Promotion requires ADR",
        "Experimental engines remain isolated",
        "No direct Clinical Runtime execution",
    )

    def all(self) -> tuple[str, ...]:
        return self.RULES

