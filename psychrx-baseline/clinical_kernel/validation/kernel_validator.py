"""Structural validation for the Clinical Kernel skeleton."""

from __future__ import annotations

from clinical_kernel.context.clinical_context import ClinicalContext
from clinical_kernel.execution.kernel_result import KernelResult
from clinical_kernel.state.clinical_state import ClinicalState


class KernelValidator:
    """Validates structure only, never clinical conduct."""

    def validate_context(self, context: ClinicalContext) -> bool:
        """Return True when a structural ClinicalContext is present."""
        return isinstance(context, ClinicalContext)

    def validate_state(self, state: ClinicalState) -> bool:
        """Return True when state is an official ClinicalState."""
        return isinstance(state, ClinicalState)

    def validate_result(self, result: KernelResult) -> bool:
        """Return True when a structural KernelResult is present."""
        return isinstance(result, KernelResult) and bool(result.status)
