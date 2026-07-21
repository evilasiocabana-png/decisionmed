"""Application-facing readiness report for non-clinical platform gates."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .evidence import EvidenceRegistry
from .knowledge import KnowledgeRegistry, SpecialtyFormSchemaRegistry


@dataclass(frozen=True, slots=True)
class ReadinessGate:
    key: str
    status: str
    reason: str

    def to_dict(self) -> dict[str, str]:
        return {"key": self.key, "status": self.status, "reason": self.reason}


class PlatformReadinessService:
    """Summarize technical gates without evaluating clinical readiness."""

    def __init__(
        self,
        evidence: EvidenceRegistry | None = None,
        knowledge: KnowledgeRegistry | None = None,
        form_schemas: SpecialtyFormSchemaRegistry | None = None,
        expected_safety_check_ids: Iterable[str] = (),
    ) -> None:
        self._evidence = evidence or EvidenceRegistry()
        self._knowledge = knowledge or KnowledgeRegistry(self._evidence)
        self._form_schemas = form_schemas or SpecialtyFormSchemaRegistry(
            self._knowledge
        )
        self._expected_safety_check_ids = tuple(expected_safety_check_ids)

    def report(self, specialty_statuses: Iterable[str]) -> dict[str, Any]:
        statuses = tuple(specialty_statuses)
        evidence_sources = self._evidence.all()
        evidence_count = len(evidence_sources)
        overdue_evidence_count = sum(
            source.review_overdue for source in evidence_sources
        )
        unscheduled_evidence_count = sum(
            source.review_due_on is None for source in evidence_sources
        )
        knowledge_objects = self._knowledge.all()
        knowledge_count = len(knowledge_objects)
        overdue_knowledge_count = sum(
            item.review_overdue for item in knowledge_objects
        )
        unscheduled_knowledge_count = sum(
            item.review_due_on is None for item in knowledge_objects
        )
        form_schemas = self._form_schemas.all()
        form_schema_count = len(form_schemas)
        overdue_form_schema_count = sum(
            schema.review_overdue for schema in form_schemas
        )
        unscheduled_form_schema_count = sum(
            schema.review_due_on is None for schema in form_schemas
        )
        safety_count = len(self._expected_safety_check_ids)
        specialty_ready = bool(statuses) and all(
            status == "ready_for_validation" for status in statuses
        )

        gates = (
            ReadinessGate(
                "domain_core",
                "available",
                "technical_contracts_loaded",
            ),
            ReadinessGate(
                "evidence_catalog",
                "available"
                if evidence_count
                and not overdue_evidence_count
                and not unscheduled_evidence_count
                else "blocked",
                "no_evidence_metadata"
                if not evidence_count
                else "overdue_evidence_review"
                if overdue_evidence_count
                else "review_schedule_missing"
                if unscheduled_evidence_count
                else "review_lifecycle_current",
            ),
            ReadinessGate(
                "knowledge_catalog",
                "available"
                if knowledge_count
                and form_schema_count
                and not overdue_knowledge_count
                and not unscheduled_knowledge_count
                and not overdue_form_schema_count
                and not unscheduled_form_schema_count
                else "blocked",
                "no_knowledge_objects"
                if not knowledge_count
                else "overdue_knowledge_review"
                if overdue_knowledge_count
                else "knowledge_review_schedule_missing"
                if unscheduled_knowledge_count
                else "no_form_schemas"
                if not form_schema_count
                else "overdue_form_schema_review"
                if overdue_form_schema_count
                else "form_schema_review_schedule_missing"
                if unscheduled_form_schema_count
                else "review_lifecycle_current",
            ),
            ReadinessGate(
                "safety_configuration",
                "available" if safety_count else "blocked",
                "checks_configured" if safety_count else "no_safety_checks_configured",
            ),
            ReadinessGate(
                "specialty_validation",
                "available" if specialty_ready else "blocked",
                "packs_ready_for_validation"
                if specialty_ready
                else "specialty_packs_not_validated",
            ),
            ReadinessGate(
                "clinical_validation",
                "blocked",
                "human_scientific_and_regulatory_validation_required",
            ),
        )
        blocked_count = sum(gate.status == "blocked" for gate in gates)
        return {
            "status": "in_progress",
            "clinical_execution_allowed": False,
            "counts": {
                "evidence_sources": evidence_count,
                "overdue_evidence_sources": overdue_evidence_count,
                "evidence_sources_without_review_schedule": (
                    unscheduled_evidence_count
                ),
                "knowledge_objects": knowledge_count,
                "overdue_knowledge_objects": overdue_knowledge_count,
                "knowledge_objects_without_review_schedule": (
                    unscheduled_knowledge_count
                ),
                "form_schemas": form_schema_count,
                "overdue_form_schemas": overdue_form_schema_count,
                "form_schemas_without_review_schedule": (
                    unscheduled_form_schema_count
                ),
                "configured_safety_checks": safety_count,
            },
            "blocked_gate_count": blocked_count,
            "gates": [gate.to_dict() for gate in gates],
        }
