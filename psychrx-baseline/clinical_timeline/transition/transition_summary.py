"""Transition summaries."""

from __future__ import annotations

from clinical_timeline.models import TimelineSummary, TimelineTransition


class TransitionSummaryBuilder:
    """Builds descriptive, non-recommendation summaries."""

    def build(self, transitions: tuple[TimelineTransition, ...]) -> TimelineSummary:
        return TimelineSummary(
            transition_summaries=tuple(transition.summary for transition in transitions)
        )
