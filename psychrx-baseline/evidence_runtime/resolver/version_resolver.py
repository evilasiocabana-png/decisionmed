"""Evidence version resolver."""

from __future__ import annotations

from evidence_runtime.models import Evidence


class EvidenceVersionResolver:
    """Selects versions reproducibly without altering evidence content."""

    def resolve(
        self,
        evidence: tuple[Evidence, ...],
        version: str = "latest",
    ) -> tuple[Evidence, ...]:
        if version in ("latest", ""):
            return evidence
        return tuple(item for item in evidence if item.metadata.version == version)
