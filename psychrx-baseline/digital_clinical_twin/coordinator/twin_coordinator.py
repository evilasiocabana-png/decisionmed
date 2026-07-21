"""Coordinator for Digital Clinical Twin Platform."""

from __future__ import annotations

from digital_clinical_twin.audit import TwinAudit
from digital_clinical_twin.builder import TwinBuilder, TwinValidator
from digital_clinical_twin.evolution import EvolutionEngine
from digital_clinical_twin.models import DigitalClinicalTwin, TwinSummary
from digital_clinical_twin.stability import TwinStabilityAnalyzer


class TwinCoordinator:
    """Coordinates Twin construction without Runtime execution or upstream mutation."""

    def __init__(self) -> None:
        self.builder = TwinBuilder()
        self.validator = TwinValidator()
        self.evolution = EvolutionEngine()
        self.stability = TwinStabilityAnalyzer()
        self.audit = TwinAudit()

    def build_twin(self) -> DigitalClinicalTwin:
        twin = self.builder.build()
        issues = self.validator.validate(twin)
        stability = self.stability.analyze(twin)
        self.audit.record("DigitalClinicalTwinBuilt")
        if issues:
            return twin.with_update(stability_profile=stability + issues)
        return twin.with_update(stability_profile=stability)

    def summarize(self, twin: DigitalClinicalTwin) -> TwinSummary:
        return TwinSummary(
            current_state=twin.current_state.name,
            history=twin.snapshot_history,
            major_transitions=tuple(item.category for item in twin.state_transitions),
            quality_overview=f"quality_events:{len(twin.quality_history)}",
            stability_overview=f"stability_items:{len(twin.stability_profile)}",
        )

