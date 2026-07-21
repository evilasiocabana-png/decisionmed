"""Official Clinical Operating Mind lifecycle."""

from __future__ import annotations

from clinical_operating_mind.models import (
    OperatingMindLifecycle,
    OperatingMindPhase,
    OperatingMindTransition,
)


class LifecycleDefinition:
    """Defines the mandatory read-only operating sequence."""

    PHASES: tuple[tuple[str, str, str], ...] = (
        ("Context Intake", "Runtime", "Load structural runtime context."),
        ("Safety Evaluation", "Safety", "Evaluate safety before downstream engines."),
        ("Evidence Resolution", "Evidence", "Resolve evidence references before hypotheses."),
        ("Therapeutic Hypothesis Generation", "Optimization", "Build non-prescriptive hypotheses."),
        ("Explanation Assembly", "Explanation", "Assemble traceable explanation."),
        ("Snapshot Creation", "Snapshot", "Create immutable computational snapshot."),
        ("Timeline Update", "Timeline", "Update longitudinal read model."),
        ("Navigation Update", "Navigation", "Expose contextual navigation state."),
    )

    def build(self) -> OperatingMindLifecycle:
        phases = tuple(
            OperatingMindPhase(name=name, order=index, required_engine=engine, purpose=purpose)
            for index, (name, engine, purpose) in enumerate(self.PHASES, start=1)
        )
        transitions = tuple(
            OperatingMindTransition(source=current.name, target=next_phase.name)
            for current, next_phase in zip(phases, phases[1:])
        )
        return OperatingMindLifecycle(phases=phases, transitions=transitions)

