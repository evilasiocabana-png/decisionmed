"""Data-driven, non-clinical workflow definitions for specialty packs."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any, Iterable

from .specialties import SpecialtyPack, SpecialtyPackRegistry


_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_VERSION = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
DEFAULT_WORKFLOW_ROOT = Path(__file__).resolve().parents[1] / "data" / "specialties"


class WorkflowDefinitionError(ValueError):
    """Raised when a workflow manifest violates the platform contract."""


class UnknownWorkflowError(KeyError):
    """Raised when no workflow exists for a specialty."""


@dataclass(frozen=True, slots=True)
class WorkflowStep:
    key: str
    title: str
    capability: str

    def __post_init__(self) -> None:
        if not _IDENTIFIER.fullmatch(self.key):
            raise WorkflowDefinitionError("step key must be a canonical identifier")
        if not isinstance(self.title, str) or not self.title.strip():
            raise WorkflowDefinitionError("step title cannot be empty")
        if not _IDENTIFIER.fullmatch(self.capability):
            raise WorkflowDefinitionError("step capability must be canonical")

    def to_dict(self, position: int) -> dict[str, Any]:
        return {
            "position": position,
            "key": self.key,
            "title": self.title,
            "capability": self.capability,
        }


@dataclass(frozen=True, slots=True)
class SpecialtyWorkflow:
    specialty_key: str
    workflow_id: str
    version: str
    mode: str
    steps: tuple[WorkflowStep, ...]

    def __post_init__(self) -> None:
        if not _IDENTIFIER.fullmatch(self.specialty_key):
            raise WorkflowDefinitionError("specialty_key must be canonical")
        if not _IDENTIFIER.fullmatch(self.workflow_id):
            raise WorkflowDefinitionError("workflow_id must be canonical")
        if not _VERSION.fullmatch(self.version):
            raise WorkflowDefinitionError("version must use semantic versioning")
        if self.mode != "reference_only":
            raise WorkflowDefinitionError("only reference_only workflows are allowed")
        steps = tuple(self.steps)
        if not steps:
            raise WorkflowDefinitionError("workflow must contain steps")
        if len({step.key for step in steps}) != len(steps):
            raise WorkflowDefinitionError("workflow step keys must be unique")
        object.__setattr__(self, "steps", steps)

    def to_dict(self) -> dict[str, Any]:
        return {
            "specialty_key": self.specialty_key,
            "workflow_id": self.workflow_id,
            "version": self.version,
            "mode": self.mode,
            "clinical_execution_allowed": False,
            "steps": [step.to_dict(index) for index, step in enumerate(self.steps, 1)],
        }


class WorkflowRegistry:
    def __init__(self, workflows: Iterable[SpecialtyWorkflow] = ()) -> None:
        self._workflows: dict[str, SpecialtyWorkflow] = {}
        for workflow in workflows:
            if workflow.specialty_key in self._workflows:
                raise WorkflowDefinitionError(
                    f"duplicate specialty workflow: {workflow.specialty_key}"
                )
            self._workflows[workflow.specialty_key] = workflow

    def require(self, specialty_key: str) -> SpecialtyWorkflow:
        try:
            return self._workflows[specialty_key]
        except KeyError as exc:
            raise UnknownWorkflowError(specialty_key) from exc


def workflow_from_mapping(payload: dict[str, Any], pack: SpecialtyPack) -> SpecialtyWorkflow:
    try:
        raw_steps = payload["steps"]
        workflow = SpecialtyWorkflow(
            specialty_key=payload["specialty_key"],
            workflow_id=payload["workflow_id"],
            version=payload["version"],
            mode=payload["mode"],
            steps=tuple(
                WorkflowStep(
                    key=item["key"],
                    title=item["title"],
                    capability=item["capability"],
                )
                for item in raw_steps
            ),
        )
    except (KeyError, TypeError) as exc:
        raise WorkflowDefinitionError("invalid workflow structure") from exc

    if workflow.specialty_key != pack.key:
        raise WorkflowDefinitionError("workflow specialty does not match its pack")
    unknown_capabilities = {
        step.capability for step in workflow.steps
    } - set(pack.required_capabilities)
    if unknown_capabilities:
        names = ", ".join(sorted(unknown_capabilities))
        raise WorkflowDefinitionError(f"workflow uses undeclared capabilities: {names}")
    return workflow


def build_default_workflow_registry(
    packs: SpecialtyPackRegistry, root: Path = DEFAULT_WORKFLOW_ROOT
) -> WorkflowRegistry:
    workflows: list[SpecialtyWorkflow] = []
    for path in sorted(root.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            pack = packs.require(payload["specialty_key"])
        except (json.JSONDecodeError, KeyError, ValueError) as exc:
            raise WorkflowDefinitionError(f"invalid workflow file: {path.name}") from exc
        workflows.append(workflow_from_mapping(payload, pack))
    return WorkflowRegistry(workflows)
