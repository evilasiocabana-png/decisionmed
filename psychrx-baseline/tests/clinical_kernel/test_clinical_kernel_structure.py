import unittest
from pathlib import Path

from clinical_kernel.audit import PipelineAudit
from clinical_kernel.context import ClinicalContext
from clinical_kernel.errors import (
    EngineUnavailable,
    InvalidClinicalContext,
    InvalidClinicalState,
    PipelineNotReady,
    StrategyLocked,
)
from clinical_kernel.execution import EngineExecutor, KernelResult
from clinical_kernel.memory import KernelMemory
from clinical_kernel.pipeline import PipelineSkeleton
from clinical_kernel.registry import EngineRegistry
from clinical_kernel.state import ClinicalState
from clinical_kernel.validation import KernelValidator


class ClinicalKernelStructureTest(unittest.TestCase):
    def test_official_package_structure_exists(self) -> None:
        required = [
            "context",
            "state",
            "pipeline",
            "execution",
            "registry",
            "memory",
            "audit",
            "validation",
            "errors",
        ]

        for dirname in required:
            with self.subTest(dirname=dirname):
                self.assertTrue((Path("clinical_kernel") / dirname).is_dir())

    def test_clinical_context_is_structural(self) -> None:
        context = ClinicalContext.empty()

        self.assertEqual(context.metadata["mode"], "read-only")
        self.assertEqual(context.medications, ())
        self.assertIn("clinical_snapshot", context.to_dict())

    def test_clinical_state_defines_initial_states(self) -> None:
        values = {state.value for state in ClinicalState}

        self.assertIn("initialized", values)
        self.assertIn("strategy_blocked", values)
        self.assertIn("completed_read_only", values)

    def test_kernel_result_blocks_strategy(self) -> None:
        result = KernelResult.read_only_blocked()

        self.assertEqual(result.status, "read_only_structural")
        self.assertIn("Strategies blocked", result.blocked_reason)
        self.assertEqual(result.audit_metadata["prescription"], "not_available")

    def test_registry_and_executor_do_not_run_clinical_logic(self) -> None:
        registry = EngineRegistry()
        engines = registry.list_engines()
        result = EngineExecutor().execute(engines)

        self.assertTrue(engines)
        self.assertTrue(all(engine.status == "future_integration" for engine in engines))
        self.assertEqual(result.audit_metadata["engine_execution"], "not_implemented")
        self.assertIn("No clinical reasoning engine", result.warnings[0])

    def test_pipeline_returns_read_only_result(self) -> None:
        result = PipelineSkeleton().run()

        self.assertEqual(result.status, "read_only_structural")
        self.assertTrue(result.audit_metadata["read_only"])
        self.assertIn("Strategy Block", result.audit_metadata["pipeline_steps"])

    def test_audit_memory_validation_and_errors_are_structural(self) -> None:
        audit = PipelineAudit(planned_steps=("ClinicalContext",), blocked_steps=("Safety",))
        memory = KernelMemory()
        validator = KernelValidator()
        result = KernelResult.read_only_blocked()

        memory.record("pipeline_started")

        self.assertEqual(audit.to_metadata()["mode"], "read-only")
        self.assertEqual(memory.snapshot(), ("pipeline_started",))
        self.assertTrue(validator.validate_context(ClinicalContext.empty()))
        self.assertTrue(validator.validate_state(ClinicalState.STRATEGY_BLOCKED))
        self.assertTrue(validator.validate_result(result))
        for error_type in (
            InvalidClinicalContext,
            InvalidClinicalState,
            PipelineNotReady,
            EngineUnavailable,
            StrategyLocked,
        ):
            with self.subTest(error_type=error_type.__name__):
                self.assertTrue(issubclass(error_type, Exception))


if __name__ == "__main__":
    unittest.main()
