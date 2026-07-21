import http.client
import json
from threading import Thread
import unittest

from decisionmed.app import DecisionMedAppService
from decisionmed.web import create_psychiatry_server, create_server


class DecisionMedAppServiceTest(unittest.TestCase):
    def test_app_state_exposes_reference_only_psychiatry(self) -> None:
        state = DecisionMedAppService().get_app_state()

        self.assertEqual("DecisionMEd", state["product"])
        self.assertEqual("read-only", state["mode"])
        self.assertFalse(state["clinical_execution_allowed"])
        self.assertFalse(state["readiness"]["clinical_execution_allowed"])
        self.assertEqual(5, state["readiness"]["blocked_gate_count"])
        psychiatry = next(
            item for item in state["specialties"] if item["key"] == "psychiatry"
        )
        self.assertEqual(6, len(state["specialties"]))
        self.assertEqual("reference_only", psychiatry["load_status"])
        self.assertFalse(psychiatry["execution_allowed"])


class DecisionMedWebTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = create_server(
            port=0, psychiatry_url="http://127.0.0.1:9876/"
        )
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.port = cls.server.server_address[1]

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def request(
        self,
        path: str,
        method: str = "GET",
        payload: dict[str, str] | None = None,
    ) -> tuple[int, dict[str, str], bytes]:
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=3)
        body = json.dumps(payload).encode("utf-8") if payload is not None else None
        headers = {"Content-Type": "application/json"} if body is not None else {}
        connection.request(method, path, body=body, headers=headers)
        response = connection.getresponse()
        response_body = response.read()
        response_headers = {
            key.lower(): value for key, value in response.getheaders()
        }
        connection.close()
        return response.status, response_headers, response_body

    def test_health_and_app_state_endpoints(self) -> None:
        health_status, _, health_body = self.request("/health")
        state_status, _, state_body = self.request("/api/app-state")
        readiness_status, _, readiness_body = self.request("/api/readiness")

        self.assertEqual(200, health_status)
        self.assertEqual("ok", json.loads(health_body)["status"])
        self.assertEqual(200, state_status)
        self.assertEqual("DecisionMEd", json.loads(state_body)["product"])
        self.assertEqual(200, readiness_status)
        self.assertFalse(json.loads(readiness_body)["clinical_execution_allowed"])

    def test_home_page_and_psychiatry_redirect(self) -> None:
        home_status, _, home_body = self.request("/")
        redirect_status, redirect_headers, _ = self.request("/psychiatry")

        self.assertEqual(200, home_status)
        self.assertIn(b"DecisionMEd", home_body)
        self.assertEqual(303, redirect_status)
        self.assertEqual("http://127.0.0.1:9876/", redirect_headers["location"])

    def test_workflow_endpoint_and_unknown_specialty(self) -> None:
        status, _, body = self.request("/api/workflows/psychiatry")
        missing_status, _, missing_body = self.request("/api/workflows/dermatology")

        self.assertEqual(200, status)
        self.assertEqual(13, len(json.loads(body)["steps"]))
        self.assertFalse(json.loads(body)["clinical_execution_allowed"])
        self.assertEqual(404, missing_status)
        self.assertEqual("workflow_not_found", json.loads(missing_body)["error"])

    def test_generic_workflow_page_is_served(self) -> None:
        status, _, body = self.request("/workflow.html?specialty=cardiology")

        self.assertEqual(200, status)
        self.assertIn(b"api/workflows", body)
        self.assertIn(b"read-only", body.lower())
        self.assertIn(b"draft", body)

    def test_structural_session_can_start_and_advance(self) -> None:
        start_status, start_headers, start_body = self.request(
            "/api/sessions", "POST", {"specialty_key": "cardiology"}
        )
        started = json.loads(start_body)
        advance_status, _, advance_body = self.request(
            f"/api/sessions/{started['session_id']}/advance",
            "POST",
            {"step_key": "context"},
        )
        advanced = json.loads(advance_body)

        self.assertEqual(201, start_status)
        self.assertEqual("no-store", start_headers["cache-control"])
        self.assertEqual("context", started["current_step_key"])
        self.assertEqual(200, advance_status)
        self.assertEqual("risk", advanced["current_step_key"])
        self.assertFalse(advanced["clinical_execution_allowed"])

    def test_session_api_rejects_extra_or_free_text_fields(self) -> None:
        status, _, body = self.request(
            "/api/sessions",
            "POST",
            {"specialty_key": "cardiology", "notes": "must not reach backend"},
        )

        self.assertEqual(400, status)
        self.assertEqual("unexpected_fields", json.loads(body)["error"])
        self.assertNotIn(b"must not reach backend", body)

    def test_psychrx_baseline_server_can_be_created(self) -> None:
        server = create_psychiatry_server(port=0)
        try:
            self.assertGreater(server.server_address[1], 0)
        finally:
            server.server_close()

    def test_unauthenticated_server_rejects_non_loopback_binding(self) -> None:
        with self.assertRaises(ValueError):
            create_server(host="0.0.0.0", port=0)
        with self.assertRaises(ValueError):
            create_psychiatry_server(host="0.0.0.0", port=0)


if __name__ == "__main__":
    unittest.main()
