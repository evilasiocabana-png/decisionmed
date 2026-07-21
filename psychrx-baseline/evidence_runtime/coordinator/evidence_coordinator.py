"""Evidence Runtime coordinator."""

from __future__ import annotations

from evidence_runtime.audit import EvidenceAudit, EvidenceAuditEntry
from evidence_runtime.citation import CitationEngine
from evidence_runtime.models import EvidenceRequest, EvidenceResult
from evidence_runtime.ranking import EvidenceRanking
from evidence_runtime.registry import EvidenceRegistry
from evidence_runtime.resolver import EvidenceResolver, EvidenceVersionResolver
from evidence_runtime.selector import EvidenceSelector
from evidence_runtime.snapshot import EvidenceSnapshotBuilder


class EvidenceCoordinator:
    """Coordinates evidence retrieval without interpreting scientific content."""

    def __init__(self, registry: EvidenceRegistry | None = None) -> None:
        self.registry = registry or EvidenceRegistry()
        self.resolver = EvidenceResolver(self.registry)
        self.version_resolver = EvidenceVersionResolver()
        self.selector = EvidenceSelector()
        self.ranking = EvidenceRanking()
        self.citation_engine = CitationEngine()
        self.snapshot_builder = EvidenceSnapshotBuilder()
        self.audit = EvidenceAudit()

    def execute(self, request: EvidenceRequest | None = None) -> EvidenceResult:
        active_request = request or EvidenceRequest(status="")
        candidates = self.resolver.resolve(active_request)
        versioned = self.version_resolver.resolve(candidates, active_request.version)
        selected = self.selector.select(versioned, active_request)
        ranked = self.ranking.rank(selected)
        discarded = tuple(item for item in versioned if item not in selected)
        citations = self.citation_engine.build(ranked)
        snapshot = self.snapshot_builder.build(
            selected=ranked,
            discarded=discarded,
            citations=citations,
            version_policy=active_request.version,
        )
        result = EvidenceResult(
            status="completed_read_only",
            query=active_request,
            selected_evidence=ranked,
            discarded_evidence=discarded,
            ranking=self.ranking.explanation(),
            sources=tuple(item.source for item in ranked if item.source is not None),
            citations=citations,
            snapshot=snapshot,
        )
        self.audit.record(
            EvidenceAuditEntry(
                event="EvidenceResolutionFinished",
                query=active_request.to_dict(),
                selected_evidence=tuple(item.evidence_id for item in ranked),
                discarded_evidence=tuple(item.evidence_id for item in discarded),
                versions=tuple(item.metadata.version for item in versioned),
                trace_id=result.trace_id,
            )
        )
        return result
