"""Workspace to Runtime adapter."""

from __future__ import annotations

from clinical_runtime.session import RuntimeSessionManager


class WorkspaceRuntimeAdapter:
    """Allows workspace to start runtime structurally."""

    def start(self) -> dict[str, str | None]:
        return RuntimeSessionManager().open_session().to_dict()
