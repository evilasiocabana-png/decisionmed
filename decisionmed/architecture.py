"""Static dependency checks for DecisionMEd's protected layers.

The scanner parses source files without importing or executing application code.
It exists to make the dependency rules in the PsychRx blueprint executable in CI.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path


PROTECTED_LAYERS = ("domain", "evidence", "knowledge", "safety", "audit")

ALLOWED_DEPENDENCIES: dict[str, frozenset[str]] = {
    "domain": frozenset(),
    "evidence": frozenset(),
    "knowledge": frozenset({"evidence"}),
    "safety": frozenset({"domain", "evidence", "knowledge"}),
    "audit": frozenset({"domain"}),
}


@dataclass(frozen=True, slots=True)
class BoundaryViolation:
    """One forbidden dependency found in a protected layer."""

    file: str
    line: int
    source_layer: str
    target_layer: str
    import_name: str


def scan_architecture(package_root: Path) -> tuple[BoundaryViolation, ...]:
    """Return all forbidden DecisionMEd imports under ``package_root``."""

    package_root = package_root.resolve()
    if not package_root.is_dir():
        raise FileNotFoundError(f"package root not found: {package_root}")

    package_name = package_root.name
    violations: list[BoundaryViolation] = []

    for source_layer in PROTECTED_LAYERS:
        layer_root = package_root / source_layer
        if not layer_root.is_dir():
            continue
        for source_file in sorted(layer_root.rglob("*.py")):
            module_name = _module_name(package_root, source_file)
            tree = ast.parse(
                source_file.read_text(encoding="utf-8"), filename=str(source_file)
            )
            for line, import_name in _decisionmed_imports(
                tree, module_name, source_file.name == "__init__.py", package_name
            ):
                target_layer = _target_layer(import_name, package_name)
                if target_layer is None or target_layer == source_layer:
                    continue
                if target_layer not in ALLOWED_DEPENDENCIES[source_layer]:
                    violations.append(
                        BoundaryViolation(
                            file=source_file.relative_to(package_root.parent).as_posix(),
                            line=line,
                            source_layer=source_layer,
                            target_layer=target_layer,
                            import_name=import_name,
                        )
                    )

    return tuple(
        sorted(violations, key=lambda item: (item.file, item.line, item.import_name))
    )


def _module_name(package_root: Path, source_file: Path) -> str:
    relative = source_file.relative_to(package_root).with_suffix("")
    parts = list(relative.parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join((package_root.name, *parts))


def _decisionmed_imports(
    tree: ast.AST,
    module_name: str,
    is_package: bool,
    package_name: str,
) -> tuple[tuple[int, str], ...]:
    imports: list[tuple[int, str]] = []
    current_package = module_name if is_package else module_name.rpartition(".")[0]

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == package_name or alias.name.startswith(f"{package_name}."):
                    imports.append((node.lineno, alias.name))
        elif isinstance(node, ast.ImportFrom):
            import_name = _resolve_from_import(node, current_package)
            if import_name == package_name or import_name.startswith(f"{package_name}."):
                imports.append((node.lineno, import_name))

    return tuple(imports)


def _resolve_from_import(node: ast.ImportFrom, current_package: str) -> str:
    if node.level == 0:
        return node.module or ""

    parts = current_package.split(".")
    parents_to_remove = node.level - 1
    if parents_to_remove >= len(parts):
        return node.module or ""
    base = parts[: len(parts) - parents_to_remove]
    if node.module:
        base.extend(node.module.split("."))
    return ".".join(base)


def _target_layer(import_name: str, package_name: str) -> str | None:
    parts = import_name.split(".")
    if not parts or parts[0] != package_name:
        return None
    return parts[1] if len(parts) > 1 else "root"
