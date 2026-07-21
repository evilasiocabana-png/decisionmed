"""Structural model for scientific evidence without evidence content."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from knowledge.core.knowledge_object import KnowledgeObject


class EvidenceQuality(StrEnum):
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    VERY_LOW = "very_low"
    UNRATED = "unrated"


@dataclass(frozen=True)
class EvidenceModel(KnowledgeObject):
    evidence_type: str = ""
    study_design: str = ""
    population: str = ""
    quality: EvidenceQuality = EvidenceQuality.UNRATED
    strength: str = ""
    limitations: tuple[str, ...] = ()
    applicability: str = ""
