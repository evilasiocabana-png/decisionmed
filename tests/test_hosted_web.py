from __future__ import annotations

import base64
import http.client
from pathlib import Path
import tempfile
from threading import Thread
import unittest

from decisionmed.app import DecisionMedAppService
from decisionmed.hosted import hosted_settings
from decisionmed.web import create_server


class HostedDecisionMedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.server = create_server(
            host="127.0.0.1",
            port=0,
            psychiatry_url=None,
            app_service=DecisionMedAppService(),
            allow_public_host=True,
            public_read_only=True,
            beta_credentials=("decisionmed", "test-secret"),
            hosted_landing="/intake.html",
        )
        self.thread = Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.server.server_address[1]

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def request(
        self,
        method: str,
        path: str,
        *,
        authenticated: bool = False,
        body: str | None = None,
    ) -> tuple[int, dict[str, str], bytes]:
        headers: dict[str, str] = {}
        if authenticated:
            token = base64.b64encode(b"decisionmed:test-secret").decode("ascii")
            headers["Authorization"] = f"Basic {token}"
        if body is not None:
            headers["Content-Type"] = "application/json"
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        connection.request(method, path, body=body, headers=headers)
        response = connection.getresponse()
        payload = response.read()
        response_headers = {key: value for key, value in response.getheaders()}
        connection.close()
        return response.status, response_headers, payload

    def test_health_is_public_for_render(self) -> None:
        status, _, body = self.request("GET", "/health")
        self.assertEqual(200, status)
        self.assertIn(b'"status": "ok"', body)

    def test_beta_content_requires_authentication(self) -> None:
        status, headers, _ = self.request("GET", "/intake.html")
        self.assertEqual(401, status)
        self.assertIn("Basic", headers["WWW-Authenticate"])

    def test_authenticated_root_opens_assisted_intake(self) -> None:
        status, headers, body = self.request("GET", "/", authenticated=True)
        self.assertEqual(200, status)
        self.assertIn("max-age=31536000", headers["Strict-Transport-Security"])
        self.assertEqual("noindex, nofollow, noarchive", headers["X-Robots-Tag"])
        self.assertIn("DecisionMEd", body.decode("utf-8"))

    def test_public_beta_rejects_server_writes(self) -> None:
        status, _, body = self.request(
            "POST",
            "/api/sessions",
            authenticated=True,
            body='{"specialty_key":"cardiology"}',
        )
        self.assertEqual(405, status)
        self.assertIn(b"public_read_only", body)

    def test_psychrx_is_not_exposed_by_hosted_server(self) -> None:
        status, _, body = self.request("GET", "/psychiatry", authenticated=True)
        self.assertEqual(404, status)
        self.assertIn(b"endpoint_not_available", body)


class HostedSettingsTests(unittest.TestCase):
    def test_settings_require_password_and_existing_knowledge_release(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            settings = hosted_settings(
                {
                    "PORT": "12000",
                    "DECISIONMED_BETA_USER": "beta",
                    "DECISIONMED_BETA_PASSWORD": "secret",
                    "DECISIONMED_KNOWLEDGE_ROOT": directory,
                }
            )
        self.assertEqual(12000, settings["port"])
        self.assertEqual("beta", settings["username"])
        self.assertEqual(Path(directory).resolve(), settings["knowledge_root"])

    def test_settings_fail_closed_without_password(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "DECISIONMED_BETA_PASSWORD"):
            hosted_settings({})

    def test_local_server_still_rejects_public_binding(self) -> None:
        with self.assertRaises(ValueError):
            create_server(host="0.0.0.0", port=0)

    def test_hosted_safeguards_allow_render_binding(self) -> None:
        server = create_server(
            host="0.0.0.0",
            port=0,
            app_service=DecisionMedAppService(),
            allow_public_host=True,
            public_read_only=True,
            beta_credentials=("decisionmed", "secret"),
        )
        server.server_close()


if __name__ == "__main__":
    unittest.main()
