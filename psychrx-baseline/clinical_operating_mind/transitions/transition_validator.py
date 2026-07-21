"""Transition validator for Clinical Operating Mind lifecycle."""

from __future__ import annotations


class TransitionValidator:
    """Prevents unsafe lifecycle shortcuts."""

    REQUIRED_ORDER = (
        "Context Intake",
        "Safety Evaluation",
        "Evidence Resolution",
        "Therapeutic Hypothesis Generation",
        "Explanation Assembly",
        "Snapshot Creation",
        "Timeline Update",
        "Navigation Update",
    )

    def validate_completed(self, completed_phases: tuple[str, ...]) -> tuple[str, ...]:
        errors: list[str] = []
        positions = {phase: index for index, phase in enumerate(self.REQUIRED_ORDER)}
        previous = -1
        for phase in completed_phases:
            position = positions.get(phase)
            if position is None:
                errors.append(f"unknown_phase:{phase}")
                continue
            if position <= previous:
                errors.append(f"invalid_phase_order:{phase}")
            if position > previous + 1:
                skipped = self.REQUIRED_ORDER[previous + 1 : position]
                errors.extend(f"skipped_phase:{item}" for item in skipped)
            previous = position
        return tuple(errors)

