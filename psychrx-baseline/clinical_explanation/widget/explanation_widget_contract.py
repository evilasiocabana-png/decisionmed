"""Clinical Explanation Widget contract."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class ExplanationWidgetContract:
    id: str = "clinical-explanation-widget"
    title: str = "Clinical Explanation"
    priority: int = 0
    state: str = "read-only"
    context: str = "clinical_workspace"
    dependencies: tuple[str, ...] = field(default_factory=lambda: ("Runtime", "Safety", "Evidence", "Optimization"))
    actions: tuple[str, ...] = field(default_factory=tuple)
    explanation: str = "Read-only explanation panel."
    visibility: str = "visible"
    permissions: tuple[str, ...] = field(default_factory=lambda: ("read",))

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
