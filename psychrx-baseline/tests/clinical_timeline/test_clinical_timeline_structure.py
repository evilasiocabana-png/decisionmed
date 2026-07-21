import unittest
from pathlib import Path

from clinical_timeline import TimelineCoordinator
from clinical_timeline.audit import TimelineAudit, TimelineAuditEntry, TimelineReplay
from clinical_timeline.export import TimelineExporter
from clinical_timeline.index import TimelineCache, TimelineIndex
from clinical_timeline.navigation import CurrentStateResolver, TimelineComparator, TimelineNavigator
from clinical_timeline.transition import TransitionClassification, TransitionSummaryBuilder
from clinical_timeline.widget import TimelineSnapshotNavigation, TimelineWidgetContract


class ClinicalTimelineStructureTest(unittest.TestCase):
    def test_package_structure_exists(self) -> None:
        for dirname in ["coordinator", "builder", "navigator", "comparator", "transition", "index", "export", "audit", "models", "navigation", "widget", "integration", "validator"]:
            with self.subTest(dirname=dirname):
                self.assertTrue((Path("clinical_timeline") / dirname).exists())

    def test_coordinator_builds_timeline_without_mutating_snapshots(self) -> None:
        snapshots = (
            {"snapshot_id": "SNP-1", "timestamp": "2026-01-01", "version": {"major": 0, "minor": 1, "patch": 0}, "trace_id": "T1"},
            {"snapshot_id": "SNP-2", "timestamp": "2026-01-02", "version": {"major": 0, "minor": 1, "patch": 1}, "trace_id": "T2"},
        )
        timeline, validation = TimelineCoordinator().execute(snapshots)

        self.assertTrue(timeline.timeline_id.startswith("TML-"))
        self.assertEqual(len(timeline.snapshots), 2)
        self.assertEqual(len(timeline.transitions), 1)
        self.assertTrue(validation.valid)
        self.assertEqual(snapshots[0]["snapshot_id"], "SNP-1")

    def test_navigation_export_index_cache_audit_and_replay_are_structural(self) -> None:
        timeline, _ = TimelineCoordinator().execute((
            {"snapshot_id": "SNP-1", "timestamp": "2026-01-01", "version": {"major": 0, "minor": 1, "patch": 0}, "trace_id": "T1"},
        ))
        navigator = TimelineNavigator()
        index = TimelineIndex()
        cache = TimelineCache()
        audit = TimelineAudit()

        index.add(timeline)
        cache.put(timeline)
        audit.record(TimelineAuditEntry(event="ClinicalTimelineCreated", timeline_id=timeline.timeline_id))

        self.assertEqual(navigator.first(timeline).snapshot_id, "SNP-1")
        self.assertEqual(CurrentStateResolver().resolve(timeline).snapshot_id, "SNP-1")
        self.assertEqual(index.lookup(timeline.timeline_id), timeline)
        self.assertEqual(cache.get(timeline.timeline_id, timeline.version), timeline)
        self.assertEqual(TimelineReplay(timeline).replay(), timeline)
        self.assertIn("timeline_id", TimelineExporter().audit_json(timeline))
        self.assertIn("Safety", TransitionClassification.categories)
        self.assertIn("Clinical Snapshot", TimelineSnapshotNavigation().links())
        self.assertEqual(TimelineWidgetContract().to_dict()["state"], "read-only")
        self.assertEqual(audit.snapshot()[0].event, "ClinicalTimelineCreated")
        self.assertEqual(TransitionSummaryBuilder().build(timeline.transitions).text, "Timeline summary is descriptive and non-interpretive.")
        self.assertEqual(TimelineComparator().compare(timeline.snapshots[0], timeline.snapshots[0]).change_type, "unchanged")

    def test_timeline_does_not_prescribe_or_replace_record(self) -> None:
        timeline, _ = TimelineCoordinator().execute(())
        payload = str(timeline.to_dict()).lower()

        self.assertNotIn("dose recomendada", payload)
        self.assertNotIn("prescrever", payload)
        self.assertNotIn("prontuario oficial", payload)


if __name__ == "__main__":
    unittest.main()
