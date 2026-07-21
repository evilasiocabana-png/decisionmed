"""Navigation replay."""

from __future__ import annotations

from clinical_navigation.models import NavigationHistory


class NavigationReplay:
    """Replays stored navigation history without mutation."""

    def __init__(self, history: NavigationHistory) -> None:
        self._history = history

    def replay(self) -> NavigationHistory:
        return self._history
