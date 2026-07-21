"""Guideline registry."""

from __future__ import annotations

from scientific_validation.models import GuidelineReference


class GuidelineRegistry:
    def __init__(self) -> None:
        self._guidelines: dict[str, GuidelineReference] = {}

    def register(self, guideline: GuidelineReference) -> GuidelineReference:
        self._guidelines[guideline.guideline_id] = guideline
        return guideline

    def all(self) -> tuple[GuidelineReference, ...]:
        return tuple(self._guidelines.values())

