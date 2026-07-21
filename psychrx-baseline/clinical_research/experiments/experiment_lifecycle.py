"""Experiment lifecycle."""

from __future__ import annotations


class ExperimentLifecycle:
    STATES = ("draft", "configured", "running", "completed", "validated", "archived")

    def can_transition(self, source: str, target: str) -> bool:
        try:
            return self.STATES.index(target) == self.STATES.index(source) + 1
        except ValueError:
            return False

