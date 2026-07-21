"""Route resolver for internal clinical artifacts."""

from __future__ import annotations

from clinical_navigation.models import NavigationRoute


class RouteResolver:
    allowed_targets = (
        "Workspace",
        "Snapshot",
        "Timeline",
        "Safety",
        "Evidence",
        "Hypotheses",
        "Explanation",
        "Runtime Trace",
    )

    def resolve(self, source: str, target: str, artifact_id: str = "") -> NavigationRoute:
        return NavigationRoute(
            source=source,
            target=target,
            artifact_id=artifact_id,
            valid=target in self.allowed_targets,
        )
