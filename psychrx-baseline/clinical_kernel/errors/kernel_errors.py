"""Structural errors for the Clinical Kernel.

These are not clinical alerts and do not represent medico-legal decisions.
"""


class KernelError(Exception):
    """Base structural kernel error."""


class InvalidClinicalContext(KernelError):
    """Raised when a structural ClinicalContext is absent or invalid."""


class InvalidClinicalState(KernelError):
    """Raised when a structural ClinicalState is absent or invalid."""


class PipelineNotReady(KernelError):
    """Raised when the structural pipeline is not ready."""


class EngineUnavailable(KernelError):
    """Raised when a future engine is unavailable."""


class StrategyLocked(KernelError):
    """Raised when strategy remains structurally locked."""
