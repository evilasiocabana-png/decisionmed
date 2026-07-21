"""Knowledge Layer adapter boundary for Evidence Runtime."""

from __future__ import annotations


class KnowledgeEvidenceAdapter:
    """Documents one-way dependency: Evidence Runtime may reference Knowledge."""

    def available_sections(self) -> tuple[str, ...]:
        return (
            "guidelines",
            "drug_models",
            "evidence_sources",
            "references",
            "validation",
        )
