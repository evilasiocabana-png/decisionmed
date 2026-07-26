"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const orchestrator = require("../decisionmed/static/intake-clinical-orchestrator.js");
const confidenceGate = require("../decisionmed/static/intake-confidence-gate.js");
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
  assert.equal(result.audit[3].confidenceProvenance.validationSetId, "fixture.engine-gate.v1");
  assert.equal(result.audit[4].invoked, false);
  assert.equal(result.audit[4].transmitted, false);
});
