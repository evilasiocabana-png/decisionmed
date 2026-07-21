"""Knowledge version manager."""

from __future__ import annotations


class KnowledgeVersionManager:
    """Creates semantic scientific knowledge versions."""

    def assign(self, major: int = 0, minor: int = 1, patch: int = 0) -> str:
        return f"{major}.{minor}.{patch}"

    def compatible(self, previous: str, current: str) -> bool:
        return previous.split(".")[0] == current.split(".")[0]

