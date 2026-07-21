"""Runtime pipeline step abstraction."""

from __future__ import annotations

from dataclasses import dataclass

from clinical_runtime.pipeline.pipeline_result import PipelineResult


@dataclass(frozen=True)
class PipelineStep:
    name: str
    status_value: str = "pending"

    def validate(self) -> bool:
        return bool(self.name)

    def execute(self) -> PipelineResult:
        return PipelineResult(status="completed", outputs={self.name: "structural"})

    def rollback(self) -> PipelineResult:
        return PipelineResult(status="rolled_back", warnings=(f"{self.name} rollback structural only.",))

    def trace(self) -> tuple[str, ...]:
        return (self.name,)

    def status(self) -> str:
        return self.status_value
