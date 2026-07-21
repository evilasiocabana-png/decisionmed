"""Initial SSRI metadata-only registry and catalog."""

from scientific_knowledge.psychopharmacology.contracts import DrugMetadata, DrugPackageContract


_SSRI_NAMES = (
    "Fluoxetine",
    "Sertraline",
    "Paroxetine",
    "Citalopram",
    "Escitalopram",
    "Fluvoxamine",
)


def create_initial_ssri_registry() -> tuple[DrugMetadata, ...]:
    return tuple(
        DrugMetadata(
            identifier=f"DRG-SSRI-{index:03d}",
            generic_name=name,
            semantic_id=f"SEM-DRG-SSRI-{name.upper()}",
            knowledge_id=f"KNW-DRG-SSRI-{index:03d}",
            review_status="registered",
            publication_status="not_populated",
            validation_status="not_validated",
        )
        for index, name in enumerate(_SSRI_NAMES, start=1)
    )


def create_initial_ssri_catalog() -> dict[str, object]:
    registry = create_initial_ssri_registry()
    return {
        "catalog_id": "OSKB-SSRI-CATALOG-0.1",
        "class": "SSRIs",
        "status": "registered_not_populated",
        "entries": registry,
        "ready_for_scientific_population": True,
        "contains_scientific_content": False,
    }


def create_ssri_package_contract() -> DrugPackageContract:
    return DrugPackageContract(
        package_id="OSKB-SSRI-PACKAGE-0.1",
        package_name="SSRIs Package",
        drug_metadata=create_initial_ssri_registry(),
        validation_status="not_validated",
        publication_status="not_populated",
        ontology_mapping=("Drug", "Mechanism", "Receptor", "Interaction", "Monitoring", "Evidence", "Guideline"),
    )

