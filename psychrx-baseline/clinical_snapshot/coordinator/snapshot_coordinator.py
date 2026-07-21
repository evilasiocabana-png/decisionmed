"""Clinical Snapshot coordinator."""

from __future__ import annotations

from typing import Any

from clinical_snapshot.audit import SnapshotAudit, SnapshotAuditEntry
from clinical_snapshot.builder import SnapshotBuilder
from clinical_snapshot.models import ClinicalSnapshot
from clinical_snapshot.validator import SnapshotValidation, SnapshotValidator


class SnapshotCoordinator:
    """Coordinates snapshot creation without modifying upstream results."""

    def __init__(self) -> None:
        self.builder = SnapshotBuilder()
        self.validator = SnapshotValidator()
        self.audit = SnapshotAudit()

    def execute(
        self,
        runtime_result: dict[str, Any],
        safety_result: dict[str, Any],
        evidence_result: dict[str, Any],
        optimization_result: dict[str, Any],
        explanation_result: dict[str, Any],
    ) -> tuple[ClinicalSnapshot, SnapshotValidation]:
        snapshot = self.builder.build(
            runtime_result,
            safety_result,
            evidence_result,
            optimization_result,
            explanation_result,
        )
        validation = self.validator.validate(snapshot)
        self.audit.record(
            SnapshotAuditEntry(
                event="ClinicalSnapshotCreated",
                snapshot_id=snapshot.snapshot_id,
                runtime_id=snapshot.runtime_id,
                trace_id=snapshot.trace_id,
                version=snapshot.version.label(),
            )
        )
        return snapshot, validation
