"""Missing data analyzer."""

from __future__ import annotations

from collections.abc import Mapping


class MissingDataAnalyzer:
    """Detects missing inputs without inferring values."""

    REQUIRED = ("clinical_operating_mind", "clinical_snapshot")
    OPTIONAL = ("patient_context", "workspace_context")

    def analyze(self, payload: Mapping[str, object]) -> tuple[str, ...]:
        missing = [f"required:{key}" for key in self.REQUIRED if key not in payload]
        missing.extend(f"optional:{key}" for key in self.OPTIONAL if key not in payload)
        return tuple(missing)

