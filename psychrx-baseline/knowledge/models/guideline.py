"""Structural model for clinical guidelines without guideline content."""

from __future__ import annotations

from dataclasses import dataclass

from knowledge.core.knowledge_object import KnowledgeObject


@dataclass(frozen=True)
class GuidelineSection:
    title: str
    summary: str = ""
    references: tuple[str, ...] = ()


@dataclass(frozen=True)
class GuidelineRecommendation:
    label: str
    strength: str
    evidence_level: str
    references: tuple[str, ...] = ()


@dataclass(frozen=True)
class GuidelineModel(KnowledgeObject):
    """Schema-level representation of a guideline.

    Instances must not contain imported guideline content until the knowledge
    population sprint explicitly authorizes it.
    """

    issuing_body: str = ""
    publication_year: int | None = None
    sections: tuple[GuidelineSection, ...] = ()
    recommendations: tuple[GuidelineRecommendation, ...] = ()
