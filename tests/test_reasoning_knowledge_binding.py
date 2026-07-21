from dataclasses import FrozenInstanceError, replace
from datetime import date, datetime, timedelta, timezone
import unittest
from unittest.mock import patch

from decisionmed.evidence import (
    EvidenceQuality,
    EvidenceSource,
    EvidenceStatus,
    EvidenceType,
    RecommendationStrength,
)
from decisionmed.knowledge import (
    EvidenceAnchor,
    KnowledgeObject,
    KnowledgeObjectType,
    KnowledgeStatus,
)
from decisionmed.reasoning import ReasoningError, ReasoningKnowledgeBinding


class ReasoningKnowledgeBindingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.source = self._source()
        self.knowledge = self._knowledge()
        self.bound_at = datetime.now(timezone.utc) - timedelta(seconds=1)

    def test_validated_current_exact_binding_is_immutable_but_not_executable(self) -> None:
        binding = self._binding()

        self.assertEqual((self.knowledge.object_id,), binding.knowledge_object_ids)
        self.assertEqual((self.source.source_id,), binding.evidence_source_ids)
        self.assertRegex(binding.content_fingerprint, r"^[0-9a-f]{64}$")
        self.assertTrue(binding.knowledge_binding_complete)
        self.assertFalse(binding.engine_invocation_allowed)
        self.assertFalse(binding.reasoning_execution_allowed)
        self.assertFalse(binding.clinical_execution_allowed)
        self.assertNotIn(self.knowledge.description, repr(binding))
        self.assertNotIn(self.source.title, repr(binding))
        with self.assertRaises(FrozenInstanceError):
            binding.specialty_key = "changed"  # type: ignore[misc]

    def test_unvalidated_release_knowledge_or_evidence_is_rejected(self) -> None:
        for values in (
            {"catalog_status": KnowledgeStatus.DRAFT},
            {"knowledge_objects": (replace(self.knowledge, status=KnowledgeStatus.DRAFT),)},
            {"evidence_sources": (replace(self.source, status=EvidenceStatus.DRAFT),)},
        ):
            with self.subTest(values=values):
                with self.assertRaises(ReasoningError):
                    self._binding(**values)

    def test_review_expiration_fails_closed_at_binding_time(self) -> None:
        binding = self._binding()
        future = date.today() + timedelta(days=60)
        with patch(
            "decisionmed.reasoning.knowledge_binding._today",
            return_value=future,
        ):
            with self.assertRaises(ReasoningError) as expired:
                self._binding()
            self.assertFalse(binding.review_current)
            self.assertFalse(binding.knowledge_binding_complete)

        self.assertIn(
            expired.exception.code,
            {
                "reasoning_knowledge.knowledge_status",
                "reasoning_knowledge.evidence_status",
            },
        )

    def test_missing_or_extra_evidence_is_rejected(self) -> None:
        extra = replace(self.source, source_id="source.extra")
        for sources in ((), (self.source, extra)):
            with self.subTest(source_ids=tuple(item.source_id for item in sources)):
                with self.assertRaises(ReasoningError):
                    self._binding(evidence_sources=sources)

    def test_wrong_specialty_is_rejected(self) -> None:
        with self.assertRaises(ReasoningError) as mismatch:
            self._binding(specialty_key="psychiatry")

        self.assertEqual(
            "reasoning_knowledge.evidence_specialty",
            mismatch.exception.code,
        )

    def test_content_change_changes_fingerprint(self) -> None:
        original = self._binding()
        changed = self._binding(
            knowledge_objects=(
                replace(
                    self.knowledge,
                    description="Changed synthetic knowledge description.",
                ),
            )
        )

        self.assertNotEqual(
            original.content_fingerprint,
            changed.content_fingerprint,
        )

    def _binding(self, **changes: object) -> ReasoningKnowledgeBinding:
        values = {
            "catalog_id": "decisionmed.knowledge",
            "catalog_version": "1.0.0",
            "catalog_status": KnowledgeStatus.VALIDATED,
            "catalog_released_on": date.today(),
            "catalog_validated_by": "reviewer.synthetic",
            "specialty_key": "cardiology",
            "bound_at": self.bound_at,
            "knowledge_objects": (self.knowledge,),
            "evidence_sources": (self.source,),
            **changes,
        }
        return ReasoningKnowledgeBinding(**values)

    @staticmethod
    def _source() -> EvidenceSource:
        return EvidenceSource(
            source_id="source.synthetic-reasoning",
            title="Synthetic source for reasoning binding tests",
            publication_year=2025,
            evidence_type=EvidenceType.OTHER,
            evidence_quality=EvidenceQuality.INSUFFICIENT,
            recommendation_strength=(
                RecommendationStrength.INSUFFICIENT_FOR_RECOMMENDATION
            ),
            locator="test-only:reasoning-binding",
            version="1.0.0",
            status=EvidenceStatus.VALIDATED,
            specialties=("cardiology",),
            reviewed_on=date.today(),
            known_conflicts="Synthetic conflicts metadata.",
            clinical_applicability="Structural tests only.",
            review_due_on=date.today() + timedelta(days=30),
        )

    @staticmethod
    def _knowledge() -> KnowledgeObject:
        return KnowledgeObject(
            object_id="knowledge.synthetic-reasoning",
            official_name="Synthetic reasoning binding knowledge",
            object_type=KnowledgeObjectType.OTHER,
            description="Synthetic knowledge description for structural tests.",
            evidence_anchors=(
                EvidenceAnchor(
                    source_id="source.synthetic-reasoning",
                    section="Synthetic section",
                    locator="Synthetic locator",
                ),
            ),
            applicability="Structural tests only.",
            limits="No clinical use.",
            version="1.0.0",
            status=KnowledgeStatus.VALIDATED,
            reviewed_on=date.today(),
            validated_by="reviewer.synthetic",
            review_due_on=date.today() + timedelta(days=30),
        )


if __name__ == "__main__":
    unittest.main()
