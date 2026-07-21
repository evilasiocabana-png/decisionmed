"""Snapshot diff engine."""

from __future__ import annotations

from dataclasses import dataclass, field

from clinical_snapshot.models import ClinicalSnapshot


@dataclass(frozen=True)
class SnapshotDiff:
    new_findings: tuple[str, ...] = field(default_factory=tuple)
    removed_findings: tuple[str, ...] = field(default_factory=tuple)
    changed_hypotheses: bool = False
    changed_safety: bool = False
    changed_evidence: bool = False
    changed_confidence: bool = False


class SnapshotDiffEngine:
    """Compares snapshots structurally without interpretation."""

    def compare(self, left: ClinicalSnapshot, right: ClinicalSnapshot) -> SnapshotDiff:
        return SnapshotDiff(
            changed_hypotheses=left.hypotheses != right.hypotheses,
            changed_safety=left.safety != right.safety,
            changed_evidence=left.evidence != right.evidence,
            changed_confidence=left.confidence != right.confidence,
        )
