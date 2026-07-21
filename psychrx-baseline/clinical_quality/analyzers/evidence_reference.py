"""Evidence reference validator."""

from __future__ import annotations

from collections.abc import Mapping


class EvidenceReferenceValidator:
    """Validates structural evidence references without interpreting content."""

    def validate(self, runtime_output: Mapping[str, object]) -> tuple[str, ...]:
        evidence = runtime_output.get("evidence_result", {})
        if not isinstance(evidence, Mapping):
            return ("missing_evidence_result",)
        if not evidence.get("trace_id"):
            return ("missing_evidence_trace",)
        return ()

