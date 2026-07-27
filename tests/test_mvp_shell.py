import http.client
import json
from datetime import date, timedelta
from types import SimpleNamespace
from threading import Thread
import unittest
from unittest.mock import Mock

from decisionmed.app import DecisionMedAppService
from decisionmed.knowledge import KnowledgeError
from decisionmed.safety import SafetyCheckStatus
from decisionmed.web import create_psychiatry_server, create_server


class DecisionMedAppServiceTest(unittest.TestCase):
    def test_app_state_exposes_reference_only_psychiatry(self) -> None:
        state = DecisionMedAppService().get_app_state()

        self.assertEqual("DecisionMEd", state["product"])
        self.assertEqual("read-only", state["mode"])
        self.assertFalse(state["clinical_execution_allowed"])
        self.assertFalse(state["knowledge_catalog"]["loaded"])
        self.assertEqual(0, state["knowledge_catalog"]["clinical_module_count"])
        self.assertFalse(state["readiness"]["clinical_execution_allowed"])
        self.assertEqual(5, state["readiness"]["blocked_gate_count"])
        safety_gate = next(
            gate
            for gate in state["readiness"]["gates"]
            if gate["key"] == "safety_configuration"
        )
        self.assertEqual("no_safety_specifications", safety_gate["reason"])
        psychiatry = next(
            item for item in state["specialties"] if item["key"] == "psychiatry"
        )
        self.assertEqual(6, len(state["specialties"]))
        self.assertEqual("reference_only", psychiatry["load_status"])
        self.assertEqual("psychrx.clinical-decision.v1", psychiatry["workflow_contract"])
        self.assertEqual(13, psychiatry["workflow_step_count"])
        self.assertEqual([], psychiatry["reference_schema_step_keys"])
        self.assertEqual(13, len(psychiatry["missing_reference_schema_step_keys"]))
        self.assertEqual(0, psychiatry["reference_knowledge_object_count"])
        self.assertEqual(0, psychiatry["reference_evidence_source_count"])
        self.assertEqual("catalog_not_loaded", psychiatry["reference_curation_state"])
        self.assertEqual(7, len(psychiatry["available_capabilities"]))
        self.assertIn("PsychRx", psychiatry["intended_scope"])
        self.assertIn("Execução clínica.", psychiatry["excluded_uses"])
        self.assertEqual([], psychiatry["incompatible_capabilities"])
        self.assertFalse(psychiatry["execution_allowed"])
        cardiology = next(
            item for item in state["specialties"] if item["key"] == "cardiology"
        )
        self.assertEqual(
            ["cardiology.clinical-snapshot", "cardiology.audit"],
            cardiology["available_capabilities"],
        )
        self.assertEqual(5, len(cardiology["missing_capabilities"]))


class DecisionMedWebTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = create_server(
            port=0,
            psychiatry_url="http://127.0.0.1:9876/",
            app_service=DecisionMedAppService(
                catalogs=cls._catalogs(),
                safety_providers=cls._safety_providers(),
            ),
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
        modules_status, _, modules_body = self.request("/api/clinical-modules")
        rules_status, _, rules_body = self.request("/api/clinical-rules")
        content_status, _, content_body = self.request("/api/clinical-content")
        cases_status, _, cases_body = self.request("/api/clinical-cases")

        self.assertEqual(200, health_status)
        self.assertEqual("ok", json.loads(health_body)["status"])
        self.assertEqual(200, state_status)
        state = json.loads(state_body)
        self.assertEqual("DecisionMEd", state["product"])
        self.assertTrue(state["knowledge_catalog"]["loaded"])
        self.assertEqual(1, state["knowledge_catalog"]["safety_check_count"])
        self.assertEqual(0, state["knowledge_catalog"]["clinical_module_count"])
        self.assertEqual(0, state["knowledge_catalog"]["clinical_rule_count"])
        self.assertEqual(0, state["knowledge_catalog"]["clinical_case_count"])
        self.assertEqual(200, modules_status)
        self.assertEqual(0, json.loads(modules_body)["count"])
        self.assertEqual(200, rules_status)
        self.assertEqual(0, json.loads(rules_body)["count"])
        self.assertEqual(200, content_status)
        self.assertEqual(0, json.loads(content_body)["count"])
        self.assertEqual(200, cases_status)
        self.assertEqual(0, json.loads(cases_body)["count"])
        cardiology = next(
            item for item in state["specialties"] if item["key"] == "cardiology"
        )
        self.assertIn("cardiology.evidence", cardiology["available_capabilities"])
        self.assertIn(
            "cardiology.clinical-snapshot", cardiology["available_capabilities"]
        )
        self.assertIn("cardiology.audit", cardiology["available_capabilities"])
        self.assertNotIn("cardiology.evidence", cardiology["missing_capabilities"])
        self.assertEqual(4, len(cardiology["missing_capabilities"]))
        self.assertEqual("blocked", cardiology["load_status"])
        self.assertEqual(7, cardiology["workflow_step_count"])
        self.assertEqual(["findings"], cardiology["reference_schema_step_keys"])
        self.assertEqual(1, cardiology["reference_knowledge_object_count"])
        self.assertEqual(1, cardiology["reference_evidence_source_count"])
        self.assertEqual("draft", cardiology["reference_curation_state"])
        self.assertEqual(
            ["context", "risk", "safety", "evidence", "decision", "monitoring"],
            cardiology["missing_reference_schema_step_keys"],
        )
        self.assertEqual(1, state["knowledge_catalog"]["form_schema_count"])
        self.assertEqual(200, readiness_status)
        self.assertEqual(200, modules_status)
        self.assertEqual(0, json.loads(modules_body)["count"])
        readiness = json.loads(readiness_body)
        self.assertEqual(1, readiness["counts"]["evidence_sources"])
        self.assertEqual(
            1, readiness["counts"]["evidence_sources_without_review_schedule"]
        )
        self.assertEqual(0, readiness["counts"]["overdue_evidence_sources"])
        evidence_gate = next(
            gate
            for gate in readiness["gates"]
            if gate["key"] == "evidence_catalog"
        )
        self.assertEqual("blocked", evidence_gate["status"])
        self.assertEqual("review_schedule_missing", evidence_gate["reason"])
        self.assertEqual(1, readiness["counts"]["knowledge_objects"])
        self.assertEqual(
            1, readiness["counts"]["knowledge_objects_without_review_schedule"]
        )
        self.assertEqual(1, readiness["counts"]["form_schemas"])
        self.assertEqual(
            1, readiness["counts"]["form_schemas_without_review_schedule"]
        )
        knowledge_gate = next(
            gate
            for gate in readiness["gates"]
            if gate["key"] == "knowledge_catalog"
        )
        self.assertEqual("knowledge_review_schedule_missing", knowledge_gate["reason"])
        self.assertEqual(1, readiness["counts"]["configured_safety_checks"])
        self.assertEqual(0, readiness["counts"]["validated_safety_checks"])
        safety_gate = next(
            gate
            for gate in readiness["gates"]
            if gate["key"] == "safety_configuration"
        )
        self.assertEqual("blocked", safety_gate["status"])
        self.assertEqual(
            "unvalidated_safety_specifications", safety_gate["reason"]
        )
        self.assertFalse(readiness["clinical_execution_allowed"])

    def test_rejects_schema_bound_to_an_unknown_workflow_step(self) -> None:
        catalogs = self._catalogs()
        catalogs.form_schemas.all.return_value[0].step_key = "unknown-step"

        with self.assertRaisesRegex(ValueError, "unknown workflow step"):
            DecisionMedAppService(catalogs=catalogs)

    def test_rejects_schema_bound_to_another_workflow_contract(self) -> None:
        catalogs = self._catalogs()
        catalogs.form_schemas.all.return_value[0].workflow_id = "other.workflow.v1"

        with self.assertRaisesRegex(ValueError, "workflow contract does not match"):
            DecisionMedAppService(catalogs=catalogs)

    def test_validated_safety_metadata_without_provider_stays_blocked(self) -> None:
        catalogs = self._catalogs()
        specification = catalogs.safety_checks.all.return_value[0]
        specification.status = SafetyCheckStatus.VALIDATED
        specification.review_due_on = date.today() + timedelta(days=30)
        specification.review_state = "current"
        service = DecisionMedAppService(
            catalogs=catalogs,
            safety_providers=self._safety_providers(),
        )

        state = service.get_app_state()
        safety_gate = next(
            gate
            for gate in state["readiness"]["gates"]
            if gate["key"] == "safety_configuration"
        )

        self.assertEqual("blocked", safety_gate["status"])
        self.assertEqual("no_safety_providers", safety_gate["reason"])
        self.assertFalse(state["clinical_execution_allowed"])

    def test_complete_provider_coverage_without_evaluator_stays_blocked(self) -> None:
        catalogs = self._catalogs()
        specification = catalogs.safety_checks.all.return_value[0]
        specification.status = SafetyCheckStatus.VALIDATED
        specification.review_due_on = date.today() + timedelta(days=30)
        specification.review_state = "current"
        service = DecisionMedAppService(
            catalogs=catalogs,
            safety_providers=self._safety_providers(bound=True),
        )

        state = service.get_app_state()
        safety_gate = next(
            gate
            for gate in state["readiness"]["gates"]
            if gate["key"] == "safety_configuration"
        )

        self.assertEqual("blocked", safety_gate["status"])
        self.assertEqual("no_safety_evaluators", safety_gate["reason"])
        self.assertFalse(state["clinical_execution_allowed"])

    def test_complete_evaluator_coverage_only_clears_technical_gate(self) -> None:
        catalogs = self._catalogs()
        specification = catalogs.safety_checks.all.return_value[0]
        specification.status = SafetyCheckStatus.VALIDATED
        specification.review_due_on = date.today() + timedelta(days=30)
        specification.review_state = "current"
        providers = self._safety_providers(bound=True)
        service = DecisionMedAppService(
            catalogs=catalogs,
            safety_providers=providers,
            safety_evaluators=self._safety_evaluators(providers),
        )

        state = service.get_app_state()
        safety_gate = next(
            gate
            for gate in state["readiness"]["gates"]
            if gate["key"] == "safety_configuration"
        )

        self.assertEqual("available", safety_gate["status"])
        self.assertEqual("safety_configuration_complete", safety_gate["reason"])
        self.assertFalse(state["clinical_execution_allowed"])

    def test_incompatible_provider_version_has_specific_reason(self) -> None:
        catalogs = self._catalogs()
        specification = catalogs.safety_checks.all.return_value[0]
        specification.status = SafetyCheckStatus.VALIDATED
        specification.review_due_on = date.today() + timedelta(days=30)
        specification.review_state = "current"
        service = DecisionMedAppService(
            catalogs=catalogs,
            safety_providers=self._safety_providers(incompatible=True),
        )

        safety_gate = next(
            gate
            for gate in service.get_readiness()["gates"]
            if gate["key"] == "safety_configuration"
        )

        self.assertEqual("blocked", safety_gate["status"])
        self.assertEqual(
            "incompatible_safety_provider_versions", safety_gate["reason"]
        )

    def test_partial_provider_coverage_has_specific_reason(self) -> None:
        catalogs = self._catalogs()
        first = catalogs.safety_checks.all.return_value[0]
        first.status = SafetyCheckStatus.VALIDATED
        first.review_due_on = date.today() + timedelta(days=30)
        first.review_state = "current"
        second = SimpleNamespace(
            check_id="check.second-synthetic-safety",
            specialty_key="cardiology",
            status=SafetyCheckStatus.VALIDATED,
            review_due_on=date.today() + timedelta(days=30),
            review_state="current",
            review_overdue=False,
        )
        catalogs.safety_checks.all.return_value = (first, second)
        service = DecisionMedAppService(
            catalogs=catalogs,
            safety_providers=self._safety_providers(partial=True),
        )

        safety_gate = next(
            gate
            for gate in service.get_readiness()["gates"]
            if gate["key"] == "safety_configuration"
        )

        self.assertEqual("blocked", safety_gate["status"])
        self.assertEqual(
            "incomplete_safety_provider_coverage", safety_gate["reason"]
        )

    def test_partial_evaluator_coverage_has_specific_reason(self) -> None:
        catalogs = self._catalogs()
        first = catalogs.safety_checks.all.return_value[0]
        first.status = SafetyCheckStatus.VALIDATED
        first.review_due_on = date.today() + timedelta(days=30)
        first.review_state = "current"
        second = SimpleNamespace(
            check_id="check.second-synthetic-safety",
            specialty_key="cardiology",
            status=SafetyCheckStatus.VALIDATED,
            review_due_on=date.today() + timedelta(days=30),
            review_state="current",
            review_overdue=False,
        )
        catalogs.safety_checks.all.return_value = (first, second)
        providers = Mock()
        providers.all.return_value = (
            SimpleNamespace(check_id=first.check_id),
            SimpleNamespace(check_id=second.check_id),
        )
        providers.coverage.return_value = SimpleNamespace(
            complete=True,
            missing_check_ids=(),
            incompatible_check_ids=(),
        )
        evaluators = Mock()
        evaluators.providers = providers
        evaluators.all.return_value = (SimpleNamespace(check_id=first.check_id),)
        evaluators.missing_check_ids = (second.check_id,)
        evaluators.complete = False
        service = DecisionMedAppService(
            catalogs=catalogs,
            safety_providers=providers,
            safety_evaluators=evaluators,
        )

        safety_gate = next(
            gate
            for gate in service.get_readiness()["gates"]
            if gate["key"] == "safety_configuration"
        )

        self.assertEqual("blocked", safety_gate["status"])
        self.assertEqual(
            "incomplete_safety_evaluator_coverage", safety_gate["reason"]
        )

    def test_evaluator_and_provider_registries_must_match(self) -> None:
        providers = self._safety_providers(bound=True)
        other_providers = self._safety_providers(bound=True)

        with self.assertRaises(ValueError):
            DecisionMedAppService(
                catalogs=self._catalogs(),
                safety_providers=providers,
                safety_evaluators=self._safety_evaluators(other_providers),
            )

    def test_home_page_and_psychiatry_redirect(self) -> None:
        home_status, home_headers, home_body = self.request("/")
        redirect_status, redirect_headers, _ = self.request("/psychiatry")

        self.assertEqual(200, home_status)
        self.assertIn(b"DecisionMEd", home_body)
        self.assertIn(b"readiness-summary", home_body)
        self.assertIn(b"module-count", home_body)
        self.assertIn(b"gate-list", home_body)
        self.assertIn(b"catalog-status", home_body)
        self.assertIn(b"item.intended_scope", home_body)
        self.assertIn(b"/intake.html", home_body)
        self.assertIn(b"/catalog.html", home_body)
        self.assertNotIn(b"innerHTML", home_body)
        self.assertEqual("nosniff", home_headers["x-content-type-options"])
        self.assertEqual("DENY", home_headers["x-frame-options"])
        self.assertEqual("no-referrer", home_headers["referrer-policy"])
        self.assertIn("default-src 'self'", home_headers["content-security-policy"])
        self.assertIn("form-action 'none'", home_headers["content-security-policy"])
        self.assertEqual(303, redirect_status)
        self.assertEqual("http://127.0.0.1:9876/", redirect_headers["location"])
        self.assertEqual("DENY", redirect_headers["x-frame-options"])

    def test_clinical_catalog_page_is_local_and_safe(self) -> None:
        status, headers, body = self.request("/catalog.html")

        self.assertEqual(200, status)
        self.assertIn("text/html", headers["content-type"])
        self.assertIn("Catálogo de módulos clínicos".encode(), body)
        self.assertIn(b"/api/clinical-modules", body)
        self.assertIn(b"pageSize=30", body)
        self.assertIn(b"entity-type", body)
        self.assertIn(b"moduleCard", body)
        self.assertIn("Execução clínica bloqueada".encode(), body)
        self.assertNotIn(b"innerHTML", body)
        self.assertEqual("DENY", headers["x-frame-options"])

    def test_guided_intake_page_is_local_and_does_not_inject_html(self) -> None:
        status, headers, body = self.request("/intake.html")

        self.assertEqual(200, status)
        self.assertIn("text/html", headers["content-type"])
        self.assertIn("Decálogo do sintoma".encode(), body)
        self.assertIn("Falta de ar".encode(), body)
        self.assertIn(b".choice.selected", body)
        self.assertIn(b"detailOnPositive", body)
        self.assertIn("O que você percebeu? Selecione todas as opções que se aplicam.".encode(), body)
        self.assertIn("Batimento irregular".encode(), body)
        self.assertIn("Qual medicamento, dose e frequência?".encode(), body)
        self.assertIn("Não precisa saber o nome técnico.".encode(), body)
        self.assertIn("Colecistectomia".encode(), body)
        self.assertIn(b"(confirmar)", body)
        self.assertIn(b"exclusiveOptions", body)
        self.assertIn(b"questionIsComplete", body)
        self.assertIn(b"value.startsWith('Nenhum')", body)
        self.assertIn("Nenhum upload foi feito".encode(), body)
        self.assertIn("Usar anexo na reavaliação".encode(), body)
        self.assertIn("não envia nem interpreta".encode(), body)
        self.assertIn("Conferir gate de conduta".encode(), body)
        self.assertIn(b"suggested-exams", body)
        self.assertIn(b"exam-photo", body)
        self.assertIn(b'capture="environment"', body)
        self.assertIn("Tirar ou anexar foto de outro exame".encode(), body)
        self.assertIn("Anexar resultado".encode(), body)
        self.assertIn(b"dataset.examKey", body)
        self.assertIn("O que este exame decide".encode(), body)
        self.assertIn("Quando considerar".encode(), body)
        self.assertIn(b"conduct-plan", body)
        self.assertIn(b"conduct-destination", body)
        self.assertIn(b"save-conduct", body)
        self.assertIn(b"professional_conduct_saved", body)
        self.assertIn(b"/api/readiness", body)
        self.assertIn(b"/intake-routing.js", body)
        self.assertIn(b"/intake-sequences.js", body)
        self.assertIn(b"/intake-patient.js", body)
        self.assertIn(b"/intake-cases.js", body)
        self.assertIn(b"/intake-reasoning.js", body)
        self.assertIn(b"/intake-syndromic-engine.js", body)
        self.assertIn(b"/intake-diagnostic-engine.js", body)
        self.assertIn(b"/intake-therapeutic-engine.js", body)
        self.assertIn(b"/intake-confidence-gate.js", body)
        self.assertIn(b"/intake-llm-standby.js", body)
        self.assertIn(b"/intake-clinical-orchestrator.js", body)
        self.assertIn(b"/intake-engine-gate-cases.js", body)
        self.assertIn(b"Motores cl\xc3\xadnicos", body)
        self.assertIn(b"Motor Sindr\xc3\xb4mico", body)
        self.assertIn(b"Motor Diagn\xc3\xb3stico", body)
        self.assertIn(b"Motor Terap\xc3\xaautico", body)
        self.assertIn(b"Caso complexo \xe2\x80\x94 LLM em standby", body)
        self.assertIn(b"Determin\xc3\xadstico, sem LLM", body)
        self.assertIn(b"clinical_orchestration_completed", body)
        self.assertIn(b"decisionmed.intake-audit.v3", body)
        self.assertIn(b"engine-gate-count", body)
        self.assertIn(b"Testar gate 1/30", body)
        self.assertIn(b"structured-summary", body)
        self.assertIn(b"audit-trail", body)
        self.assertIn(b"decisionmed.intake-audit.v2", body)
        self.assertIn(b"crypto.subtle.digest", body)
        self.assertIn(b"answer_confirmed", body)
        self.assertIn(b"modules_confirmed", body)
        self.assertIn("Laboratório de simulação".encode(), body)
        self.assertIn(b"case-mode", body)
        self.assertIn(b"case-count", body)
        self.assertIn(b"buildSuite", body)
        self.assertIn("Iniciar simulação 1/45".encode(), body)
        self.assertIn(b"/intake-sources.js", body)
        self.assertIn(b"/api/evidence-sources", body)
        self.assertIn(b"source-legend", body)
        self.assertIn("FONTE ESPECÍFICA PENDENTE".encode(), body)
        self.assertIn("CASO SINTÉTICO — NÃO É PACIENTE REAL".encode(), body)
        self.assertIn(b"next-test-case", body)
        self.assertIn(b"safety-panel", body)
        self.assertIn(b"syndrome-options", body)
        self.assertIn(b"continue-reasoning", body)
        self.assertIn(b"mode-assisted", body)
        self.assertIn(b"mode-direct", body)
        self.assertIn(b"mode-investigation", body)
        self.assertIn(b'fieldset class="patient-context hidden"', body)
        self.assertIn(b'id="patient-name"', body)
        self.assertIn(b'id="patient-age"', body)
        self.assertIn(b'id="patient-error"', body)
        self.assertIn(b'maxlength="120"', body)
        self.assertIn(b'min="0" max="130" step="1"', body)
        self.assertIn(b"DecisionMedPatient.validateStart", body)
        self.assertIn(b"patient:patientAuditRecord()", body)
        self.assertIn(b"PACIENTE:", body)
        self.assertIn(b"IDADE:", body)
        self.assertIn(b"direct-syndrome-choices", body)
        self.assertIn(b"investigation-syndrome-choices", body)
        self.assertIn(b"begin-investigation", body)
        self.assertIn("Comparação qualitativa das hipóteses".encode(), body)
        self.assertIn("Por que estou perguntando?".encode(), body)
        self.assertIn(b"question-rationale", body)
        self.assertIn(b"initializeTargetedCase", body)
        self.assertIn(b"flow_mode", body)
        self.assertIn(b"reassessment-impact", body)
        self.assertIn(b"impression-status", body)
        self.assertIn("Graves que não podem ser perdidos".encode(), body)
        self.assertIn("MÓDULOS PERCORRIDOS".encode(), body)
        self.assertIn("Justificativa do roteamento".encode(), body)
        self.assertIn(b"cardiology", body)
        self.assertNotIn(b"innerHTML", body)
        self.assertEqual("DENY", headers["x-frame-options"])

    def test_adaptive_intake_router_is_served_locally(self) -> None:
        status, headers, body = self.request("/intake-routing.js")
        rules_status, rules_headers, rules_body = self.request(
            "/intake-routing-rules.js"
        )
        engine_status, engine_headers, engine_body = self.request(
            "/intake-rule-engine.js"
        )

        self.assertEqual(200, status)
        self.assertIn("javascript", headers["content-type"])
        self.assertIn(b"configureRules", body)
        self.assertIn(b"evaluateRules", body)
        self.assertIn(b"generalmedicine", body)
        self.assertIn(b"module.exports", body)
        self.assertNotIn(b"fetch(", body)
        self.assertEqual(200, rules_status)
        self.assertIn("javascript", rules_headers["content-type"])
        self.assertIn(b"route.pattern.possible-anginal-equivalent", rules_body)
        self.assertEqual(200, engine_status)
        self.assertIn("javascript", engine_headers["content-type"])
        self.assertIn(b"evaluateCondition", engine_body)
        self.assertIn(b'"all"', engine_body)
        self.assertIn(b'"any"', engine_body)
        self.assertIn(b'"none"', engine_body)

    def test_adaptive_sequence_generator_is_served_locally(self) -> None:
        status, headers, body = self.request("/intake-sequences.js")

        self.assertEqual(200, status)
        self.assertIn("javascript", headers["content-type"])
        self.assertIn(b"buildSymptomQuestions", body)
        self.assertIn(b"symptom.fever_measurement", body)
        self.assertIn(b"symptom.radiation", body)
        self.assertIn(b"module.exports", body)

    def test_synthetic_case_generator_is_served_locally(self) -> None:
        status, headers, body = self.request("/intake-cases.js")

        self.assertEqual(200, status)
        self.assertIn("javascript", headers["content-type"])
        self.assertIn(b"buildCases", body)
        self.assertIn(b"cardiac-equivalent", body)
        self.assertIn(b"expectedModules", body)
        self.assertNotIn(b"fetch(", body)

    def test_source_presenter_is_served_locally(self) -> None:
        status, headers, body = self.request("/intake-sources.js")

        self.assertEqual(200, status)
        self.assertIn("javascript", headers["content-type"])
        self.assertIn(b"citationLabel", body)
        self.assertIn(b"legendEntries", body)
        self.assertIn(b"FONTE ESPEC", body)
        self.assertNotIn(b"fetch(", body)

    def test_syndromic_reasoning_engine_is_served_locally(self) -> None:
        status, headers, body = self.request("/intake-reasoning.js")

        self.assertEqual(200, status)
        self.assertIn("javascript", headers["content-type"])
        self.assertIn(b"problemRepresentation", body)
        self.assertIn(b"safetyAssessment", body)
        self.assertIn(b"discriminatorQuestions", body)
        self.assertIn(b"cannotMiss", body)
        self.assertIn(b"physicalExam", body)
        self.assertIn("Síndrome torácica aguda".encode(), body)
        self.assertIn("Síndrome coronariana aguda (SCA)".encode(), body)
        self.assertIn(b"ANOCA/INOCA", body)
        self.assertIn(b"initial_syndrome", body)
        self.assertNotIn("Síndrome de desconforto cardiovascular".encode(), body)
        self.assertNotIn(b"fetch(", body)

    def test_workflow_endpoint_and_unknown_specialty(self) -> None:
        status, _, body = self.request("/api/workflows/psychiatry")
        missing_status, _, missing_body = self.request("/api/workflows/dermatology")

        self.assertEqual(200, status)
        self.assertEqual(13, len(json.loads(body)["steps"]))
        self.assertFalse(json.loads(body)["clinical_execution_allowed"])
        self.assertEqual(404, missing_status)
        self.assertEqual("workflow_not_found", json.loads(missing_body)["error"])

    def test_governed_form_endpoint_exposes_sources_but_no_execution(self) -> None:
        status, _, body = self.request("/api/form-schemas/cardiology/findings")
        missing_status, _, missing_body = self.request(
            "/api/form-schemas/cardiology/context"
        )
        payload = json.loads(body)

        self.assertEqual(200, status)
        self.assertEqual("reference_only", payload["mode"])
        self.assertFalse(payload["runtime_eligible"])
        self.assertFalse(payload["clinical_execution_allowed"])
        self.assertEqual(
            "symptoms.chest_pain_or_discomfort_present",
            payload["fields"][0]["field_key"],
        )
        self.assertFalse(payload["fields"][0]["runtime_eligible"])
        knowledge = payload["fields"][0]["knowledge"]
        source = knowledge["evidence_sources"][0]
        self.assertIsNone(payload["review_due_on"])
        self.assertEqual("unscheduled", payload["review_state"])
        self.assertEqual("evidence", knowledge["object_type"])
        self.assertEqual("Synthetic applicability.", knowledge["applicability"])
        self.assertEqual("Synthetic limits.", knowledge["limits"])
        self.assertFalse(knowledge["runtime_eligible"])
        self.assertIsNone(knowledge["review_due_on"])
        self.assertEqual("unscheduled", knowledge["review_state"])
        self.assertEqual("insufficient", source["evidence_quality"])
        self.assertEqual(
            "insufficient_for_recommendation",
            source["recommendation_strength"],
        )
        self.assertEqual("2026-07-21", source["reviewed_on"])
        self.assertIsNone(source["review_due_on"])
        self.assertEqual("unscheduled", source["review_state"])
        self.assertEqual("Synthetic conflicts.", source["known_conflicts"])
        self.assertFalse(source["runtime_eligible"])
        self.assertEqual("Table 3 — Nature", source["anchors"][0]["section"])
        self.assertEqual(
            "https://example.test/official-guideline#table-3",
            source["anchors"][0]["locator"],
        )
        self.assertFalse(source["anchors"][0]["runtime_eligible"])
        self.assertEqual(
            "https://example.test/official-guideline",
            payload["fields"][0]["knowledge"]["evidence_sources"][0]["locator"],
        )
        self.assertEqual(404, missing_status)
        self.assertEqual("form_schema_not_found", json.loads(missing_body)["error"])

    def test_generic_workflow_page_is_served(self) -> None:
        status, _, body = self.request("/workflow.html?specialty=cardiology")

        self.assertEqual(200, status)
        self.assertIn(b"api/workflows", body)
        self.assertIn(b"api/form-schemas", body)
        self.assertIn(b"known_conflicts", body)
        self.assertIn(b"review_due_on", body)
        self.assertIn(b"review_state", body)
        self.assertIn("Seção específica".encode(), body)
        self.assertIn("Base científica e limites".encode(), body)
        self.assertIn("somente referência".encode(), body.lower())
        self.assertIn(b"Fluxo governado", body)
        self.assertIn(b"data-workspace=\"governed-reference\"", body)
        self.assertNotIn(b"<textarea", body.lower())
        self.assertNotIn(b"innerHTML", body)

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

    @staticmethod
    def _catalogs() -> SimpleNamespace:
        draft = SimpleNamespace(value="draft")
        field = SimpleNamespace(
            field_key="symptoms.chest_pain_or_discomfort_present",
            label="Dor ou desconforto torácico presente",
            section=SimpleNamespace(value="symptoms"),
            value_type=SimpleNamespace(value="boolean"),
            knowledge_object_id="knowledge.cardiology.chest-pain-presence",
            required=False,
            allowed_values=(),
        )
        schema = SimpleNamespace(
            schema_id="schema.cardiology.chest-pain.findings",
            specialty_key="cardiology",
            workflow_id="decisionmed.cardiology.workflow.v1",
            step_key="findings",
            version="0.1.0",
            status=draft,
            reviewed_on=None,
            review_due_on=None,
            review_state="unscheduled",
            review_overdue=False,
            validated_by=None,
            fields=(field,),
        )
        knowledge = SimpleNamespace(
            object_id="knowledge.cardiology.chest-pain-presence",
            official_name="Synthetic chest pain presence",
            object_type=SimpleNamespace(value="evidence"),
            description="Synthetic description.",
            version="0.1.0",
            status=draft,
            reviewed_on=None,
            review_due_on=None,
            review_state="unscheduled",
            review_overdue=False,
            validated_by=None,
            applicability="Synthetic applicability.",
            limits="Synthetic limits.",
            evidence_anchors=(
                SimpleNamespace(
                    source_id="acc-aha.2021.chest-pain-guideline",
                    section="Table 3 — Nature",
                    locator="https://example.test/official-guideline#table-3",
                ),
            ),
            evidence_source_ids=("acc-aha.2021.chest-pain-guideline",),
        )
        source = SimpleNamespace(
            source_id="acc-aha.2021.chest-pain-guideline",
            title="Official synthetic guideline fixture",
            publication_year=2021,
            evidence_type=SimpleNamespace(value="guideline"),
            evidence_quality=SimpleNamespace(value="insufficient"),
            recommendation_strength=SimpleNamespace(
                value="insufficient_for_recommendation"
            ),
            locator="https://example.test/official-guideline",
            version="1.0.0",
            status=draft,
            specialties=("cardiology",),
            reviewed_on=date(2026, 7, 21),
            known_conflicts="Synthetic conflicts.",
            clinical_applicability="Synthetic clinical applicability.",
            review_due_on=None,
            review_state="unscheduled",
            review_overdue=False,
        )
        safety_specification = SimpleNamespace(
            check_id="check.synthetic-safety",
            specialty_key="cardiology",
            status=draft,
            review_due_on=None,
            review_state="unscheduled",
            review_overdue=False,
        )
        form_schemas = Mock()

        def require_schema(
            specialty_key: str, workflow_id: str, step_key: str
        ) -> SimpleNamespace:
            if (
                specialty_key,
                workflow_id,
                step_key,
            ) != (
                "cardiology",
                "decisionmed.cardiology.workflow.v1",
                "findings",
            ):
                raise KnowledgeError(
                    "specialty_form_schema_registry.unknown", "not registered"
                )
            return schema

        form_schemas.require.side_effect = require_schema
        form_schemas.all.return_value = (schema,)
        knowledge_registry = Mock()
        knowledge_registry.require.return_value = knowledge
        knowledge_registry.all.return_value = (knowledge,)
        evidence_registry = Mock()
        evidence_registry.require.return_value = source
        evidence_registry.all.return_value = (source,)
        safety_checks = Mock()
        safety_checks.all.return_value = (safety_specification,)
        return SimpleNamespace(
            manifest=SimpleNamespace(
                catalog_id="decisionmed.knowledge",
                release_version="0.5.0",
                status=draft,
            ),
            form_schemas=form_schemas,
            knowledge=knowledge_registry,
            evidence=evidence_registry,
            safety_checks=safety_checks,
        )

    @staticmethod
    def _safety_providers(
        *,
        bound: bool = False,
        incompatible: bool = False,
        partial: bool = False,
    ) -> Mock:
        registry = Mock()
        registry.all.return_value = (
            (SimpleNamespace(check_id="check.synthetic-safety"),)
            if bound or incompatible or partial
            else ()
        )
        registry.coverage.return_value = SimpleNamespace(
            complete=bound and not incompatible and not partial,
            missing_check_ids=("check.second-synthetic-safety",)
            if partial
            else ()
            if bound or incompatible
            else ("check.synthetic-safety",),
            incompatible_check_ids=("check.synthetic-safety",)
            if incompatible
            else (),
        )
        return registry

    @staticmethod
    def _safety_evaluators(providers: Mock) -> Mock:
        registry = Mock()
        registry.providers = providers
        registry.all.return_value = (
            (SimpleNamespace(check_id="check.synthetic-safety"),)
        )
        registry.missing_check_ids = ()
        registry.complete = True
        return registry


if __name__ == "__main__":
    unittest.main()
