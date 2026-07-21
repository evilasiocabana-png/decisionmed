"""Trace validator."""

from __future__ import annotations

from collections.abc import Mapping

from clinical_quality.models import QualityDimension


class TraceValidator:
    """Validates the complete structural trace chain."""

    REQUIRED_TRACE_FIELDS = (
        "runtime_trace",
        "safety_trace",
        "evidence_trace",
        "optimization_trace",
        "explanation_trace",
        "snapshot_id",
        "timeline_id",
        "navigation_session",
    )

    def validate(self, runtime_output: Mapping[str, object]) -> QualityDimension:
        operating_mind = runtime_output.get("clinical_operating_mind", {})
        state = operating_mind.get("state", {}) if isinstance(operating_mind, Mapping) else {}
        trace = state.get("trace", {}) if isinstance(state, Mapping) else {}
        missing = tuple(
            key for key in self.REQUIRED_TRACE_FIELDS if not isinstance(trace, Mapping) or not trace.get(key)
        )
        return QualityDimension(
            name="traceability",
            status="valid" if not missing else "incomplete",
            score=1.0 if not missing else round((len(self.REQUIRED_TRACE_FIELDS) - len(missing)) / len(self.REQUIRED_TRACE_FIELDS), 3),
            details=tuple(f"missing_trace:{key}" for key in missing),
        )

