"""Unified trace builder for Clinical Operating Mind."""

from __future__ import annotations

from typing import Mapping

from clinical_operating_mind.models import OperatingMindTrace


class OperatingMindTraceBuilder:
    """Builds unified traces from upstream structural outputs."""

    def build(
        self,
        safety_result: Mapping[str, object],
        evidence_result: Mapping[str, object],
        optimization_result: Mapping[str, object],
        explanation_result: Mapping[str, object],
        clinical_snapshot: Mapping[str, object],
        clinical_timeline: Mapping[str, object],
        clinical_navigation: Mapping[str, object],
    ) -> OperatingMindTrace:
        explanation_trace = explanation_result.get("trace", {})
        return OperatingMindTrace(
            safety_trace=str(safety_result.get("trace_id", "")),
            evidence_trace=str(evidence_result.get("trace_id", "")),
            optimization_trace=str(optimization_result.get("trace_id", "")),
            explanation_trace=str(
                explanation_trace.get("trace_id", "") if isinstance(explanation_trace, Mapping) else ""
            ),
            snapshot_id=str(clinical_snapshot.get("snapshot_id", "")),
            timeline_id=str(clinical_timeline.get("timeline_id", "")),
            navigation_session=str(clinical_navigation.get("navigation_id", "")),
        )

