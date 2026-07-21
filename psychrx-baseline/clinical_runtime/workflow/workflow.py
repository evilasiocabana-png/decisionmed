"""Official structural workflows for the Clinical Runtime."""

from __future__ import annotations

from dataclasses import dataclass

from clinical_runtime.workflow.workflow_node import WorkflowNode
from clinical_runtime.workflow.workflow_transition import WorkflowTransition


@dataclass(frozen=True)
class ClinicalWorkflow:
    """A read-only workflow definition."""

    workflow_id: str
    title: str
    nodes: tuple[WorkflowNode, ...]
    transitions: tuple[WorkflowTransition, ...]
    status: str = "read_only_structural"

    def node_ids(self) -> tuple[str, ...]:
        """Return the node ids in workflow order."""
        return tuple(node.id for node in self.nodes)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-safe representation."""
        return {
            "workflow_id": self.workflow_id,
            "title": self.title,
            "status": self.status,
            "nodes": tuple(node.to_dict() for node in self.nodes),
            "transitions": tuple(transition.to_dict() for transition in self.transitions),
        }


def consultation_workflow() -> ClinicalWorkflow:
    """Return the official read-only consultation workflow."""
    steps = (
        ("consultation_start", "Consultation Start", "Open the read-only consultation workspace."),
        ("patient_context", "Patient Context", "Present patient context without deciding conduct."),
        ("clinical_investigation", "Clinical Investigation", "Organize missing information prompts."),
        ("clinical_snapshot", "Clinical Snapshot", "Represent current structural state."),
        ("objectives", "Objectives", "Show therapeutic objectives as review targets."),
        ("risk_review", "Risk Review", "Keep risk review before strategy display."),
        ("strategy_blocked", "Strategy (Blocked)", "Keep strategy locked until future gates."),
        ("monitoring", "Monitoring", "Represent monitoring area without clinical plan execution."),
        ("explanation", "Explanation", "Show explanation area for future traceability."),
        ("consultation_end", "Consultation End", "Close the structural consultation flow."),
    )
    nodes = tuple(
        WorkflowNode(
            id=node_id,
            title=title,
            description=description,
            next_nodes=(steps[index + 1][0],) if index + 1 < len(steps) else (),
            metadata={"clinical_logic": "forbidden", "read_only": "true"},
        )
        for index, (node_id, title, description) in enumerate(steps)
    )
    transitions = tuple(
        WorkflowTransition(origin=steps[index][0], destination=steps[index + 1][0])
        for index in range(len(steps) - 1)
    )
    return ClinicalWorkflow(
        workflow_id="consultation_workflow",
        title="Consultation Workflow",
        nodes=nodes,
        transitions=transitions,
    )

