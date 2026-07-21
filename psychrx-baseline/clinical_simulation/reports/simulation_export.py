"""Simulation export."""

from __future__ import annotations

from clinical_simulation.models import SimulationReport


class SimulationExport:
    ALLOWED = ("internal_json", "developer_json", "research_json")

    def export(self, report: SimulationReport, format_name: str) -> tuple[str, str]:
        if format_name not in self.ALLOWED:
            return ("rejected", "production_export_not_allowed")
        return ("exported", report.report_id)

