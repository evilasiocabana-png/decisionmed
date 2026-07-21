"""Scenario registry."""

from __future__ import annotations

from clinical_research.models import ResearchScenario


class ScenarioRegistry:
    """Stores reference, synthetic and benchmark scenarios."""

    def scenarios(self) -> tuple[ResearchScenario, ...]:
        return (
            ResearchScenario("SCN-REFERENCE", "reference", "Reference scenario placeholder"),
            ResearchScenario("SCN-BENCHMARK", "benchmark", "Benchmark scenario placeholder"),
        )

