"""Confidence metadata registry."""

from __future__ import annotations


class ConfidenceRegistry:
    def metadata(self) -> tuple[str, ...]:
        return (
            "confidence_level:structural",
            "uncertainty:declared",
            "missing_information:tracked",
            "quality_dependencies:required",
            "clinical_confidence_scoring:not_available",
        )

