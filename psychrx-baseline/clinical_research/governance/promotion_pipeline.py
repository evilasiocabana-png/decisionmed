"""Promotion pipeline."""

from __future__ import annotations


class PromotionPipeline:
    STAGES = ("Experimental", "Validation", "Architecture Review", "Governance Review", "Approved", "Integrated")

    def stages(self) -> tuple[str, ...]:
        return self.STAGES

