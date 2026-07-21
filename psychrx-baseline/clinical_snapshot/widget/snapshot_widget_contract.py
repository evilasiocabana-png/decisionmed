"""Clinical Snapshot Widget contract."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class SnapshotWidgetContract:
    id: str = "clinical-snapshot-widget"
    title: str = "Clinical Snapshot"
    priority: int = 0
    state: str = "read-only"
    context: str = "clinical_workspace"
    dependencies: tuple[str, ...] = field(default_factory=lambda: ("Runtime", "Safety", "Evidence", "Optimization", "Explanation"))
    actions: tuple[str, ...] = field(default_factory=tuple)
    explanation: str = "Primary read model for Clinical Workspace."
    visibility: str = "visible"
    permissions: tuple[str, ...] = field(default_factory=lambda: ("read",))

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
