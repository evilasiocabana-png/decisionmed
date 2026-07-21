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
            views.append(
                SpecialtyView(
                    key=pack.key,
                    display_name=pack.display_name,
                    intended_scope=pack.intended_scope,
                    excluded_uses=pack.excluded_uses,
                    version=pack.version,
                    workflow_contract=workflow.workflow_id,
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
            }
        return {
            "loaded": True,
            "catalog_id": self._catalogs.manifest.catalog_id,
            "release_version": self._catalogs.manifest.release_version,
            "status": self._catalogs.manifest.status.value,
            "clinical_execution_allowed": False,
            "form_schema_count": len(self._catalogs.form_schemas.all()),
            "safety_check_count": len(self._catalogs.safety_checks.all()),
        }

    def get_readiness(self) -> dict[str, Any]:
        specialties = self.specialties()
        return self._readiness.report(item.load_status for item in specialties)

    def start_session(self, specialty_key: str) -> dict[str, object]:
        return self._sessions.start(specialty_key).to_dict()

    def advance_session(self, session_id: str, step_key: str) -> dict[str, object]:
        return self._sessions.advance(session_id, step_key).to_dict()


def _public_locator(locator: str) -> str | None:
    parsed = urlsplit(locator)
    if parsed.scheme in {"http", "https"} and parsed.netloc:
        return locator
    return None
