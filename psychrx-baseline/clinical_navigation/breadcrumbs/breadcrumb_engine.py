"""Breadcrumb engine."""

from __future__ import annotations

from clinical_navigation.models import Breadcrumb, NavigationRoute


class BreadcrumbEngine:
    """Builds contextual breadcrumb trails without UI rendering."""

    def build(self, routes: tuple[NavigationRoute, ...]) -> tuple[Breadcrumb, ...]:
        return tuple(Breadcrumb(label=route.target, route=route) for route in routes)
