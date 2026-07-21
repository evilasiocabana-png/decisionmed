"""Compatibility analyzer."""

from __future__ import annotations

from knowledge_governance_platform.models import SemanticVersion


class CompatibilityAnalyzer:
    def compatible(self, current: SemanticVersion, target: SemanticVersion) -> tuple[bool, str]:
        if current.major != target.major:
            return False, "major_version_mismatch"
        if target.breaking_change:
            return False, "breaking_change"
        return True, "compatible"

