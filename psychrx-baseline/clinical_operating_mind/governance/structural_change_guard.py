"""ADR guard for structural Clinical Operating Mind changes."""

from __future__ import annotations


class StructuralChangeGuard:
    """Requires ADRs for lifecycle, contract, order or widget contract changes."""

    GUARDED_AREAS = ("lifecycle", "contracts", "engine_order", "widget_contract")

    def validate(self, changed_area: str, adr_reference: str = "") -> tuple[str, ...]:
        if changed_area in self.GUARDED_AREAS and not adr_reference:
            return (f"adr_required:{changed_area}",)
        return ()

