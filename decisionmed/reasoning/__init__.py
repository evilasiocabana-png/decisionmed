"""DecisionMEd Reasoning Layer structural contracts."""

from .gate import (
    ReasoningError,
    ReasoningGate,
    ReasoningGateResult,
    ReasoningGateStatus,
)
from .input import ReasoningInputEnvelope
from .knowledge_binding import ReasoningKnowledgeBinding
from .governed_input import GovernedReasoningInput
from .question_engine import (
    QuestionEngine,
    QuestionEngineItem,
    QuestionEngineResult,
    QuestionEngineState,
    QuestionRequirement,
)
from .question_validation import (
    QuestionEngineOutputValidator,
    QuestionEngineValidationReceipt,
)
from .question_registry import QuestionEngineBinding, QuestionEngineRegistry

__all__ = [
    "ReasoningError",
    "ReasoningGate",
    "ReasoningGateResult",
    "ReasoningGateStatus",
    "ReasoningInputEnvelope",
    "ReasoningKnowledgeBinding",
    "GovernedReasoningInput",
    "QuestionEngine",
    "QuestionEngineItem",
    "QuestionEngineResult",
    "QuestionEngineState",
    "QuestionRequirement",
    "QuestionEngineOutputValidator",
    "QuestionEngineValidationReceipt",
    "QuestionEngineBinding",
    "QuestionEngineRegistry",
]
