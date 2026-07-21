import copy
import json
from pathlib import Path
import unittest

from decisionmed.specialties import PSYCHIATRY_PACK, build_default_specialty_registry
from decisionmed.workflows import (
    WorkflowDefinitionError,
    build_default_workflow_registry,
    workflow_from_mapping,
)


WORKFLOW_PATH = Path(__file__).resolve().parents[1] / "data" / "specialties" / "psychiatry.json"


class WorkflowContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = json.loads(WORKFLOW_PATH.read_text(encoding="utf-8"))

    def test_default_psychiatry_workflow_has_ordered_reference_steps(self) -> None:
        registry = build_default_workflow_registry(build_default_specialty_registry())
        workflow = registry.require("psychiatry")
        rendered = workflow.to_dict()

        self.assertEqual("psychrx.clinical-decision.v1", workflow.workflow_id)
        self.assertEqual(13, len(workflow.steps))
        self.assertEqual("context", workflow.steps[0].key)
        self.assertEqual("monitoring", workflow.steps[-1].key)
        self.assertEqual(1, rendered["steps"][0]["position"])
        self.assertFalse(rendered["clinical_execution_allowed"])

    def test_rejects_duplicate_steps(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["steps"][1]["key"] = payload["steps"][0]["key"]

        with self.assertRaises(WorkflowDefinitionError):
            workflow_from_mapping(payload, PSYCHIATRY_PACK)

    def test_rejects_undeclared_capability(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["steps"][0]["capability"] = "prescribing"

        with self.assertRaises(WorkflowDefinitionError):
            workflow_from_mapping(payload, PSYCHIATRY_PACK)

    def test_rejects_clinical_execution_mode(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["mode"] = "active"

        with self.assertRaises(WorkflowDefinitionError):
            workflow_from_mapping(payload, PSYCHIATRY_PACK)


if __name__ == "__main__":
    unittest.main()
