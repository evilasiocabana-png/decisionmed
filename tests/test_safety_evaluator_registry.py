from datetime import date, timedelta
import unittest

from decisionmed.domain import ClinicalSnapshot
from decisionmed.evidence import (
    EvidenceQuality,
    EvidenceRegistry,
    EvidenceSource,
    EvidenceStatus,
    EvidenceType,
    RecommendationStrength,
)
from decisionmed.safety import (
    SafetyCheckEvaluatorRegistry,
    SafetyCheckProviderBinding,
    SafetyCheckProviderRegistry,
    SafetyCheckRegistry,
    SafetyCheckResult,
    SafetyCheckSpecification,
    SafetyCheckStatus,
    SafetyError,
)


class SyntheticEvaluator:
    def __init__(
        self,
        check_id: str = "check.synthetic-evaluator",
        provider: str = "decisionmed.safety.synthetic-evaluator",
        specification_version: str = "0.1.0",
    ) -> None:
        self.check_id = check_id
        self.provider = provider
        self.specification_version = specification_version
        self.call_count = 0

    def evaluate(
        self, snapshot: ClinicalSnapshot, *, trace_id: str
    ) -> SafetyCheckResult:
        self.call_count += 1
        raise AssertionError("registry must not invoke evaluators")


def providers() -> SafetyCheckProviderRegistry:
    evidence = EvidenceRegistry(
        (
            EvidenceSource(
                source_id="source.synthetic-evaluator",
                title="Synthetic evaluator registry evidence",
                publication_year=2025,
                evidence_type=EvidenceType.OTHER,
                evidence_quality=EvidenceQuality.INSUFFICIENT,
                recommendation_strength=(
                    RecommendationStrength.INSUFFICIENT_FOR_RECOMMENDATION
                ),
                locator="test-only:synthetic-evaluator",
                version="0.1.0",
                status=EvidenceStatus.VALIDATED,
                specialties=("cardiology",),
                reviewed_on=date.today(),
                known_conflicts="Synthetic fixture.",
                clinical_applicability="Structural tests only.",
                review_due_on=date.today() + timedelta(days=30),
            ),
        )
    )
    specifications = SafetyCheckRegistry(
        evidence,
        (
            SafetyCheckSpecification(
                check_id="check.synthetic-evaluator",
                specialty_key="cardiology",
                purpose="Synthetic registry contract without a clinical rule.",
                limits="Does not evaluate patient data or authorize execution.",
                evidence_source_ids=("source.synthetic-evaluator",),
                version="0.1.0",
                status=SafetyCheckStatus.VALIDATED,
                reviewed_on=date.today(),
                validated_by="reviewer.synthetic",
                review_due_on=date.today() + timedelta(days=30),
            ),
        ),
    )
    return SafetyCheckProviderRegistry(
        specifications,
        (
            SafetyCheckProviderBinding(
                "check.synthetic-evaluator",
                "decisionmed.safety.synthetic-evaluator",
                "0.1.0",
            ),
        ),
    )


class SafetyCheckEvaluatorRegistryTest(unittest.TestCase):
    def test_exact_identity_completes_registration_without_invocation(self) -> None:
        evaluator = SyntheticEvaluator()
        registry = SafetyCheckEvaluatorRegistry(providers())

        self.assertFalse(registry.complete)
        self.assertEqual((evaluator.check_id,), registry.missing_check_ids)
        registry.register(evaluator)

        self.assertTrue(registry.complete)
        self.assertEqual(0, evaluator.call_count)
        self.assertFalse(registry.clinical_execution_allowed)

    def test_unknown_or_mismatched_identity_is_rejected(self) -> None:
        registry = SafetyCheckEvaluatorRegistry(providers())
        with self.assertRaises(SafetyError) as unknown:
            registry.register(SyntheticEvaluator(check_id="check.unknown"))
        self.assertEqual(
            "safety_evaluator_registry.unknown_provider", unknown.exception.code
        )

        for evaluator in (
            SyntheticEvaluator(provider="decisionmed.safety.other"),
            SyntheticEvaluator(specification_version="0.2.0"),
        ):
            with self.assertRaises(SafetyError) as mismatch:
                registry.register(evaluator)
            self.assertEqual(
                "safety_evaluator_registry.identity_mismatch",
                mismatch.exception.code,
            )

    def test_duplicate_or_non_protocol_evaluator_is_rejected(self) -> None:
        evaluator = SyntheticEvaluator()
        registry = SafetyCheckEvaluatorRegistry(providers(), (evaluator,))

        with self.assertRaises(SafetyError) as duplicate:
            registry.register(evaluator)
        self.assertEqual(
            "safety_evaluator_registry.duplicate", duplicate.exception.code
        )
        with self.assertRaises(TypeError):
            registry.register(object())  # type: ignore[arg-type]

    def test_incomplete_or_incompatible_provider_coverage_is_rejected(self) -> None:
        complete = providers()
        incomplete = SafetyCheckProviderRegistry(complete.specifications)
        incompatible = SafetyCheckProviderRegistry(
            complete.specifications,
            (
                SafetyCheckProviderBinding(
                    "check.synthetic-evaluator",
                    "decisionmed.safety.synthetic-evaluator",
                    "0.2.0",
                ),
            ),
        )

        for provider_registry in (incomplete, incompatible):
            with self.assertRaises(SafetyError) as coverage:
                SafetyCheckEvaluatorRegistry(provider_registry)
            self.assertEqual(
                "safety_evaluator_registry.provider_coverage",
                coverage.exception.code,
            )


if __name__ == "__main__":
    unittest.main()
