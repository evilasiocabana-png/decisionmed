import json
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from decisionmed.application import CatalogLoadError, load_governed_catalogs
from decisionmed.app import DecisionMedAppService


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
        self.assertEqual(1, len(catalogs.safety_checks.all()))
        self.assertEqual((), catalogs.clinical_modules.all())
        self.assertEqual(
            "check.synthetic-safety",
            catalogs.safety_checks.all()[0].check_id,
        )
        schema = catalogs.form_schemas.require(
            "cardiology", "decisionmed.cardiology.workflow.v1", "context"
        )
        self.assertEqual("symptoms.present", schema.fields[0].field_key)
        self.assertFalse(schema.clinical_execution_allowed)

    def test_schema_8_loads_governed_clinical_modules(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self._write_catalog_v8(root)

            catalogs = load_governed_catalogs(root)

        self.assertEqual("8.0.0", catalogs.manifest.schema_version)
        self.assertEqual(1, catalogs.manifest.clinical_module_count)
        module = catalogs.clinical_modules.require("cardiovascular_discomfort")
        self.assertEqual("Síndrome torácica aguda", module.official_name)
        self.assertEqual("initial_syndrome", module.entity_type.value)
        self.assertEqual("draft", module.status.value)
        self.assertFalse(module.clinical_execution_allowed)
        service = DecisionMedAppService(catalogs=catalogs)
        public_catalog = service.clinical_module_catalog()
        self.assertEqual(1, public_catalog["count"])
        self.assertEqual(
            "module.cardiology.acute-thoracic-syndrome",
            public_catalog["items"][0]["module_id"],
        )
        self.assertEqual(
            public_catalog["items"][0],
            service.clinical_module("cardiovascular_discomfort"),
        )
        self.assertFalse(public_catalog["clinical_execution_allowed"])

    def test_schema_8_module_count_and_sources_fail_closed(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            payloads = self._write_catalog_v8(root)
            manifest = json.loads(
                (root / "catalog-manifest.json").read_text(encoding="utf-8")
            )
            manifest["clinical_module_count"] = 2
            (root / "catalog-manifest.json").write_text(
                json.dumps(manifest), encoding="utf-8"
            )
            with self.assertRaises(CatalogLoadError) as context:
                load_governed_catalogs(root)
            self.assertEqual("catalog.module_count", context.exception.code)

            payloads = self._write_catalog_v8(root)
            payloads["clinical_modules"]["items"][0]["source_ids"] = [
                "evidence.missing"
            ]
            self._write(
                root / "clinical-modules.json",
                payloads["clinical_modules"],
            )
            self._write_manifest_v8(root, module_count=1)
            with self.assertRaises(CatalogLoadError) as context:
                load_governed_catalogs(root)
            self.assertEqual("catalog.invalid_content", context.exception.code)

    def test_schema_9_loads_declarative_clinical_rules(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self._write_catalog_v9(root)

            catalogs = load_governed_catalogs(root)

        self.assertEqual("9.0.0", catalogs.manifest.schema_version)
        self.assertEqual(1, catalogs.manifest.clinical_rule_count)
        rule = catalogs.clinical_rules.require("route.test.chest")
        self.assertEqual(
            "module.cardiology.acute-thoracic-syndrome",
            rule.module_id,
        )
        self.assertEqual("route", rule.effect.value)
        self.assertEqual("cardiology", rule.output_key)
        self.assertFalse(rule.clinical_execution_allowed)
        public_rules = DecisionMedAppService(
            catalogs=catalogs
        ).clinical_rule_catalog()
        self.assertEqual(1, public_rules["count"])
        self.assertEqual("route.test.chest", public_rules["items"][0]["rule_id"])
        self.assertEqual(
            "equals",
            public_rules["items"][0]["when"]["all"][0]["operator"],
        )
        self.assertFalse(public_rules["clinical_execution_allowed"])

    def test_schema_9_rule_count_and_references_fail_closed(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self._write_catalog_v9(root)
            self._write_manifest_v9(root, module_count=1, rule_count=2)
            with self.assertRaises(CatalogLoadError) as context:
                load_governed_catalogs(root)
            self.assertEqual("catalog.rule_count", context.exception.code)

            payloads = self._write_catalog_v9(root)
            payloads["clinical_rules"]["items"][0]["module_id"] = (
                "module.cardiology.missing"
            )
            self._write(root / "clinical-rules.json", payloads["clinical_rules"])
            self._write_manifest_v9(root, module_count=1, rule_count=1)
            with self.assertRaises(CatalogLoadError) as context:
                load_governed_catalogs(root)
            self.assertEqual("catalog.invalid_content", context.exception.code)

    def test_schema_10_loads_partial_clinical_content(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self._write_catalog_v10(root)

            catalogs = load_governed_catalogs(root)

        self.assertEqual("10.0.0", catalogs.manifest.schema_version)
        self.assertEqual(1, catalogs.manifest.clinical_content_count)
        content = catalogs.clinical_content.require(
            "cardiovascular_discomfort"
        )
        self.assertEqual("partial", content.content_status.value)
        self.assertEqual(1, len(content.discriminators))
        self.assertEqual(1, len(content.complementary_exams))
        self.assertFalse(content.clinical_execution_allowed)
        public_content = DecisionMedAppService(
            catalogs=catalogs
        ).clinical_content_catalog()
        self.assertEqual(1, public_content["count"])
        self.assertEqual(
            "discriminator.cardiovascular.duration",
            public_content["items"][0]["discriminators"][0]["question_id"],
        )
        self.assertFalse(public_content["clinical_execution_allowed"])

    def test_schema_10_content_count_and_references_fail_closed(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self._write_catalog_v10(root)
            self._write_manifest_v10(
                root, module_count=1, rule_count=1, content_count=2
            )
            with self.assertRaises(CatalogLoadError) as context:
                load_governed_catalogs(root)
            self.assertEqual("catalog.content_count", context.exception.code)

            payloads = self._write_catalog_v10(root)
            payloads["clinical_content"]["items"][0]["module_id"] = (
                "module.cardiology.missing"
            )
            self._write(
                root / "clinical-content.json",
                payloads["clinical_content"],
            )
            self._write_manifest_v10(
                root, module_count=1, rule_count=1, content_count=1
            )
            with self.assertRaises(CatalogLoadError) as context:
                load_governed_catalogs(root)
            self.assertEqual("catalog.invalid_content", context.exception.code)

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

            payloads = self._write_catalog(root)
            payloads["safety"]["items"][0]["evidence_source_ids"] = ["missing"]
            self._write(root / "safety-checks.json", payloads["safety"])
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

    def test_empty_safety_catalog_is_valid_but_registers_no_checks(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            payloads = self._write_catalog(root)
            payloads["safety"]["items"] = []
            self._write(root / "safety-checks.json", payloads["safety"])
            self._write_manifest(root)

            catalogs = load_governed_catalogs(root)

        self.assertEqual((), catalogs.safety_checks.all())

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
        safety = cls._envelope(
            [{
                "check_id": "check.synthetic-safety",
                "specialty_key": "cardiology",
                "purpose": "Synthetic metadata without a clinical rule.",
                "limits": "Contract tests only; no patient evaluation.",
                "evidence_source_ids": ["evidence.sample"],
                "version": "0.1.0",
                "status": "draft",
                "reviewed_on": None,
                "validated_by": None,
                "review_due_on": None,
            }]
        )
        payloads = {
            "evidence": evidence,
            "knowledge": knowledge,
            "schemas": schemas,
            "safety": safety,
        }
        cls._write(root / "evidence.json", evidence)
        cls._write(root / "knowledge.json", knowledge)
        cls._write(root / "form-schemas.json", schemas)
        cls._write(root / "safety-checks.json", safety)
        cls._write_manifest(root)
        return payloads

    @classmethod
    def _write_catalog_v8(cls, root: Path) -> dict[str, dict[str, object]]:
        payloads = cls._write_catalog(root)
        for payload in payloads.values():
            payload["schema_version"] = "8.0.0"
        clinical_modules = {
            "schema_version": "8.0.0",
            "items": [
                {
                    "module_id": "module.cardiology.acute-thoracic-syndrome",
                    "version": "0.1.0",
                    "official_name": "Síndrome torácica aguda",
                    "display_name": "Síndrome torácica aguda",
                    "entity_type": "initial_syndrome",
                    "primary_specialty": "cardiology",
                    "synonyms": [],
                    "abbreviations": [],
                    "related_specialties": ["emergency"],
                    "parent_module_id": None,
                    "related_module_ids": [],
                    "terminology_codes": [],
                    "populations": ["adult"],
                    "care_settings": ["emergency"],
                    "source_ids": ["evidence.sample"],
                    "legacy_keys": ["cardiovascular_discomfort"],
                    "terminology_status": "candidate",
                    "content_status": "skeleton",
                    "status": "draft",
                    "reviewed_on": None,
                    "reviewed_by": None,
                    "review_due_on": None,
                }
            ],
        }
        payloads["clinical_modules"] = clinical_modules
        cls._write(root / "evidence.json", payloads["evidence"])
        cls._write(root / "knowledge.json", payloads["knowledge"])
        cls._write(root / "form-schemas.json", payloads["schemas"])
        cls._write(root / "safety-checks.json", payloads["safety"])
        cls._write(root / "clinical-modules.json", clinical_modules)
        cls._write_manifest_v8(root, module_count=1)
        return payloads

    @classmethod
    def _write_catalog_v9(cls, root: Path) -> dict[str, dict[str, object]]:
        payloads = cls._write_catalog_v8(root)
        for payload in payloads.values():
            payload["schema_version"] = "9.0.0"
        clinical_rules = {
            "schema_version": "9.0.0",
            "items": [
                {
                    "rule_id": "route.test.chest",
                    "module_id": "module.cardiology.acute-thoracic-syndrome",
                    "version": "0.1.0",
                    "effect": "route",
                    "strength": "moderate",
                    "rationale": "Synthetic route for contract tests.",
                    "when": {
                        "all": [
                            {
                                "fact": "complaint",
                                "operator": "equals",
                                "value": "Dor",
                            },
                            {
                                "fact": "values",
                                "operator": "contains",
                                "value": "Peito",
                            },
                        ]
                    },
                    "output_key": "cardiology",
                    "priority": False,
                    "source_ids": [],
                    "status": "draft",
                    "reviewed_on": None,
                    "reviewed_by": None,
                    "review_due_on": None,
                }
            ],
        }
        payloads["clinical_rules"] = clinical_rules
        for filename, key in (
            ("evidence.json", "evidence"),
            ("knowledge.json", "knowledge"),
            ("form-schemas.json", "schemas"),
            ("safety-checks.json", "safety"),
            ("clinical-modules.json", "clinical_modules"),
            ("clinical-rules.json", "clinical_rules"),
        ):
            cls._write(root / filename, payloads[key])
        cls._write_manifest_v9(root, module_count=1, rule_count=1)
        return payloads

    @classmethod
    def _write_catalog_v10(cls, root: Path) -> dict[str, dict[str, object]]:
        payloads = cls._write_catalog_v9(root)
        for payload in payloads.values():
            payload["schema_version"] = "10.0.0"
        clinical_content = {
            "schema_version": "10.0.0",
            "items": [
                {
                    "module_id": "module.cardiology.acute-thoracic-syndrome",
                    "version": "0.1.0",
                    "definition": None,
                    "boundaries": None,
                    "anchor_values": ["Peito"],
                    "required_manifestations": [],
                    "frequent_manifestations": [],
                    "atypical_manifestations": [],
                    "contrary_findings": [],
                    "risk_factors": [],
                    "red_flags": [],
                    "stop_conditions": [],
                    "likely_hypotheses": ["Síndrome coronariana aguda"],
                    "cannot_miss_hypotheses": ["Dissecção aguda de aorta"],
                    "mimics": ["Dor musculoesquelética"],
                    "discriminators": [
                        {
                            "question_id": "discriminator.cardiovascular.duration",
                            "text": "Quanto dura cada episódio?",
                            "options": ["Segundos", "Minutos"],
                            "rationale": None,
                            "detail_on_positive": False,
                            "detail_required": False,
                            "source_ids": [],
                        }
                    ],
                    "physical_examination": ["Sinais vitais"],
                    "complementary_exams": [
                        {
                            "exam_id": "exam.cardiology.ecg",
                            "name": "ECG de 12 derivações",
                            "clinical_question": "Há alteração isquêmica?",
                            "when": "Na avaliação inicial quando indicado.",
                            "limitations": None,
                            "source_ids": [],
                        }
                    ],
                    "diagnostic_criteria": [],
                    "post_exam_reassessment": [],
                    "safety_conduct": [],
                    "initial_treatment": [],
                    "definitive_treatment": [],
                    "destination_return_followup": [],
                    "source_ids": [],
                    "content_status": "partial",
                    "status": "draft",
                    "reviewed_on": None,
                    "reviewed_by": None,
                    "review_due_on": None,
                }
            ],
        }
        payloads["clinical_content"] = clinical_content
        for filename, key in (
            ("evidence.json", "evidence"),
            ("knowledge.json", "knowledge"),
            ("form-schemas.json", "schemas"),
            ("safety-checks.json", "safety"),
            ("clinical-modules.json", "clinical_modules"),
            ("clinical-rules.json", "clinical_rules"),
            ("clinical-content.json", "clinical_content"),
        ):
            cls._write(root / filename, payloads[key])
        cls._write_manifest_v10(
            root, module_count=1, rule_count=1, content_count=1
        )
        return payloads

    @staticmethod
    def _envelope(items: list[dict[str, object]]) -> dict[str, object]:
        return {"schema_version": "7.0.0", "items": items}

    @staticmethod
    def _write(path: Path, payload: dict[str, object]) -> None:
        path.write_text(json.dumps(payload), encoding="utf-8")

    @staticmethod
    def _write_manifest(root: Path) -> None:
        files = {
            name: sha256((root / name).read_bytes()).hexdigest()
            for name in (
                "evidence.json",
                "knowledge.json",
                "form-schemas.json",
                "safety-checks.json",
            )
        }
        manifest = {
            "schema_version": "7.0.0",
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

    @staticmethod
    def _write_manifest_v8(root: Path, module_count: int) -> None:
        files = {
            name: sha256((root / name).read_bytes()).hexdigest()
            for name in (
                "evidence.json",
                "knowledge.json",
                "form-schemas.json",
                "safety-checks.json",
                "clinical-modules.json",
            )
        }
        manifest = {
            "schema_version": "8.0.0",
            "catalog_id": "decisionmed.knowledge",
            "release_version": "0.11.0",
            "status": "draft",
            "released_on": None,
            "validated_by": None,
            "clinical_module_count": module_count,
            "files": files,
        }
        (root / "catalog-manifest.json").write_text(
            json.dumps(manifest), encoding="utf-8"
        )

    @staticmethod
    def _write_manifest_v9(
        root: Path, module_count: int, rule_count: int
    ) -> None:
        files = {
            name: sha256((root / name).read_bytes()).hexdigest()
            for name in (
                "evidence.json",
                "knowledge.json",
                "form-schemas.json",
                "safety-checks.json",
                "clinical-modules.json",
                "clinical-rules.json",
            )
        }
        manifest = {
            "schema_version": "9.0.0",
            "catalog_id": "decisionmed.knowledge",
            "release_version": "0.12.0",
            "status": "draft",
            "released_on": None,
            "validated_by": None,
            "clinical_module_count": module_count,
            "clinical_rule_count": rule_count,
            "files": files,
        }
        (root / "catalog-manifest.json").write_text(
            json.dumps(manifest), encoding="utf-8"
        )

    @staticmethod
    def _write_manifest_v10(
        root: Path, module_count: int, rule_count: int, content_count: int
    ) -> None:
        files = {
            name: sha256((root / name).read_bytes()).hexdigest()
            for name in (
                "evidence.json",
                "knowledge.json",
                "form-schemas.json",
                "safety-checks.json",
                "clinical-modules.json",
                "clinical-rules.json",
                "clinical-content.json",
            )
        }
        manifest = {
            "schema_version": "10.0.0",
            "catalog_id": "decisionmed.knowledge",
            "release_version": "0.13.0",
            "status": "draft",
            "released_on": None,
            "validated_by": None,
            "clinical_module_count": module_count,
            "clinical_rule_count": rule_count,
            "clinical_content_count": content_count,
            "files": files,
        }
        (root / "catalog-manifest.json").write_text(
            json.dumps(manifest), encoding="utf-8"
        )


if __name__ == "__main__":
    unittest.main()
