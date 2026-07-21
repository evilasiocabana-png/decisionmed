"""Snapshot summary builder."""

from __future__ import annotations

from clinical_snapshot.models import ClinicalSnapshot, SnapshotSummary


class SnapshotSummaryBuilder:
    """Builds a non-interpretive summary."""

    def build(self, snapshot: ClinicalSnapshot) -> SnapshotSummary:
        return SnapshotSummary(
            main_findings=("Snapshot consolidated structural engine outputs.",),
            active_alerts=tuple(str(item.get("alert_id", "")) for item in snapshot.safety.get("alerts", ())),
            confidence_summary=snapshot.confidence.explanation,
        )
