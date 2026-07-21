"""Read-only explainability navigation."""

from __future__ import annotations


class ExplainabilityNavigation:
    """Creates read-only links between explanatory artifacts."""

    def links(self) -> tuple[str, ...]:
        return (
            "Safety Snapshot",
            "Evidence Snapshot",
            "Therapeutic Hypotheses",
            "Clinical Snapshot",
            "Runtime Trace",
        )
