"""Application-facing readiness report for non-clinical platform gates."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .evidence import EvidenceRegistry
from .knowledge import KnowledgeRegistry, SpecialtyFormSchemaRegistry
from .safety import SafetyCheckRegistry, SafetyCheckStatus


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
        safety_checks: SafetyCheckRegistry | None = None,
    ) -> None:
        self._evidence = evidence or EvidenceRegistry()
        self._knowledge = knowledge or KnowledgeRegistry(self._evidence)
        self._form_schemas = form_schemas or SpecialtyFormSchemaRegistry(
            self._knowledge
        )
        self._safety_checks = safety_checks or SafetyCheckRegistry(self._evidence)

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
        safety_specifications = self._safety_checks.all()
        safety_count = len(safety_specifications)
        validated_safety_count = sum(
            item.status is SafetyCheckStatus.VALIDATED
            for item in safety_specifications
        )
        overdue_safety_count = sum(
            item.review_overdue for item in safety_specifications
        )
        unscheduled_safety_count = sum(
            item.review_due_on is None for item in safety_specifications
        )
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
                "available"
                if safety_count
                and validated_safety_count == safety_count
                and not overdue_safety_count
                and not unscheduled_safety_count
                else "blocked",
                "no_safety_specifications"
                if not safety_count
                else "unvalidated_safety_specifications"
                if validated_safety_count != safety_count
                else "overdue_safety_review"
                if overdue_safety_count
                else "safety_review_schedule_missing"
                if unscheduled_safety_count
                else "safety_specifications_current",
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
                "validated_safety_checks": validated_safety_count,
                "overdue_safety_checks": overdue_safety_count,
                "safety_checks_without_review_schedule": unscheduled_safety_count,
            },
            "blocked_gate_count": blocked_count,
            "gates": [gate.to_dict() for gate in gates],
        }
