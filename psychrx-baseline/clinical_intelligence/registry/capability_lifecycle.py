"""Capability lifecycle."""

from __future__ import annotations


class CapabilityLifecycle:
    STATES = ("experimental", "registered", "validated", "active", "deprecated", "retired")

    def can_transition(self, source: str, target: str) -> bool:
        try:
            return self.STATES.index(target) == self.STATES.index(source) + 1
        except ValueError:
            return False

