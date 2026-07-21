"""Runtime pipeline engine."""

from __future__ import annotations

from clinical_runtime.pipeline.pipeline_result import PipelineResult
from clinical_runtime.pipeline.pipeline_step import PipelineStep


class RuntimePipeline:
    """Sequential structural pipeline. No clinical engine logic."""

    def __init__(self, steps: tuple[PipelineStep, ...]) -> None:
        self._steps = steps

    def run(self) -> PipelineResult:
        outputs = {}
        for step in self._steps:
            if not step.validate():
                return PipelineResult(status="invalid", errors=(f"{step.name} invalid",))
            result = step.execute()
            outputs.update(result.outputs)
        return PipelineResult(status="completed_read_only", outputs=outputs)
