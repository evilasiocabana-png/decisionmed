"""Evidence hierarchy engine."""

from __future__ import annotations


class HierarchyEngine:
    PRIORITY = (
        "Clinical Guidelines",
        "Systematic Reviews",
        "Meta Analyses",
        "RCT",
        "Observational",
        "Consensus",
        "Reference Books",
    )

    def hierarchy(self) -> tuple[str, ...]:
        return self.PRIORITY

