"""Timeline snapshot navigation links."""


class TimelineSnapshotNavigation:
    def links(self) -> tuple[str, ...]:
        return ("Clinical Snapshot", "Safety", "Evidence", "Explanation", "Hypotheses", "Runtime Trace")
