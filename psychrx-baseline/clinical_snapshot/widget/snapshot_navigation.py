"""Snapshot navigation."""

from __future__ import annotations


class SnapshotNavigation:
    def links(self) -> tuple[str, ...]:
        return ("Snapshot Summary", "Safety", "Evidence", "Hypotheses", "Explanation", "Trace")
