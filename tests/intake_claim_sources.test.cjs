"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const sources = require("../decisionmed/static/intake-sources.js");
const cases = require("../decisionmed/static/intake-cases.js");

const evidencePath = [
  path.join(__dirname, "..", "knowledge-release", "evidence.json"),
  path.join(__dirname, "..", "..", "DecisionMEd-Knowledge", "evidence.json"),
].find((candidate) => fs.existsSync(candidate));
assert.ok(evidencePath, "DecisionMEd knowledge evidence catalog is available");
const evidence = JSON.parse(fs.readFileSync(evidencePath, "utf8")).items;
const evidenceIds = new Set(evidence.map((item) => item.source_id));

test("source presenter uses abbreviations without exposing raw ids in clinical text", () => {
  const hydration = sources.configure([
    {
      source_id: "acc.2025.acute-coronary-syndromes",
      citation_label: "ACC/AHA 2025",
      title: "Guideline for Acute Coronary Syndromes",
      publisher: "ACC/AHA",
      publication_year: 2025,
      version: "1.0.0",
      status: "draft",
      locator: "https://www.jacc.org/guidelines/acute-coronary-syndromes",
    },
  ]);

  assert.deepEqual(hydration, { count: 1, complete: true });
  assert.equal(
    sources.citationText(["acc.2025.acute-coronary-syndromes"]),
    "[ACC/AHA 2025]",
  );
  assert.doesNotMatch(
    sources.citationText(["acc.2025.acute-coronary-syndromes"]),
    /acc\.2025/,
  );
  assert.equal(
    sources.displayStatus("draft"),
    "Referência vinculada · revisão clínica pendente",
  );
  assert.equal(
    sources.displayStatus("structural_review_only"),
    "Plano estrutural em revisão · uso clínico automático bloqueado",
  );
});

test("source presenter declares missing citations instead of silently omitting them", () => {
  sources.configure([]);
  assert.equal(sources.citationText([]), "[FONTE ESPECÍFICA PENDENTE]");
  assert.equal(sources.citationText([], "case"), "[CASO]");
  const claim = sources.claim("Afirmação sem binding", []);
  assert.equal(claim.cited, false);
  assert.deepEqual(claim.sourceIds, []);
});

test("all 45 generated cases have complete, cited, simulation-only conclusions", () => {
  const suite = cases.buildSuite(15, "all");
  assert.equal(suite.length, 45);

  for (const scenario of suite) {
    const completion = scenario.syntheticCompletion;
    assert.equal(cases.isSyntheticCompletionComplete(completion), true, scenario.id);
    assert.equal(completion.status, "simulation_only");
    assert.equal(completion.simulationOnly, true);
    assert.equal(completion.governance.validationStatus, "not_validated");
    assert.equal(completion.governance.clinicalExecutionAllowed, false);
    assert.equal(completion.governance.automaticTreatmentAllowed, false);
    assert.equal(completion.governance.automaticPrescriptionAllowed, false);
    assert.equal(completion.governance.llmUsed, false);
    assert.ok(completion.postExam.results.length > 0);
    assert.ok(completion.conduct.treatment.length > 0);
    assert.ok(completion.conduct.returnPrecautions.length > 0);
    assert.ok(completion.conduct.followUp.length > 0);

    const usedSourceIds = cases.sourceIdsForCase(scenario);
    assert.ok(usedSourceIds.length > 0, scenario.id);
    for (const sourceId of usedSourceIds) {
      assert.equal(
        evidenceIds.has(sourceId),
        true,
        `${scenario.id} uses unknown source ${sourceId}`,
      );
    }
  }
});

test("source registry filters non-http locators from presentation", () => {
  sources.configure([
    {
      source_id: "local.source",
      citation_label: "LOCAL",
      title: "Local fixture",
      status: "draft",
      locator: "C:\\private\\guideline.pdf",
    },
  ]);
  assert.equal(sources.get("local.source").locator, null);
});
