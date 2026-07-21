from __future__ import annotations

import http.client
import threading
import unittest

from interfaces.web.auth import SESSION_COOKIE, WebAccessPolicy
from interfaces.web.server import create_server


class WebAccessPolicyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = WebAccessPolicy(
            required=True,
            password="strong-test-password",
            session_secret="test-session-secret-with-at-least-32-characters",
            session_ttl_seconds=3600,
        )

    def test_signed_session_expires_and_rejects_tampering(self) -> None:
        token = self.policy.issue_session(now=1_000)

        self.assertTrue(self.policy.session_is_valid(token, now=1_500))
        self.assertFalse(self.policy.session_is_valid(token + "x", now=1_500))
        self.assertFalse(self.policy.session_is_valid(token, now=5_000))

    def test_protected_configuration_requires_strong_secrets(self) -> None:
        with self.assertRaises(RuntimeError):
            WebAccessPolicy(True, "short", "also-short").validate()

    def test_password_comparison(self) -> None:
        self.assertTrue(self.policy.password_matches("strong-test-password"))
        self.assertFalse(self.policy.password_matches("wrong-password"))


class ProtectedPsychRxServerTest(unittest.TestCase):
    def setUp(self) -> None:
        policy = WebAccessPolicy(
            required=True,
            password="strong-test-password",
            session_secret="test-session-secret-with-at-least-32-characters",
            session_ttl_seconds=3600,
        )
        self.server = create_server(port=0, access_policy=policy)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.host, self.port = self.server.server_address

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def request(
        self,
        method: str,
        path: str,
        body: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> tuple[int, dict[str, str], bytes]:
        connection = http.client.HTTPConnection(self.host, self.port, timeout=5)
        connection.request(method, path, body=body, headers=headers or {})
        response = connection.getresponse()
        response_body = response.read()
        response_headers = {key: value for key, value in response.getheaders()}
        connection.close()
        return response.status, response_headers, response_body

    def test_health_is_public_but_app_and_api_are_protected(self) -> None:
        health_status, _, health_body = self.request("GET", "/health")
        page_status, page_headers, _ = self.request("GET", "/")
        api_status, _, api_body = self.request("GET", "/api/app-state")

        self.assertEqual(health_status, 200)
        self.assertIn(b'"access": "protected"', health_body)
        self.assertEqual(page_status, 303)
        self.assertEqual(page_headers["Location"], "/login")
        self.assertEqual(api_status, 401)
        self.assertIn(b"authentication_required", api_body)

    def test_login_opens_authenticated_session_and_logout_clears_it(self) -> None:
        login_status, _, login_body = self.request("GET", "/login")
        self.assertEqual(login_status, 200)
        self.assertIn("Área clínica protegida".encode("utf-8"), login_body)

        wrong_status, wrong_headers, _ = self.request(
            "POST",
            "/login",
            body="password=wrong-password",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        self.assertEqual(wrong_status, 303)
        self.assertEqual(wrong_headers["Location"], "/login?error=1")

        status, headers, _ = self.request(
            "POST",
            "/login",
            body="password=strong-test-password",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        self.assertEqual(status, 303)
        self.assertEqual(headers["Location"], "/")
        session_cookie = headers["Set-Cookie"]
        self.assertIn(f"{SESSION_COOKIE}=", session_cookie)
        self.assertIn("HttpOnly", session_cookie)
        self.assertIn("SameSite=Strict", session_cookie)

        cookie_value = session_cookie.split(";", 1)[0]
        api_status, _, api_body = self.request(
            "GET",
            "/api/app-state",
            headers={"Cookie": cookie_value},
        )
        self.assertEqual(api_status, 200)
        self.assertIn(b"Clinical", api_body)

        logout_status, logout_headers, _ = self.request(
            "POST",
            "/logout",
            headers={"Cookie": cookie_value},
        )
        self.assertEqual(logout_status, 303)
        self.assertEqual(logout_headers["Location"], "/login")
        self.assertIn("Max-Age=0", logout_headers["Set-Cookie"])


if __name__ == "__main__":
    unittest.main()
