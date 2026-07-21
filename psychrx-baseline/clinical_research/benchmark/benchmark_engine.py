"""Benchmark engine."""

from __future__ import annotations

from clinical_research.models import BenchmarkResult


class BenchmarkEngine:
    """Benchmarks structures, not patient outcomes."""

    def run(self, measured_items: tuple[str, ...] = ()) -> BenchmarkResult:
        return BenchmarkResult(measured_items=measured_items or ("architecture", "contract", "quality"))

