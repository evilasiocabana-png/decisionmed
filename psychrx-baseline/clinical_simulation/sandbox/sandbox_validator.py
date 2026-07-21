"""Sandbox validator."""

from __future__ import annotations

from clinical_simulation.models import SimulationSandbox


class SandboxValidator:
    def validate(self, sandbox: SimulationSandbox) -> tuple[str, ...]:
        issues = []
        if not sandbox.isolated:
            issues.append("sandbox_not_isolated")
        if sandbox.cleanup_policy != "automatic":
            issues.append("unsafe_cleanup_policy")
        if not sandbox.version:
            issues.append("missing_version")
        return tuple(issues)

