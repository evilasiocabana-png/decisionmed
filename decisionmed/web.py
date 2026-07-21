"""Local DecisionMEd hub with the PsychRx baseline as Psychiatry pack."""

from __future__ import annotations

import argparse
import importlib
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
from threading import Thread
from typing import Any
from urllib.parse import urlparse

from .app import DecisionMedAppService
from .application import load_governed_catalogs
from .knowledge import KnowledgeError
from .specialties import UnknownSpecialtyPackError
from .sessions import WorkflowSessionError
from .workflows import UnknownWorkflowError


PROJECT_ROOT = Path(__file__).resolve().parents[1]
STATIC_ROOT = Path(__file__).resolve().parent / "static"
PSYCHRX_BASELINE_ROOT = PROJECT_ROOT / "psychrx-baseline"
DEFAULT_KNOWLEDGE_ROOT = PROJECT_ROOT.parent / "DecisionMEd-Knowledge"


class DecisionMedRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(STATIC_ROOT), **kwargs)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._send_json({"status": "ok", "mode": "read-only"})
            return
        if parsed.path == "/api/app-state":
            self._send_json(self._app_service.get_app_state())
            return
        if parsed.path == "/api/readiness":
            self._send_json(self._app_service.get_readiness())
            return
        if parsed.path.startswith("/api/workflows/"):
            specialty_key = parsed.path.removeprefix("/api/workflows/")
            try:
                workflow = self._app_service.workflow(specialty_key)
            except (UnknownSpecialtyPackError, UnknownWorkflowError):
                self._send_json({"error": "workflow_not_found"}, status=404)
                return
            self._send_json(workflow.to_dict())
            return
        parts = parsed.path.strip("/").split("/")
        if len(parts) == 4 and parts[:2] == ["api", "form-schemas"]:
            try:
                schema = self._app_service.form_schema(parts[2], parts[3])
            except (UnknownSpecialtyPackError, UnknownWorkflowError, KnowledgeError):
                self._send_json({"error": "form_schema_not_found"}, status=404)
                return
            self._send_json(schema)
            return
        if parsed.path == "/psychiatry":
            self._redirect(self._psychiatry_url)
            return
        if parsed.path == "/":
            self.path = "/index.html"
        super().do_GET()

    def end_headers(self) -> None:
        """Apply browser protections to every local hub response."""

        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; base-uri 'none'; form-action 'none'; "
            "frame-ancestors 'none'; connect-src 'self'; img-src 'self' data:; "
            "style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'",
        )
        super().end_headers()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        try:
            payload = self._read_json()
            if parsed.path == "/api/sessions":
                self._require_keys(payload, {"specialty_key"})
                result = self._app_service.start_session(payload["specialty_key"])
                self._send_json(result, status=201)
                return

            parts = parsed.path.strip("/").split("/")
            if len(parts) == 4 and parts[:2] == ["api", "sessions"] and parts[3] == "advance":
                self._require_keys(payload, {"step_key"})
                result = self._app_service.advance_session(parts[2], payload["step_key"])
                self._send_json(result)
                return
            self._send_json({"error": "endpoint_not_found"}, status=404)
        except RequestPayloadError as exc:
            self._send_json({"error": exc.code}, status=400)
        except WorkflowSessionError as exc:
            status = 404 if exc.code in {
                "workflow_session.unknown",
                "workflow_session.unknown_specialty",
            } else 503 if exc.code == "workflow_session.capacity" else 409
            self._send_json({"error": exc.code}, status=status)

    @property
    def _app_service(self) -> DecisionMedAppService:
        return self.server.app_service  # type: ignore[attr-defined]

    @property
    def _psychiatry_url(self) -> str:
        return self.server.psychiatry_url  # type: ignore[attr-defined]

    def _send_json(self, payload: dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict[str, str]:
        if not self.headers.get("Content-Type", "").lower().startswith(
            "application/json"
        ):
            raise RequestPayloadError("invalid_content_type")
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise RequestPayloadError("invalid_content_length") from exc
        if not 1 <= length <= 1024:
            raise RequestPayloadError("invalid_content_length")
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RequestPayloadError("invalid_json") from exc
        if not isinstance(payload, dict) or not all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in payload.items()
        ):
            raise RequestPayloadError("invalid_payload")
        if any(not value or len(value) > 200 for value in payload.values()):
            raise RequestPayloadError("invalid_payload")
        return payload

    @staticmethod
    def _require_keys(payload: dict[str, str], expected: set[str]) -> None:
        if set(payload) != expected:
            raise RequestPayloadError("unexpected_fields")

    def _redirect(self, location: str) -> None:
        self.send_response(303)
        self.send_header("Location", location)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

    def log_message(self, format: str, *args: Any) -> None:
        return


class RequestPayloadError(ValueError):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


def create_server(
    host: str = "127.0.0.1",
    port: int = 8765,
    psychiatry_url: str = "http://127.0.0.1:8766/",
    app_service: DecisionMedAppService | None = None,
    knowledge_root: Path | None = None,
) -> ThreadingHTTPServer:
    _require_loopback_host(host)
    if app_service is not None and knowledge_root is not None:
        raise ValueError("provide app_service or knowledge_root, not both")
    server = ThreadingHTTPServer((host, port), DecisionMedRequestHandler)
    if app_service is None:
        catalogs = (
            load_governed_catalogs(knowledge_root)
            if knowledge_root is not None
            else None
        )
        app_service = DecisionMedAppService(catalogs=catalogs)
    server.app_service = app_service  # type: ignore[attr-defined]
    server.psychiatry_url = psychiatry_url  # type: ignore[attr-defined]
    return server


def create_psychiatry_server(
    host: str = "127.0.0.1", port: int = 8766
) -> ThreadingHTTPServer:
    """Create the existing PsychRx server without modifying its baseline."""

    _require_loopback_host(host)
    if not PSYCHRX_BASELINE_ROOT.exists():
        raise FileNotFoundError("psychrx-baseline was not found")
    baseline_path = str(PSYCHRX_BASELINE_ROOT)
    if baseline_path not in sys.path:
        sys.path.insert(0, baseline_path)
    module = importlib.import_module("interfaces.web.server")
    return module.create_server(host, port)


def _require_loopback_host(host: str) -> None:
    if host not in {"127.0.0.1", "localhost"}:
        raise ValueError("DecisionMEd without authentication must bind to loopback")


def run(
    host: str = "127.0.0.1",
    port: int = 8765,
    psychiatry_port: int = 8766,
    knowledge_root: Path | None = None,
) -> None:
    hub_server = create_server(
        host,
        port,
        psychiatry_url=f"http://{host}:{psychiatry_port}/",
        knowledge_root=knowledge_root,
    )
    try:
        psychiatry_server = create_psychiatry_server(host, psychiatry_port)
    except Exception:
        hub_server.server_close()
        raise
    psychiatry_thread = Thread(target=psychiatry_server.serve_forever, daemon=True)
    psychiatry_thread.start()
    print(f"DecisionMEd running at http://{host}:{port}")
    print(f"Psychiatry pack running at http://{host}:{psychiatry_port}")
    try:
        hub_server.serve_forever()
    finally:
        hub_server.server_close()
        psychiatry_server.shutdown()
        psychiatry_server.server_close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local DecisionMEd MVP")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8765, type=int)
    parser.add_argument("--psychiatry-port", default=8766, type=int)
    parser.add_argument(
        "--knowledge-root",
        type=Path,
        default=DEFAULT_KNOWLEDGE_ROOT if DEFAULT_KNOWLEDGE_ROOT.is_dir() else None,
    )
    args = parser.parse_args()
    run(args.host, args.port, args.psychiatry_port, args.knowledge_root)


if __name__ == "__main__":
    main()
