"""Clinical Snapshot validation."""

from __future__ import annotations

from dataclasses import dataclass, field

from clinical_snapshot.models import ClinicalSnapshot


@dataclass(frozen=True)
class SnapshotValidation:
    missing_sections: tuple[str, ...] = field(default_factory=tuple)
    broken_traces: tuple[str, ...] = field(default_factory=tuple)
    invalid_versions: tuple[str, ...] = field(default_factory=tuple)
    duplicate_identifiers: tuple[str, ...] = field(default_factory=tuple)

    @property
    def valid(self) -> bool:
        return not (
            self.missing_sections
            or self.broken_traces
            or self.invalid_versions
            or self.duplicate_identifiers
        )


class SnapshotValidator:
    """Validates structural integrity only."""

    def validate(self, snapshot: ClinicalSnapshot) -> SnapshotValidation:
        missing = []
        if not snapshot.snapshot_id:
            missing.append("snapshot_id")
        if not snapshot.safety:
            missing.append("safety")
        if not snapshot.evidence:
            missing.append("evidence")
        if not snapshot.explanations:
            missing.append("explanations")
        broken = tuple(
            name
            for name, value in snapshot.references.__dict__.items()
            if not value
        )
        return SnapshotValidation(missing_sections=tuple(missing), broken_traces=broken)
