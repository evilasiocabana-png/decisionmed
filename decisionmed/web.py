"""Local DecisionMEd hub with the PsychRx baseline as Psychiatry pack."""

from __future__ import annotations

import argparse
import base64
import hmac
import importlib
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
from threading import Thread
from typing import Any
from urllib.parse import parse_qs, urlparse

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
        if not self._authorize_request():
            return
        if parsed.path == "/api/app-state":
            self._send_json(self._app_service.get_app_state())
            return
        if parsed.path == "/api/readiness":
            self._send_json(self._app_service.get_readiness())
            return
        if parsed.path == "/api/evidence-sources":
            self._send_json(self._app_service.evidence_source_catalog())
            return
        if parsed.path == "/api/clinical-modules":
            self._send_json(self._app_service.clinical_module_catalog())
            return
        if parsed.path == "/api/clinical-rules":
            self._send_json(self._app_service.clinical_rule_catalog())
            return
        if parsed.path == "/api/clinical-content":
            self._send_json(self._app_service.clinical_content_catalog())
            return
        if parsed.path == "/api/clinical-cases":
            query = parse_qs(parsed.query, keep_blank_values=False)
            try:
                module_id = query.get("module_id", [None])[0]
                offset = int(query.get("offset", ["0"])[0])
                limit = int(query.get("limit", ["50"])[0])
                self._send_json(
                    self._app_service.clinical_case_catalog(
                        module_id,
                        offset=offset,
                        limit=limit,
                    )
                )
            except (KnowledgeError, TypeError, ValueError):
                self._send_json(
                    {"error": "invalid_clinical_case_query"},
                    status=400,
                )
            return
        if parsed.path.startswith("/api/clinical-modules/"):
            module_id = parsed.path.removeprefix("/api/clinical-modules/")
            try:
                module = self._app_service.clinical_module(module_id)
            except KnowledgeError:
                self._send_json({"error": "clinical_module_not_found"}, status=404)
                return
            self._send_json(module)
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
            if self._psychiatry_url:
                self._redirect(self._psychiatry_url)
            else:
                self._send_json({"error": "endpoint_not_available"}, status=404)
            return
        if parsed.path == "/":
            self.path = self._hosted_landing or "/index.html"
        super().do_GET()

    def end_headers(self) -> None:
        """Apply browser protections to every local hub response."""

        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        if self._public_read_only:
            self.send_header("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
            self.send_header("X-Robots-Tag", "noindex, nofollow, noarchive")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; base-uri 'none'; form-action 'none'; "
            "frame-ancestors 'none'; connect-src 'self'; img-src 'self' data:; "
            "style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'",
        )
        super().end_headers()

    def do_POST(self) -> None:
        if not self._authorize_request():
            return
        if self._public_read_only:
            self._send_json({"error": "public_read_only"}, status=405)
            return
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
    def _psychiatry_url(self) -> str | None:
        return self.server.psychiatry_url  # type: ignore[attr-defined]

    @property
    def _public_read_only(self) -> bool:
        return bool(getattr(self.server, "public_read_only", False))

    @property
    def _hosted_landing(self) -> str | None:
        return getattr(self.server, "hosted_landing", None)

    @property
    def _beta_credentials(self) -> tuple[str, str] | None:
        return getattr(self.server, "beta_credentials", None)

    def _authorize_request(self) -> bool:
        credentials = self._beta_credentials
        if credentials is None:
            return True
        header = self.headers.get("Authorization", "")
        if not header.startswith("Basic "):
            self._send_auth_required()
            return False
        try:
            raw = base64.b64decode(header[6:], validate=True).decode("utf-8")
            supplied_user, supplied_password = raw.split(":", 1)
        except (ValueError, UnicodeDecodeError):
            self._send_auth_required()
            return False
        expected_user, expected_password = credentials
        authorized = hmac.compare_digest(supplied_user, expected_user) and hmac.compare_digest(
            supplied_password,
            expected_password,
        )
        if not authorized:
            self._send_auth_required()
        return authorized

    def _send_auth_required(self) -> None:
        body = json.dumps({"error": "beta_authentication_required"}).encode("utf-8")
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="DecisionMed Beta", charset="UTF-8"')
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

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
    psychiatry_url: str | None = "http://127.0.0.1:8766/",
    app_service: DecisionMedAppService | None = None,
    knowledge_root: Path | None = None,
    *,
    allow_public_host: bool = False,
    public_read_only: bool = False,
    beta_credentials: tuple[str, str] | None = None,
    hosted_landing: str | None = None,
) -> ThreadingHTTPServer:
    _require_host(host, allow_public_host=allow_public_host)
    if host == "0.0.0.0" and (
        not allow_public_host or not public_read_only or beta_credentials is None
    ):
        raise ValueError(
            "public binding requires read-only mode and beta authentication"
        )
    if beta_credentials is not None and (
        not beta_credentials[0] or not beta_credentials[1]
    ):
        raise ValueError("beta credentials must not be empty")
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
    server.public_read_only = public_read_only  # type: ignore[attr-defined]
    server.beta_credentials = beta_credentials  # type: ignore[attr-defined]
    server.hosted_landing = hosted_landing  # type: ignore[attr-defined]
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
    _require_host(host, allow_public_host=False)


def _require_host(host: str, *, allow_public_host: bool) -> None:
    allowed = {"127.0.0.1", "localhost"}
    if allow_public_host:
        allowed.add("0.0.0.0")
    if host not in allowed:
        raise ValueError("DecisionMEd without hosted safeguards must bind to loopback")


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
