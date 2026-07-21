"""Version primitives for structured PsychRx knowledge."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True, order=True)
class KnowledgeVersion:
    """Semantic version for a knowledge object."""

    major: int
    minor: int = 0
    patch: int = 0

    def __post_init__(self) -> None:
        for part_name, value in (
            ("major", self.major),
            ("minor", self.minor),
            ("patch", self.patch),
        ):
            if value < 0:
                raise ValueError(f"{part_name} must be non-negative")

    @classmethod
    def parse(cls, value: str) -> "KnowledgeVersion":
        parts = value.split(".")
        if len(parts) != 3:
            raise ValueError("knowledge version must use major.minor.patch")
        return cls(*(int(part) for part in parts))

    def bump_major(self) -> "KnowledgeVersion":
        return KnowledgeVersion(self.major + 1, 0, 0)

    def bump_minor(self) -> "KnowledgeVersion":
        return KnowledgeVersion(self.major, self.minor + 1, 0)

    def bump_patch(self) -> "KnowledgeVersion":
        return KnowledgeVersion(self.major, self.minor, self.patch + 1)

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


@dataclass(frozen=True)
class VersionRecord:
    """Audit-friendly record of a knowledge version change."""

    version: KnowledgeVersion
    reason: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not self.reason.strip():
            raise ValueError("version record reason is required")


@dataclass(frozen=True)
class VersionHistory:
    """Ordered history for a knowledge object."""

    records: tuple[VersionRecord, ...] = ()

    def append(self, record: VersionRecord) -> "VersionHistory":
        if self.records and record.version <= self.records[-1].version:
            raise ValueError("new version must be greater than current version")
        return VersionHistory(self.records + (record,))

    @property
    def current(self) -> KnowledgeVersion | None:
        if not self.records:
            return None
        return self.records[-1].version
