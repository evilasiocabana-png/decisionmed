"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const orchestrator = require("../decisionmed/static/intake-clinical-orchestrator.js");
const confidenceGate = require("../decisionmed/static/intake-confidence-gate.js");
const therapeuticEngine = require("../decisionmed/static/intake-therapeutic-engine.js");
const llmStandby = require("../decisionmed/static/intake-llm-standby.js");
const engineCases = require("../decisionmed/static/intake-engine-gate-cases.js");
const legacyCases = require("../decisionmed/static/intake-cases.js");

const fixtures = engineCases.buildEngineGateSuite();
const highFixtures = fixtures.filter((item) => item.kind === "high");
const complexFixtures = fixtures.filter((item) => item.kind === "complex");

test("engine gate registry contains 15 high and 15 complex isolated fixtures", () => {
  assert.equal(engineCases.fixtureCount, 30);
  assert.equal(highFixtures.length, 15);
  assert.equal(complexFixtures.length, 15);
  assert.equal(new Set(fixtures.map((item) => item.id)).size, 30);
  for (const kindFixtures of [highFixtures, complexFixtures]) {
    assert.deepEqual(
      Object.fromEntries(
        ["assisted", "direct", "investigation"].map((mode) => [
          mode,
          kindFixtures.filter((item) => item.mode === mode).length,
        ]),
      ),
      { assisted: 5, direct: 5, investigation: 5 },
    );
  }
  assert.ok(fixtures.every((item) => item.fixtureOnly && item.simulationOnly));
});

test("all high fixtures are calibrated above 95 percent and use the full motor order", () => {
  for (const fixture of highFixtures) {
    assert.ok(fixture.input.confidenceEvidence.score > 0.95);
    assert.equal(fixture.input.confidenceEvidence.calibrationStatus, "validated");
    assert.ok(fixture.input.confidenceEvidence.provenance.validationSetId);
    const execution = engineCases.runFixture(fixture.id);
    const result = execution.result;
    assert.deepEqual(result.sequence, [
      "syndromic",
      "diagnostic",
      "therapeutic",
      "confidence_gate",
      "deterministic_response",
    ]);
    assert.equal(result.gate.route, "deterministic_no_llm");
    assert.deepEqual(result.gate.reasonCodes, []);
    assert.equal(result.deterministicResponse.generatedWithoutLlm, true);
    assert.equal(result.therapeutic.automaticTreatmentAllowed, false);
    assert.equal(result.therapeutic.automaticPrescriptionAllowed, false);
    assert.equal(execution.publicClinicalExecutionAllowed, false);
    assert.equal(execution.automaticPrescriptionAllowed, false);
  }
});

test("all complex fixtures fail closed for their expected reason", () => {
  for (const fixture of complexFixtures) {
    const result = engineCases.runFixture(fixture.id).result;
    assert.equal(result.gate.route, "complex_case_llm_standby");
    assert.ok(
      result.gate.reasonCodes.includes(fixture.expected.reasonCode),
      `${fixture.id} should include ${fixture.expected.reasonCode}: ${result.gate.reasonCodes.join(", ")}`,
    );
    assert.equal(result.deterministicResponse, null);
  }
});

test("the confidence boundary is strictly greater than 95 percent", () => {
  const exact = engineCases.runFixture("fixture.engine-gate.complex.02").result;
  const below = engineCases.runFixture("fixture.engine-gate.complex.03").result;
  assert.equal(exact.gate.score, 0.95);
  assert.equal(exact.gate.eligible, false);
  assert.equal(below.gate.score, 0.949);
  assert.equal(below.gate.eligible, false);
  assert.equal(confidenceGate.HIGH_CONFIDENCE_THRESHOLD, 0.95);
  assert.equal(confidenceGate.evaluate({}).comparison, "strictly_greater_than");
});

test("qualitative compatibility cannot become numeric confidence", () => {
  const high = JSON.parse(JSON.stringify(highFixtures[0].input));
  delete high.confidenceEvidence;
  high.reasoning.syndromes[0].compatibility = "alto";
  const result = orchestrator.run(high);
  assert.equal(result.gate.score, null);
  assert.equal(result.gate.calibrated, false);
  assert.equal(result.gate.compatibilityUsedAsProbability, false);
  assert.equal(result.gate.route, "complex_case_llm_standby");
});

test("syndromic treatment is never copied into diagnosis-specific plans", () => {
  for (const fixture of highFixtures) {
    const result = engineCases.runFixture(fixture.id).result;
    assert.ok(result.therapeutic.syndromicSupportPlans.length > 0);
    assert.ok(
      result.therapeutic.syndromicSupportPlans.every(
        (item) =>
          item.scope === "syndromic_shared_support" &&
          item.diagnosisSpecificTreatmentIncluded === false &&
          item.preExamSymptomaticCareScope ===
            "explicit_symptom_relief_for_professional_review" &&
          item.preExamSymptomaticCareExplicitlySeparated === true &&
          item.preExamSymptomaticCare.length > 0 &&
          item.preExamInitialCareScope ===
            "syndromic_initial_care_not_assumed_to_be_symptomatic" &&
          item.preExamInitialCare.length > 0 &&
          item.automaticTreatmentAllowed === false &&
          item.automaticPrescriptionAllowed === false &&
          item.safety.length > 0 &&
          item.physicalExam.length > 0 &&
          item.tests.length > 0,
      ),
    );
    assert.equal(result.therapeutic.allTreatmentBindingsValidated, false);
    assert.equal(
      result.therapeutic.unboundTreatmentHypothesisKeys.length,
      result.therapeutic.plan.length,
    );
    for (const item of result.therapeutic.plan) {
      assert.equal(item.contentScope, "unbound");
      assert.equal(item.supportScope, "syndromic_shared_support");
      assert.ok(item.syndromicSupportPlanIds.length > 0);
      assert.equal(item.treatmentBindingStatus, "unbound");
      assert.equal(
        item.treatmentBindingReason,
        "missing_explicit_diagnostic_binding",
      );
      assert.deepEqual(item.initialTreatment, []);
      assert.deepEqual(item.definitiveTreatment, []);
      assert.deepEqual(item.treatmentSourceIds, []);
      assert.equal(item.postExamTreatment.status, "unbound");
      assert.deepEqual(item.postExamTreatment.initial, []);
      assert.deepEqual(item.postExamTreatment.definitive, []);
      assert.equal(item.postExamTreatment.requiresPostExamReassessment, true);
      assert.equal(item.postExamTreatment.requiresProfessionalConfirmation, true);
      assert.deepEqual(item.sourceIds, []);
      assert.ok(item.syndromicSupportSourceIds.length > 0);
      assert.equal(item.status, "treatment_unbound_review_only");
    }
    assert.doesNotMatch(
      JSON.stringify(result.therapeutic.syndromicSupportPlans.map(
        (item) => item.preExamSymptomaticCare,
      )),
      /Medida inicial sintética|Tratamento definitivo sintético/,
    );
    assert.equal(result.therapeutic.automaticTreatmentAllowed, false);
    assert.equal(result.therapeutic.automaticPrescriptionAllowed, false);
  }
});

test("diagnosis-specific treatment requires an explicit fully validated binding", () => {
  const baseline = engineCases.runFixture(highFixtures[0].id).result;
  const candidate = baseline.diagnostic.candidates[0];
  const validatedBinding = {
    scope: "diagnosis_specific",
    status: "validated",
    hypothesisKey: candidate.key,
    hypothesisName: candidate.name,
    moduleId: "module.test.bound-diagnosis",
    contentVersion: "1.2.3",
    moduleStatus: "validated",
    contentRecordStatus: "validated",
    sourceBindingValidated: true,
    sourceIds: ["source.test.bound-treatment"],
    initialTreatment: ["Tratamento inicial explicitamente vinculado."],
    definitiveTreatment: ["Tratamento definitivo explicitamente vinculado."],
  };
  const diagnosticWithBinding = {
    ...baseline.diagnostic,
    candidates: [
      { ...candidate, treatmentBinding: validatedBinding },
      ...baseline.diagnostic.candidates.slice(1),
    ],
  };
  const bound = therapeuticEngine.analyze({
    reasoning: highFixtures[0].input.reasoning,
    syndromic: baseline.syndromic,
    diagnostic: diagnosticWithBinding,
    reassessments: [{
      hypothesis: candidate.name,
      impact: "Aumenta compatibilidade",
      examName: "Exame complementar sintético",
      finding: "Achado sintético compatível",
    }],
    professionalImpression: {
      hypothesis: candidate.name,
      status: "Diagnóstico provável",
    },
    knownSourceIds: ["source.test.bound-treatment"],
    professionalConfirmation: true,
    clinicalExecutionAllowed: true,
  });
  const boundPlan = bound.plan.find((item) => item.hypothesisKey === candidate.key);
  assert.equal(boundPlan.treatmentBindingStatus, "validated");
  assert.equal(boundPlan.contentScope, "diagnosis_specific");
  assert.equal(boundPlan.treatmentModuleId, "module.test.bound-diagnosis");
  assert.equal(boundPlan.treatmentContentVersion, "1.2.3");
  assert.deepEqual(boundPlan.initialTreatment, [
    "Tratamento inicial explicitamente vinculado.",
  ]);
  assert.deepEqual(boundPlan.definitiveTreatment, [
    "Tratamento definitivo explicitamente vinculado.",
  ]);
  assert.deepEqual(boundPlan.treatmentSourceIds, [
    "source.test.bound-treatment",
  ]);
  assert.equal(
    boundPlan.postExamTreatment.status,
    "ready_for_professional_review",
  );
  assert.deepEqual(boundPlan.postExamTreatment.initial, [
    "Tratamento inicial explicitamente vinculado.",
  ]);
  assert.deepEqual(boundPlan.postExamTreatment.definitive, [
    "Tratamento definitivo explicitamente vinculado.",
  ]);
  assert.deepEqual(boundPlan.postExamTreatment.sourceIds, [
    "source.test.bound-treatment",
  ]);
  assert.equal(boundPlan.postExamTreatment.requiresPostExamReassessment, true);
  assert.equal(boundPlan.postExamTreatment.requiresProfessionalConfirmation, true);
  assert.equal(boundPlan.postExamTreatment.relevantReassessmentCount, 1);
  assert.equal(boundPlan.postExamTreatment.reassessmentSupportsTreatment, true);
  assert.equal(boundPlan.postExamTreatment.professionalImpressionMatches, true);
  assert.equal(bound.automaticTreatmentAllowed, false);
  assert.equal(bound.automaticPrescriptionAllowed, false);

  const awaitingReassessment = therapeuticEngine.analyze({
    reasoning: highFixtures[0].input.reasoning,
    syndromic: baseline.syndromic,
    diagnostic: diagnosticWithBinding,
    reassessments: [],
    professionalImpression: {
      hypothesis: candidate.name,
      status: "Diagnóstico provável",
    },
    knownSourceIds: ["source.test.bound-treatment"],
    professionalConfirmation: true,
    clinicalExecutionAllowed: true,
  });
  const awaitingPlan = awaitingReassessment.plan.find(
    (item) => item.hypothesisKey === candidate.key,
  );
  assert.equal(
    awaitingPlan.postExamTreatment.status,
    "awaiting_post_exam_reassessment",
  );
  assert.deepEqual(awaitingPlan.postExamTreatment.initial, []);
  assert.deepEqual(awaitingPlan.postExamTreatment.definitive, []);

  const unknownSource = therapeuticEngine.analyze({
    reasoning: highFixtures[0].input.reasoning,
    syndromic: baseline.syndromic,
    diagnostic: diagnosticWithBinding,
    reassessments: [{
      hypothesis: candidate.name,
      impact: "Aumenta compatibilidade",
      examName: "Exame complementar sintético",
      finding: "Achado sintético compatível",
    }],
    professionalImpression: {
      hypothesis: candidate.name,
      status: "Diagnóstico provável",
    },
    knownSourceIds: [],
    professionalConfirmation: true,
    clinicalExecutionAllowed: true,
  });
  assert.equal(
    unknownSource.plan.find((item) => item.hypothesisKey === candidate.key)
      .postExamTreatment.status,
    "unbound",
  );

  const unvalidated = therapeuticEngine.analyze({
    reasoning: highFixtures[0].input.reasoning,
    syndromic: baseline.syndromic,
    diagnostic: {
      ...diagnosticWithBinding,
      candidates: [
        {
          ...candidate,
          treatmentBinding: { ...validatedBinding, status: "in_review" },
        },
        ...baseline.diagnostic.candidates.slice(1),
      ],
    },
    reassessments: [{
      hypothesis: candidate.name,
      impact: "Aumenta compatibilidade",
      examName: "Exame complementar sintético",
      finding: "Achado sintético compatível",
    }],
    professionalImpression: {
      hypothesis: candidate.name,
      status: "Diagnóstico provável",
    },
    knownSourceIds: ["source.test.bound-treatment"],
    professionalConfirmation: true,
    clinicalExecutionAllowed: true,
  });
  const rejectedPlan = unvalidated.plan.find(
    (item) => item.hypothesisKey === candidate.key,
  );
  assert.equal(rejectedPlan.treatmentBindingStatus, "unbound");
  assert.equal(
    rejectedPlan.treatmentBindingReason,
    "explicit_diagnostic_binding_not_validated",
  );
  assert.deepEqual(rejectedPlan.initialTreatment, []);
  assert.deepEqual(rejectedPlan.definitiveTreatment, []);
  assert.deepEqual(rejectedPlan.treatmentSourceIds, []);
  assert.equal(rejectedPlan.postExamTreatment.status, "unbound");
  assert.deepEqual(rejectedPlan.postExamTreatment.initial, []);
  assert.deepEqual(rejectedPlan.postExamTreatment.definitive, []);
});

test("tampering with canonical fixture facts invalidates the deterministic gate", () => {
  const fixture = highFixtures[0];
  const tamperedFacts = {
    ...fixture.input.facts,
    complaint: `${fixture.input.facts.complaint} alterada`,
  };
  const result = engineCases.runFixture(fixture.id, { facts: tamperedFacts }).result;
  assert.equal(result.gate.route, "complex_case_llm_standby");
  assert.ok(result.gate.reasonCodes.includes("input_integrity_failed"));
});

test("manual confidence payload without registered governance fails closed", () => {
  const input = JSON.parse(JSON.stringify(highFixtures[0].input));
  delete input.confidenceEvidence.governanceAuthority;
  const result = orchestrator.run(input);
  assert.equal(result.gate.route, "complex_case_llm_standby");
  assert.ok(result.gate.reasonCodes.includes("governance_authority_missing"));
});

test("LLM adapter is inert on deterministic and complex routes", () => {
  for (const fixture of fixtures) {
    const llm = engineCases.runFixture(fixture.id).result.llm;
    assert.deepEqual(
      {
        disabled: llm.disabled,
        provider: llm.provider,
        invoked: llm.invoked,
        transmitted: llm.transmitted,
        tokenUsage: llm.tokenUsage,
      },
      { disabled: true, provider: null, invoked: false, transmitted: false, tokenUsage: 0 },
    );
  }
  assert.deepEqual(llmStandby.invoke(), {
    ok: false,
    code: "llm_standby_disabled",
    invoked: false,
    transmitted: false,
    tokenUsage: 0,
  });
  const source = fs.readFileSync(
    path.join(__dirname, "..", "decisionmed", "static", "intake-llm-standby.js"),
    "utf8",
  );
  assert.doesNotMatch(source, /\b(fetch|XMLHttpRequest|WebSocket)\b/);
});

test("post-exam contradiction is diagnostic evidence and cannot bypass the gate", () => {
  const execution = engineCases.runFixture("fixture.engine-gate.complex.14");
  assert.equal(execution.result.gate.route, "complex_case_llm_standby");
  assert.ok(execution.result.gate.reasonCodes.includes("post_exam_conflict"));
  assert.ok(
    execution.result.diagnostic.candidates.some(
      (candidate) => candidate.criteria.conflicting.length > 0,
    ),
  );
});

test("malformed and empty inputs fail closed without calling LLM", () => {
  const result = orchestrator.run({});
  assert.equal(result.gate.route, "complex_case_llm_standby");
  assert.equal(result.llm.invoked, false);
  assert.equal(result.llm.transmitted, false);
  assert.equal(result.llm.tokenUsage, 0);
});

test("legacy 45-case generator stays separate and current draft inputs all route to standby", () => {
  const suite = legacyCases.buildSuite(15, "all");
  assert.equal(suite.length, 45);
  assert.equal(fixtures.some((fixture) => suite.some((item) => item.id === fixture.id)), false);
  for (const scenario of suite) {
    const key = scenario.syndromeKeys[0] || `draft_${scenario.flowMode}`;
    const reasoning = {
      representation: scenario.label,
      safety: { level: "continue", reasons: [] },
      syndromes: [{
        key,
        name: scenario.label,
        compatibility: "alto",
        moduleStatus: "draft",
        contentRecordStatus: "draft",
        supports: [],
        against: [],
        differential: { likely: ["Hipótese em revisão"], cannotMiss: [], mimics: [] },
        physicalExam: [],
        tests: [],
        initialTreatment: [],
        definitiveTreatment: [],
      }],
    };
    const result = orchestrator.run({
      reasoning,
      selectedSyndromeKeys: [key],
      clinicalExecutionAllowed: false,
    });
    assert.equal(result.gate.route, "complex_case_llm_standby");
  }
});

test("orchestrator audit reconstructs versions, order, decisions, and LLM state", () => {
  const result = engineCases.runFixture(highFixtures[0].id).result;
  assert.equal(result.audit.length, 5);
  assert.deepEqual(result.audit.map((item) => item.order), [1, 2, 3, 4, 5]);
  assert.deepEqual(
    result.audit.map((item) => item.engine),
    [
      "DecisionMedSyndromicEngine",
      "DecisionMedDiagnosticEngine",
      "DecisionMedTherapeuticEngine",
      "DecisionMedConfidenceGate",
      "DecisionMedLlmStandby",
    ],
  );
  assert.ok(result.audit.every((item) => item.version));
  assert.equal(result.therapeutic.version, "1.3.0");
  assert.equal(result.audit[2].version, "1.3.0");
  assert.equal(result.audit[3].confidenceProvenance.validationSetId, "fixture.engine-gate.v1");
  assert.equal(result.audit[4].invoked, false);
  assert.equal(result.audit[4].transmitted, false);
});
