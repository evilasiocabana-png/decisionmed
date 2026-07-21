"""Immutability validator."""

from __future__ import annotations

from collections.abc import Mapping


class ImmutabilityValidator:
    """Reports whether upstream objects are consumed as immutable snapshots."""

    def validate(self, before: Mapping[str, object], after: Mapping[str, object]) -> tuple[str, ...]:
        if before != after:
            return ("upstream_mutation_detected",)
        return ()

