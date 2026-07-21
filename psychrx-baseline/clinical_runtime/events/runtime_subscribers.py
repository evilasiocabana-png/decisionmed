"""Internal runtime subscribers."""

from __future__ import annotations

from dataclasses import dataclass, field

from clinical_runtime.events.runtime_event_bus import RuntimeEvent


@dataclass
class RuntimeSubscribers:
    """Captures internal subscriber events for logger/audit/trace/workspace/store."""

    logger: list[RuntimeEvent] = field(default_factory=list)
    audit: list[RuntimeEvent] = field(default_factory=list)
    trace: list[RuntimeEvent] = field(default_factory=list)
    workspace: list[RuntimeEvent] = field(default_factory=list)
    store: list[RuntimeEvent] = field(default_factory=list)

    def capture_all(self, event: RuntimeEvent) -> None:
        self.logger.append(event)
        self.audit.append(event)
        self.trace.append(event)
        self.workspace.append(event)
        self.store.append(event)
