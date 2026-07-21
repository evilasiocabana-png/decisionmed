from dataclasses import replace
from datetime import date, timedelta
import unittest

from decisionmed.evidence import (
    EvidenceContractError,
    EvidenceRegistry,
    EvidenceRegistryError,
    EvidenceQuality,
    EvidenceSource,
    EvidenceStatus,
    EvidenceType,
    RecommendationStrength,
)


def source(source_id: str = "source.alpha") -> EvidenceSource:
    return EvidenceSource(
        source_id=source_id,
        title="Synthetic source metadata for contract testing",
        publication_year=2025,
        evidence_type=EvidenceType.GUIDELINE,
        evidence_quality=EvidenceQuality.INSUFFICIENT,
        recommendation_strength=RecommendationStrength.INSUFFICIENT_FOR_RECOMMENDATION,
        locator="test-only:source-alpha",
        version="0.1.0",
        status=EvidenceStatus.DRAFT,
        specialties=("cardiology",),
        reviewed_on=date(2026, 7, 21),
        known_conflicts="No conflicts assessed; synthetic fixture.",
        clinical_applicability="Contract tests only.",
    )


class EvidenceSourceTest(unittest.TestCase):
    def test_metadata_is_immutable_and_never_runtime_eligible(self) -> None:
        item = source()

        self.assertFalse(item.runtime_eligible)
        with self.assertRaises(AttributeError):
            item.title = "changed"  # type: ignore[misc]

    def test_every_status_requires_review_date_and_stays_blocked(self) -> None:
        with self.assertRaises(EvidenceContractError):
            replace(source(), reviewed_on=date.today() + timedelta(days=1))

        validated = EvidenceSource(
            source_id="source.validated",
            title="Synthetic validated metadata",
            publication_year=2025,
            evidence_type=EvidenceType.SYSTEMATIC_REVIEW,
            evidence_quality=EvidenceQuality.MODERATE,
            recommendation_strength=RecommendationStrength.CONDITIONAL,
            locator="test-only:source-validated",
            version="1.0.0",
            status=EvidenceStatus.VALIDATED,
            specialties=("psychiatry",),
            reviewed_on=date(2026, 7, 21),
            known_conflicts="No known conflicts in this synthetic fixture.",
            clinical_applicability="Contract tests only.",
        )
        self.assertFalse(validated.runtime_eligible)

    def test_rejects_invalid_year_version_and_specialties(self) -> None:
        base = {
            "source_id": "source.invalid",
            "title": "Synthetic source",
            "publication_year": 2025,
            "evidence_type": EvidenceType.OTHER,
            "evidence_quality": EvidenceQuality.INSUFFICIENT,
            "recommendation_strength": RecommendationStrength.INSUFFICIENT_FOR_RECOMMENDATION,
            "locator": "test-only:invalid",
            "version": "1.0.0",
            "status": EvidenceStatus.DRAFT,
            "specialties": ("neurology",),
            "reviewed_on": date(2026, 7, 21),
            "known_conflicts": "No conflicts assessed; synthetic fixture.",
            "clinical_applicability": "Contract tests only.",
        }
        for replacement in (
            {"publication_year": 1499},
            {"version": "v1"},
            {"specialties": ("neurology", "neurology")},
            {"known_conflicts": ""},
            {"clinical_applicability": ""},
        ):
            with self.subTest(replacement=replacement):
                with self.assertRaises(EvidenceContractError):
                    EvidenceSource(**{**base, **replacement})

    def test_registry_is_deterministic_and_rejects_duplicates(self) -> None:
        registry = EvidenceRegistry((source("source.beta"), source("source.alpha")))

        self.assertEqual(
            ("source.alpha", "source.beta"),
            tuple(item.source_id for item in registry.all()),
        )
        with self.assertRaises(EvidenceRegistryError) as duplicate:
            registry.register(source("source.alpha"))
        self.assertEqual("evidence_registry.duplicate", duplicate.exception.code)

    def test_registry_requires_known_source(self) -> None:
        with self.assertRaises(EvidenceRegistryError) as unknown:
            EvidenceRegistry().require("source.missing")

        self.assertEqual("evidence_registry.unknown", unknown.exception.code)


if __name__ == "__main__":
    unittest.main()
