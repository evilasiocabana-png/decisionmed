"""Snapshot identifier generation."""

from __future__ import annotations

from uuid import uuid5, NAMESPACE_URL


class SnapshotIdentifier:
    """Generates replay-friendly identifiers from deterministic seeds."""

    def generate(self, seed: str | None = None) -> str:
        if seed:
            return f"SNP-{uuid5(NAMESPACE_URL, seed)}"
        from uuid import uuid4

        return f"SNP-{uuid4()}"
