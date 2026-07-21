"""Standard structural result returned by the Clinical Kernel."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from clinical_kernel.context.clinical_context import ClinicalContext


@dataclass(frozen=True)
class KernelResult:
    """Read-only response contract for the Application Layer."""

    status: str
    context: ClinicalContext = field(default_factory=ClinicalContext.empty)
    messages: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)
    blocked_reason: str = ""
    audit_metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-safe representation."""
        return asdict(self)

    @classmethod
    def read_only_blocked(cls) -> "KernelResult":
        """Return the default safe result before real clinical engines exist."""
        return cls(
            status="read_only_structural",
            messages=("Clinical Kernel structural skeleton available.",),
            warnings=("No clinical reasoning engine is implemented.",),
            blocked_reason=(
                "Strategies blocked: Clinical Kernel still has no Safety Engine, "
                "Evidence Graph Runtime, or Therapeutic Optimization Runtime."
            ),
            audit_metadata={
                "mode": "read-only",
                "clinical_decision": "not_implemented",
                "prescription": "not_available",
            },
        )
