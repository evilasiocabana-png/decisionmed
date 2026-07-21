"""Validation for structural workflow definitions."""

from __future__ import annotations

from dataclasses import dataclass

from clinical_runtime.workflow.workflow import ClinicalWorkflow


@dataclass(frozen=True)
class WorkflowValidationIssue:
    """Structural workflow validation issue."""

    code: str
    message: str


class WorkflowValidator:
    """Validate workflow structure without validating clinical content."""

    def validate(self, workflow: ClinicalWorkflow) -> tuple[WorkflowValidationIssue, ...]:
        """Validate node and transition references."""
        issues: list[WorkflowValidationIssue] = []
        node_ids = set(workflow.node_ids())
        if not workflow.nodes:
            issues.append(WorkflowValidationIssue("workflow_empty", "Workflow has no nodes."))
        for transition in workflow.transitions:
            if transition.origin not in node_ids:
                issues.append(WorkflowValidationIssue("origin_missing", transition.origin))
            if transition.destination not in node_ids:
                issues.append(WorkflowValidationIssue("destination_missing", transition.destination))
        return tuple(issues)

