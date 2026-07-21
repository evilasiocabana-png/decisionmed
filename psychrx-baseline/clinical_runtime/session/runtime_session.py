"""Runtime session structures."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class RuntimeSession:
    """Read-only runtime session metadata. No persistence."""

    session_id: str
    workspace_id: str
    patient_id: str
    user_id: str
    runtime_version: str
    kernel_version: str
    opened_at: str
    closed_at: str | None = None
    status: str = "open"

    def close(self) -> "RuntimeSession":
        """Return a closed copy of the session."""
        return RuntimeSession(
            session_id=self.session_id,
            workspace_id=self.workspace_id,
            patient_id=self.patient_id,
            user_id=self.user_id,
            runtime_version=self.runtime_version,
            kernel_version=self.kernel_version,
            opened_at=self.opened_at,
            closed_at=_now(),
            status="closed",
        )

    def to_dict(self) -> dict[str, str | None]:
        return asdict(self)


class RuntimeSessionManager:
    """Creates and closes structural runtime sessions."""

    def open_session(
        self,
        workspace_id: str = "workspace-read-only",
        patient_id: str = "patient-placeholder",
        user_id: str = "user-placeholder",
        runtime_version: str = "0.1-structural",
        kernel_version: str = "0.3-kernel-structural",
    ) -> RuntimeSession:
        return RuntimeSession(
            session_id=f"RTS-{uuid4()}",
            workspace_id=workspace_id,
            patient_id=patient_id,
            user_id=user_id,
            runtime_version=runtime_version,
            kernel_version=kernel_version,
            opened_at=_now(),
        )
