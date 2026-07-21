"""Clinical Snapshot builder."""

from __future__ import annotations

from typing import Any

from clinical_snapshot.models import (
    ClinicalSnapshot,
    SnapshotConfidence,
    SnapshotReference,
    SnapshotStatistics,
)


class SnapshotBuilder:
    """Aggregates upstream results without modifying them."""

    def build(
        self,
        runtime_result: dict[str, Any],
        safety_result: dict[str, Any],
        evidence_result: dict[str, Any],
        optimization_result: dict[str, Any],
        explanation_result: dict[str, Any],
    ) -> ClinicalSnapshot:
        session = runtime_result.get("session", {})
        return ClinicalSnapshot(
            runtime_id=str(session.get("session_id", "not_bound")),
            safety=safety_result,
            evidence=evidence_result,
            hypotheses=tuple(optimization_result.get("hypotheses", ())),
            explanations=explanation_result,
            confidence=SnapshotConfidence(
                value=float(optimization_result.get("confidence", 0.0)),
                explanation="Structural confidence consolidated from optimization output.",
            ),
            uncertainties=tuple(optimization_result.get("uncertainties", ())),
            references=SnapshotReference(
                runtime_trace=str(runtime_result.get("result", {}).get("trace_id", "not_bound")),
                safety_trace=str(safety_result.get("trace_id", "not_bound")),
                evidence_trace=str(evidence_result.get("trace_id", "not_bound")),
                optimization_trace=str(optimization_result.get("trace_id", "not_bound")),
                explanation_trace=str(explanation_result.get("trace", {}).get("trace_id", "not_bound")),
            ),
            statistics=SnapshotStatistics(
                safety_alerts=int(safety_result.get("snapshot", {}).get("alert_count", 0)),
                evidence_items=int(evidence_result.get("snapshot", {}).get("selected_count", 0)),
                hypotheses=len(optimization_result.get("hypotheses", ())),
                explanations=len(explanation_result.get("sections", ())),
                uncertainties=len(optimization_result.get("uncertainties", ())),
            ),
        )
