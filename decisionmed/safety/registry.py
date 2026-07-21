"""Deterministic safety-check registry backed by governed evidence metadata."""

from __future__ import annotations

from collections.abc import Iterable

from decisionmed.evidence import EvidenceRegistry, EvidenceStatus

from .definitions import SafetyCheckSpecification, SafetyCheckStatus
from .models import SafetyError


class SafetyCheckRegistry:
    """Register check specifications without evaluating patient data."""

    def __init__(
        self,
        evidence: EvidenceRegistry,
        specifications: Iterable[SafetyCheckSpecification] = (),
    ) -> None:
        if not isinstance(evidence, EvidenceRegistry):
            raise TypeError("evidence must be an EvidenceRegistry")
        self._evidence = evidence
        self._specifications: dict[str, SafetyCheckSpecification] = {}
        for specification in specifications:
            self.register(specification)

    def register(
        self, specification: SafetyCheckSpecification
    ) -> SafetyCheckSpecification:
        if not isinstance(specification, SafetyCheckSpecification):
            raise TypeError("specification must be a SafetyCheckSpecification")
        if specification.check_id in self._specifications:
            raise SafetyError(
                "safety_check_registry.duplicate",
                f"check already registered: {specification.check_id}",
            )
        sources = tuple(
            self._evidence.get(source_id)
            for source_id in specification.evidence_source_ids
        )
        missing = tuple(
            source_id
            for source_id, source in zip(specification.evidence_source_ids, sources)
            if source is None
        )
        if missing:
            raise SafetyError(
                "safety_check_registry.unknown_evidence",
                f"unknown evidence sources: {', '.join(missing)}",
            )
        if any(
            specification.specialty_key not in source.specialties
            for source in sources
            if source is not None
        ):
            raise SafetyError(
                "safety_check_registry.specialty_evidence_mismatch",
                "evidence must declare the specification specialty",
            )
        if specification.status is SafetyCheckStatus.VALIDATED and any(
            source.status is not EvidenceStatus.VALIDATED
            for source in sources
            if source is not None
        ):
            raise SafetyError(
                "safety_check_registry.unvalidated_evidence",
                "validated specification requires validated evidence",
            )
        self._specifications[specification.check_id] = specification
        return specification

    def get(self, check_id: str) -> SafetyCheckSpecification | None:
        return self._specifications.get(check_id)

    def require(self, check_id: str) -> SafetyCheckSpecification:
        specification = self.get(check_id)
        if specification is None:
            raise SafetyError(
                "safety_check_registry.unknown",
                f"check not registered: {check_id}",
            )
        return specification

    def all(self) -> tuple[SafetyCheckSpecification, ...]:
        return tuple(
            self._specifications[check_id]
            for check_id in sorted(self._specifications)
        )

    @property
    def evidence(self) -> EvidenceRegistry:
        return self._evidence

    def for_specialty(
        self, specialty_key: str
    ) -> tuple[SafetyCheckSpecification, ...]:
        return tuple(
            specification
            for specification in self.all()
            if specification.specialty_key == specialty_key
        )
