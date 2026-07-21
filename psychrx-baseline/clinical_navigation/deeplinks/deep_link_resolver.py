"""Deep link resolver."""

from __future__ import annotations

from clinical_navigation.models import DeepLink, NavigationRoute


class DeepLinkResolver:
    supported = (
        "Snapshot",
        "Hypothesis",
        "Evidence",
        "Safety Alert",
        "Explanation",
        "Timeline Event",
        "Runtime Trace",
    )

    def resolve(self, target_type: str, target_id: str) -> DeepLink:
        return DeepLink(
            target_type=target_type,
            target_id=target_id,
            route=NavigationRoute(source="DeepLink", target=target_type, artifact_id=target_id, valid=target_type in self.supported),
        )
