"""Read-only context broker."""

from __future__ import annotations

from clinical_intelligence.models import IntelligenceContext


class ContextBroker:
    def distribute(self) -> IntelligenceContext:
        return IntelligenceContext(
            snapshot="snapshot-reference",
            timeline="timeline-reference",
            operating_mind="operating-mind-reference",
            quality_result="quality-reference",
            knowledge_version="0.1.0",
            read_only=True,
        )

