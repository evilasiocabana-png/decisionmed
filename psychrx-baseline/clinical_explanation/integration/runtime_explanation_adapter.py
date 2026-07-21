"""Runtime adapter for Clinical Explanation Engine."""

from __future__ import annotations

from clinical_explanation import ClinicalExplanationResult, ExplanationCoordinator


class RuntimeExplanationAdapter:
    """Runs explanation after optimization in read-only mode."""

    def __init__(self, coordinator: ExplanationCoordinator | None = None) -> None:
        self._coordinator = coordinator or ExplanationCoordinator()

    def explain(
        self,
        runtime_result: dict[str, object],
        safety_result: dict[str, object],
        evidence_result: dict[str, object],
        optimization_result: dict[str, object],
    ) -> ClinicalExplanationResult:
        return self._coordinator.execute(
            runtime_result=runtime_result,
            safety_result=safety_result,
            evidence_result=evidence_result,
            optimization_result=optimization_result,
            clinical_snapshot={},
        )
