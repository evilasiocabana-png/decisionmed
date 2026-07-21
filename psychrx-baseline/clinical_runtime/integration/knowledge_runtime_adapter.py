"""Runtime to Knowledge Library adapter."""

from __future__ import annotations

from pathlib import Path


class KnowledgeRuntimeAdapter:
    """Loads structural knowledge files on demand without hardcoded medical content."""

    def list_available_sections(self) -> tuple[str, ...]:
        root = Path("knowledge_library")
        if not root.exists():
            return ()
        return tuple(sorted(path.name for path in root.iterdir() if path.is_dir()))
