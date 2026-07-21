import unittest

from knowledge.core.knowledge_object import KnowledgeObject
from knowledge.core.status import KnowledgeStatus
from knowledge.validators.knowledge_validator import KnowledgeValidator
from knowledge.versioning.version import KnowledgeVersion, VersionHistory, VersionRecord

from tests.knowledge.helpers import build_knowledge_object


class KnowledgeObjectBaseTest(unittest.TestCase):
    def test_requires_identifier_name_and_origin(self) -> None:
        version = KnowledgeVersion(0, 1, 0)

        with self.assertRaises(ValueError):
            KnowledgeObject("", "Name", version, "origin")
        with self.assertRaises(ValueError):
            KnowledgeObject("id", "", version, "origin")
        with self.assertRaises(ValueError):
            KnowledgeObject("id", "Name", version, "")

    def test_metadata_is_read_only_copy(self) -> None:
        metadata = {"source": "fixture"}
        knowledge_object = KnowledgeObject(
            "id",
            "Name",
            KnowledgeVersion(0, 1, 0),
            "origin",
            metadata=metadata,
        )
        metadata["source"] = "changed"

        self.assertEqual(knowledge_object.metadata["source"], "fixture")
        with self.assertRaises(TypeError):
            knowledge_object.metadata["source"] = "blocked"  # type: ignore[index]

    def test_active_statuses_are_structural_only(self) -> None:
        draft = build_knowledge_object(status=KnowledgeStatus.DRAFT)
        validated = build_knowledge_object(
            status=KnowledgeStatus.VALIDATED,
            references=("ref-1",),
        )

        self.assertFalse(draft.is_active)
        self.assertTrue(validated.is_active)


class KnowledgeVersioningTest(unittest.TestCase):
    def test_version_parse_and_bump(self) -> None:
        version = KnowledgeVersion.parse("1.2.3")

        self.assertEqual(str(version), "1.2.3")
        self.assertEqual(str(version.bump_major()), "2.0.0")
        self.assertEqual(str(version.bump_minor()), "1.3.0")
        self.assertEqual(str(version.bump_patch()), "1.2.4")

    def test_version_history_requires_increasing_versions(self) -> None:
        history = VersionHistory().append(
            VersionRecord(KnowledgeVersion(0, 1, 0), "initial")
        )

        self.assertEqual(str(history.current), "0.1.0")
        with self.assertRaises(ValueError):
            history.append(VersionRecord(KnowledgeVersion(0, 1, 0), "duplicate"))


class KnowledgeValidationTest(unittest.TestCase):
    def test_validated_knowledge_requires_reference(self) -> None:
        result = KnowledgeValidator().validate(
            build_knowledge_object(status=KnowledgeStatus.VALIDATED)
        )

        self.assertFalse(result.is_valid)
        self.assertEqual(result.issues[0].field, "references")

    def test_draft_fixture_is_valid_without_reference(self) -> None:
        result = KnowledgeValidator().validate(build_knowledge_object())

        self.assertTrue(result.is_valid)


if __name__ == "__main__":
    unittest.main()
