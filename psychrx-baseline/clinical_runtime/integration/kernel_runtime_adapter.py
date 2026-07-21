"""Runtime to Kernel adapter."""

from __future__ import annotations

from application.kernel_adapter import ApplicationKernelAdapter


class KernelRuntimeAdapter:
    """Executes the structural kernel through the runtime boundary."""

    def execute_kernel(self) -> dict[str, object]:
        return ApplicationKernelAdapter().get_kernel_result().to_dict()
