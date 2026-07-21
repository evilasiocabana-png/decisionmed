"""Workflow node model for structural consultation flow."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from clinical_runtime.workflow.workflow_state import WorkflowState


@dataclass(frozen=True)
class WorkflowNode:
    """A structural node in a runtime workflow.

    Nodes describe presentation/runtime order only. They do not decide,
    diagnose, recommend, prescribe, or execute clinical engines.
    """

    id: str
    title: str
    description: str
    status: WorkflowState = WorkflowState.READ_ONLY
    dependencies: tuple[str, ...] = ()
    next_nodes: tuple[str, ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-safe representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "dependencies": self.dependencies,
            "next_nodes": self.next_nodes,
            "metadata": dict(self.metadata),
        }

