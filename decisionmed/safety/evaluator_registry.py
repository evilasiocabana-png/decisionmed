"""Identity-only registry for future safety-check evaluators."""

from __future__ import annotations

from collections.abc import Iterable

from .evaluator import SafetyCheckEvaluator
from .models import SafetyError
from .providers import SafetyCheckProviderRegistry


class SafetyCheckEvaluatorRegistry:
    """Bind evaluator objects to governed descriptors without invoking them."""

    def __init__(
        self,
        providers: SafetyCheckProviderRegistry,
        evaluators: Iterable[SafetyCheckEvaluator] = (),
    ) -> None:
        if not isinstance(providers, SafetyCheckProviderRegistry):
            raise TypeError("providers must be a SafetyCheckProviderRegistry")
        if not providers.coverage().complete:
            raise SafetyError(
                "safety_evaluator_registry.provider_coverage",
                "complete compatible provider coverage is required",
            )
        self._providers = providers
        self._evaluators: dict[str, SafetyCheckEvaluator] = {}
        for evaluator in evaluators:
            self.register(evaluator)

    def register(self, evaluator: SafetyCheckEvaluator) -> SafetyCheckEvaluator:
        if not isinstance(evaluator, SafetyCheckEvaluator):
            raise TypeError("evaluator must satisfy SafetyCheckEvaluator")
        binding = self._providers.get(evaluator.check_id)
        if binding is None:
            raise SafetyError(
                "safety_evaluator_registry.unknown_provider",
                f"provider not registered for check: {evaluator.check_id}",
            )
        if (
            evaluator.provider != binding.provider
            or evaluator.specification_version != binding.version
        ):
            raise SafetyError(
                "safety_evaluator_registry.identity_mismatch",
                "evaluator identity must exactly match its provider binding",
            )
        if evaluator.check_id in self._evaluators:
            raise SafetyError(
                "safety_evaluator_registry.duplicate",
                f"evaluator already registered: {evaluator.check_id}",
            )
        self._evaluators[evaluator.check_id] = evaluator
        return evaluator

    def get(self, check_id: str) -> SafetyCheckEvaluator | None:
        return self._evaluators.get(check_id)

    def all(self) -> tuple[SafetyCheckEvaluator, ...]:
        return tuple(self._evaluators[key] for key in sorted(self._evaluators))

    @property
    def missing_check_ids(self) -> tuple[str, ...]:
        return tuple(
            binding.check_id
            for binding in self._providers.all()
            if binding.check_id not in self._evaluators
        )

    @property
    def complete(self) -> bool:
        return bool(self._providers.all()) and not self.missing_check_ids

    @property
    def clinical_execution_allowed(self) -> bool:
        return False
