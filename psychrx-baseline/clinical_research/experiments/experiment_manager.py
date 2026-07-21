"""Experiment manager."""

from __future__ import annotations

from clinical_research.models import ResearchExperiment


class ExperimentManager:
    """Registers research experiments without clinical execution."""

    def __init__(self) -> None:
        self._experiments: dict[str, ResearchExperiment] = {}

    def register(self, experiment: ResearchExperiment) -> ResearchExperiment:
        self._experiments[experiment.experiment_id] = experiment
        return experiment

    def all(self) -> tuple[ResearchExperiment, ...]:
        return tuple(self._experiments.values())

