"""Safety governance gate."""

from __future__ import annotations

from typing import Mapping


class SafetyGovernanceGate:
    """Stops downstream optimization when safety blocks the route."""

    def evaluate(self, safety_result: Mapping[str, object]) -> tuple[bool, str]:
        blocking = safety_result.get("blocking_decision")
        if isinstance(blocking, Mapping) and blocking.get("status") == "blocked":
            return False, "safety_blocking_decision"
        return True, ""

