import unittest
from pathlib import Path

from evidence_runtime import EvidenceCoordinator
from evidence_runtime.api import EvidenceRuntimeAPI
from evidence_runtime.audit import EvidenceAudit, EvidenceAuditEntry, EvidenceReplay, EvidenceTrace
from evidence_runtime.cache import EvidenceCache
from evidence_runtime.citation import CitationEngine
from evidence_runtime.models import Evidence, EvidenceMetadata, EvidenceRequest, EvidenceSource
from evidence_runtime.ranking import EvidenceRanking
from evidence_runtime.registry import ConflictRegistry, EvidenceRegistry
from evidence_runtime.registry.conflict_registry import EvidenceConflict
from evidence_runtime.resolver import EvidenceResolver, EvidenceVersionResolver
from evidence_runtime.selector import EvidenceSelector


class EvidenceRuntimeStructureTest(unittest.TestCase):
    def test_evidence_runtime_package_structure_exists(self) -> None:
        required_dirs = [
            "coordinator",
            "resolver",
            "registry",
            "selector",
            "ranking",
            "snapshot",
            "citation",
            "audit",
            "models",
            "api",
            "cache",
            "integration",
        ]

        for dirname in required_dirs:
            with self.subTest(dirname=dirname):
                self.assertTrue((Path("evidence_runtime") / dirname).is_dir())

    def test_coordinator_returns_empty_structural_result_without_real_evidence(self) -> None:
        result = EvidenceCoordinator().execute()

        self.assertEqual(result.status, "completed_read_only")
        self.assertEqual(result.selected_evidence, ())
        self.assertEqual(result.snapshot.selected_count, 0)
        self.assertIn("guideline", result.ranking)

    def test_registry_resolver_selector_ranking_and_citations_are_structural(self) -> None:
        registry = EvidenceRegistry()
        source = EvidenceSource("SRC-001", source_type="guideline", version="v1")
        evidence = Evidence(
            "EVD-001",
            "guideline",
            metadata=EvidenceMetadata(
                title="Structural Evidence",
                version="v1",
                status="validated",
                category="test",
            ),
            source=source,
            scope="general",
        )
        registry.register(evidence)
        request = EvidenceRequest(category="test", scope="general", version="v1", status="validated")

        candidates = EvidenceResolver(registry).resolve(request)
        versioned = EvidenceVersionResolver().resolve(candidates, "v1")
        selected = EvidenceSelector().select(versioned, request)
        ranked = EvidenceRanking().rank(selected)
        citations = CitationEngine().build(ranked)

        self.assertEqual(candidates, (evidence,))
        self.assertEqual(versioned, (evidence,))
        self.assertEqual(selected, (evidence,))
        self.assertEqual(ranked, (evidence,))
        self.assertEqual(citations[0].evidence_id, "EVD-001")

    def test_conflict_audit_trace_replay_api_and_cache_are_structural(self) -> None:
        conflicts = ConflictRegistry()
        audit = EvidenceAudit()
        cache = EvidenceCache()

        conflicts.register(EvidenceConflict("CONFLICT-001", ("EVD-A", "EVD-B")))
        audit.record(EvidenceAuditEntry(event="EvidenceResolutionFinished"))
        cache.put("EVD-001", "v1", {"status": "cached"})

        replayed = EvidenceReplay(audit.snapshot()).replay()
        api_result = EvidenceRuntimeAPI().find()
        trace = EvidenceTrace(version="v1")

        self.assertEqual(len(conflicts.all()), 1)
        self.assertEqual(replayed[0].event, "EvidenceResolutionFinished")
        self.assertEqual(cache.get("EVD-001", "v1")["status"], "cached")
        self.assertEqual(api_result.status, "completed_read_only")
        self.assertTrue(trace.trace_id.startswith("EVD-TRC-"))

    def test_evidence_runtime_does_not_recommend_or_prescribe(self) -> None:
        payload = str(EvidenceCoordinator().execute().to_dict()).lower()

        self.assertNotIn("dose recomendada", payload)
        self.assertNotIn("prescrever", payload)
        self.assertNotIn("estrategia superior", payload)


if __name__ == "__main__":
    unittest.main()
