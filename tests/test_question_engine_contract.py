from dataclasses import FrozenInstanceError, replace
import inspect
from typing import get_type_hints
import unittest

from decisionmed.reasoning import (
    GovernedReasoningInput,
    QuestionEngine,
    QuestionEngineItem,
    QuestionEngineResult,
    QuestionEngineState,
    QuestionRequirement,
    ReasoningError,
)


INPUT_FINGERPRINT = "a" * 64
TRACE_ID = "trace.synthetic-question-engine"


class SyntheticQuestionEngine:
    engine_id = "question-engine.synthetic"
    provider = "decisionmed.reasoning.question-engine.synthetic"
    contract_version = "0.1.0"

    def generate(self, input_value: GovernedReasoningInput) -> QuestionEngineResult:
        raise AssertionError("contract test must not invoke a concrete engine")


class QuestionEngineContractTest(unittest.TestCase):
    def test_prioritized_result_is_immutable_traceable_and_non_executable(self) -> None:
        second = self._question(
            question_id="question.second",
            field_key="symptoms.second",
            priority_rank=2,
            requirement=QuestionRequirement.CONDITIONAL,
        )
        first = self._question(
            question_id="question.first",
            field_key="symptoms.first",
            priority_rank=1,
        )
        result = self._result(
            questions=(second, first),
            gaps=("symptoms.first", "symptoms.second"),
        )

        self.assertEqual((first, second), result.questions)
        self.assertEqual(
            ("knowledge.synthetic-question",),
            result.knowledge_object_ids,
        )
        self.assertEqual(
            ("source.synthetic-question",),
            result.evidence_source_ids,
        )
        self.assertFalse(result.reasoning_execution_allowed)
        self.assertFalse(result.clinical_execution_allowed)
        self.assertFalse(first.clinical_execution_allowed)
        with self.assertRaises(FrozenInstanceError):
            result.state = QuestionEngineState.COLLECTION_SUFFICIENT  # type: ignore[misc]

    def test_collection_sufficient_has_no_questions_or_open_gaps(self) -> None:
        result = self._result(
            state=QuestionEngineState.COLLECTION_SUFFICIENT,
            questions=(),
            gaps=(),
        )

        self.assertEqual((), result.questions)
        self.assertEqual((), result.open_gap_field_keys)

    def test_result_rejects_noncontiguous_or_duplicate_priorities(self) -> None:
        for questions in (
            (
                self._question(question_id="question.one", priority_rank=1),
                self._question(question_id="question.two", priority_rank=3),
            ),
            (
                self._question(question_id="question.one", priority_rank=1),
                self._question(question_id="question.two", priority_rank=1),
            ),
        ):
            with self.subTest(ranks=tuple(item.priority_rank for item in questions)):
                with self.assertRaises(ReasoningError):
                    self._result(questions=questions, gaps=("symptoms.synthetic",))

    def test_result_rejects_mismatched_input_trace_and_untracked_gap(self) -> None:
        base = self._question()
        for question, gaps in (
            (replace(base, governed_input_fingerprint="b" * 64), (base.field_key,)),
            (replace(base, trace_id="trace.other"), (base.field_key,)),
            (base, ("symptoms.other",)),
        ):
            with self.subTest(question=question, gaps=gaps):
                with self.assertRaises(ReasoningError):
                    self._result(questions=(question,), gaps=gaps)

    def test_state_invariants_fail_closed(self) -> None:
        question = self._question()
        for state, questions, gaps in (
            (QuestionEngineState.COLLECTION_PENDING, (), ()),
            (
                QuestionEngineState.COLLECTION_SUFFICIENT,
                (question,),
                (question.field_key,),
            ),
            (QuestionEngineState.UNCERTAINTY_PERSISTS, (), ()),
        ):
            with self.subTest(state=state):
                with self.assertRaises(ReasoningError):
                    self._result(state=state, questions=questions, gaps=gaps)

    def test_question_requires_explanation_and_exact_source_references(self) -> None:
        base = self._question()
        for values in (
            {"prompt": ""},
            {"rationale": ""},
            {"knowledge_object_ids": ()},
            {"evidence_source_ids": ()},
            {"governed_input_fingerprint": "invalid"},
        ):
            with self.subTest(values=values):
                with self.assertRaises(ReasoningError):
                    replace(base, **values)

    def test_port_declares_exact_input_output_and_has_no_implementation(self) -> None:
        signature = inspect.signature(QuestionEngine.generate)
        hints = get_type_hints(QuestionEngine.generate)
        adapter = SyntheticQuestionEngine()

        self.assertIs(GovernedReasoningInput, hints["input_value"])
        self.assertIs(QuestionEngineResult, hints["return"])
        self.assertIn("input_value", signature.parameters)
        self.assertIsInstance(adapter, QuestionEngine)
        self.assertNotIsInstance(object(), QuestionEngine)
        with self.assertRaises(TypeError):
            QuestionEngine()  # type: ignore[misc]

    def _question(
        self,
        *,
        question_id: str = "question.synthetic",
        field_key: str = "symptoms.synthetic",
        priority_rank: int = 1,
        requirement: QuestionRequirement = QuestionRequirement.REQUIRED,
    ) -> QuestionEngineItem:
        return QuestionEngineItem(
            question_id=question_id,
            field_key=field_key,
            prompt="Synthetic structural prompt?",
            requirement=requirement,
            priority_rank=priority_rank,
            rationale="Synthetic structural rationale.",
            knowledge_object_ids=("knowledge.synthetic-question",),
            evidence_source_ids=("source.synthetic-question",),
            trace_id=TRACE_ID,
            governed_input_fingerprint=INPUT_FINGERPRINT,
        )

    def _result(
        self,
        *,
        state: QuestionEngineState = QuestionEngineState.COLLECTION_PENDING,
        questions: tuple[QuestionEngineItem, ...] | None = None,
        gaps: tuple[str, ...] | None = None,
    ) -> QuestionEngineResult:
        if questions is None:
            questions = (self._question(),)
        if gaps is None:
            gaps = tuple(question.field_key for question in questions)
        return QuestionEngineResult(
            engine_id="question-engine.synthetic",
            engine_version="0.1.0",
            provider="decisionmed.reasoning.question-engine.synthetic",
            governed_input_fingerprint=INPUT_FINGERPRINT,
            trace_id=TRACE_ID,
            state=state,
            questions=questions,
            open_gap_field_keys=gaps,
            explanation="Synthetic structural result explanation.",
        )


if __name__ == "__main__":
    unittest.main()
