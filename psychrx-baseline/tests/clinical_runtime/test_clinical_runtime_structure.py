import io
import unittest
from pathlib import Path
from contextlib import redirect_stdout

from clinical_runtime import ClinicalRuntime
from clinical_runtime.audit import RuntimeAudit, RuntimeAuditEntry, RuntimeLogger
from clinical_runtime.context import RuntimeContext
from clinical_runtime.events import RuntimeEvent, RuntimeEventBus, RuntimeSubscribers, default_runtime_events
from clinical_runtime.integration import (
    KernelRuntimeAdapter,
    KnowledgeRuntimeAdapter,
    WorkspaceRuntimeAdapter,
)
from clinical_runtime.pipeline import PipelineStep, RuntimePipeline
from clinical_runtime.replay import RuntimeReplay
from clinical_runtime.scheduler import ExecutionMonitor, ExecutionQueue, RuntimeScheduler, ScheduledItem
from clinical_runtime.session import RuntimeSessionManager
from clinical_runtime.store import RuntimeStore
from clinical_runtime.trace import ExecutionTrace
from clinical_runtime.validator import RuntimeValidator


class ClinicalRuntimeStructureTest(unittest.TestCase):
    def test_runtime_package_structure_exists(self) -> None:
        required_dirs = [
            "session",
            "context",
            "pipeline",
            "scheduler",
            "events",
            "store",
            "validator",
            "audit",
            "trace",
            "replay",
            "integration",
        ]

        for dirname in required_dirs:
            with self.subTest(dirname=dirname):
                self.assertTrue((Path("clinical_runtime") / dirname).is_dir())

    def test_session_context_store_and_validator_are_structural(self) -> None:
        session = RuntimeSessionManager().open_session()
        closed = session.close()
        context = RuntimeContext().with_update(execution_status="running")
        store = RuntimeStore()
        validator = RuntimeValidator()

        store.set("kernel", "structural")

        self.assertTrue(session.session_id.startswith("RTS-"))
        self.assertEqual(closed.status, "closed")
        self.assertEqual(context.execution_status, "running")
        self.assertEqual(store.get("kernel"), "structural")
        self.assertEqual(validator.validate_context(context), ())

    def test_pipeline_scheduler_queue_and_monitor_are_structural(self) -> None:
        pipeline = RuntimePipeline((PipelineStep("Kernel"), PipelineStep("Knowledge")))
        result = pipeline.run()
        scheduler = RuntimeScheduler()
        queue = ExecutionQueue()
        item = ScheduledItem(priority=1, name="Kernel")
        monitor = ExecutionMonitor(current_engine="Kernel", waiting_engines=("Knowledge",))

        queue.push(item)

        self.assertEqual(result.status, "completed_read_only")
        self.assertEqual(scheduler.order((item,))[0].name, "Kernel")
        self.assertEqual(queue.pop().name, "Kernel")
        self.assertEqual(monitor.current_engine, "Kernel")

    def test_events_subscribers_audit_trace_and_replay_are_structural(self) -> None:
        bus = RuntimeEventBus()
        subscribers = RuntimeSubscribers()
        event = RuntimeEvent("RuntimeFinished", {"status": "completed_read_only"})
        audit = RuntimeAudit()
        entry = RuntimeAuditEntry(event="RuntimeFinished")
        trace = ExecutionTrace(execution_tree=("Kernel",), widget_tree=("Strategy Widget",))

        bus.subscribe("RuntimeFinished", subscribers.capture_all)
        bus.publish(event)
        audit.record(entry)
        replayed = RuntimeReplay(audit.snapshot()).replay()

        self.assertIn("RuntimeFinished", default_runtime_events())
        self.assertEqual(len(subscribers.logger), 1)
        self.assertEqual(replayed[0].event, "RuntimeFinished")
        self.assertTrue(trace.trace_id.startswith("TRC-"))
        stream = io.StringIO()
        with redirect_stdout(stream):
            line = RuntimeLogger().log("test")
        self.assertIn("[clinical-runtime]", line)

    def test_integrations_do_not_create_clinical_decision(self) -> None:
        workspace_session = WorkspaceRuntimeAdapter().start()
        kernel_result = KernelRuntimeAdapter().execute_kernel()
        knowledge_sections = KnowledgeRuntimeAdapter().list_available_sections()
        runtime_result = ClinicalRuntime().execute()

        self.assertEqual(workspace_session["status"], "open")
        self.assertEqual(kernel_result["status"], "read_only_structural")
        self.assertIn("guidelines", knowledge_sections)
        self.assertEqual(runtime_result["clinical_decision"], "not_implemented")
        self.assertEqual(runtime_result["prescription"], "not_available")


if __name__ == "__main__":
    unittest.main()
