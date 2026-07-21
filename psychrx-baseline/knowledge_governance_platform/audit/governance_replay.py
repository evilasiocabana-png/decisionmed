"""Read-only governance replay."""

from __future__ import annotations

from knowledge_governance_platform.models import KnowledgeGovernanceResult


class GovernanceReplay:
    def replay(self, result: KnowledgeGovernanceResult) -> KnowledgeGovernanceResult:
        return result

