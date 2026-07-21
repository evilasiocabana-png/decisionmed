import unittest

from decisionmed.reasoning import (
    GovernedReasoningInput,
    QuestionEngineBinding,
    QuestionEngineRegistry,
    QuestionEngineResult,
    ReasoningError,
)


class SyntheticQuestionEngine:
    def __init__(
        self,
        engine_id: str = "question-engine.synthetic",
        provider: str = "decisionmed.reasoning.question-engine.synthetic",
        contract_version: str = "0.1.0",
    ) -> None:
        self.engine_id = engine_id
        self.provider = provider
        self.contract_version = contract_version
        self.call_count = 0

    def generate(self, input_value: GovernedReasoningInput) -> QuestionEngineResult:
        self.call_count += 1
        raise AssertionError("registry must not invoke engines")


def binding() -> QuestionEngineBinding:
    return QuestionEngineBinding(
        engine_id="question-engine.synthetic",
        provider="decisionmed.reasoning.question-engine.synthetic",
        contract_version="0.1.0",
    )


class QuestionEngineRegistryTest(unittest.TestCase):
    def test_exact_identity_completes_registry_without_invocation(self) -> None:
        engine = SyntheticQuestionEngine()
        registry = QuestionEngineRegistry((binding(),))

        self.assertFalse(registry.complete)
        self.assertEqual((engine.engine_id,), registry.missing_engine_ids)
        registry.register(engine)

        self.assertTrue(registry.complete)
        self.assertIs(engine, registry.get(engine.engine_id))
        self.assertEqual((engine,), registry.all())
        self.assertEqual(0, engine.call_count)
        self.assertFalse(registry.engine_invocation_allowed)
        self.assertFalse(registry.reasoning_execution_allowed)
        self.assertFalse(registry.clinical_execution_allowed)

    def test_unknown_or_mismatched_identity_is_rejected(self) -> None:
        registry = QuestionEngineRegistry((binding(),))
        values = (
            SyntheticQuestionEngine(engine_id="question-engine.unknown"),
            SyntheticQuestionEngine(provider="decisionmed.reasoning.other"),
            SyntheticQuestionEngine(contract_version="0.2.0"),
        )
        for engine in values:
            with self.subTest(engine=engine):
                with self.assertRaises(ReasoningError):
                    registry.register(engine)

    def test_duplicate_and_non_protocol_engines_are_rejected(self) -> None:
        engine = SyntheticQuestionEngine()
        registry = QuestionEngineRegistry((binding(),), (engine,))

        with self.assertRaises(ReasoningError) as duplicate:
            registry.register(engine)
        self.assertEqual("question_engine_registry.duplicate", duplicate.exception.code)
        with self.assertRaises(TypeError):
            registry.register(object())  # type: ignore[arg-type]

    def test_bindings_must_be_nonempty_unique_and_valid(self) -> None:
        duplicate = binding()
        for bindings in ((), (duplicate, duplicate), (object(),)):
            with self.subTest(bindings=bindings):
                with self.assertRaises((ReasoningError, TypeError)):
                    QuestionEngineRegistry(bindings)  # type: ignore[arg-type]

        for values in (
            {"engine_id": "Invalid Engine"},
            {"provider": "Invalid Provider"},
            {"contract_version": "v1"},
        ):
            with self.subTest(values=values):
                with self.assertRaises(ReasoningError):
                    QuestionEngineBinding(
                        engine_id=values.get("engine_id", "question-engine.synthetic"),
                        provider=values.get(
                            "provider", "decisionmed.reasoning.question-engine.synthetic"
                        ),
                        contract_version=values.get("contract_version", "0.1.0"),
                    )


if __name__ == "__main__":
    unittest.main()
