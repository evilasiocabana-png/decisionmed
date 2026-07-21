"""Scientific conflict registry."""

from __future__ import annotations


class ConflictResolutionEngine:
    """Registers conflicts without arbitration."""

    def register_conflict(self, left: str, right: str, reason: str) -> str:
        return f"conflict:{left}:{right}:{reason}"

