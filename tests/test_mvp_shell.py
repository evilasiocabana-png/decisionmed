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

    def request(self, path: str) -> tuple[int, dict[str, str], bytes]:
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=3)
        connection.request("GET", path)
        response = connection.getresponse()
        body = response.read()
        headers = {key.lower(): value for key, value in response.getheaders()}
        connection.close()
        return response.status, headers, body

    def test_health_and_app_state_endpoints(self) -> None:
        health_status, _, health_body = self.request("/health")
        state_status, _, state_body = self.request("/api/app-state")

        self.assertEqual(200, health_status)
        self.assertEqual("ok", json.loads(health_body)["status"])
        self.assertEqual(200, state_status)
        self.assertEqual("DecisionMEd", json.loads(state_body)["product"])

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

    def test_psychrx_baseline_server_can_be_created(self) -> None:
        server = create_psychiatry_server(port=0)
        try:
            self.assertGreater(server.server_address[1], 0)
        finally:
            server.server_close()


if __name__ == "__main__":
    unittest.main()
