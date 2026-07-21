"""Read-only adapter between Application Layer and Clinical Kernel."""

from __future__ import annotations

from clinical_kernel.context.clinical_context import ClinicalContext
from clinical_kernel.execution.kernel_result import KernelResult
from clinical_kernel.pipeline.pipeline_skeleton import PipelineSkeleton


class ApplicationKernelAdapter:
    """Application-facing adapter for structural Clinical Kernel state."""

    def __init__(self, pipeline: PipelineSkeleton | None = None) -> None:
        self._pipeline = pipeline or PipelineSkeleton()

    def get_kernel_result(self) -> KernelResult:
        """Return structural kernel metadata without clinical execution."""
        return self._pipeline.run(ClinicalContext.empty())
