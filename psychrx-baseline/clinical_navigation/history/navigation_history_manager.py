"""Navigation history manager."""

from __future__ import annotations

from clinical_navigation.models import NavigationHistory, NavigationRoute


class NavigationHistoryManager:
    def push(self, history: NavigationHistory, route: NavigationRoute) -> NavigationHistory:
        return history.push(route)

    def back(self, history: NavigationHistory) -> NavigationHistory:
        return history.back()

    def forward(self, history: NavigationHistory) -> NavigationHistory:
        return history.forward()

    def jump(self, history: NavigationHistory, cursor: int) -> NavigationHistory:
        if 0 <= cursor < len(history.entries):
            return NavigationHistory(entries=history.entries, cursor=cursor)
        return history

    def restore(self, entries: tuple[NavigationRoute, ...]) -> NavigationHistory:
        return NavigationHistory(entries=entries, cursor=len(entries) - 1)

    def clear(self) -> NavigationHistory:
        return NavigationHistory()
