import unittest
from pathlib import Path

from clinical_snapshot import SnapshotCoordinator
from clinical_snapshot.audit import SnapshotAudit, SnapshotAuditEntry, SnapshotReplay
from clinical_snapshot.diff import ChangeClassification, SnapshotDiffEngine
from clinical_snapshot.export import SnapshotExporter
from clinical_snapshot.index import SnapshotCache, SnapshotIndex
from clinical_snapshot.summary import SnapshotSummaryBuilder
from clinical_snapshot.versioning import SnapshotIdentifier, SnapshotLineage, SnapshotLineageGraph, SnapshotVersionManager
from clinical_snapshot.widget import SnapshotNavigation, SnapshotWidgetContract


class ClinicalSnapshotStructureTest(unittest.TestCase):
    def test_package_structure_exists(self) -> None:
        for dirname in ["coordinator", "builder", "validator", "versioning", "diff", "index", "export", "audit", "models", "widget", "summary", "integration"]:
            with self.subTest(dirname=dirname):
                self.assertTrue((Path("clinical_snapshot") / dirname).is_dir())

    def test_coordinator_builds_immutable_structural_snapshot(self) -> None:
        snapshot, validation = SnapshotCoordinator().execute(
            {"session": {"session_id": "RTS-1"}, "result": {"trace_id": "RT"}},
            {"trace_id": "ST", "snapshot": {"alert_count": 0}, "alerts": ()},
            {"trace_id": "EV", "snapshot": {"selected_count": 0}},
            {"trace_id": "OP", "hypotheses": (), "uncertainties": (), "confidence": 0.0},
            {"trace": {"trace_id": "EX"}, "sections": ()},
        )

        self.assertTrue(snapshot.snapshot_id.startswith("SNP-"))
        self.assertEqual(snapshot.runtime_id, "RTS-1")
        self.assertTrue(validation.valid)

    def test_version_diff_index_export_audit_replay_and_widget_are_structural(self) -> None:
        snapshot, _ = SnapshotCoordinator().execute(
            {"session": {}, "result": {}},
            {"snapshot": {}, "alerts": ()},
            {"snapshot": {}},
            {},
            {"trace": {}, "sections": ()},
        )
        version = SnapshotVersionManager().next_patch(snapshot.version)
        lineage = SnapshotLineageGraph()
        index = SnapshotIndex()
        cache = SnapshotCache()
        audit = SnapshotAudit()

        lineage.add(SnapshotLineage(parent_snapshot="A", child_snapshot="B"))
        index.add(snapshot)
        cache.put(snapshot)
        audit.record(SnapshotAuditEntry(event="ClinicalSnapshotCreated", snapshot_id=snapshot.snapshot_id))

        self.assertEqual(version.patch, snapshot.version.patch + 1)
        self.assertEqual(len(lineage.all()), 1)
        self.assertEqual(index.latest(), snapshot)
        self.assertEqual(cache.get(snapshot.snapshot_id, snapshot.version.label()), snapshot)
        self.assertEqual(SnapshotReplay(snapshot).replay(), snapshot)
        self.assertIn("Safety", ChangeClassification.categories)
        self.assertFalse(SnapshotDiffEngine().compare(snapshot, snapshot).changed_safety)
        self.assertIn("snapshot_id", SnapshotExporter().audit_json(snapshot))
        self.assertIn("Snapshot Summary", SnapshotNavigation().links())
        self.assertEqual(SnapshotWidgetContract().to_dict()["state"], "read-only")
        self.assertTrue(SnapshotIdentifier().generate("stable").startswith("SNP-"))
        self.assertIn("Snapshot consolidated", SnapshotSummaryBuilder().build(snapshot).main_findings[0])
        self.assertEqual(audit.snapshot()[0].event, "ClinicalSnapshotCreated")

    def test_snapshot_does_not_prescribe_or_decide(self) -> None:
        snapshot, _ = SnapshotCoordinator().execute({}, {}, {}, {}, {})
        payload = str(snapshot.to_dict()).lower()

        self.assertNotIn("dose recomendada", payload)
        self.assertNotIn("prescrever", payload)
        self.assertNotIn("decisao clinica final", payload)


if __name__ == "__main__":
    unittest.main()
