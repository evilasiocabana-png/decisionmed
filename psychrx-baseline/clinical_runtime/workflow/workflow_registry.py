"""Registry for structural runtime workflows."""

from __future__ import annotations

from dataclasses import dataclass, field

from clinical_runtime.workflow.workflow import ClinicalWorkflow, consultation_workflow


@dataclass
class WorkflowRegistry:
    """In-memory registry for workflow definitions."""

    workflows: dict[str, ClinicalWorkflow] = field(default_factory=dict)

    @classmethod
    def with_defaults(cls) -> "WorkflowRegistry":
        """Create a registry with official structural workflows."""
        registry = cls()
        registry.register(consultation_workflow())
        return registry

    def register(self, workflow: ClinicalWorkflow) -> None:
        """Register a workflow definition."""
        self.workflows[workflow.workflow_id] = workflow

    def get(self, workflow_id: str) -> ClinicalWorkflow | None:
        """Return a workflow by id."""
        return self.workflows.get(workflow_id)

    def list_ids(self) -> tuple[str, ...]:
        """Return registered workflow ids."""
        return tuple(sorted(self.workflows))

