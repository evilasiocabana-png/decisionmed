"""Snapshot lineage graph."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SnapshotLineage:
    parent_snapshot: str = ""
    child_snapshot: str = ""
    derived_snapshot: str = ""
    branch_identifier: str = "main"


@dataclass
class SnapshotLineageGraph:
    """Read-only lineage registry."""

    edges: list[SnapshotLineage] = field(default_factory=list)

    def add(self, lineage: SnapshotLineage) -> None:
        self.edges.append(lineage)

    def all(self) -> tuple[SnapshotLineage, ...]:
        return tuple(self.edges)
