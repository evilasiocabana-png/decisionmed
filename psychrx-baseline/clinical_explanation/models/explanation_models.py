"""Typed models for safe clinical explanations."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class ExplanationAudience:
    name: str = "clinician"


@dataclass(frozen=True)
class ExplanationLevel:
    name: str = "summary"


@dataclass(frozen=True)
class ExplanationTrace:
    trace_id: str = field(default_factory=lambda: f"EXP-TRC-{uuid4()}")
    runtime_trace_id: str = "not_bound"
    safety_trace_id: str = "not_applicable"
    evidence_trace_id: str = "not_applicable"
    optimization_trace_id: str = "not_applicable"
    knowledge_version: str = "not_bound"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExplanationReference:
    reference_id: str
    citation_id: str = ""
    evidence_version: str = ""
    source_type: str = ""
    selection_reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExplanationSource:
    source_id: str
    source_type: str
    trace: ExplanationTrace = field(default_factory=ExplanationTrace)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExplanationWarning:
    category: str
    message: str
    trace: ExplanationTrace = field(default_factory=ExplanationTrace)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExplanationNode:
    node_id: str
    title: str
    text: str
    source: ExplanationSource
    references: tuple[ExplanationReference, ...] = field(default_factory=tuple)
    warnings: tuple[ExplanationWarning, ...] = field(default_factory=tuple)
    trace: ExplanationTrace = field(default_factory=ExplanationTrace)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExplanationSection:
    section_id: str
    title: str
    nodes: tuple[ExplanationNode, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ClinicalExplanationResult:
    status: str
    sections: tuple[ExplanationSection, ...] = field(default_factory=tuple)
    warnings: tuple[ExplanationWarning, ...] = field(default_factory=tuple)
    audience: ExplanationAudience = field(default_factory=ExplanationAudience)
    level: ExplanationLevel = field(default_factory=ExplanationLevel)
    trace: ExplanationTrace = field(default_factory=ExplanationTrace)
    readable_text: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
