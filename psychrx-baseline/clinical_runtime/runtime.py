"""Clinical Runtime facade."""

from __future__ import annotations

from copy import deepcopy

from clinical_quality.integration import RuntimeQualityAdapter
from clinical_runtime.context import RuntimeContext
from clinical_runtime.events import RuntimeEvent, RuntimeEventBus
from clinical_runtime.pipeline import PipelineStep, RuntimePipeline
from clinical_runtime.session import RuntimeSessionManager
from clinical_runtime.store import RuntimeStore
from clinical_runtime.validator import RuntimeValidator
from clinical_explanation.integration import RuntimeExplanationAdapter
from clinical_navigation.integration import RuntimeNavigationAdapter
from clinical_operating_mind.integration import RuntimeOperatingMindAdapter
from clinical_snapshot.integration import RuntimeSnapshotAdapter
from clinical_timeline.integration import RuntimeTimelineAdapter
from evidence_runtime.integration import RuntimeEvidenceAdapter
from safety_engine.integration import RuntimeSafetyAdapter
from therapeutic_optimization.integration import RuntimeOptimizationAdapter


class ClinicalRuntime:
    """Structural runtime facade. It coordinates, never decides clinically."""

    def __init__(self) -> None:
        self.session_manager = RuntimeSessionManager()
        self.store = RuntimeStore()
        self.validator = RuntimeValidator()
        self.event_bus = RuntimeEventBus()
        self.safety_adapter = RuntimeSafetyAdapter()
        self.evidence_adapter = RuntimeEvidenceAdapter()
        self.optimization_adapter = RuntimeOptimizationAdapter()
        self.explanation_adapter = RuntimeExplanationAdapter()
        self.snapshot_adapter = RuntimeSnapshotAdapter()
        self.timeline_adapter = RuntimeTimelineAdapter()
        self.navigation_adapter = RuntimeNavigationAdapter()
        self.operating_mind_adapter = RuntimeOperatingMindAdapter()
        self.quality_adapter = RuntimeQualityAdapter()

    def execute(self, context: RuntimeContext | None = None) -> dict[str, object]:
        runtime_context = context or RuntimeContext()
        errors = self.validator.validate_context(runtime_context)
        if errors:
            return {"status": "invalid", "errors": tuple(error.code for error in errors)}
        session = self.session_manager.open_session()
        safety_result = self.safety_adapter.evaluate(runtime_context)
        evidence_result = self.evidence_adapter.resolve(runtime_context)
        optimization_result = self.optimization_adapter.optimize(
            runtime_context,
            safety_result.to_dict(),
            evidence_result.to_dict(),
        )
        explanation_input = {
            "status": "structural",
            "result": {"outputs": {"Safety": "structural", "Evidence": "structural", "Optimization": "structural"}},
        }
        explanation_result = self.explanation_adapter.explain(
            explanation_input,
            safety_result.to_dict(),
            evidence_result.to_dict(),
            optimization_result.to_dict(),
        )
        snapshot_runtime_input = {
            "session": session.to_dict(),
            "result": {"trace_id": "runtime-structural"},
        }
        clinical_snapshot = self.snapshot_adapter.build(
            snapshot_runtime_input,
            safety_result.to_dict(),
            evidence_result.to_dict(),
            optimization_result.to_dict(),
            explanation_result.to_dict(),
        )
        clinical_timeline = self.timeline_adapter.build((clinical_snapshot.to_dict(),))
        clinical_navigation = self.navigation_adapter.build_state()
        clinical_operating_mind = self.operating_mind_adapter.coordinate(
            safety_result.to_dict(),
            evidence_result.to_dict(),
            optimization_result.to_dict(),
            explanation_result.to_dict(),
            clinical_snapshot.to_dict(),
            clinical_timeline.to_dict(),
            clinical_navigation.to_dict(),
        )
        quality_payload = {
            "status": "completed_read_only",
            "session": session.to_dict(),
            "safety_result": safety_result.to_dict(),
            "evidence_result": evidence_result.to_dict(),
            "optimization_result": optimization_result.to_dict(),
            "explanation_result": explanation_result.to_dict(),
            "clinical_snapshot": clinical_snapshot.to_dict(),
            "clinical_timeline": clinical_timeline.to_dict(),
            "clinical_navigation": clinical_navigation.to_dict(),
            "clinical_operating_mind": clinical_operating_mind.to_dict(),
            "clinical_decision": "not_implemented",
            "prescription": "not_available",
        }
        clinical_quality = self.quality_adapter.evaluate(deepcopy(quality_payload))
        pipeline = RuntimePipeline(
            (
                PipelineStep("Safety"),
                PipelineStep("Evidence"),
                PipelineStep("Optimization"),
                PipelineStep("Explanation"),
                PipelineStep("Snapshot"),
                PipelineStep("Timeline"),
                PipelineStep("Navigation"),
                PipelineStep("Operating Mind"),
                PipelineStep("Quality"),
                PipelineStep("Kernel"),
                PipelineStep("Knowledge"),
            )
        )
        result = pipeline.run()
        self.event_bus.publish(RuntimeEvent("RuntimeFinished", {"status": result.status}))
        return {
            "status": result.status,
            "session": session.to_dict(),
            "safety_result": safety_result.to_dict(),
            "evidence_result": evidence_result.to_dict(),
            "optimization_result": optimization_result.to_dict(),
            "explanation_result": explanation_result.to_dict(),
            "clinical_snapshot": clinical_snapshot.to_dict(),
            "clinical_timeline": clinical_timeline.to_dict(),
            "clinical_navigation": clinical_navigation.to_dict(),
            "clinical_operating_mind": clinical_operating_mind.to_dict(),
            "clinical_quality": clinical_quality.to_dict(),
            "result": result.to_dict(),
            "clinical_decision": "not_implemented",
            "prescription": "not_available",
        }
