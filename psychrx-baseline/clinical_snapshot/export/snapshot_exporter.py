"""Snapshot exporter."""

from __future__ import annotations

from clinical_snapshot.models import ClinicalSnapshot


class SnapshotExporter:
    """Exports internal representations without external libraries."""

    def internal_json(self, snapshot: ClinicalSnapshot) -> dict[str, object]:
        return snapshot.to_dict()

    def developer_json(self, snapshot: ClinicalSnapshot) -> dict[str, object]:
        return {"snapshot": snapshot.to_dict(), "developer": True}

    def audit_json(self, snapshot: ClinicalSnapshot) -> dict[str, object]:
        return {"snapshot_id": snapshot.snapshot_id, "trace_id": snapshot.trace_id}

    def future_fhir_placeholder(self) -> dict[str, str]:
        return {"status": "future_adapter_placeholder"}
