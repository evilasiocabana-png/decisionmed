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


PROJECT_ROOT = Path(__file__).resolve().parents[1]
STATIC_ROOT = Path(__file__).resolve().parent / "static"
PSYCHRX_BASELINE_ROOT = PROJECT_ROOT / "psychrx-baseline"


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
        if parsed.path == "/psychiatry":
            self._redirect(self._psychiatry_url)
            return
        if parsed.path == "/":
            self.path = "/index.html"
        super().do_GET()

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
        self.end_headers()
        self.wfile.write(body)

    def _redirect(self, location: str) -> None:
        self.send_response(303)
        self.send_header("Location", location)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

    def log_message(self, format: str, *args: Any) -> None:
        return


def create_server(
    host: str = "127.0.0.1",
    port: int = 8765,
    psychiatry_url: str = "http://127.0.0.1:8766/",
    app_service: DecisionMedAppService | None = None,
) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer((host, port), DecisionMedRequestHandler)
    server.app_service = app_service or DecisionMedAppService()  # type: ignore[attr-defined]
    server.psychiatry_url = psychiatry_url  # type: ignore[attr-defined]
    return server


def create_psychiatry_server(
    host: str = "127.0.0.1", port: int = 8766
) -> ThreadingHTTPServer:
    """Create the existing PsychRx server without modifying its baseline."""

    if not PSYCHRX_BASELINE_ROOT.exists():
        raise FileNotFoundError("psychrx-baseline was not found")
    baseline_path = str(PSYCHRX_BASELINE_ROOT)
    if baseline_path not in sys.path:
        sys.path.insert(0, baseline_path)
    module = importlib.import_module("interfaces.web.server")
    return module.create_server(host, port)


def run(host: str = "127.0.0.1", port: int = 8765, psychiatry_port: int = 8766) -> None:
    psychiatry_server = create_psychiatry_server(host, psychiatry_port)
    psychiatry_thread = Thread(target=psychiatry_server.serve_forever, daemon=True)
    psychiatry_thread.start()

    hub_server = create_server(
        host,
        port,
        psychiatry_url=f"http://{host}:{psychiatry_port}/",
    )
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
    args = parser.parse_args()
    run(args.host, args.port, args.psychiatry_port)


if __name__ == "__main__":
    main()
