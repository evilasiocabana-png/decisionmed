import json
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from decisionmed.application import CatalogLoadError, load_governed_catalogs


class GovernedCatalogLoaderTest(unittest.TestCase):
    def test_valid_external_catalog_builds_complete_registry_chain(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self._write_catalog(root)

            catalogs = load_governed_catalogs(root)

        self.assertEqual(1, len(catalogs.evidence.all()))
        self.assertEqual("decisionmed.knowledge", catalogs.manifest.catalog_id)
        self.assertFalse(catalogs.manifest.clinical_execution_allowed)
        self.assertEqual(1, len(catalogs.knowledge.all()))
        schema = catalogs.form_schemas.require(
            "cardiology", "decisionmed.cardiology.workflow.v1", "context"
        )
        self.assertEqual("symptoms.present", schema.fields[0].field_key)
        self.assertFalse(schema.clinical_execution_allowed)

    def test_unknown_fields_and_cross_reference_fail_closed(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            payloads = self._write_catalog(root)
            payloads["evidence"]["items"][0]["unexpected"] = True
            self._write(root / "evidence.json", payloads["evidence"])
            self._write_manifest(root)
            with self.assertRaises(CatalogLoadError) as context:
                load_governed_catalogs(root)
            self.assertEqual("catalog.fields", context.exception.code)

            payloads = self._write_catalog(root)
            payloads["knowledge"]["items"][0]["evidence_anchors"][0][
                "source_id"
            ] = "missing"
            self._write(root / "knowledge.json", payloads["knowledge"])
            self._write_manifest(root)
            with self.assertRaises(CatalogLoadError) as context:
                load_governed_catalogs(root)
            self.assertEqual("catalog.invalid_content", context.exception.code)

    def test_duplicate_json_keys_and_symlinks_are_rejected(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self._write_catalog(root)
            (root / "evidence.json").write_text(
                '{"schema_version":"1.0.0","schema_version":"1.0.0","items":[]}',
                encoding="utf-8",
            )
            self._write_manifest(root)
            with self.assertRaises(CatalogLoadError) as context:
                load_governed_catalogs(root)
            self.assertEqual("catalog.duplicate_key", context.exception.code)

    def test_wrong_version_and_missing_files_are_rejected(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            with self.assertRaises(CatalogLoadError):
                load_governed_catalogs(root)
            payloads = self._write_catalog(root)
            payloads["evidence"]["schema_version"] = "1.0.0"
            self._write(root / "evidence.json", payloads["evidence"])
            self._write_manifest(root)
            with self.assertRaises(CatalogLoadError) as context:
                load_governed_catalogs(root)
            self.assertEqual("catalog.version", context.exception.code)

    def test_collection_fields_must_be_json_arrays(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            payloads = self._write_catalog(root)
            payloads["evidence"]["items"][0]["specialties"] = "cardiology"
            self._write(root / "evidence.json", payloads["evidence"])
            self._write_manifest(root)

            with self.assertRaises(CatalogLoadError) as context:
                load_governed_catalogs(root)

            self.assertEqual("catalog.collection", context.exception.code)

    def test_evidence_anchors_require_exact_fields(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            payloads = self._write_catalog(root)
            payloads["knowledge"]["items"][0]["evidence_anchors"][0][
                "unexpected"
            ] = True
            self._write(root / "knowledge.json", payloads["knowledge"])
            self._write_manifest(root)

            with self.assertRaises(CatalogLoadError) as context:
                load_governed_catalogs(root)

            self.assertEqual("catalog.evidence_anchors", context.exception.code)

    def test_modified_file_is_rejected_before_parsing(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self._write_catalog(root)
            (root / "evidence.json").write_text("{}", encoding="utf-8")

            with self.assertRaises(CatalogLoadError) as context:
                load_governed_catalogs(root)

            self.assertEqual("catalog.integrity", context.exception.code)

    @classmethod
    def _write_catalog(cls, root: Path) -> dict[str, dict[str, object]]:
        evidence = cls._envelope(
            [{
                "source_id": "evidence.sample", "title": "Structural source",
                "publication_year": 2025, "evidence_type": "guideline",
                "evidence_quality": "insufficient",
                "recommendation_strength": "insufficient_for_recommendation",
                "locator": "external-catalog", "version": "1.0.0",
                "status": "draft", "specialties": ["cardiology"],
                "reviewed_on": "2026-07-21",
                "known_conflicts": "No conflicts assessed; synthetic fixture.",
                "clinical_applicability": "Contract tests only.",
                "review_due_on": None,
            }]
        )
        knowledge = cls._envelope(
            [{
                "object_id": "knowledge.sample", "official_name": "Structural sample",
                "object_type": "other", "description": "No clinical claim.",
                "evidence_anchors": [{
                    "source_id": "evidence.sample",
                    "section": "Synthetic section",
                    "locator": "https://example.test/source#section",
                }], "applicability": "Tests only.",
                "limits": "No clinical use.", "version": "1.0.0", "status": "draft",
                "reviewed_on": None, "validated_by": None, "review_due_on": None,
            }]
        )
        schemas = cls._envelope(
            [{
                "schema_id": "schema.cardiology.sample", "specialty_key": "cardiology",
                "workflow_id": "decisionmed.cardiology.workflow.v1", "step_key": "context",
                "version": "0.1.0", "status": "draft", "reviewed_on": None,
                "validated_by": None, "review_due_on": None, "fields": [{
                    "field_key": "symptoms.present", "label": "Structural sample",
                    "section": "symptoms", "value_type": "boolean",
                    "knowledge_object_id": "knowledge.sample", "required": True,
                    "allowed_values": [],
                }],
            }]
        )
        payloads = {"evidence": evidence, "knowledge": knowledge, "schemas": schemas}
        cls._write(root / "evidence.json", evidence)
        cls._write(root / "knowledge.json", knowledge)
        cls._write(root / "form-schemas.json", schemas)
        cls._write_manifest(root)
        return payloads

    @staticmethod
    def _envelope(items: list[dict[str, object]]) -> dict[str, object]:
        return {"schema_version": "6.0.0", "items": items}

    @staticmethod
    def _write(path: Path, payload: dict[str, object]) -> None:
        path.write_text(json.dumps(payload), encoding="utf-8")

    @staticmethod
    def _write_manifest(root: Path) -> None:
        files = {
            name: sha256((root / name).read_bytes()).hexdigest()
            for name in ("evidence.json", "knowledge.json", "form-schemas.json")
        }
        manifest = {
            "schema_version": "6.0.0",
            "catalog_id": "decisionmed.knowledge",
            "release_version": "0.1.0",
            "status": "draft",
            "released_on": None,
            "validated_by": None,
            "files": files,
        }
        (root / "catalog-manifest.json").write_text(
            json.dumps(manifest), encoding="utf-8"
        )


if __name__ == "__main__":
    unittest.main()
