(function exposeDecisionMedClinicalOrchestrator(root, factory) {
  let syndromic = root.DecisionMedSyndromicEngine;
  let diagnostic = root.DecisionMedDiagnosticEngine;
  let therapeutic = root.DecisionMedTherapeuticEngine;
  let confidenceGate = root.DecisionMedConfidenceGate;
  let llmStandby = root.DecisionMedLlmStandby;
  if (typeof module === "object" && module.exports) {
    syndromic = require("./intake-syndromic-engine.js");
    diagnostic = require("./intake-diagnostic-engine.js");
    therapeutic = require("./intake-therapeutic-engine.js");
    confidenceGate = require("./intake-confidence-gate.js");
    llmStandby = require("./intake-llm-standby.js");
  }
  const api = factory(syndromic, diagnostic, therapeutic, confidenceGate, llmStandby);
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.DecisionMedClinicalOrchestrator = api;
})(
  typeof globalThis === "object" ? globalThis : this,
  function createClinicalOrchestrator(
    syndromicEngine,
    diagnosticEngine,
    therapeuticEngine,
    confidenceGate,
    llmStandby,
  ) {
    "use strict";

    const VERSION = "1.2.0";
    if (!syndromicEngine || !diagnosticEngine || !therapeuticEngine || !confidenceGate || !llmStandby) {
      throw new Error("DecisionMed clinical motor dependency is unavailable");
    }

    function run(input = {}) {
      const syndromic = syndromicEngine.analyze({
        reasoning: input.reasoning,
        selectedSyndromeKeys: input.selectedSyndromeKeys,
      });
      const diagnostic = diagnosticEngine.analyze({
        reasoning: input.reasoning,
        syndromic,
        diagnosticProfiles: input.diagnosticProfiles,
        reassessments: input.reassessments,
        professionalImpression: input.professionalImpression,
      });
      const therapeutic = therapeuticEngine.analyze({
        reasoning: input.reasoning,
        syndromic,
        diagnostic,
        reassessments: input.reassessments,
        professionalImpression: input.professionalImpression,
        knownSourceIds: input.knownSourceIds,
        professionalConfirmation: input.professionalConfirmation,
        clinicalExecutionAllowed: input.clinicalExecutionAllowed,
      });
      const gate = confidenceGate.evaluate({
        syndromic,
        diagnostic,
        therapeutic,
        confidenceEvidence: input.confidenceEvidence,
      });
      const llm = llmStandby.status({ route: gate.route, reasons: gate.reasons });
      const audit = Object.freeze([
        Object.freeze({ order: 1, engine: syndromic.engine, version: syndromic.version, output: syndromic.status, classificationKeys: Object.freeze(syndromic.classifications.map((item) => item.key)) }),
        Object.freeze({ order: 2, engine: diagnostic.engine, version: diagnostic.version, output: diagnostic.status, candidateKeys: Object.freeze(diagnostic.candidates.map((item) => item.key)) }),
        Object.freeze({ order: 3, engine: therapeutic.engine, version: therapeutic.version, output: therapeutic.status, hypothesisKeys: Object.freeze(therapeutic.plan.map((item) => item.hypothesisKey)), automaticTreatmentAllowed: false, automaticPrescriptionAllowed: false }),
        Object.freeze({ order: 4, engine: gate.engine, version: gate.version, output: gate.route, reasonCodes: Object.freeze([...gate.reasonCodes]), confidenceProvenance: gate.provenance }),
        Object.freeze({ order: 5, engine: llm.adapter, version: llm.version, output: "standby_not_invoked", invoked: false, transmitted: false, tokenUsage: 0 }),
      ]);

      return Object.freeze({
        engine: "DecisionMedClinicalOrchestrator",
        version: VERSION,
        sequence: Object.freeze([
          "syndromic",
          "diagnostic",
          "therapeutic",
          "confidence_gate",
          gate.route === "deterministic_no_llm" ? "deterministic_response" : "llm_standby",
        ]),
        syndromic,
        diagnostic,
        therapeutic,
        gate,
        llm,
        deterministicResponse:
          gate.route === "deterministic_no_llm"
            ? Object.freeze({
                generatedWithoutLlm: true,
                dominantHypothesis: input.confidenceEvidence.dominantHypothesis,
                therapeuticStatus: therapeutic.status,
                professionalConfirmationRequired: true,
                automaticTreatmentAllowed: false,
                automaticPrescriptionAllowed: false,
                simulationOnly: input.confidenceEvidence.governanceAuthority === "registered_fixture",
              })
            : null,
        audit,
      });
    }

    return Object.freeze({ version: VERSION, run });
  },
);
