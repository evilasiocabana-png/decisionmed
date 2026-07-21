"""Explanation section composer."""

from __future__ import annotations

from clinical_explanation.models import ExplanationNode, ExplanationSection


class ExplanationComposer:
    """Composes explanation sections in the official order."""

    order = (
        ("clinical-context", "Clinical context used"),
        ("safety-findings", "Safety findings"),
        ("evidence-used", "Evidence used"),
        ("strategies-considered", "Strategies considered"),
        ("hypotheses-generated", "Hypotheses generated"),
        ("main-limitations", "Main limitations"),
        ("trace-summary", "Trace summary"),
    )

    def compose(self, nodes: tuple[ExplanationNode, ...]) -> tuple[ExplanationSection, ...]:
        return tuple(
            ExplanationSection(section_id=section_id, title=title, nodes=nodes)
            for section_id, title in self.order
        )
