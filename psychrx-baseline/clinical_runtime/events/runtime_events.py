"""Official structural runtime event names."""


def default_runtime_events() -> tuple[str, ...]:
    return (
        "PatientLoaded",
        "WidgetStarted",
        "WidgetCompleted",
        "KernelExecuted",
        "ReasoningExecuted",
        "SafetyDetected",
        "EvidenceLoaded",
        "SnapshotUpdated",
        "RuntimeFinished",
    )
