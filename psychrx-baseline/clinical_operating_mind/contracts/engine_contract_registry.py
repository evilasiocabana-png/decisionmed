"""Registry and validator for engine contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from clinical_operating_mind.models import OperatingMindContract


@dataclass(frozen=True)
class EngineContract:
    name: str
    input_keys: tuple[str, ...]
    output_keys: tuple[str, ...]
    version: str = "1.0"
    immutable_upstream: bool = True
    trace_required: bool = True
    failure_behavior: str = "return_structured_error"

    def to_operating_contract(self) -> OperatingMindContract:
        return OperatingMindContract(
            engine=self.name,
            input_contract=self.input_keys,
            output_contract=self.output_keys,
            immutable_upstream=self.immutable_upstream,
            trace_required=self.trace_required,
            failure_behavior=self.failure_behavior,
        )


class EngineContractRegistry:
    """Stores official structural contracts for the engine sequence."""

    def __init__(self) -> None:
        self._contracts = {
            "Runtime": EngineContract("Runtime", ("context",), ("session", "result")),
            "Safety": EngineContract("Safety", ("runtime_context",), ("status", "trace_id")),
            "Evidence": EngineContract("Evidence", ("runtime_context",), ("status", "trace_id")),
            "Optimization": EngineContract(
                "Optimization",
                ("runtime_context", "safety_result", "evidence_result"),
                ("status", "trace_id", "hypotheses"),
            ),
            "Explanation": EngineContract(
                "Explanation",
                ("runtime_result", "safety_result", "evidence_result", "optimization_result"),
                ("status", "trace"),
            ),
            "Snapshot": EngineContract(
                "Snapshot",
                ("safety_result", "evidence_result", "optimization_result", "explanation_result"),
                ("snapshot_id", "trace_id"),
            ),
            "Timeline": EngineContract("Timeline", ("clinical_snapshot",), ("timeline_id", "trace_id")),
            "Navigation": EngineContract("Navigation", ("workspace_context",), ("navigation_id", "trace_id")),
        }

    def all(self) -> tuple[EngineContract, ...]:
        return tuple(self._contracts.values())

    def operating_contracts(self) -> tuple[OperatingMindContract, ...]:
        return tuple(contract.to_operating_contract() for contract in self.all())

    def validate_payload(self, engine: str, payload: Mapping[str, object]) -> tuple[str, ...]:
        contract = self._contracts[engine]
        errors = [f"missing_input:{key}" for key in contract.input_keys if key not in payload]
        if contract.trace_required and payload.get("trace_id") == "":
            errors.append("missing_trace")
        return tuple(errors)

