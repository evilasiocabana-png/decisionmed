"""Structural conflict detector."""

from __future__ import annotations

from collections.abc import Mapping


class ConflictDetector:
    """Detects structural conflicts without resolving them."""

    def detect(self, runtime_output: Mapping[str, object]) -> tuple[str, ...]:
        conflicts: list[str] = []
        operating_mind = runtime_output.get("clinical_operating_mind")
        if isinstance(operating_mind, Mapping):
            state = operating_mind.get("state", {})
            if isinstance(state, Mapping) and state.get("status") == "blocked":
                conflicts.append("operating_mind_blocked")
        if runtime_output.get("prescription") not in ("not_available", None):
            conflicts.append("prescription_output_detected")
        return tuple(conflicts)

