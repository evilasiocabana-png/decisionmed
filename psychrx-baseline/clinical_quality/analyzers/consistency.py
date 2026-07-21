"""Consistency analyzer."""

from __future__ import annotations

from collections.abc import Mapping

from clinical_quality.models import QualityDimension


class ConsistencyAnalyzer:
    """Detects broken structural references."""

    def analyze(self, runtime_output: Mapping[str, object]) -> QualityDimension:
        details: list[str] = []
        snapshot = runtime_output.get("clinical_snapshot")
        timeline = runtime_output.get("clinical_timeline")
        if isinstance(snapshot, Mapping) and isinstance(timeline, Mapping):
            if timeline.get("current_snapshot") and timeline.get("current_snapshot") != snapshot.get("snapshot_id"):
                details.append("snapshot_timeline_mismatch")
        else:
            details.append("missing_snapshot_or_timeline")
        return QualityDimension(
            name="consistency",
            status="valid" if not details else "inconsistent",
            score=1.0 if not details else 0.5,
            details=tuple(details),
        )

