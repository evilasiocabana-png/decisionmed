import http.client
import json
from datetime import date
from threading import Thread
from types import SimpleNamespace
import unittest
from unittest.mock import Mock

from decisionmed.app import DecisionMedAppService
from decisionmed.web import create_server


class _Registry:
    def __init__(self, *items: object) -> None:
        self._items = items

    def all(self) -> tuple[object, ...]:
        return self._items


def _source(
    source_id: str,
    *,
    title: str,
    year: int,
    locator: str,
) -> SimpleNamespace:
    return SimpleNamespace(
        source_id=source_id,
        title=title,
        publication_year=year,
        evidence_type=SimpleNamespace(value="guideline"),
        evidence_quality=SimpleNamespace(value="insufficient"),
        recommendation_strength=SimpleNamespace(
            value="insufficient_for_recommendation"
        ),
        locator=locator,
        version="0.1.0",
        status=SimpleNamespace(value="draft"),
        specialties=("cardiology",),
        reviewed_on=date(2026, 7, 21),
        known_conflicts="Specific conflicts have not been reviewed.",
        clinical_applicability="Catalog metadata only.",
        review_due_on=None,
        review_state="unscheduled",
    )


class EvidenceSourceCatalogTest(unittest.TestCase):
    def test_unloaded_catalog_is_explicit_and_fail_closed(self) -> None:
        payload = DecisionMedAppService().evidence_source_catalog()

        self.assertFalse(payload["loaded"])
        self.assertEqual(0, payload["count"])
        self.assertEqual([], payload["items"])
        self.assertFalse(payload["clinical_execution_allowed"])

    def test_exposes_real_status_safe_locator_labels_and_binding_scope(self) -> None:
        acute = _source(
            "acc.2023.atrial-fibrillation",
            title="2023 ACC/AHA Guideline for Atrial Fibrillation",
            year=2023,
            locator="https://www.acc.org/guidelines/atrial-fibrillation",
        )
        chronic = _source(
            "acc.2023.chronic-coronary-disease",
            title="2023 ACC/AHA Guideline for Chronic Coronary Disease",
            year=2023,
            locator="https://127.0.0.1/private-catalog",
        )
        content = SimpleNamespace(
            module_id="syndrome.atrial-fibrillation",
            source_ids=("acc.2023.atrial-fibrillation",),
            discriminators=(
                SimpleNamespace(
                    source_ids=("acc.2023.chronic-coronary-disease",)
                ),
            ),
            complementary_exams=(),
        )
        catalogs = SimpleNamespace(
            manifest=SimpleNamespace(
                schema_version="11.0.0",
                release_version="0.6.0",
            ),
            evidence=_Registry(acute, chronic),
            clinical_modules=_Registry(
                SimpleNamespace(
                    module_id="syndrome.atrial-fibrillation",
                    source_ids=("acc.2023.atrial-fibrillation",),
                )
            ),
            clinical_content=_Registry(content),
            clinical_rules=_Registry(
                SimpleNamespace(
                    rule_id="rule.atrial-fibrillation",
                    source_ids=("acc.2023.atrial-fibrillation",),
                )
            ),
            knowledge=_Registry(
                SimpleNamespace(
                    evidence_source_ids=("acc.2023.atrial-fibrillation",)
                )
            ),
            safety_checks=_Registry(
                SimpleNamespace(
                    evidence_source_ids=("acc.2023.atrial-fibrillation",)
                )
            ),
        )
        service = object.__new__(DecisionMedAppService)
        service._catalogs = catalogs

        payload = service.evidence_source_catalog()

        self.assertTrue(payload["loaded"])
        self.assertEqual(2, payload["count"])
        self.assertFalse(payload["clinical_execution_allowed"])
        first, second = payload["items"]
        self.assertEqual("ACC/AHA 2023a", first["citation_label"])
        self.assertEqual("ACC/AHA 2023b", second["citation_label"])
        self.assertEqual(
            "American College of Cardiology / American Heart Association",
            first["publisher"],
        )
        self.assertEqual(2023, first["year"])
        self.assertEqual(2023, first["publication_year"])
        self.assertEqual("draft", first["status"])
        self.assertEqual("insufficient", first["evidence_quality"])
        self.assertEqual(
            "https://www.acc.org/guidelines/atrial-fibrillation",
            first["locator"],
        )
        self.assertIsNone(second["locator"])
        self.assertFalse(first["runtime_eligible"])
        self.assertEqual(
            ["syndrome.atrial-fibrillation"],
            first["binding_scope"]["clinical_module_ids"],
        )
        self.assertEqual(
            ["syndrome.atrial-fibrillation"],
            first["binding_scope"]["clinical_content_module_ids"],
        )
        self.assertEqual(
            ["rule.atrial-fibrillation"],
            first["binding_scope"]["clinical_rule_ids"],
        )
        self.assertEqual(1, first["binding_scope"]["knowledge_object_count"])
        self.assertEqual(1, first["binding_scope"]["safety_check_count"])
        self.assertEqual(
            ["syndrome.atrial-fibrillation"],
            second["binding_scope"]["clinical_content_module_ids"],
        )


class EvidenceSourceCatalogWebTest(unittest.TestCase):
    def setUp(self) -> None:
        self.app_service = Mock()
        self.app_service.evidence_source_catalog.return_value = {
            "loaded": True,
            "count": 1,
            "clinical_execution_allowed": False,
            "items": [{"source_id": "source.test", "status": "draft"}],
        }
        self.server = create_server(
            port=0,
            app_service=self.app_service,
        )
        self.thread = Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def test_get_evidence_sources_returns_catalog(self) -> None:
        connection = http.client.HTTPConnection(
            "127.0.0.1", self.server.server_address[1], timeout=3
        )
        connection.request("GET", "/api/evidence-sources")
        response = connection.getresponse()
        body = json.loads(response.read())
        headers = {key.lower(): value for key, value in response.getheaders()}
        connection.close()

        self.assertEqual(200, response.status)
        self.assertEqual("no-store", headers["cache-control"])
        self.assertEqual("source.test", body["items"][0]["source_id"])
        self.app_service.evidence_source_catalog.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
