"""Metadata-only catalogs for Official Scientific Knowledge Base."""

from scientific_knowledge.catalogs.initial_catalog import (
    create_empty_drug_catalog,
    create_guideline_source_catalog,
    create_package_registry_baseline,
)

__all__ = [
    "create_empty_drug_catalog",
    "create_guideline_source_catalog",
    "create_package_registry_baseline",
]
