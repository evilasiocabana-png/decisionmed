from dataclasses import replace
from datetime import date, timedelta
import unittest

from decisionmed.evidence import (
    EvidenceRegistry,
    EvidenceQuality,
    EvidenceSource,
    EvidenceStatus,
    EvidenceType,
    RecommendationStrength,
)
from decisionmed.knowledge import (
    EvidenceAnchor,
    KnowledgeError,
    KnowledgeObject,
    KnowledgeObjectType,
    KnowledgeRegistry,
    KnowledgeStatus,
)


def evidence(status: EvidenceStatus = EvidenceStatus.DRAFT) -> EvidenceSource:
    return EvidenceSource(
        source_id="source.synthetic",
        title="Synthetic metadata used only for contract testing",
        publication_year=2025,
        evidence_type=EvidenceType.OTHER,
        evidence_quality=EvidenceQuality.INSUFFICIENT,
        recommendation_strength=RecommendationStrength.INSUFFICIENT_FOR_RECOMMENDATION,
        locator="test-only:synthetic",
        version="0.1.0",
        status=status,
        specialties=("cardiology",),
        reviewed_on=date(2026, 7, 21),
        known_conflicts="No conflicts assessed; synthetic fixture.",
        clinical_applicability="Contract tests only.",
        review_due_on=(
            date.today() + timedelta(days=30)
            if status is EvidenceStatus.VALIDATED
            else None
        ),
    )


def knowledge(status: KnowledgeStatus = KnowledgeStatus.DRAFT) -> KnowledgeObject:
    return KnowledgeObject(
        object_id="knowledge.synthetic",
        official_name="Synthetic knowledge contract fixture",
        object_type=KnowledgeObjectType.OTHER,
        description="Non-clinical fixture content.",
        evidence_anchors=(
            EvidenceAnchor(
                source_id="source.synthetic",
                section="Synthetic section",
                locator="https://example.test/source#section",
            ),
        ),
        applicability="Contract tests only.",
        limits="Not clinical knowledge and never runtime eligible.",
        version="0.1.0",
        status=status,
        reviewed_on=date(2026, 7, 21)
        if status is KnowledgeStatus.VALIDATED
        else None,
        validated_by="reviewer.synthetic"
        if status is KnowledgeStatus.VALIDATED
        else None,
    )


class KnowledgeContractTest(unittest.TestCase):
    def test_object_is_immutable_and_runtime_blocked(self) -> None:
        item = knowledge()

        self.assertFalse(item.runtime_eligible)
        self.assertEqual(("source.synthetic",), item.evidence_source_ids)
        self.assertFalse(item.evidence_anchors[0].runtime_eligible)
        with self.assertRaises(AttributeError):
            item.status = KnowledgeStatus.VALIDATED  # type: ignore[misc]

    def test_validated_object_requires_human_review_metadata(self) -> None:
        with self.assertRaises(KnowledgeError):
            replace(knowledge(), status=KnowledgeStatus.VALIDATED)

    def test_object_requires_unique_precise_evidence_anchors(self) -> None:
        anchor = knowledge().evidence_anchors[0]
        with self.assertRaises(KnowledgeError) as context:
            replace(knowledge(), evidence_anchors=(anchor, anchor))

        self.assertEqual("knowledge_object.evidence_anchors", context.exception.code)

    def test_registry_rejects_unknown_evidence(self) -> None:
        with self.assertRaises(KnowledgeError) as error:
            KnowledgeRegistry(EvidenceRegistry()).register(knowledge())

        self.assertEqual("knowledge_registry.unknown_evidence", error.exception.code)

    def test_validated_object_requires_validated_evidence_metadata(self) -> None:
        registry = KnowledgeRegistry(EvidenceRegistry((evidence(),)))

        with self.assertRaises(KnowledgeError) as error:
            registry.register(knowledge(KnowledgeStatus.VALIDATED))

        self.assertEqual(
            "knowledge_registry.unvalidated_evidence", error.exception.code
        )

    def test_validated_metadata_still_does_not_clear_runtime_gate(self) -> None:
        registry = KnowledgeRegistry(
            EvidenceRegistry((evidence(EvidenceStatus.VALIDATED),))
        )
        item = registry.register(knowledge(KnowledgeStatus.VALIDATED))

        self.assertFalse(item.runtime_eligible)
        self.assertIs(item, registry.require(item.object_id))

    def test_registry_rejects_duplicate_and_sorts_objects(self) -> None:
        registry = KnowledgeRegistry(EvidenceRegistry((evidence(),)))
        alpha = knowledge()
        beta = replace(alpha, object_id="knowledge.beta")
        registry.register(beta)
        registry.register(alpha)

        self.assertEqual(
            ("knowledge.beta", "knowledge.synthetic"),
            tuple(item.object_id for item in registry.all()),
        )
        with self.assertRaises(KnowledgeError) as duplicate:
            registry.register(alpha)
        self.assertEqual("knowledge_registry.duplicate", duplicate.exception.code)


if __name__ == "__main__":
    unittest.main()
