from dataclasses import FrozenInstanceError
from datetime import date, timedelta
import unittest

from decisionmed.evidence import (
    EvidenceQuality,
    EvidenceRegistry,
    EvidenceSource,
    EvidenceStatus,
    EvidenceType,
    RecommendationStrength,
)
from decisionmed.safety import (
    SafetyCheckProviderBinding,
    SafetyCheckProviderRegistry,
    SafetyCheckRegistry,
    SafetyCheckSpecification,
    SafetyCheckStatus,
    SafetyError,
)


def evidence(status: EvidenceStatus = EvidenceStatus.VALIDATED) -> EvidenceSource:
    return EvidenceSource(
        source_id="source.synthetic-provider",
        title="Synthetic evidence metadata for provider tests",
        publication_year=2025,
        evidence_type=EvidenceType.OTHER,
        evidence_quality=EvidenceQuality.INSUFFICIENT,
        recommendation_strength=RecommendationStrength.INSUFFICIENT_FOR_RECOMMENDATION,
        locator="test-only:synthetic-provider",
        version="0.1.0",
        status=status,
        specialties=("cardiology",),
        reviewed_on=date.today(),
        known_conflicts="Synthetic fixture; no clinical conflicts assessed.",
        clinical_applicability="Structural contract tests only.",
        review_due_on=(
            date.today() + timedelta(days=30)
            if status is EvidenceStatus.VALIDATED
            else None
        ),
    )


def specification(
    *,
    check_id: str = "check.synthetic-provider",
    status: SafetyCheckStatus = SafetyCheckStatus.VALIDATED,
) -> SafetyCheckSpecification:
    return SafetyCheckSpecification(
        check_id=check_id,
        specialty_key="cardiology",
        purpose="Synthetic provider contract without a clinical rule.",
        limits="Does not evaluate patient data or authorize execution.",
        evidence_source_ids=("source.synthetic-provider",),
        version="0.1.0",
        status=status,
        reviewed_on=date.today()
        if status is SafetyCheckStatus.VALIDATED
        else None,
        validated_by="reviewer.synthetic"
        if status is SafetyCheckStatus.VALIDATED
        else None,
        review_due_on=(
            date.today() + timedelta(days=30)
            if status is SafetyCheckStatus.VALIDATED
            else None
        ),
    )


def specifications(
    *items: SafetyCheckSpecification,
) -> SafetyCheckRegistry:
    return SafetyCheckRegistry(EvidenceRegistry((evidence(),)), items)


class SafetyCheckProviderRegistryTest(unittest.TestCase):
    def test_binding_is_immutable_versioned_and_non_executable(self) -> None:
        binding = SafetyCheckProviderBinding(
            "check.synthetic-provider", "decisionmed.safety.synthetic", "0.1.0"
        )

        self.assertFalse(binding.clinical_execution_allowed)
        with self.assertRaises(FrozenInstanceError):
            binding.version = "0.2.0"  # type: ignore[misc]
        with self.assertRaises(SafetyError):
            SafetyCheckProviderBinding("invalid id", "provider", "0.1.0")

    def test_registry_rejects_unknown_or_unvalidated_specifications(self) -> None:
        binding = SafetyCheckProviderBinding(
            "check.synthetic-provider", "decisionmed.safety.synthetic", "0.1.0"
        )
        with self.assertRaises(SafetyError) as unknown:
            SafetyCheckProviderRegistry(specifications()).register(binding)
        self.assertEqual(
            "safety_provider_registry.unknown_specification",
            unknown.exception.code,
        )

        draft_registry = SafetyCheckRegistry(
            EvidenceRegistry((evidence(EvidenceStatus.DRAFT),)),
            (specification(status=SafetyCheckStatus.DRAFT),),
        )
        with self.assertRaises(SafetyError) as draft:
            SafetyCheckProviderRegistry(draft_registry).register(binding)
        self.assertEqual(
            "safety_provider_registry.unvalidated_specification",
            draft.exception.code,
        )

    def test_exact_binding_produces_complete_structural_coverage_only(self) -> None:
        item = specification()
        registry = SafetyCheckProviderRegistry(
            specifications(item),
            (
                SafetyCheckProviderBinding(
                    item.check_id, "decisionmed.safety.synthetic", item.version
                ),
            ),
        )

        coverage = registry.coverage()

        self.assertTrue(coverage.complete)
        self.assertEqual((item.check_id,), coverage.bound_check_ids)
        self.assertFalse(coverage.clinical_execution_allowed)

    def test_missing_and_incompatible_bindings_fail_coverage(self) -> None:
        alpha = specification(check_id="check.alpha")
        beta = specification(check_id="check.beta")
        registry = SafetyCheckProviderRegistry(
            specifications(alpha, beta),
            (
                SafetyCheckProviderBinding(
                    alpha.check_id, "decisionmed.safety.alpha", "0.2.0"
                ),
            ),
        )

        coverage = registry.coverage()

        self.assertFalse(coverage.complete)
        self.assertEqual((beta.check_id,), coverage.missing_check_ids)
        self.assertEqual((alpha.check_id,), coverage.incompatible_check_ids)
        self.assertEqual((), coverage.bound_check_ids)

    def test_duplicate_provider_is_rejected(self) -> None:
        item = specification()
        binding = SafetyCheckProviderBinding(
            item.check_id, "decisionmed.safety.synthetic", item.version
        )
        registry = SafetyCheckProviderRegistry(specifications(item), (binding,))

        with self.assertRaises(SafetyError) as duplicate:
            registry.register(binding)

        self.assertEqual("safety_provider_registry.duplicate", duplicate.exception.code)


if __name__ == "__main__":
    unittest.main()
