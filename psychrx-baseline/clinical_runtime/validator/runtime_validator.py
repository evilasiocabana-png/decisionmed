"""Runtime structural validator."""

from __future__ import annotations

from dataclasses import dataclass

from clinical_runtime.context import RuntimeContext


@dataclass(frozen=True)
class RuntimeValidationError:
    """Controlled runtime validation error."""

    code: str
    message: str


class RuntimeValidator:
    """Validates runtime structure, never clinical validity."""

    def validate_context(self, context: RuntimeContext | None) -> tuple[RuntimeValidationError, ...]:
        errors: list[RuntimeValidationError] = []
        if context is None:
            errors.append(RuntimeValidationError("missing_context", "RuntimeContext is required."))
        return tuple(errors)

    def validate_pipeline(self, steps: tuple[str, ...]) -> tuple[RuntimeValidationError, ...]:
        if not steps:
            return (RuntimeValidationError("invalid_pipeline", "Pipeline requires at least one step."),)
        if len(set(steps)) != len(steps):
            return (RuntimeValidationError("duplicated_execution", "Pipeline steps must be unique."),)
        return ()
