"""Official navigation event names."""


def navigation_event_types() -> tuple[str, ...]:
    return (
        "SnapshotSelected",
        "TimelineChanged",
        "EvidenceOpened",
        "SafetyAlertOpened",
        "HypothesisSelected",
        "ExplanationExpanded",
    )
