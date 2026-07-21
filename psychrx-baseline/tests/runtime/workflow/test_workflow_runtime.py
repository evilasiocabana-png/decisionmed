import unittest

from clinical_runtime.workflow import (
    WorkflowAudit,
    WorkflowEvent,
    WorkflowExecutor,
    WorkflowRegistry,
    WorkflowState,
    WorkflowValidator,
    consultation_workflow,
    default_workflow_events,
)


class WorkflowRuntimeTest(unittest.TestCase):
    def test_consultation_workflow_is_structural(self) -> None:
        workflow = consultation_workflow()

        self.assertEqual(workflow.workflow_id, "consultation_workflow")
        self.assertIn("strategy_blocked", workflow.node_ids())
        self.assertEqual(workflow.status, "read_only_structural")
        self.assertEqual(WorkflowValidator().validate(workflow), ())

    def test_registry_and_executor_do_not_create_clinical_decision(self) -> None:
        registry = WorkflowRegistry.with_defaults()
        workflow = registry.get("consultation_workflow")
        self.assertIsNotNone(workflow)
        assert workflow is not None

        executor = WorkflowExecutor()
        started = executor.start(workflow)
        paused = executor.pause(workflow)
        resumed = executor.resume(workflow)
        finished = executor.finish(workflow)

        self.assertEqual(registry.list_ids(), ("consultation_workflow",))
        self.assertEqual(started["clinical_decision"], "not_implemented")
        self.assertEqual(started["prescription"], "not_available")
        self.assertFalse(started["runtime_consumption_allowed"])
        self.assertEqual(paused["state"], WorkflowState.WAITING.value)
        self.assertEqual(resumed["state"], WorkflowState.RUNNING.value)
        self.assertEqual(finished["state"], WorkflowState.COMPLETED.value)

    def test_workflow_events_and_audit_are_structural(self) -> None:
        audit = WorkflowAudit()
        event = WorkflowEvent("WorkflowStarted", "consultation_workflow")

        audit.record(event)

        self.assertIn("WorkflowStarted", default_workflow_events())
        self.assertEqual(audit.snapshot()[0]["name"], "WorkflowStarted")
        self.assertTrue(audit.snapshot()[0]["event_id"].startswith("WFE-"))


if __name__ == "__main__":
    unittest.main()

