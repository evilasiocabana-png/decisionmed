"""Quality trace builder."""

from __future__ import annotations

from collections.abc import Mapping


class QualityTraceBuilder:
    """Extracts trace references required by QualityResult."""

    def build(self, runtime_output: Mapping[str, object]) -> tuple[str, ...]:
        keys = (
            "clinical_operating_mind",
            "clinical_snapshot",
            "clinical_timeline",
            "safety_result",
            "evidence_result",
            "optimization_result",
            "explanation_result",
        )
        return tuple(key for key in keys if key in runtime_output)

