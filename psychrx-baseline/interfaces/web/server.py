"""Localhost server for the PsychRx read-only app shell."""

from __future__ import annotations

import json
import csv
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from application.clinical_decision_support_service import ClinicalDecisionSupportService
from application.clinical_context_registry import ClinicalContextRegistry
from application.clinical_coverage_matrix import ClinicalCoverageMatrix
from application.pharmacological_coverage_audit import PharmacologicalCoverageAuditService
from application.app_service import PsychRxAppService
from interfaces.web.auth import SESSION_COOKIE, WebAccessPolicy


PROJECT_ROOT = Path(__file__).resolve().parents[2]
STATIC_ROOT = Path(__file__).resolve().parent / "static"
MOTOR_MATRIX_PATH = (
    PROJECT_ROOT
    / "knowledge_base"
    / "decision_support_engine"
    / "tables"
    / "pharmacological_decision_matrix.csv"
)
STRATEGY_TABLE_PATH = (
    PROJECT_ROOT
    / "knowledge_base"
    / "decision_support_engine"
    / "tables"
    / "medication_strategy_table.csv"
)
EXPLANATION_PROFILE_PATH = (
    PROJECT_ROOT
    / "knowledge_base"
    / "decision_support_engine"
    / "tables"
    / "medication_explanation_profile_backlog.csv"
)
MOTOR2_STRATEGY_PATH = (
    PROJECT_ROOT
    / "knowledge_base"
    / "decision_support_engine"
    / "tables"
    / "motor2_strategy_matrix.csv"
)
TOXIDROME_SCREENING_PATH = (
    PROJECT_ROOT
    / "knowledge_base"
    / "decision_support_engine"
    / "tables"
    / "toxidrome_screening_matrix.csv"
)


class PsychRxRequestHandler(SimpleHTTPRequestHandler):
    """Serves static files and a read-only application state endpoint."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(STATIC_ROOT), **kwargs)

    def do_GET(self) -> None:
        """Handle static pages and JSON app state."""
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._send_json(
                {
                    "status": "ok",
                    "mode": "read-only",
                    "access": "protected" if self._access_policy.required else "local",
                }
            )
            return
        if parsed.path == "/login":
            if self._is_authenticated():
                self._redirect("/")
                return
            self.path = "/login.html"
            super().do_GET()
            return
        if parsed.path == "/login.html":
            self._redirect("/login")
            return
        if not self._is_authenticated():
            self._reject_unauthenticated(parsed.path)
            return
        if parsed.path == "/api/app-state":
            self._send_json(PsychRxAppService().get_app_view_model().to_dict())
            return
        if parsed.path == "/api/medications":
            medication_details = _load_motor_medication_details()
            self._send_json(
                {
                    "medications": [item["name"] for item in medication_details],
                    "medication_details": medication_details,
                }
            )
            return
        if parsed.path == "/api/toxidrome-screening":
            self._send_json({"signals": _load_toxidrome_screening_signals()})
            return
        if parsed.path == "/api/clinical-contexts":
            self._send_json({"contexts": ClinicalContextRegistry().as_payload()})
            return
        if parsed.path == "/api/coverage-audit":
            self._send_json(PharmacologicalCoverageAuditService().run().to_dict())
            return
        if parsed.path == "/api/clinical-coverage":
            self._send_json(ClinicalCoverageMatrix().as_payload())
            return
        if parsed.path == "/":
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self) -> None:
        """Handle structured decision-support requests."""
        parsed = urlparse(self.path)
        if parsed.path == "/login":
            self._handle_login()
            return
        if parsed.path == "/logout":
            self._clear_session()
            return
        if not self._is_authenticated():
            self._reject_unauthenticated(parsed.path)
            return
        if parsed.path != "/api/decision-support":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length).decode("utf-8")
            payload = json.loads(body) if body else {}
            response = ClinicalDecisionSupportService().build_response(payload)
            self._send_json(response.to_dict())
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            self._send_json(
                {"error": "invalid_decision_support_payload", "detail": str(exc)},
                status=400,
            )

    def log_message(self, format: str, *args: Any) -> None:
        """Keep the local server quiet during tests and development."""
        return

    def _send_json(self, payload: dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    @property
    def _access_policy(self) -> WebAccessPolicy:
        return self.server.access_policy  # type: ignore[attr-defined]

    def _is_authenticated(self) -> bool:
        return self._access_policy.request_is_authenticated(self.headers.get("Cookie"))

    def _reject_unauthenticated(self, path: str) -> None:
        if path.startswith("/api/"):
            self._send_json({"error": "authentication_required"}, status=401)
            return
        self._redirect("/login")

    def _handle_login(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8")
        password = parse_qs(body).get("password", [""])[0]
        if not self._access_policy.password_matches(password):
            self._redirect("/login?error=1")
            return
        token = self._access_policy.issue_session()
        secure = self.headers.get("X-Forwarded-Proto", "").lower() == "https"
        cookie = (
            f"{SESSION_COOKIE}={token}; Path=/; HttpOnly; SameSite=Strict; "
            f"Max-Age={self._access_policy.session_ttl_seconds}"
        )
        if secure:
            cookie += "; Secure"
        self.send_response(303)
        self.send_header("Location", "/")
        self.send_header("Set-Cookie", cookie)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

    def _clear_session(self) -> None:
        self.send_response(303)
        self.send_header("Location", "/login")
        self.send_header(
            "Set-Cookie",
            f"{SESSION_COOKIE}=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0",
        )
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

    def _redirect(self, location: str) -> None:
        self.send_response(303)
        self.send_header("Location", location)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()


def create_server(
    host: str = "127.0.0.1",
    port: int = 8765,
    access_policy: WebAccessPolicy | None = None,
) -> ThreadingHTTPServer:
    """Create the local HTTP server."""
    policy = access_policy or WebAccessPolicy.from_environment()
    policy.validate()
    server = ThreadingHTTPServer((host, port), PsychRxRequestHandler)
    server.access_policy = policy  # type: ignore[attr-defined]
    return server


def _load_motor_medication_details() -> list[dict[str, str]]:
    """Return medication names and classes from the local pharmacological matrix."""
    if not MOTOR_MATRIX_PATH.exists():
        return []
    strategy_details = _load_strategy_details()
    explanation_details = _load_explanation_profile_details()
    motor2_details = _load_motor2_strategy_details()
    with MOTOR_MATRIX_PATH.open("r", encoding="utf-8", newline="") as handle:
        details: dict[str, dict[str, str]] = {}
        for row in csv.DictReader(handle):
            name = row.get("drug_name", "").strip()
            if not name:
                continue
            details.setdefault(
                name,
                {
                    "drug_class": row.get("drug_class", "").strip(),
                    "therapeutic_targets": row.get("therapeutic_targets", "").strip(),
                    "preferred_contexts": row.get("preferred_contexts", "").strip(),
                },
            )
    medications: list[dict[str, str]] = []
    for name in sorted(details, key=str.casefold):
        motor2_ranges = motor2_details.get(name, [])
        dose_band = explanation_details.get(name, {}).get("dose_band", "")
        dose_source = explanation_details.get(name, {}).get("source_reference", "")
        enriched_motor2_ranges = []
        for row in motor2_ranges:
            enriched = dict(row)
            if not enriched.get("dose_effect_band") and dose_band:
                enriched["dose_effect_band"] = dose_band
            if not enriched.get("dose_effect_source") and dose_source:
                enriched["dose_effect_source"] = dose_source
            enriched_motor2_ranges.append(enriched)
        medications.append(
            {
            "name": name,
            "drug_class": details[name].get("drug_class", ""),
            "therapeutic_targets": details[name].get("therapeutic_targets", ""),
            "preferred_contexts": details[name].get("preferred_contexts", ""),
            "association_fit": strategy_details.get(name, {}).get("association_fit", ""),
            "dose_band": dose_band,
            "motor2_ranges": enriched_motor2_ranges,
        }
        )
    return medications


def _load_toxidrome_screening_signals() -> list[dict[str, str]]:
    """Return source-anchored acute safety screening options for the UI."""
    if not TOXIDROME_SCREENING_PATH.exists():
        return []
    with TOXIDROME_SCREENING_PATH.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle) if row.get("ui_label", "").strip()]


def _load_strategy_details() -> dict[str, dict[str, str]]:
    """Return strategy metadata used by the local test-case generator."""
    if not STRATEGY_TABLE_PATH.exists():
        return {}
    with STRATEGY_TABLE_PATH.open("r", encoding="utf-8", newline="") as handle:
        return {
            row.get("drug_name", "").strip(): {
                "association_fit": row.get("association_fit", "").strip(),
            }
            for row in csv.DictReader(handle)
            if row.get("drug_name", "").strip()
        }


def _load_explanation_profile_details() -> dict[str, dict[str, str]]:
    """Return dose-effect metadata used by the local test-case generator."""
    if not EXPLANATION_PROFILE_PATH.exists():
        return {}
    with EXPLANATION_PROFILE_PATH.open("r", encoding="utf-8", newline="") as handle:
        return {
            row.get("medication_name", "").strip(): {
                "dose_band": row.get("dose_band", "").strip(),
                "source_reference": row.get("source_reference", "").strip(),
            }
            for row in csv.DictReader(handle)
            if row.get("medication_name", "").strip()
        }


def _load_motor2_strategy_details() -> dict[str, list[dict[str, str]]]:
    """Return dose-effect and condition range rows used by the UI comparison."""
    if not MOTOR2_STRATEGY_PATH.exists():
        return {}
    details: dict[str, list[dict[str, str]]] = {}
    with MOTOR2_STRATEGY_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            name = row.get("medication_name", "").strip()
            if not name:
                continue
            details.setdefault(name, []).append(
                {
                    "condition": row.get("condition_or_context", "").strip(),
                    "condition_key": row.get("condition_key", "").strip(),
                    "condition_range": row.get("condition_range", "").strip(),
                    "condition_range_min": row.get("condition_range_min", "").strip(),
                    "condition_range_max": row.get("condition_range_max", "").strip(),
                    "range_source": row.get("range_source", "").strip(),
                    "dose_effect_band": row.get("dose_effect_band", "").strip(),
                    "dose_effect_min": row.get("dose_effect_min", "").strip(),
                    "dose_effect_max": row.get("dose_effect_max", "").strip(),
                    "dose_effect_goal": row.get("dose_effect_goal", "").strip(),
                    "dose_effect_source": row.get("dose_effect_source", "").strip(),
                    "dominant_effect": row.get("dominant_effect", "").strip(),
                    "mechanism_or_target": row.get("mechanism_or_target", "").strip(),
                    "evidence_status": row.get("evidence_status", "").strip(),
                }
            )
    return details


def run(host: str | None = None, port: int | None = None) -> None:
    """Run the local app until interrupted."""
    policy = WebAccessPolicy.from_environment()
    resolved_host = host or ("0.0.0.0" if policy.required else "127.0.0.1")
    resolved_port = port or int(os.getenv("PORT", "8765"))
    server = create_server(resolved_host, resolved_port, access_policy=policy)
    print(f"PsychRx local app running at http://{resolved_host}:{resolved_port}")
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
