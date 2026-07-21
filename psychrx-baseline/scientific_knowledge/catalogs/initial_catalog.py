"""Initial metadata-only catalogs.

The catalogs intentionally avoid drug content and therapeutic rules.
"""

from scientific_knowledge.models import KnowledgePackageRegistryEntry


def create_empty_drug_catalog() -> dict[str, object]:
    return {
        "catalog_id": "OSKB-DRUG-CATALOG-0.1",
        "status": "empty_metadata_only",
        "entries": (),
        "allows_clinical_content": False,
    }


def create_guideline_source_catalog() -> tuple[dict[str, str], ...]:
    sources = (
        "APA",
        "CANMAT",
        "NICE",
        "WFSBP",
        "ABP",
        "Maudsley",
        "Stahl",
        "Ministerio da Saude",
        "ANVISA",
        "FDA",
        "EMA",
        "Cochrane",
        "PubMed",
    )
    return tuple({"source": source, "status": "metadata_only"} for source in sources)


def create_package_registry_baseline() -> tuple[KnowledgePackageRegistryEntry, ...]:
    return (
        KnowledgePackageRegistryEntry(
            package_id="OSKB-DRUGS-0.1",
            package_type="drug_catalog",
            status="empty_metadata_only",
        ),
        KnowledgePackageRegistryEntry(
            package_id="OSKB-GUIDELINES-0.1",
            package_type="guideline_catalog",
            status="metadata_only",
        ),
    )

