"""Structural workflow executor."""

from __future__ import annotations

from dataclasses import dataclass

from clinical_runtime.workflow.workflow import ClinicalWorkflow
from clinical_runtime.workflow.workflow_state import WorkflowState


@dataclass
class WorkflowExecutor:
    """Executor facade that changes structural state only."""

    state: WorkflowState = WorkflowState.NOT_STARTED

    def start(self, workflow: ClinicalWorkflow) -> dict[str, object]:
        """Mark a workflow as running without executing clinical nodes."""
        self.state = WorkflowState.RUNNING
        return self._result(workflow, "workflow_started")

    def pause(self, workflow: ClinicalWorkflow) -> dict[str, object]:
        """Mark a workflow as paused."""
        self.state = WorkflowState.WAITING
        return self._result(workflow, "workflow_paused")

    def resume(self, workflow: ClinicalWorkflow) -> dict[str, object]:
        """Mark a workflow as running again."""
        self.state = WorkflowState.RUNNING
        return self._result(workflow, "workflow_resumed")

    def finish(self, workflow: ClinicalWorkflow) -> dict[str, object]:
        """Mark a workflow as completed."""
        self.state = WorkflowState.COMPLETED
        return self._result(workflow, "workflow_finished")

    def _result(self, workflow: ClinicalWorkflow, event: str) -> dict[str, object]:
        return {
            "workflow_id": workflow.workflow_id,
            "event": event,
            "state": self.state.value,
            "clinical_decision": "not_implemented",
            "prescription": "not_available",
            "runtime_consumption_allowed": False,
        }

