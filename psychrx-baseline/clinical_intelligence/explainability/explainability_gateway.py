"""Explainability gateway."""

from __future__ import annotations


class ExplainabilityGateway:
    def explain(self, output: str, trace: str, references: tuple[str, ...], limitations: tuple[str, ...]) -> tuple[str, ...]:
        return (
            f"output:{output}",
            f"trace:{trace}",
            f"references:{len(references)}",
            f"limitations:{len(limitations)}",
        )

