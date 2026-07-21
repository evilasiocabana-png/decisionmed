"""Semantic version manager."""

from __future__ import annotations

from knowledge_governance_platform.models import SemanticVersion


class SemanticVersionManager:
    def create(self, major: int = 0, minor: int = 1, patch: int = 0, breaking: bool = False) -> SemanticVersion:
        return SemanticVersion(major=major, minor=minor, patch=patch, breaking_change=breaking)

