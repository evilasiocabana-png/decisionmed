"""Evidence Snapshot builder."""

from __future__ import annotations

from evidence_runtime.models import Citation, Evidence, EvidenceSnapshot


class EvidenceSnapshotBuilder:
    """Builds a compact runtime summary of evidence usage."""

    def build(
        self,
        selected: tuple[Evidence, ...] = (),
        discarded: tuple[Evidence, ...] = (),
        citations: tuple[Citation, ...] = (),
        version_policy: str = "latest",
    ) -> EvidenceSnapshot:
        return EvidenceSnapshot(
            selected_count=len(selected),
            discarded_count=len(discarded),
            citation_count=len(citations),
            version_policy=version_policy,
        )
