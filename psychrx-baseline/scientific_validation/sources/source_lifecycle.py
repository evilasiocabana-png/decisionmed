"""Scientific source lifecycle."""

from __future__ import annotations


class SourceLifecycle:
    STATES = ("candidate", "validated", "active", "deprecated", "retired", "archived")

    def can_transition(self, source: str, target: str) -> bool:
        try:
            return self.STATES.index(target) == self.STATES.index(source) + 1
        except ValueError:
            return False

