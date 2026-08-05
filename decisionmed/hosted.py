"""Production entry point for the protected DecisionMed internet beta."""

from __future__ import annotations

import os
from pathlib import Path

from .web import PROJECT_ROOT, create_server


DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 10000
DEFAULT_KNOWLEDGE_ROOT = PROJECT_ROOT / "knowledge-release"


def hosted_settings(environ: dict[str, str] | None = None) -> dict[str, object]:
    values = os.environ if environ is None else environ
    password = values.get("DECISIONMED_BETA_PASSWORD", "")
    if not password:
        raise RuntimeError("DECISIONMED_BETA_PASSWORD is required")
    knowledge_root = Path(
        values.get("DECISIONMED_KNOWLEDGE_ROOT", str(DEFAULT_KNOWLEDGE_ROOT))
    ).resolve()
    if not knowledge_root.is_dir():
        raise RuntimeError(f"DecisionMed knowledge release not found: {knowledge_root}")
    try:
        port = int(values.get("PORT", str(DEFAULT_PORT)))
    except ValueError as exc:
        raise RuntimeError("PORT must be an integer") from exc
    if not 1 <= port <= 65535:
        raise RuntimeError("PORT must be between 1 and 65535")
    return {
        "host": DEFAULT_HOST,
        "port": port,
        "knowledge_root": knowledge_root,
        "username": values.get("DECISIONMED_BETA_USER", "decisionmed"),
        "password": password,
    }


def main() -> None:
    settings = hosted_settings()
    server = create_server(
        host=str(settings["host"]),
        port=int(settings["port"]),
        psychiatry_url=None,
        knowledge_root=settings["knowledge_root"],  # type: ignore[arg-type]
        allow_public_host=True,
        public_read_only=True,
        beta_credentials=(str(settings["username"]), str(settings["password"])),
        hosted_landing="/intake.html",
    )
    print(f"DecisionMed protected beta listening on 0.0.0.0:{settings['port']}")
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
