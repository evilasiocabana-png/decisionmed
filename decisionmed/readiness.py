"""Application-facing readiness report for non-clinical platform gates."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .evidence import EvidenceRegistry
from .knowledge import KnowledgeRegistry


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
        expected_safety_check_ids: Iterable[str] = (),
    ) -> None:
        self._evidence = evidence or EvidenceRegistry()
        self._knowledge = knowledge or KnowledgeRegistry(self._evidence)
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
        knowledge_count = len(self._knowledge.all())
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
                "available" if knowledge_count else "blocked",
                "metadata_present" if knowledge_count else "no_knowledge_objects",
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
                "configured_safety_checks": safety_count,
            },
            "blocked_gate_count": blocked_count,
            "gates": [gate.to_dict() for gate in gates],
        }
