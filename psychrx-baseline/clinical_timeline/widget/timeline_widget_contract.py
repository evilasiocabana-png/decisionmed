"""Clinical Timeline Widget contract."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class TimelineWidgetContract:
    id: str = "clinical-timeline-widget"
    title: str = "Clinical Timeline"
    priority: int = 0
    state: str = "read-only"
    context: str = "clinical_workspace"
    dependencies: tuple[str, ...] = field(default_factory=lambda: ("ClinicalSnapshot",))
    actions: tuple[str, ...] = field(default_factory=tuple)
    explanation: str = "Read-only timeline navigation over immutable snapshots."
    visibility: str = "visible"
    permissions: tuple[str, ...] = field(default_factory=lambda: ("read",))

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
