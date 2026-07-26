"""Read-only application service for the DecisionMEd MVP shell."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from urllib.parse import urlsplit

from .application import GovernedCatalogs
from .composition import SpecialtyPackResolver, build_reference_resolver
from .knowledge import KnowledgeError
from .readiness import PlatformReadinessService
from .safety import SafetyCheckEvaluatorRegistry, SafetyCheckProviderRegistry
from .sessions import WorkflowSessionService
from .specialties import SpecialtyPackRegistry, build_default_specialty_registry
from .workflows import (
    SpecialtyWorkflow,
    WorkflowRegistry,
    build_default_workflow_registry,
)


@dataclass(frozen=True, slots=True)
class SpecialtyView:
    key: str
    display_name: str
    intended_scope: str
    excluded_uses: tuple[str, ...]
    version: str
    workflow_contract: str
    workflow_step_count: int
    reference_schema_step_keys: tuple[str, ...]
    missing_reference_schema_step_keys: tuple[str, ...]
    reference_knowledge_object_count: int
    reference_evidence_source_count: int
    reference_curation_state: str
    pack_status: str
    load_status: str
    execution_allowed: bool
    available_capabilities: tuple[str, ...]
    missing_capabilities: tuple[str, ...]
    incompatible_capabilities: tuple[str, ...]
    blocking_reasons: tuple[str, ...]
    trace_id: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "display_name": self.display_name,
            "intended_scope": self.intended_scope,
            "excluded_uses": list(self.excluded_uses),
            "version": self.version,
            "workflow_contract": self.workflow_contract,
            "workflow_step_count": self.workflow_step_count,
            "reference_schema_step_keys": list(self.reference_schema_step_keys),
            "missing_reference_schema_step_keys": list(
                self.missing_reference_schema_step_keys
            ),
            "reference_knowledge_object_count": self.reference_knowledge_object_count,
            "reference_evidence_source_count": self.reference_evidence_source_count,
            "reference_curation_state": self.reference_curation_state,
            "pack_status": self.pack_status,
            "load_status": self.load_status,
            "execution_allowed": self.execution_allowed,
            "available_capabilities": list(self.available_capabilities),
            "missing_capabilities": list(self.missing_capabilities),
            "incompatible_capabilities": list(self.incompatible_capabilities),
            "blocking_reasons": list(self.blocking_reasons),
            "trace_id": self.trace_id,
        }


class DecisionMedAppService:
    """Expose composition state without running clinical capabilities."""

    def __init__(
        self,
        registry: SpecialtyPackRegistry | None = None,
        resolver: SpecialtyPackResolver | None = None,
        workflows: WorkflowRegistry | None = None,
        readiness: PlatformReadinessService | None = None,
        sessions: WorkflowSessionService | None = None,
        catalogs: GovernedCatalogs | None = None,
        safety_providers: SafetyCheckProviderRegistry | None = None,
        safety_evaluators: SafetyCheckEvaluatorRegistry | None = None,
    ) -> None:
        self._registry = registry or build_default_specialty_registry()
        if resolver is None:
            catalog_specialty_keys = (
                tuple(
                    schema.specialty_key for schema in catalogs.form_schemas.all()
                )
                if catalogs is not None
                else ()
            )
            resolver = build_reference_resolver(
                catalog_specialty_keys,
                platform_specialty_keys=tuple(
                    pack.key for pack in self._registry.all()
                ),
            )
        self._resolver = resolver
        self._workflows = workflows or build_default_workflow_registry(self._registry)
        self._catalogs = catalogs
        self._validate_catalog_workflow_bindings()
        self._readiness = readiness or PlatformReadinessService(
            evidence=catalogs.evidence if catalogs is not None else None,
            knowledge=catalogs.knowledge if catalogs is not None else None,
            form_schemas=catalogs.form_schemas if catalogs is not None else None,
            safety_checks=catalogs.safety_checks if catalogs is not None else None,
            safety_providers=safety_providers,
            safety_evaluators=safety_evaluators,
        )
        self._sessions = sessions or WorkflowSessionService(
            self._registry, self._workflows
        )

    def workflow(self, specialty_key: str) -> SpecialtyWorkflow:
        self._registry.require(specialty_key)
        return self._workflows.require(specialty_key)

    def specialties(self) -> tuple[SpecialtyView, ...]:
        views: list[SpecialtyView] = []
        for pack in self._registry.all():
            result = self._resolver.resolve(pack)
            workflow = self._workflows.require(pack.key)
            workflow_step_keys = tuple(step.key for step in workflow.steps)
            schema_step_keys = self._reference_schema_step_keys(workflow)
            knowledge_object_ids = self._reference_knowledge_object_ids(workflow)
            source_ids = self._reference_evidence_source_ids(knowledge_object_ids)
            views.append(
                SpecialtyView(
                    key=pack.key,
                    display_name=pack.display_name,
                    intended_scope=pack.intended_scope,
                    excluded_uses=pack.excluded_uses,
                    version=pack.version,
                    workflow_contract=workflow.workflow_id,
                    workflow_step_count=len(workflow_step_keys),
                    reference_schema_step_keys=schema_step_keys,
                    missing_reference_schema_step_keys=tuple(
                        step_key
                        for step_key in workflow_step_keys
                        if step_key not in schema_step_keys
                    ),
                    reference_knowledge_object_count=len(knowledge_object_ids),
                    reference_evidence_source_count=len(source_ids),
                    reference_curation_state=self._reference_curation_state(
                        knowledge_object_ids
                    ),
                    pack_status=pack.status.value,
                    load_status=result.status.value,
                    execution_allowed=result.clinical_execution_allowed,
                    available_capabilities=tuple(
                        binding.capability for binding in result.bindings
                    ),
                    missing_capabilities=result.missing_capabilities,
                    incompatible_capabilities=result.incompatible_capabilities,
                    blocking_reasons=result.blocking_reasons,
                    trace_id=result.trace_id,
                )
            )
        return tuple(views)

    def _reference_schema_step_keys(
        self, workflow: SpecialtyWorkflow
    ) -> tuple[str, ...]:
        if self._catalogs is None:
            return ()
        return tuple(
            schema.step_key
            for schema in self._catalogs.form_schemas.all()
            if (
                schema.specialty_key == workflow.specialty_key
                and schema.workflow_id == workflow.workflow_id
            )
        )

    def _reference_knowledge_object_ids(
        self, workflow: SpecialtyWorkflow
    ) -> tuple[str, ...]:
        if self._catalogs is None:
            return ()
        return tuple(
            sorted(
                field.knowledge_object_id
                for schema in self._catalogs.form_schemas.all()
                if (
                    schema.specialty_key == workflow.specialty_key
                    and schema.workflow_id == workflow.workflow_id
                )
                for field in schema.fields
            )
        )

    def _reference_evidence_source_ids(
        self, knowledge_object_ids: tuple[str, ...]
    ) -> tuple[str, ...]:
        if self._catalogs is None:
            return ()
        return tuple(
            sorted(
                {
                    source_id
                    for object_id in knowledge_object_ids
                    for source_id in self._catalogs.knowledge.require(
                        object_id
                    ).evidence_source_ids
                }
            )
        )

    def _reference_curation_state(
        self, knowledge_object_ids: tuple[str, ...]
    ) -> str:
        if self._catalogs is None:
            return "catalog_not_loaded"
        if not knowledge_object_ids:
            return "not_started"
        statuses = {
            self._catalogs.knowledge.require(object_id).status.value
            for object_id in knowledge_object_ids
        }
        return "validated_reference_only" if statuses == {"validated"} else "draft"

    def _validate_catalog_workflow_bindings(self) -> None:
        """Reject reference schemas that do not map to a declared workflow step."""

        if self._catalogs is None:
            return
        for schema in self._catalogs.form_schemas.all():
            try:
                workflow = self._workflows.require(schema.specialty_key)
            except KeyError as exc:
                raise ValueError(
                    "catalog form schema references an unknown specialty workflow: "
                    f"{schema.specialty_key}"
                ) from exc
            if schema.workflow_id != workflow.workflow_id:
                raise ValueError(
                    "catalog form schema workflow contract does not match specialty "
                    f"workflow: {schema.schema_id}"
                )
            if schema.step_key not in {step.key for step in workflow.steps}:
                raise ValueError(
                    "catalog form schema references an unknown workflow step: "
                    f"{schema.schema_id}"
                )

    def form_schema(self, specialty_key: str, step_key: str) -> dict[str, Any]:
        """Expose governed metadata without accepting or interpreting values."""

        workflow = self.workflow(specialty_key)
        if step_key not in {step.key for step in workflow.steps}:
            raise KnowledgeError(
                "specialty_form_schema_registry.unknown",
                "workflow step does not exist",
            )
        if self._catalogs is None:
            raise KnowledgeError(
                "specialty_form_schema_registry.unknown",
                "knowledge catalog is not loaded",
            )
        schema = self._catalogs.form_schemas.require(
            specialty_key, workflow.workflow_id, step_key
        )
        fields: list[dict[str, Any]] = []
        for field in schema.fields:
            knowledge = self._catalogs.knowledge.require(field.knowledge_object_id)
            sources = tuple(
                (
                    self._catalogs.evidence.require(source_id),
                    tuple(
                        anchor
                        for anchor in knowledge.evidence_anchors
                        if anchor.source_id == source_id
                    ),
                )
                for source_id in knowledge.evidence_source_ids
            )
            fields.append(
                {
                    "field_key": field.field_key,
                    "label": field.label,
                    "section": field.section.value,
                    "value_type": field.value_type.value,
                    "required": field.required,
                    "allowed_values": list(field.allowed_values),
                    "runtime_eligible": False,
                    "knowledge": {
                        "object_id": knowledge.object_id,
                        "official_name": knowledge.official_name,
                        "object_type": knowledge.object_type.value,
                        "description": knowledge.description,
                        "version": knowledge.version,
                        "status": knowledge.status.value,
                        "reviewed_on": (
                            knowledge.reviewed_on.isoformat()
                            if knowledge.reviewed_on is not None
                            else None
                        ),
                        "review_due_on": (
                            knowledge.review_due_on.isoformat()
                            if knowledge.review_due_on is not None
                            else None
                        ),
                        "review_state": knowledge.review_state,
                        "validated_by": knowledge.validated_by,
                        "applicability": knowledge.applicability,
                        "limits": knowledge.limits,
                        "runtime_eligible": False,
                        "evidence_sources": [
                            {
                                "source_id": source.source_id,
                                "title": source.title,
                                "publication_year": source.publication_year,
                                "evidence_type": source.evidence_type.value,
                                "evidence_quality": source.evidence_quality.value,
                                "recommendation_strength": (
                                    source.recommendation_strength.value
                                ),
                                "locator": _public_locator(source.locator),
                                "version": source.version,
                                "status": source.status.value,
                                "specialties": list(source.specialties),
                                "reviewed_on": source.reviewed_on.isoformat(),
                                "review_due_on": (
                                    source.review_due_on.isoformat()
                                    if source.review_due_on is not None
                                    else None
                                ),
                                "review_state": source.review_state,
                                "known_conflicts": source.known_conflicts,
                                "clinical_applicability": (
                                    source.clinical_applicability
                                ),
                                "anchors": [
                                    {
                                        "section": anchor.section,
                                        "locator": _public_locator(anchor.locator),
                                        "runtime_eligible": False,
                                    }
                                    for anchor in anchors
                                ],
                                "runtime_eligible": False,
                            }
                            for source, anchors in sources
                        ],
                    },
                }
            )
        return {
            "schema_id": schema.schema_id,
            "specialty_key": schema.specialty_key,
            "workflow_id": schema.workflow_id,
            "step_key": schema.step_key,
            "version": schema.version,
            "status": schema.status.value,
            "reviewed_on": (
                schema.reviewed_on.isoformat()
                if schema.reviewed_on is not None
                else None
            ),
            "review_due_on": (
                schema.review_due_on.isoformat()
                if schema.review_due_on is not None
                else None
            ),
            "review_state": schema.review_state,
            "validated_by": schema.validated_by,
            "mode": "reference_only",
            "runtime_eligible": False,
            "clinical_execution_allowed": False,
            "fields": fields,
        }

    def get_app_state(self) -> dict[str, Any]:
        specialties = self.specialties()
        readiness = self._readiness.report(item.load_status for item in specialties)
        return {
            "product": "DecisionMEd",
            "mode": "read-only",
            "clinical_execution_allowed": False,
            "specialties": [item.to_dict() for item in specialties],
            "workflow_specialties": [item.key for item in specialties],
            "knowledge_catalog": self._catalog_state(),
            "readiness": readiness,
        }

    def _catalog_state(self) -> dict[str, Any]:
        if self._catalogs is None:
            return {
                "loaded": False,
                "clinical_execution_allowed": False,
                "form_schema_count": 0,
                "clinical_module_count": 0,
                "clinical_module_counts_by_specialty": {},
                "clinical_module_counts_by_entity_type": {},
                "clinical_module_counts_by_status": {},
                "clinical_rule_count": 0,
                "clinical_rule_counts_by_status": {},
                "clinical_content_count": 0,
                "clinical_content_counts_by_status": {},
                "clinical_case_count": 0,
            }
        clinical_modules = getattr(self._catalogs, "clinical_modules", None)
        clinical_rules = getattr(self._catalogs, "clinical_rules", None)
        clinical_content = getattr(self._catalogs, "clinical_content", None)
        clinical_cases = getattr(self._catalogs, "clinical_cases", None)
        return {
            "loaded": True,
            "schema_version": getattr(
                self._catalogs.manifest, "schema_version", "7.0.0"
            ),
            "catalog_id": self._catalogs.manifest.catalog_id,
            "release_version": self._catalogs.manifest.release_version,
            "status": self._catalogs.manifest.status.value,
            "clinical_execution_allowed": False,
            "form_schema_count": len(self._catalogs.form_schemas.all()),
            "safety_check_count": len(self._catalogs.safety_checks.all()),
            "clinical_module_count": (
                len(clinical_modules.all()) if clinical_modules is not None else 0
            ),
            "clinical_module_counts_by_specialty": (
                clinical_modules.counts_by_specialty()
                if clinical_modules is not None
                else {}
            ),
            "clinical_module_counts_by_entity_type": (
                clinical_modules.counts_by_entity_type()
                if clinical_modules is not None
                else {}
            ),
            "clinical_module_counts_by_status": (
                clinical_modules.counts_by_status()
                if clinical_modules is not None
                else {}
            ),
            "clinical_rule_count": (
                len(clinical_rules.all()) if clinical_rules is not None else 0
            ),
            "clinical_rule_counts_by_status": (
                clinical_rules.counts_by_status()
                if clinical_rules is not None
                else {}
            ),
            "clinical_content_count": (
                len(clinical_content.all())
                if clinical_content is not None
                else 0
            ),
            "clinical_content_counts_by_status": (
                clinical_content.counts_by_content_status()
                if clinical_content is not None
                else {}
            ),
            "clinical_case_count": (
                len(clinical_cases.all())
                if clinical_cases is not None
                else 0
            ),
        }

    def get_readiness(self) -> dict[str, Any]:
        specialties = self.specialties()
        return self._readiness.report(item.load_status for item in specialties)

    def clinical_module_catalog(self) -> dict[str, Any]:
        if self._catalogs is None:
            return {
                "loaded": False,
                "schema_version": None,
                "release_version": None,
                "count": 0,
                "items": [],
            }
        clinical_modules = getattr(self._catalogs, "clinical_modules", None)
        modules = clinical_modules.all() if clinical_modules is not None else ()
        return {
            "loaded": True,
            "schema_version": getattr(
                self._catalogs.manifest, "schema_version", "7.0.0"
            ),
            "release_version": getattr(
                self._catalogs.manifest, "release_version", None
            ),
            "count": len(modules),
            "clinical_execution_allowed": False,
            "items": [
                self._clinical_module_to_dict(module)
                for module in modules
            ],
        }

    def clinical_module(self, module_id_or_legacy_key: str) -> dict[str, Any]:
        clinical_modules = (
            getattr(self._catalogs, "clinical_modules", None)
            if self._catalogs is not None
            else None
        )
        if clinical_modules is None:
            raise KnowledgeError(
                "clinical_module_catalog.not_loaded",
                "clinical module catalog is not loaded",
            )
        module = clinical_modules.require(module_id_or_legacy_key)
        return self._clinical_module_to_dict(module)

    def clinical_rule_catalog(self) -> dict[str, Any]:
        if self._catalogs is None:
            return {
                "loaded": False,
                "schema_version": None,
                "release_version": None,
                "count": 0,
                "items": [],
            }
        clinical_rules = getattr(self._catalogs, "clinical_rules", None)
        rules = clinical_rules.all() if clinical_rules is not None else ()
        return {
            "loaded": True,
            "schema_version": getattr(
                self._catalogs.manifest, "schema_version", "7.0.0"
            ),
            "release_version": getattr(
                self._catalogs.manifest, "release_version", None
            ),
            "count": len(rules),
            "clinical_execution_allowed": False,
            "items": [self._clinical_rule_to_dict(rule) for rule in rules],
        }

    def _clinical_rule_to_dict(self, rule: Any) -> dict[str, Any]:
        return {
            "rule_id": rule.rule_id,
            "module_id": rule.module_id,
            "version": rule.version,
            "effect": rule.effect.value,
            "strength": rule.strength.value,
            "rationale": rule.rationale,
            "when": _clinical_rule_condition_to_dict(rule.when),
            "output_key": rule.output_key,
            "output_value": rule.output_value,
            "priority": rule.priority,
            "source_ids": list(rule.source_ids),
            "status": rule.status.value,
            "reviewed_on": (
                rule.reviewed_on.isoformat()
                if rule.reviewed_on is not None
                else None
            ),
            "reviewed_by": rule.reviewed_by,
            "review_due_on": (
                rule.review_due_on.isoformat()
                if rule.review_due_on is not None
                else None
            ),
            "clinical_execution_allowed": False,
        }

    def clinical_content_catalog(self) -> dict[str, Any]:
        if self._catalogs is None:
            return {
                "loaded": False,
                "schema_version": None,
                "release_version": None,
                "count": 0,
                "items": [],
            }
        registry = getattr(self._catalogs, "clinical_content", None)
        contents = registry.all() if registry is not None else ()
        return {
            "loaded": True,
            "schema_version": getattr(
                self._catalogs.manifest, "schema_version", "7.0.0"
            ),
            "release_version": getattr(
                self._catalogs.manifest, "release_version", None
            ),
            "count": len(contents),
            "clinical_execution_allowed": False,
            "items": [
                self._clinical_content_to_dict(content)
                for content in contents
            ],
        }

    def _clinical_content_to_dict(self, content: Any) -> dict[str, Any]:
        return {
            "module_id": content.module_id,
            "version": content.version,
            "definition": content.definition,
            "boundaries": content.boundaries,
            "anchor_values": list(content.anchor_values),
            "required_manifestations": list(
                content.required_manifestations
            ),
            "frequent_manifestations": list(
                content.frequent_manifestations
            ),
            "atypical_manifestations": list(
                content.atypical_manifestations
            ),
            "contrary_findings": list(content.contrary_findings),
            "risk_factors": list(content.risk_factors),
            "red_flags": list(content.red_flags),
            "stop_conditions": list(content.stop_conditions),
            "likely_hypotheses": list(content.likely_hypotheses),
            "cannot_miss_hypotheses": list(
                content.cannot_miss_hypotheses
            ),
            "mimics": list(content.mimics),
            "discriminators": [
                {
                    "question_id": item.question_id,
                    "text": item.text,
                    "options": list(item.options),
                    "rationale": item.rationale,
                    "detail_on_positive": item.detail_on_positive,
                    "detail_required": item.detail_required,
                    "source_ids": list(item.source_ids),
                }
                for item in content.discriminators
            ],
            "physical_examination": list(content.physical_examination),
            "complementary_exams": [
                {
                    "exam_id": item.exam_id,
                    "name": item.name,
                    "clinical_question": item.clinical_question,
                    "when": item.when,
                    "limitations": item.limitations,
                    "source_ids": list(item.source_ids),
                }
                for item in content.complementary_exams
            ],
            "diagnostic_criteria": list(content.diagnostic_criteria),
            "post_exam_reassessment": list(
                content.post_exam_reassessment
            ),
            "safety_conduct": list(content.safety_conduct),
            "initial_treatment": list(content.initial_treatment),
            "definitive_treatment": list(content.definitive_treatment),
            "destination_return_followup": list(
                content.destination_return_followup
            ),
            "source_ids": list(content.source_ids),
            "content_status": content.content_status.value,
            "status": content.status.value,
            "reviewed_on": (
                content.reviewed_on.isoformat()
                if content.reviewed_on is not None
                else None
            ),
            "reviewed_by": content.reviewed_by,
            "review_due_on": (
                content.review_due_on.isoformat()
                if content.review_due_on is not None
                else None
            ),
            "clinical_execution_allowed": False,
        }

    def clinical_case_catalog(
        self,
        module_id: str | None = None,
        *,
        offset: int = 0,
        limit: int = 50,
    ) -> dict[str, Any]:
        if not isinstance(offset, int) or offset < 0:
            raise ValueError("offset must be a non-negative integer")
        if not isinstance(limit, int) or not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")
        if self._catalogs is None:
            return {
                "loaded": False,
                "schema_version": None,
                "release_version": None,
                "count": 0,
                "filtered_count": 0,
                "offset": offset,
                "limit": limit,
                "items": [],
            }
        registry = getattr(self._catalogs, "clinical_cases", None)
        if registry is None:
            cases = ()
        elif module_id:
            cases = registry.for_module(module_id)
        else:
            cases = registry.all()
        page = cases[offset : offset + limit]
        return {
            "loaded": True,
            "schema_version": getattr(
                self._catalogs.manifest, "schema_version", "7.0.0"
            ),
            "release_version": getattr(
                self._catalogs.manifest, "release_version", None
            ),
            "count": (
                len(registry.all()) if registry is not None else 0
            ),
            "filtered_count": len(cases),
            "offset": offset,
            "limit": limit,
            "clinical_execution_allowed": False,
            "items": [
                self._clinical_case_to_dict(case) for case in page
            ],
        }

    @staticmethod
    def _clinical_case_to_dict(case: Any) -> dict[str, Any]:
        return {
            "case_id": case.case_id,
            "module_id": case.module_id,
            "ordinal": case.ordinal,
            "category": case.category.value,
            "narrative": case.narrative,
            "selected_answers": [
                {
                    "fact_id": answer.fact_id,
                    "values": list(answer.values),
                    "detail": answer.detail,
                }
                for answer in case.selected_answers
            ],
            "positive_details": list(case.positive_details),
            "expected_route_module_ids": list(
                case.expected_route_module_ids
            ),
            "obtained_route_module_ids": list(
                case.obtained_route_module_ids
            ),
            "opened_question_ids": list(case.opened_question_ids),
            "initial_classification": case.initial_classification,
            "differentials": list(case.differentials),
            "physical_examination": list(case.physical_examination),
            "complementary_exams": list(case.complementary_exams),
            "post_exam_result": case.post_exam_result,
            "expected_impression": case.expected_impression,
            "audit_events": [
                {
                    "sequence": event.sequence,
                    "event_type": event.event_type,
                    "payload": event.payload,
                }
                for event in case.audit_events
            ],
            "audit_hash": case.audit_hash,
            "clinical_execution_allowed": False,
        }

    def _clinical_module_to_dict(self, module: Any) -> dict[str, Any]:
        sources = []
        if self._catalogs is not None:
            for source_id in module.source_ids:
                source = self._catalogs.evidence.require(source_id)
                sources.append(
                    {
                        "source_id": source.source_id,
                        "title": source.title,
                        "publication_year": source.publication_year,
                        "version": source.version,
                        "status": source.status.value,
                        "locator": _public_locator(source.locator),
                    }
                )
        return {
            "module_id": module.module_id,
            "version": module.version,
            "official_name": module.official_name,
            "display_name": module.display_name,
            "entity_type": module.entity_type.value,
            "primary_specialty": module.primary_specialty,
            "related_specialties": list(module.related_specialties),
            "synonyms": list(module.synonyms),
            "abbreviations": list(module.abbreviations),
            "parent_module_id": module.parent_module_id,
            "related_module_ids": list(module.related_module_ids),
            "populations": list(module.populations),
            "care_settings": list(module.care_settings),
            "legacy_keys": list(module.legacy_keys),
            "terminology_status": module.terminology_status.value,
            "content_status": module.content_status.value,
            "status": module.status.value,
            "reviewed_on": (
                module.reviewed_on.isoformat()
                if module.reviewed_on is not None
                else None
            ),
            "reviewed_by": module.reviewed_by,
            "review_due_on": (
                module.review_due_on.isoformat()
                if module.review_due_on is not None
                else None
            ),
            "sources": sources,
            "clinical_execution_allowed": False,
        }

    def start_session(self, specialty_key: str) -> dict[str, object]:
        return self._sessions.start(specialty_key).to_dict()

    def advance_session(self, session_id: str, step_key: str) -> dict[str, object]:
        return self._sessions.advance(session_id, step_key).to_dict()


def _clinical_rule_condition_to_dict(condition: Any) -> dict[str, Any]:
    if condition.all_of or condition.any_of or condition.none_of:
        payload: dict[str, Any] = {}
        if condition.all_of:
            payload["all"] = [
                _clinical_rule_condition_to_dict(item)
                for item in condition.all_of
            ]
        if condition.any_of:
            payload["any"] = [
                _clinical_rule_condition_to_dict(item)
                for item in condition.any_of
            ]
        if condition.none_of:
            payload["none"] = [
                _clinical_rule_condition_to_dict(item)
                for item in condition.none_of
            ]
        return payload
    payload = {
        "fact": condition.fact,
        "operator": condition.operator.value,
    }
    if condition.value is not None:
        payload["value"] = condition.value
    if condition.values:
        payload["values"] = list(condition.values)
    if condition.threshold is not None:
        payload["threshold"] = condition.threshold
    if condition.pattern is not None:
        payload["pattern"] = condition.pattern
    return payload

def _public_locator(locator: str) -> str | None:
    parsed = urlsplit(locator)
    if parsed.scheme in {"http", "https"} and parsed.netloc:
        return locator
    return None
