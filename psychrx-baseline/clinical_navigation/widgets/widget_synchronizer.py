"""Widget synchronizer."""

from __future__ import annotations


class WidgetSynchronizer:
    """Computes related widgets without circular updates."""

    def related_widgets(self, selected_widget: str) -> tuple[str, ...]:
        mapping = {
            "Timeline": ("Snapshot", "Evidence", "Safety", "Explanation"),
            "Snapshot": ("Timeline", "Evidence", "Safety", "Explanation"),
            "Evidence": ("Snapshot", "Hypotheses", "Explanation"),
            "Safety": ("Snapshot", "Hypotheses", "Explanation"),
            "Hypotheses": ("Evidence", "Safety", "Explanation", "Runtime Trace"),
        }
        return mapping.get(selected_widget, ())
