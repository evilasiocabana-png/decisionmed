"""Editorial workflow for psychopharmacology package publication."""

from __future__ import annotations

from dataclasses import dataclass


class DrugEditorialWorkflow:
    stages: tuple[str, ...] = (
        "Draft",
        "Scientific Review",
        "Editorial Review",
        "Approved",
        "Published",
        "Deprecated",
    )

    def next_stage(self, current_stage: str) -> str:
        if current_stage not in self.stages:
            return "Draft"
        index = self.stages.index(current_stage)
        if index >= len(self.stages) - 1:
            return current_stage
        return self.stages[index + 1]


@dataclass(frozen=True)
class DrugPublicationChecklist:
    scientific_validation: bool = False
    knowledge_governance: bool = False
    editorial_approval: bool = False
    version_assignment: bool = False
    trace_validation: bool = False

    def passes(self) -> bool:
        return all(
            (
                self.scientific_validation,
                self.knowledge_governance,
                self.editorial_approval,
                self.version_assignment,
                self.trace_validation,
            )
        )


class DrugPublicationGate:
    def evaluate(self, checklist: DrugPublicationChecklist) -> str:
        return "publication_allowed" if checklist.passes() else "publication_rejected_incomplete_package"

