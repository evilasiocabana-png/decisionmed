import inspect
from typing import get_type_hints
import unittest

from decisionmed.domain import ClinicalSnapshot
from decisionmed.safety import SafetyCheckEvaluator, SafetyCheckResult


class SafetyCheckEvaluatorPortTest(unittest.TestCase):
    def test_port_declares_snapshot_trace_and_result_contract(self) -> None:
        signature = inspect.signature(SafetyCheckEvaluator.evaluate)
        hints = get_type_hints(SafetyCheckEvaluator.evaluate)

        self.assertIs(ClinicalSnapshot, hints["snapshot"])
        self.assertIs(str, hints["trace_id"])
        self.assertIs(SafetyCheckResult, hints["return"])
        self.assertEqual(
            inspect.Parameter.KEYWORD_ONLY,
            signature.parameters["trace_id"].kind,
        )

    def test_port_requires_identity_and_exact_specification_version(self) -> None:
        self.assertIsInstance(SafetyCheckEvaluator.check_id, property)
        self.assertIsInstance(SafetyCheckEvaluator.provider, property)
        self.assertIsInstance(SafetyCheckEvaluator.specification_version, property)
        self.assertIs(str, get_type_hints(SafetyCheckEvaluator.check_id.fget)["return"])
        self.assertIs(str, get_type_hints(SafetyCheckEvaluator.provider.fget)["return"])
        self.assertIs(
            str,
            get_type_hints(SafetyCheckEvaluator.specification_version.fget)["return"],
        )

    def test_protocol_has_no_default_evaluator(self) -> None:
        with self.assertRaises(TypeError):
            SafetyCheckEvaluator()  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
