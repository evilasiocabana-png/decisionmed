"""Policy registry."""

from __future__ import annotations


class PolicyRegistry:
    POLICIES = (
        "security",
        "immutability",
        "traceability",
        "scientific validation",
        "knowledge governance",
        "quality compliance",
    )

    def all(self) -> tuple[str, ...]:
        return self.POLICIES

