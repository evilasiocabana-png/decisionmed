"""Load and register scientific knowledge packages in memory."""

from scientific_knowledge.models import KnowledgePackage, KnowledgePackageRegistryEntry


class KnowledgePackageRegistry:
    """In-memory registry for scientific package metadata."""

    def __init__(self) -> None:
        self._entries: dict[str, KnowledgePackageRegistryEntry] = {}

    def register(self, entry: KnowledgePackageRegistryEntry) -> None:
        self._entries[entry.package_id] = entry

    def list_entries(self) -> tuple[KnowledgePackageRegistryEntry, ...]:
        return tuple(self._entries.values())

    def get(self, package_id: str) -> KnowledgePackageRegistryEntry | None:
        return self._entries.get(package_id)


class KnowledgePackageLoader:
    """Load packages only after structural dependency checks."""

    def __init__(self, registry: KnowledgePackageRegistry | None = None) -> None:
        self._registry = registry or KnowledgePackageRegistry()

    def load(self, package: KnowledgePackage) -> tuple[str, ...]:
        issues = [dependency for dependency in package.dependencies if self._registry.get(dependency) is None]
        if not issues:
            self._registry.register(
                KnowledgePackageRegistryEntry(
                    package_id=package.package_id,
                    package_type=package.package_type,
                    status=package.publication_status,
                    version=package.version.semantic_version,
                    owner=package.owner,
                    dependencies=package.dependencies,
                    approval="not_approved",
                )
            )
        return tuple(f"missing_dependency:{dependency}" for dependency in issues)

    @property
    def registry(self) -> KnowledgePackageRegistry:
        return self._registry

