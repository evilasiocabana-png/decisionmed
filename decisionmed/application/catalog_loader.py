"""Strict loader for an external, versioned DecisionMEd knowledge catalog."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from hashlib import sha256
import hmac
import json
from pathlib import Path
import re
from typing import Any

from decisionmed.domain import ClinicalSnapshotSection
from decisionmed.evidence import (
    EvidenceRegistry,
    EvidenceSource,
    EvidenceStatus,
    EvidenceType,
    EvidenceQuality,
    RecommendationStrength,
)
from decisionmed.knowledge import (
    ClinicalCaseAnswer,
    ClinicalCaseAuditEvent,
    ClinicalCaseCategory,
    ClinicalCaseRegistry,
    ClinicalTestCase,
    ClinicalContentStatus,
    ClinicalComplementaryExam,
    ClinicalDiscriminator,
    ClinicalEntityType,
    ClinicalFieldDefinition,
    ClinicalFieldValueType,
    ClinicalModuleDefinition,
    ClinicalModuleRegistry,
    ClinicalModuleStatus,
    ClinicalModuleContent,
    ClinicalModuleContentRegistry,
    ClinicalRuleCondition,
    ClinicalRuleDefinition,
    ClinicalRuleEffect,
    ClinicalRuleOperator,
    ClinicalRuleRegistry,
    ClinicalRuleStatus,
    ClinicalRuleStrength,
    EvidenceAnchor,
    KnowledgeObject,
    KnowledgeObjectType,
    KnowledgeRegistry,
    KnowledgeStatus,
    SpecialtyFormSchema,
    SpecialtyFormSchemaRegistry,
    TerminologyCode,
    TerminologyStatus,
)
from decisionmed.safety import (
    SafetyCheckRegistry,
    SafetyCheckSpecification,
    SafetyCheckStatus,
)


CATALOG_SCHEMA_VERSION = "11.0.0"
SUPPORTED_CATALOG_SCHEMA_VERSIONS = (
    "7.0.0",
    "8.0.0",
    "9.0.0",
    "10.0.0",
    CATALOG_SCHEMA_VERSION,
)
MAX_CATALOG_BYTES = 33_554_432
MAX_CATALOG_ITEMS = 10_000
_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_VERSION = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
_HASH = re.compile(r"^[0-9a-f]{64}$")
_LEGACY_CATALOG_FILES = (
    "evidence.json",
    "knowledge.json",
    "form-schemas.json",
    "safety-checks.json",
)
_MODULE_CATALOG_FILES = _LEGACY_CATALOG_FILES + ("clinical-modules.json",)
_RULE_CATALOG_FILES = _MODULE_CATALOG_FILES + ("clinical-rules.json",)
_CONTENT_CATALOG_FILES = _RULE_CATALOG_FILES + ("clinical-content.json",)
_CATALOG_FILES = _CONTENT_CATALOG_FILES + ("clinical-cases.json",)


class CatalogLoadError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass(frozen=True, slots=True)
class GovernedCatalogs:
    manifest: CatalogReleaseManifest
    evidence: EvidenceRegistry
    knowledge: KnowledgeRegistry
    form_schemas: SpecialtyFormSchemaRegistry
    safety_checks: SafetyCheckRegistry
    clinical_modules: ClinicalModuleRegistry
    clinical_rules: ClinicalRuleRegistry
    clinical_content: ClinicalModuleContentRegistry
    clinical_cases: ClinicalCaseRegistry


@dataclass(frozen=True, slots=True)
class CatalogReleaseManifest:
    schema_version: str
    catalog_id: str
    release_version: str
    status: KnowledgeStatus
    released_on: date | None
    validated_by: str | None
    clinical_module_count: int
    clinical_rule_count: int
    clinical_content_count: int
    clinical_case_count: int
    file_hashes: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if self.schema_version not in SUPPORTED_CATALOG_SCHEMA_VERSIONS:
            raise CatalogLoadError("catalog.version", "unsupported manifest version")
        if not isinstance(self.catalog_id, str) or not _IDENTIFIER.fullmatch(self.catalog_id):
            raise CatalogLoadError("catalog.manifest_id", "catalog id must be canonical")
        if not isinstance(self.release_version, str) or not _VERSION.fullmatch(self.release_version):
            raise CatalogLoadError("catalog.manifest_version", "release version is invalid")
        if not isinstance(self.status, KnowledgeStatus):
            raise TypeError("status must be a KnowledgeStatus")
        hashes = tuple(self.file_hashes)
        expected_files = _files_for_schema(self.schema_version)
        if tuple(name for name, _ in hashes) != expected_files or any(
            not isinstance(value, str) or not _HASH.fullmatch(value)
            for _, value in hashes
        ):
            raise CatalogLoadError("catalog.manifest_hashes", "manifest hashes are invalid")
        object.__setattr__(self, "file_hashes", hashes)
        if (
            not isinstance(self.clinical_module_count, int)
            or isinstance(self.clinical_module_count, bool)
            or self.clinical_module_count < 0
            or self.clinical_module_count > MAX_CATALOG_ITEMS
            or (
                self.schema_version == "7.0.0"
                and self.clinical_module_count != 0
            )
        ):
            raise CatalogLoadError(
                "catalog.manifest_module_count",
                "clinical module count is invalid",
            )
        if (
            not isinstance(self.clinical_rule_count, int)
            or isinstance(self.clinical_rule_count, bool)
            or self.clinical_rule_count < 0
            or self.clinical_rule_count > MAX_CATALOG_ITEMS
            or (
                self.schema_version
                not in ("9.0.0", "10.0.0", CATALOG_SCHEMA_VERSION)
                and self.clinical_rule_count != 0
            )
        ):
            raise CatalogLoadError(
                "catalog.manifest_rule_count",
                "clinical rule count is invalid",
            )
        if (
            not isinstance(self.clinical_content_count, int)
            or isinstance(self.clinical_content_count, bool)
            or self.clinical_content_count < 0
            or self.clinical_content_count > MAX_CATALOG_ITEMS
            or (
                self.schema_version not in ("10.0.0", CATALOG_SCHEMA_VERSION)
                and self.clinical_content_count != 0
            )
        ):
            raise CatalogLoadError(
                "catalog.manifest_content_count",
                "clinical content count is invalid",
            )
        if (
            not isinstance(self.clinical_case_count, int)
            or isinstance(self.clinical_case_count, bool)
            or self.clinical_case_count < 0
            or self.clinical_case_count > MAX_CATALOG_ITEMS
            or (
                self.schema_version != CATALOG_SCHEMA_VERSION
                and self.clinical_case_count != 0
            )
        ):
            raise CatalogLoadError(
                "catalog.manifest_case_count",
                "clinical case count is invalid",
            )
        if self.released_on is not None and not isinstance(self.released_on, date):
            raise TypeError("released_on must be a date or None")
        if self.validated_by is not None and (
            not isinstance(self.validated_by, str)
            or not _IDENTIFIER.fullmatch(self.validated_by)
        ):
            raise CatalogLoadError("catalog.manifest_validator", "validator is invalid")
        if self.status is KnowledgeStatus.VALIDATED and (
            self.released_on is None or self.validated_by is None
        ):
            raise CatalogLoadError(
                "catalog.manifest_validation",
                "validated release requires review metadata",
            )

    @property
    def clinical_execution_allowed(self) -> bool:
        return False


def load_governed_catalogs(root: Path) -> GovernedCatalogs:
    """Load a fixed, versioned external catalog release and fail closed."""

    root = root.resolve()
    if not root.is_dir():
        raise CatalogLoadError("catalog.root", "catalog root is not a directory")
    try:
        manifest = _load_manifest(root / "catalog-manifest.json")
        hashes = dict(manifest.file_hashes)
        evidence_payload = _load_file(
            root / "evidence.json",
            hashes["evidence.json"],
            manifest.schema_version,
        )
        knowledge_payload = _load_file(
            root / "knowledge.json",
            hashes["knowledge.json"],
            manifest.schema_version,
        )
        schema_payload = _load_file(
            root / "form-schemas.json",
            hashes["form-schemas.json"],
            manifest.schema_version,
        )
        safety_payload = _load_file(
            root / "safety-checks.json",
            hashes["safety-checks.json"],
            manifest.schema_version,
        )
        clinical_module_payload = (
            _load_file(
                root / "clinical-modules.json",
                hashes["clinical-modules.json"],
                manifest.schema_version,
            )
            if manifest.schema_version != "7.0.0"
            else {
                "schema_version": manifest.schema_version,
                "items": [],
            }
        )
        clinical_rule_payload = (
            _load_file(
                root / "clinical-rules.json",
                hashes["clinical-rules.json"],
                manifest.schema_version,
            )
            if manifest.schema_version
            in ("9.0.0", "10.0.0", CATALOG_SCHEMA_VERSION)
            else {
                "schema_version": manifest.schema_version,
                "items": [],
            }
        )
        clinical_content_payload = (
            _load_file(
                root / "clinical-content.json",
                hashes["clinical-content.json"],
                manifest.schema_version,
            )
            if manifest.schema_version in ("10.0.0", CATALOG_SCHEMA_VERSION)
            else {
                "schema_version": manifest.schema_version,
                "items": [],
            }
        )
        clinical_case_payload = (
            _load_file(
                root / "clinical-cases.json",
                hashes["clinical-cases.json"],
                manifest.schema_version,
            )
            if manifest.schema_version == CATALOG_SCHEMA_VERSION
            else {
                "schema_version": manifest.schema_version,
                "items": [],
            }
        )

        evidence = EvidenceRegistry(
            EvidenceSource(
                source_id=item["source_id"],
                title=item["title"],
                publication_year=item["publication_year"],
                evidence_type=EvidenceType(item["evidence_type"]),
                evidence_quality=EvidenceQuality(item["evidence_quality"]),
                recommendation_strength=RecommendationStrength(
                    item["recommendation_strength"]
                ),
                locator=item["locator"],
                version=item["version"],
                status=EvidenceStatus(item["status"]),
                specialties=_list(item, "specialties"),
                reviewed_on=_date_or_none(item["reviewed_on"]),
                known_conflicts=item["known_conflicts"],
                clinical_applicability=item["clinical_applicability"],
                review_due_on=_date_or_none(item["review_due_on"]),
            )
            for item in _items(evidence_payload, "evidence.json", _EVIDENCE_KEYS)
        )
        knowledge = KnowledgeRegistry(
            evidence,
            (
                KnowledgeObject(
                    object_id=item["object_id"],
                    official_name=item["official_name"],
                    object_type=KnowledgeObjectType(item["object_type"]),
                    description=item["description"],
                    evidence_anchors=_evidence_anchors(item),
                    applicability=item["applicability"],
                    limits=item["limits"],
                    version=item["version"],
                    status=KnowledgeStatus(item["status"]),
                    reviewed_on=_date_or_none(item["reviewed_on"]),
                    validated_by=item["validated_by"],
                    review_due_on=_date_or_none(item["review_due_on"]),
                )
                for item in _items(
                    knowledge_payload, "knowledge.json", _KNOWLEDGE_KEYS
                )
            ),
        )
        schemas = SpecialtyFormSchemaRegistry(
            knowledge,
            (
                _form_schema(item)
                for item in _items(
                    schema_payload, "form-schemas.json", _SCHEMA_KEYS
                )
            ),
        )
        safety_checks = SafetyCheckRegistry(
            evidence,
            (
                SafetyCheckSpecification(
                    check_id=item["check_id"],
                    specialty_key=item["specialty_key"],
                    purpose=item["purpose"],
                    limits=item["limits"],
                    evidence_source_ids=_list(item, "evidence_source_ids"),
                    version=item["version"],
                    status=SafetyCheckStatus(item["status"]),
                    reviewed_on=_date_or_none(item["reviewed_on"]),
                    validated_by=item["validated_by"],
                    review_due_on=_date_or_none(item["review_due_on"]),
                )
                for item in _items(
                    safety_payload, "safety-checks.json", _SAFETY_CHECK_KEYS
                )
            ),
        )
        clinical_modules = ClinicalModuleRegistry(
            tuple(
                _clinical_module(item)
                for item in _items(
                    clinical_module_payload,
                    "clinical-modules.json",
                    _CLINICAL_MODULE_KEYS,
                )
            )
        )
        if len(clinical_modules.all()) != manifest.clinical_module_count:
            raise CatalogLoadError(
                "catalog.module_count",
                "clinical module count does not match the manifest",
            )
        for module in clinical_modules.all():
            for source_id in module.source_ids:
                evidence.require(source_id)
        clinical_rules = ClinicalRuleRegistry(
            clinical_modules,
            tuple(
                _clinical_rule(item)
                for item in _items(
                    clinical_rule_payload,
                    "clinical-rules.json",
                    (
                        _CLINICAL_RULE_KEYS
                        if manifest.schema_version == "11.0.0"
                        else _CLINICAL_RULE_KEYS - {"output_value"}
                    ),
                )
            ),
        )
        if len(clinical_rules.all()) != manifest.clinical_rule_count:
            raise CatalogLoadError(
                "catalog.rule_count",
                "clinical rule count does not match the manifest",
            )
        for rule in clinical_rules.all():
            for source_id in rule.source_ids:
                evidence.require(source_id)
        clinical_content = ClinicalModuleContentRegistry(
            clinical_modules,
            tuple(
                _clinical_content(item)
                for item in _items(
                    clinical_content_payload,
                    "clinical-content.json",
                    _CLINICAL_CONTENT_KEYS,
                )
            ),
        )
        if len(clinical_content.all()) != manifest.clinical_content_count:
            raise CatalogLoadError(
                "catalog.content_count",
                "clinical content count does not match the manifest",
            )
        for content in clinical_content.all():
            content_source_ids = set(content.source_ids)
            for discriminator in content.discriminators:
                content_source_ids.update(discriminator.source_ids)
            for exam in content.complementary_exams:
                content_source_ids.update(exam.source_ids)
            for source_id in content_source_ids:
                evidence.require(source_id)
        clinical_cases = ClinicalCaseRegistry(
            clinical_modules,
            tuple(
                _clinical_case(item)
                for item in _items(
                    clinical_case_payload,
                    "clinical-cases.json",
                    _CLINICAL_CASE_KEYS,
                )
            ),
        )
        if len(clinical_cases.all()) != manifest.clinical_case_count:
            raise CatalogLoadError(
                "catalog.case_count",
                "clinical case count does not match the manifest",
            )
        if manifest.schema_version == CATALOG_SCHEMA_VERSION:
            clinical_cases.validate_dm300_distribution()
    except CatalogLoadError:
        raise
    except (KeyError, TypeError, ValueError) as exc:
        raise CatalogLoadError(
            "catalog.invalid_content", "catalog content violates its contracts"
        ) from exc
    return GovernedCatalogs(
        manifest,
        evidence,
        knowledge,
        schemas,
        safety_checks,
        clinical_modules,
        clinical_rules,
        clinical_content,
        clinical_cases,
    )


def _load_manifest(path: Path) -> CatalogReleaseManifest:
    payload = _decode_json(_read_file(path), path.name)
    base_fields = {
        "schema_version", "catalog_id", "release_version", "status",
        "released_on", "validated_by", "files",
    }
    if not isinstance(payload, dict):
        raise CatalogLoadError("catalog.manifest", "invalid catalog manifest")
    schema_version = payload.get("schema_version")
    if schema_version not in SUPPORTED_CATALOG_SCHEMA_VERSIONS:
        raise CatalogLoadError("catalog.version", "unsupported manifest version")
    if schema_version == "7.0.0":
        expected = base_fields
    elif schema_version == "8.0.0":
        expected = base_fields | {"clinical_module_count"}
    elif schema_version == "9.0.0":
        expected = base_fields | {
            "clinical_module_count",
            "clinical_rule_count",
        }
    elif schema_version == "10.0.0":
        expected = base_fields | {
            "clinical_module_count",
            "clinical_rule_count",
            "clinical_content_count",
        }
    else:
        expected = base_fields | {
            "clinical_module_count",
            "clinical_rule_count",
            "clinical_content_count",
            "clinical_case_count",
        }
    if set(payload) != expected:
        raise CatalogLoadError("catalog.manifest", "invalid catalog manifest")
    expected_files = _files_for_schema(schema_version)
    files = payload["files"]
    if not isinstance(files, dict) or set(files) != set(expected_files):
        raise CatalogLoadError("catalog.manifest_hashes", "manifest hashes are invalid")
    return CatalogReleaseManifest(
        schema_version=schema_version,
        catalog_id=payload["catalog_id"],
        release_version=payload["release_version"],
        status=KnowledgeStatus(payload["status"]),
        released_on=_date_or_none(payload["released_on"]),
        validated_by=payload["validated_by"],
        clinical_module_count=payload.get("clinical_module_count", 0),
        clinical_rule_count=payload.get("clinical_rule_count", 0),
        clinical_content_count=payload.get("clinical_content_count", 0),
        clinical_case_count=payload.get("clinical_case_count", 0),
        file_hashes=tuple((name, files[name]) for name in expected_files),
    )


def _load_file(
    path: Path, expected_hash: str, schema_version: str
) -> dict[str, Any]:
    data = _read_file(path)
    actual_hash = sha256(data).hexdigest()
    if not hmac.compare_digest(actual_hash, expected_hash):
        raise CatalogLoadError("catalog.integrity", f"catalog hash mismatch: {path.name}")
    payload = _decode_json(data, path.name)
    if not isinstance(payload, dict) or set(payload) != {"schema_version", "items"}:
        raise CatalogLoadError("catalog.envelope", f"invalid catalog envelope: {path.name}")
    if payload["schema_version"] != schema_version:
        raise CatalogLoadError("catalog.version", f"unsupported catalog version: {path.name}")
    return payload


def _clinical_module(item: dict[str, Any]) -> ClinicalModuleDefinition:
    raw_codes = item["terminology_codes"]
    if not isinstance(raw_codes, list) or any(
        not isinstance(code, dict) or set(code) != _TERMINOLOGY_CODE_KEYS
        for code in raw_codes
    ):
        raise CatalogLoadError(
            "catalog.terminology_codes",
            "terminology codes are invalid",
        )
    return ClinicalModuleDefinition(
        module_id=item["module_id"],
        version=item["version"],
        official_name=item["official_name"],
        display_name=item["display_name"],
        entity_type=ClinicalEntityType(item["entity_type"]),
        primary_specialty=item["primary_specialty"],
        synonyms=_list(item, "synonyms"),
        abbreviations=_list(item, "abbreviations"),
        related_specialties=_list(item, "related_specialties"),
        parent_module_id=item["parent_module_id"],
        related_module_ids=_list(item, "related_module_ids"),
        terminology_codes=tuple(
            TerminologyCode(
                system=code["system"],
                code=code["code"],
                display=code["display"],
                version=code["version"],
            )
            for code in raw_codes
        ),
        populations=_list(item, "populations"),
        care_settings=_list(item, "care_settings"),
        source_ids=_list(item, "source_ids"),
        legacy_keys=_list(item, "legacy_keys"),
        terminology_status=TerminologyStatus(item["terminology_status"]),
        content_status=ClinicalContentStatus(item["content_status"]),
        status=ClinicalModuleStatus(item["status"]),
        reviewed_on=_date_or_none(item["reviewed_on"]),
        reviewed_by=item["reviewed_by"],
        review_due_on=_date_or_none(item["review_due_on"]),
    )


def _clinical_rule(item: dict[str, Any]) -> ClinicalRuleDefinition:
    return ClinicalRuleDefinition(
        rule_id=item["rule_id"],
        module_id=item["module_id"],
        version=item["version"],
        effect=ClinicalRuleEffect(item["effect"]),
        strength=ClinicalRuleStrength(item["strength"]),
        rationale=item["rationale"],
        when=_clinical_rule_condition(item["when"]),
        output_key=item.get("output_key"),
        output_value=item.get("output_value"),
        priority=item["priority"],
        source_ids=_list(item, "source_ids"),
        status=ClinicalRuleStatus(item["status"]),
        reviewed_on=_date_or_none(item["reviewed_on"]),
        reviewed_by=item["reviewed_by"],
        review_due_on=_date_or_none(item["review_due_on"]),
    )


def _clinical_rule_condition(item: object) -> ClinicalRuleCondition:
    if not isinstance(item, dict):
        raise CatalogLoadError(
            "catalog.rule_condition",
            "clinical rule condition must be an object",
        )
    group_keys = frozenset({"all", "any", "none"})
    present_group_keys = set(item) & group_keys
    if present_group_keys:
        if not set(item) <= group_keys:
            raise CatalogLoadError(
                "catalog.rule_condition",
                "clinical rule group has invalid fields",
            )
        parsed: dict[str, tuple[ClinicalRuleCondition, ...]] = {}
        for key in group_keys:
            raw = item.get(key, [])
            if not isinstance(raw, list) or (key in item and not raw):
                raise CatalogLoadError(
                    "catalog.rule_condition",
                    "clinical rule groups must be non-empty arrays",
                )
            parsed[key] = tuple(_clinical_rule_condition(value) for value in raw)
        return ClinicalRuleCondition(
            all_of=parsed["all"],
            any_of=parsed["any"],
            none_of=parsed["none"],
        )

    operator = ClinicalRuleOperator(item.get("operator"))
    expected_fields = {
        ClinicalRuleOperator.EQUALS: {"fact", "operator", "value"},
        ClinicalRuleOperator.CONTAINS: {"fact", "operator", "value"},
        ClinicalRuleOperator.CONTAINS_ANY: {"fact", "operator", "values"},
        ClinicalRuleOperator.CONTAINS_ALL: {"fact", "operator", "values"},
        ClinicalRuleOperator.COUNT_AT_LEAST: {
            "fact",
            "operator",
            "values",
            "threshold",
        },
        ClinicalRuleOperator.MATCHES: {"fact", "operator", "pattern"},
        ClinicalRuleOperator.PRESENT: {"fact", "operator"},
    }[operator]
    if set(item) != expected_fields:
        raise CatalogLoadError(
            "catalog.rule_condition",
            "clinical rule predicate has invalid fields",
        )
    raw_values = item.get("values", [])
    if not isinstance(raw_values, list):
        raise CatalogLoadError(
            "catalog.rule_condition",
            "clinical rule values must be an array",
        )
    return ClinicalRuleCondition(
        fact=item["fact"],
        operator=operator,
        value=item.get("value"),
        values=tuple(raw_values),
        threshold=item.get("threshold"),
        pattern=item.get("pattern"),
    )


def _clinical_content(item: dict[str, Any]) -> ClinicalModuleContent:
    raw_discriminators = item["discriminators"]
    if not isinstance(raw_discriminators, list) or any(
        not isinstance(value, dict) or set(value) != _DISCRIMINATOR_KEYS
        for value in raw_discriminators
    ):
        raise CatalogLoadError(
            "catalog.discriminators",
            "clinical discriminators are invalid",
        )
    raw_exams = item["complementary_exams"]
    if not isinstance(raw_exams, list) or any(
        not isinstance(value, dict) or set(value) != _COMPLEMENTARY_EXAM_KEYS
        for value in raw_exams
    ):
        raise CatalogLoadError(
            "catalog.complementary_exams",
            "clinical complementary exams are invalid",
        )
    return ClinicalModuleContent(
        module_id=item["module_id"],
        version=item["version"],
        definition=item["definition"],
        boundaries=item["boundaries"],
        anchor_values=_list(item, "anchor_values"),
        required_manifestations=_list(item, "required_manifestations"),
        frequent_manifestations=_list(item, "frequent_manifestations"),
        atypical_manifestations=_list(item, "atypical_manifestations"),
        contrary_findings=_list(item, "contrary_findings"),
        risk_factors=_list(item, "risk_factors"),
        red_flags=_list(item, "red_flags"),
        stop_conditions=_list(item, "stop_conditions"),
        likely_hypotheses=_list(item, "likely_hypotheses"),
        cannot_miss_hypotheses=_list(item, "cannot_miss_hypotheses"),
        mimics=_list(item, "mimics"),
        discriminators=tuple(
            ClinicalDiscriminator(
                question_id=value["question_id"],
                text=value["text"],
                options=_list(value, "options"),
                rationale=value["rationale"],
                detail_on_positive=value["detail_on_positive"],
                detail_required=value["detail_required"],
                source_ids=_list(value, "source_ids"),
            )
            for value in raw_discriminators
        ),
        physical_examination=_list(item, "physical_examination"),
        complementary_exams=tuple(
            ClinicalComplementaryExam(
                exam_id=value["exam_id"],
                name=value["name"],
                clinical_question=value["clinical_question"],
                when=value["when"],
                limitations=value["limitations"],
                source_ids=_list(value, "source_ids"),
            )
            for value in raw_exams
        ),
        diagnostic_criteria=_list(item, "diagnostic_criteria"),
        post_exam_reassessment=_list(item, "post_exam_reassessment"),
        safety_conduct=_list(item, "safety_conduct"),
        initial_treatment=_list(item, "initial_treatment"),
        definitive_treatment=_list(item, "definitive_treatment"),
        destination_return_followup=_list(
            item, "destination_return_followup"
        ),
        source_ids=_list(item, "source_ids"),
        content_status=ClinicalContentStatus(item["content_status"]),
        status=ClinicalModuleStatus(item["status"]),
        reviewed_on=_date_or_none(item["reviewed_on"]),
        reviewed_by=item["reviewed_by"],
        review_due_on=_date_or_none(item["review_due_on"]),
    )


def _clinical_case(item: dict[str, Any]) -> ClinicalTestCase:
    raw_answers = item["selected_answers"]
    if not isinstance(raw_answers, list) or any(
        not isinstance(value, dict) or set(value) != _CLINICAL_CASE_ANSWER_KEYS
        for value in raw_answers
    ):
        raise CatalogLoadError(
            "catalog.case_answers",
            "clinical case answers are invalid",
        )
    raw_events = item["audit_events"]
    if not isinstance(raw_events, list) or any(
        not isinstance(value, dict) or set(value) != _CLINICAL_CASE_EVENT_KEYS
        for value in raw_events
    ):
        raise CatalogLoadError(
            "catalog.case_events",
            "clinical case audit events are invalid",
        )
    return ClinicalTestCase(
        case_id=item["case_id"],
        module_id=item["module_id"],
        ordinal=item["ordinal"],
        category=ClinicalCaseCategory(item["category"]),
        narrative=item["narrative"],
        selected_answers=tuple(
            ClinicalCaseAnswer(
                fact_id=value["fact_id"],
                values=_list(value, "values"),
                detail=value["detail"],
            )
            for value in raw_answers
        ),
        positive_details=_list(item, "positive_details"),
        expected_route_module_ids=_list(
            item, "expected_route_module_ids"
        ),
        obtained_route_module_ids=_list(
            item, "obtained_route_module_ids"
        ),
        opened_question_ids=_list(item, "opened_question_ids"),
        initial_classification=item["initial_classification"],
        differentials=_list(item, "differentials"),
        physical_examination=_list(item, "physical_examination"),
        complementary_exams=_list(item, "complementary_exams"),
        post_exam_result=item["post_exam_result"],
        expected_impression=item["expected_impression"],
        audit_events=tuple(
            ClinicalCaseAuditEvent(
                sequence=value["sequence"],
                event_type=value["event_type"],
                payload=value["payload"],
            )
            for value in raw_events
        ),
        audit_hash=item["audit_hash"],
    )


def _files_for_schema(schema_version: str) -> tuple[str, ...]:
    if schema_version == "7.0.0":
        return _LEGACY_CATALOG_FILES
    if schema_version == "8.0.0":
        return _MODULE_CATALOG_FILES
    if schema_version == "9.0.0":
        return _RULE_CATALOG_FILES
    if schema_version == "10.0.0":
        return _CONTENT_CATALOG_FILES
    if schema_version == CATALOG_SCHEMA_VERSION:
        return _CATALOG_FILES
    raise CatalogLoadError("catalog.version", "unsupported manifest version")


def _read_file(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise CatalogLoadError("catalog.file", f"required catalog file unavailable: {path.name}")
    if path.stat().st_size > MAX_CATALOG_BYTES:
        raise CatalogLoadError("catalog.size", f"catalog file too large: {path.name}")
    try:
        return path.read_bytes()
    except OSError as exc:
        raise CatalogLoadError("catalog.file", f"catalog file unreadable: {path.name}") from exc


def _decode_json(data: bytes, filename: str) -> Any:
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=_object)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise CatalogLoadError("catalog.json", f"invalid catalog JSON: {filename}") from exc


def _object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CatalogLoadError("catalog.duplicate_key", "duplicate JSON key")
        result[key] = value
    return result


def _items(
    payload: dict[str, Any], filename: str, expected_keys: frozenset[str]
) -> tuple[dict[str, Any], ...]:
    values = payload["items"]
    if not isinstance(values, list) or len(values) > MAX_CATALOG_ITEMS:
        raise CatalogLoadError("catalog.items", f"invalid item collection: {filename}")
    if any(not isinstance(item, dict) or set(item) != expected_keys for item in values):
        raise CatalogLoadError("catalog.fields", f"invalid item fields: {filename}")
    return tuple(values)


def _form_schema(item: dict[str, Any]) -> SpecialtyFormSchema:
    raw_fields = item["fields"]
    if not isinstance(raw_fields, list) or not raw_fields:
        raise CatalogLoadError("catalog.schema_fields", "form schema fields are invalid")
    if any(not isinstance(field, dict) or set(field) != _FIELD_KEYS for field in raw_fields):
        raise CatalogLoadError("catalog.schema_fields", "form schema fields are invalid")
    return SpecialtyFormSchema(
        schema_id=item["schema_id"],
        specialty_key=item["specialty_key"],
        workflow_id=item["workflow_id"],
        step_key=item["step_key"],
        version=item["version"],
        fields=tuple(
            ClinicalFieldDefinition(
                field_key=field["field_key"],
                label=field["label"],
                section=ClinicalSnapshotSection(field["section"]),
                value_type=ClinicalFieldValueType(field["value_type"]),
                knowledge_object_id=field["knowledge_object_id"],
                required=field["required"],
                allowed_values=_list(field, "allowed_values"),
            )
            for field in raw_fields
        ),
        status=KnowledgeStatus(item["status"]),
        reviewed_on=_date_or_none(item["reviewed_on"]),
        validated_by=item["validated_by"],
        review_due_on=_date_or_none(item["review_due_on"]),
    )


def _date_or_none(value: object) -> date | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise CatalogLoadError("catalog.date", "review date must be ISO text or null")
    return date.fromisoformat(value)


def _list(item: dict[str, Any], key: str) -> tuple[Any, ...]:
    value = item[key]
    if not isinstance(value, list):
        raise CatalogLoadError("catalog.collection", f"{key} must be a JSON array")
    return tuple(value)


def _evidence_anchors(item: dict[str, Any]) -> tuple[EvidenceAnchor, ...]:
    values = item["evidence_anchors"]
    if not isinstance(values, list) or not values:
        raise CatalogLoadError(
            "catalog.evidence_anchors", "evidence anchors are invalid"
        )
    expected = {"source_id", "section", "locator"}
    if any(not isinstance(value, dict) or set(value) != expected for value in values):
        raise CatalogLoadError(
            "catalog.evidence_anchors", "evidence anchors are invalid"
        )
    return tuple(
        EvidenceAnchor(
            source_id=value["source_id"],
            section=value["section"],
            locator=value["locator"],
        )
        for value in values
    )


_EVIDENCE_KEYS = frozenset(
    {
        "source_id", "title", "publication_year", "evidence_type",
        "evidence_quality", "recommendation_strength", "locator", "version",
        "status", "specialties", "reviewed_on", "known_conflicts",
        "clinical_applicability", "review_due_on",
    }
)
_KNOWLEDGE_KEYS = frozenset(
    {
        "object_id", "official_name", "object_type", "description",
        "evidence_anchors", "applicability", "limits", "version", "status",
        "reviewed_on", "validated_by", "review_due_on",
    }
)
_SCHEMA_KEYS = frozenset(
    {
        "schema_id", "specialty_key", "workflow_id", "step_key", "version",
        "status", "reviewed_on", "validated_by", "review_due_on", "fields",
    }
)
_FIELD_KEYS = frozenset(
    {"field_key", "label", "section", "value_type", "knowledge_object_id", "required", "allowed_values"}
)
_SAFETY_CHECK_KEYS = frozenset(
    {
        "check_id", "specialty_key", "purpose", "limits",
        "evidence_source_ids", "version", "status", "reviewed_on",
        "validated_by", "review_due_on",
    }
)
_TERMINOLOGY_CODE_KEYS = frozenset({"system", "code", "display", "version"})
_CLINICAL_MODULE_KEYS = frozenset(
    {
        "module_id",
        "version",
        "official_name",
        "display_name",
        "entity_type",
        "primary_specialty",
        "synonyms",
        "abbreviations",
        "related_specialties",
        "parent_module_id",
        "related_module_ids",
        "terminology_codes",
        "populations",
        "care_settings",
        "source_ids",
        "legacy_keys",
        "terminology_status",
        "content_status",
        "status",
        "reviewed_on",
        "reviewed_by",
        "review_due_on",
    }
)
_CLINICAL_RULE_KEYS = frozenset(
    {
        "rule_id",
        "module_id",
        "version",
        "effect",
        "strength",
        "rationale",
        "when",
        "output_key",
        "output_value",
        "priority",
        "source_ids",
        "status",
        "reviewed_on",
        "reviewed_by",
        "review_due_on",
    }
)
_CLINICAL_CONTENT_KEYS = frozenset(
    {
        "module_id",
        "version",
        "definition",
        "boundaries",
        "anchor_values",
        "required_manifestations",
        "frequent_manifestations",
        "atypical_manifestations",
        "contrary_findings",
        "risk_factors",
        "red_flags",
        "stop_conditions",
        "likely_hypotheses",
        "cannot_miss_hypotheses",
        "mimics",
        "discriminators",
        "physical_examination",
        "complementary_exams",
        "diagnostic_criteria",
        "post_exam_reassessment",
        "safety_conduct",
        "initial_treatment",
        "definitive_treatment",
        "destination_return_followup",
        "source_ids",
        "content_status",
        "status",
        "reviewed_on",
        "reviewed_by",
        "review_due_on",
    }
)
_DISCRIMINATOR_KEYS = frozenset(
    {
        "question_id",
        "text",
        "options",
        "rationale",
        "detail_on_positive",
        "detail_required",
        "source_ids",
    }
)
_COMPLEMENTARY_EXAM_KEYS = frozenset(
    {
        "exam_id",
        "name",
        "clinical_question",
        "when",
        "limitations",
        "source_ids",
    }
)
_CLINICAL_CASE_KEYS = frozenset(
    {
        "case_id",
        "module_id",
        "ordinal",
        "category",
        "narrative",
        "selected_answers",
        "positive_details",
        "expected_route_module_ids",
        "obtained_route_module_ids",
        "opened_question_ids",
        "initial_classification",
        "differentials",
        "physical_examination",
        "complementary_exams",
        "post_exam_result",
        "expected_impression",
        "audit_events",
        "audit_hash",
    }
)
_CLINICAL_CASE_ANSWER_KEYS = frozenset({"fact_id", "values", "detail"})
_CLINICAL_CASE_EVENT_KEYS = frozenset(
    {"sequence", "event_type", "payload"}
)
