from dataclasses import FrozenInstanceError, replace
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
    SafetyCheckRegistry,
    SafetyCheckSpecification,
    SafetyCheckStatus,
    SafetyError,
)


def source(
    *,
    source_id: str = "source.synthetic-safety",
    status: EvidenceStatus = EvidenceStatus.DRAFT,
    specialties: tuple[str, ...] = ("cardiology",),
) -> EvidenceSource:
    return EvidenceSource(
        source_id=source_id,
        title="Synthetic evidence metadata for safety registry tests",
        publication_year=2025,
        evidence_type=EvidenceType.OTHER,
        evidence_quality=EvidenceQuality.INSUFFICIENT,
        recommendation_strength=RecommendationStrength.INSUFFICIENT_FOR_RECOMMENDATION,
        locator="test-only:synthetic-safety",
        version="0.1.0",
        status=status,
        specialties=specialties,
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
    check_id: str = "check.synthetic-safety",
    status: SafetyCheckStatus = SafetyCheckStatus.DRAFT,
    source_id: str = "source.synthetic-safety",
) -> SafetyCheckSpecification:
    return SafetyCheckSpecification(
        check_id=check_id,
        specialty_key="cardiology",
        purpose="Synthetic metadata contract with no clinical rule.",
        limits="Does not evaluate a patient or authorize execution.",
        evidence_source_ids=(source_id,),
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


class SafetyCheckSpecificationTest(unittest.TestCase):
    def test_metadata_is_immutable_and_never_runtime_eligible(self) -> None:
        item = specification()

        self.assertEqual("unscheduled", item.review_state)
        self.assertFalse(item.runtime_eligible)
        self.assertFalse(item.clinical_execution_allowed)
        with self.assertRaises(FrozenInstanceError):
            item.status = SafetyCheckStatus.VALIDATED  # type: ignore[misc]

    def test_validated_specification_requires_current_review_metadata(self) -> None:
        with self.assertRaises(SafetyError) as missing:
            replace(specification(), status=SafetyCheckStatus.VALIDATED)
        self.assertEqual(
            "safety_check_specification.validation", missing.exception.code
        )

        item = specification(status=SafetyCheckStatus.VALIDATED)
        self.assertEqual("current", item.review_state)
        self.assertFalse(item.review_overdue)

    def test_review_due_date_requires_a_prior_review(self) -> None:
        with self.assertRaises(SafetyError) as no_review:
            replace(
                specification(),
                review_due_on=date.today() + timedelta(days=1),
            )
        self.assertEqual(
            "safety_check_specification.review_due_on", no_review.exception.code
        )


class SafetyCheckRegistryTest(unittest.TestCase):
    def test_registry_rejects_unknown_or_wrong_specialty_evidence(self) -> None:
        with self.assertRaises(SafetyError) as unknown:
            SafetyCheckRegistry(EvidenceRegistry()).register(specification())
        self.assertEqual(
            "safety_check_registry.unknown_evidence", unknown.exception.code
        )

        registry = SafetyCheckRegistry(
            EvidenceRegistry((source(specialties=("neurology",)),))
        )
        with self.assertRaises(SafetyError) as mismatch:
            registry.register(specification())
        self.assertEqual(
            "safety_check_registry.specialty_evidence_mismatch",
            mismatch.exception.code,
        )

    def test_validated_specification_requires_validated_evidence(self) -> None:
        registry = SafetyCheckRegistry(EvidenceRegistry((source(),)))

        with self.assertRaises(SafetyError) as error:
            registry.register(specification(status=SafetyCheckStatus.VALIDATED))

        self.assertEqual(
            "safety_check_registry.unvalidated_evidence", error.exception.code
        )

    def test_registry_is_deterministic_and_rejects_duplicates(self) -> None:
        evidence = EvidenceRegistry((source(status=EvidenceStatus.VALIDATED),))
        alpha = specification(
            check_id="check.alpha", status=SafetyCheckStatus.VALIDATED
        )
        beta = specification(
            check_id="check.beta", status=SafetyCheckStatus.VALIDATED
        )
        registry = SafetyCheckRegistry(evidence, (beta, alpha))

        self.assertEqual(
            ("check.alpha", "check.beta"),
            tuple(item.check_id for item in registry.all()),
        )
        self.assertEqual((alpha, beta), registry.for_specialty("cardiology"))
        self.assertIs(alpha, registry.require("check.alpha"))
        with self.assertRaises(SafetyError) as duplicate:
            registry.register(alpha)
        self.assertEqual("safety_check_registry.duplicate", duplicate.exception.code)


if __name__ == "__main__":
    unittest.main()
