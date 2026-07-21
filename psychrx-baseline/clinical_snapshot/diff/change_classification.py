"""Snapshot change categories."""

from __future__ import annotations


class ChangeClassification:
    categories = (
        "Context",
        "Safety",
        "Evidence",
        "Hypothesis",
        "Explanation",
        "Metadata",
        "Trace",
    )
