"""Reference resolver."""

from __future__ import annotations

from clinical_navigation.models import NavigationRoute


class ReferenceResolver:
    """Resolves references to navigation targets only."""

    def resolve(self, reference_type: str, reference_id: str) -> NavigationRoute:
        return NavigationRoute(source="Reference", target=reference_type, artifact_id=reference_id)
