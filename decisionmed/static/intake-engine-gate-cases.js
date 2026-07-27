(function exposeDecisionMedEngineGateCases(root, factory) {
  let orchestrator = root.DecisionMedClinicalOrchestrator;
  if (typeof module === "object" && module.exports) {
    orchestrator = require("./intake-clinical-orchestrator.js");
  }
  const api = factory(orchestrator);
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.DecisionMedEngineGateCases = api;
})(typeof globalThis === "object" ? globalThis : this, function createEngineGateCases(orchestrator) {
  "use strict";

  const VERSION = "1.0.0";
  const MODES = Object.freeze(["assisted", "direct", "investigation"]);
  const HIGH_SCENARIOS = Object.freeze([
    ["cardiovascular_discomfort", "Síndrome torácica aguda", "Síndrome coronariana aguda", 0.951],
    ["respiratory", "Dispneia em investigação", "Insuficiência cardíaca aguda", 0.956],
    ["lower_urinary_tract", "Sintomas do trato urinário inferior", "Infecção do trato urinário", 0.961],
    ["cutaneous", "Lesão cutânea em investigação", "Dermatose inflamatória", 0.966],
    ["musculoskeletal", "Apresentação musculoesquelética", "Dor musculoesquelética", 0.971],
    ["visual", "Alteração visual ou ocular", "Doença ocular aguda", 0.952],
    ["abdominal", "Dor abdominal aguda", "Síndrome abdominal aguda", 0.957],
    ["gynecologic_pelvic", "Alteração ginecológica ou pélvica", "Doença ginecológica", 0.962],
    ["obstetric", "Sinais e sintomas obstétricos", "Condição obstétrica estável", 0.967],
    ["mental_health", "Alteração de humor, sono ou pensamento", "Síndrome psiquiátrica", 0.972],
    ["metabolic_endocrine", "Alteração metabólica ou endócrina", "Doença metabólica", 0.953],
    ["systemic_inflammatory", "Doença inflamatória sistêmica", "Vasculite sistêmica", 0.958],
    ["musculoskeletal", "Apresentação musculoesquelética", "Dor musculoesquelética", 0.963],
    ["respiratory", "Dispneia em investigação", "Doença respiratória aguda", 0.968],
    ["metabolic_endocrine", "Alteração metabólica ou endócrina", "Doença endócrina", 0.973],
  ]);
  const COMPLEX_REASONS = Object.freeze([
    "calibrated_score_missing",
    "confidence_not_above_threshold",
    "confidence_not_above_threshold",
    "confidence_provenance_missing",
    "calibration_not_validated",
    "dominant_hypothesis",
    "clinical_instability",
    "criteria_insufficient",
    "severe_conflict_present",
    "module_not_validated",
    "content_not_validated",
    "clinical_execution_blocked",
    "critical_evidence_pending",
    "post_exam_conflict",
    "unresolved_competition",
  ]);

  function stableStringify(value) {
    if (Array.isArray(value)) return `[${value.map(stableStringify).join(",")}]`;
    if (value && typeof value === "object") {
      return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`).join(",")}}`;
    }
    return JSON.stringify(value);
  }

  function digest(value) {
    const text = stableStringify(value);
    let hash = 2166136261;
    for (let index = 0; index < text.length; index += 1) {
      hash ^= text.charCodeAt(index);
      hash = Math.imul(hash, 16777619);
    }
    return `fnv1a32:${(hash >>> 0).toString(16).padStart(8, "0")}`;
  }

  function syndrome(key, name, dominant, validated = true) {
    return {
      key,
      moduleId: `fixture.module.${key}`,
      name,
      entityType: "initial_syndrome",
      entityTypeLabel: "Síndrome clínica inicial",
      compatibility: "alto",
      supports: ["Manifestação principal presente", "Padrão temporal compatível", "Achado discriminador presente"],
      against: [],
      redFlags: [],
      stopConditions: [],
      sourceIds: ["fixture.source.guideline"],
      contentSourceIds: ["fixture.source.guideline"],
      moduleVersion: "fixture-1.0.0",
      moduleStatus: validated ? "validated" : "draft",
      contentVersion: "fixture-1.0.0",
      contentRecordStatus: validated ? "validated" : "draft",
      terminologyStatus: "validated",
      differential: {
        likely: [dominant],
        cannotMiss: [],
        mimics: ["Hipótese alternativa sintética"],
      },
      contraryFindings: [],
      diagnosticCriteria: [],
      physicalExam: ["Exame físico dirigido sintético"],
      tests: [{ name: "Exame complementar sintético", question: "Este resultado diferencia a hipótese dominante?", when: "Quando indicado na fixture.", sourceIds: ["fixture.source.guideline"] }],
      safetyConduct: ["Reavaliar estabilidade clínica"],
      symptomaticCare: ["Alívio sintomático sintético explicitamente separado"],
      initialTreatment: ["Medida inicial sintética para revisão"],
      definitiveTreatment: ["Tratamento definitivo sintético para revisão"],
      postExamReassessment: ["Reavaliar a hipótese após o resultado"],
      destinationReturnFollowup: ["Definir retorno e sinais de alarme"],
    };
  }

  function baseInput(index, high) {
    const scenario = HIGH_SCENARIOS[index % HIGH_SCENARIOS.length];
    const mode = MODES[Math.floor(index / 5)];
    const competing =
      mode === "investigation"
        ? syndrome(
            `competing_${scenario[0]}`,
            `Hipótese concorrente de ${scenario[1]}`,
            "Hipótese concorrente sintética",
            true,
          )
        : null;
    const selectedSyndromeKeys = competing
      ? [scenario[0], competing.key]
      : [scenario[0]];
    const facts = {
      flowMode: mode,
      complaint: scenario[1],
      answers: ["Manifestação principal presente", "Padrão temporal compatível", "Achado discriminador presente"],
      selectedSyndromeKeys,
      reassessments: [],
    };
    const inputDigest = digest(facts);
    return {
      facts,
      reasoning: {
        representation: `${scenario[1]} com padrão sintético governado.`,
        safety: { level: "continue", label: "Fluxo pode continuar", reasons: [] },
        syndromes: [syndrome(scenario[0], scenario[1], scenario[2], true), ...(competing ? [competing] : [])],
      },
      selectedSyndromeKeys,
      reassessments: [],
      professionalImpression: { hypothesis: scenario[2], status: "Confirmada na fixture sintética" },
      professionalConfirmation: true,
      clinicalExecutionAllowed: true,
      confidenceEvidence: {
        score: high ? scenario[3] : null,
        calibrated: high,
        calibrationStatus: high ? "validated" : "missing",
        dominantHypothesis: scenario[2],
        criteriaSufficient: true,
        unresolvedCriticalConflict: false,
        cannotMissExcluded: true,
        criticalEvidencePending: false,
        postExamConflict: false,
        unresolvedCompetition: false,
        contentComplete: true,
        sourceBindingValidated: true,
        governanceAuthority: "registered_fixture",
        inputDigest,
        registeredInputDigest: inputDigest,
        provenance: high ? {
          method: "synthetic_fixture_calibration",
          modelVersion: "fixture.calibrator.v1",
          validationSetId: "fixture.engine-gate.v1",
          calibratedAt: "2026-07-26",
          reviewedBy: "fixture-governance",
        } : null,
      },
    };
  }

  function complexInput(index) {
    const input = baseInput(index, true);
    const evidence = input.confidenceEvidence;
    switch (index) {
      case 0: evidence.score = null; evidence.calibrated = false; break;
      case 1: evidence.score = 0.95; break;
      case 2: evidence.score = 0.949; break;
      case 3: evidence.provenance = null; break;
      case 4: evidence.calibrationStatus = "draft"; break;
      case 5: evidence.dominantHypothesis = null; break;
      case 6: input.reasoning.safety = { level: "immediate", label: "Atendimento imediato", reasons: ["Instabilidade sintética"] }; break;
      case 7: evidence.criteriaSufficient = false; break;
      case 8: evidence.unresolvedCriticalConflict = true; break;
      case 9: input.reasoning.syndromes[0].moduleStatus = "draft"; break;
      case 10: input.reasoning.syndromes[0].contentRecordStatus = "draft"; break;
      case 11: input.clinicalExecutionAllowed = false; break;
      case 12: evidence.criticalEvidencePending = true; break;
      case 13: evidence.postExamConflict = true; input.reassessments = [{ hypothesis: evidence.dominantHypothesis, impact: "Exige reformular a classificação clínica", examName: "Exame sintético", finding: "Resultado contraditório" }]; break;
      case 14: evidence.unresolvedCompetition = true; break;
      default: break;
    }
    return input;
  }

  function fixture(id, mode, kind, input, expectedReasonCode = null) {
    return Object.freeze({
      id,
      schemaVersion: "decisionmed.engine-gate-fixture.v1",
      fixtureOnly: true,
      simulationOnly: true,
      mode,
      kind,
      inputDigest: input.confidenceEvidence.inputDigest,
      input,
      expected: Object.freeze({
        route: kind === "high" ? "deterministic_no_llm" : "complex_case_llm_standby",
        reasonCode: expectedReasonCode,
        llm: Object.freeze({ disabled: true, provider: null, invoked: false, transmitted: false, tokenUsage: 0 }),
      }),
    });
  }

  const FIXTURES = Object.freeze([
    ...HIGH_SCENARIOS.map((_, index) => {
      const input = baseInput(index, true);
      return fixture(
        `fixture.engine-gate.high.${String(index + 1).padStart(2, "0")}`,
        MODES[Math.floor(index / 5)],
        "high",
        input,
      );
    }),
    ...COMPLEX_REASONS.map((reason, index) => {
      const input = complexInput(index);
      return fixture(
        `fixture.engine-gate.complex.${String(index + 1).padStart(2, "0")}`,
        MODES[Math.floor(index / 5)],
        "complex",
        input,
        reason,
      );
    }),
  ]);
  const BY_ID = new Map(FIXTURES.map((item) => [item.id, item]));

  function buildEngineGateSuite(kind = "all") {
    if (kind === "high" || kind === "complex") {
      return Object.freeze(FIXTURES.filter((item) => item.kind === kind));
    }
    return FIXTURES;
  }

  function runFixture(id, options = {}) {
    const item = BY_ID.get(id);
    if (!item) throw new Error(`Unknown engine gate fixture: ${id}`);
    const canonicalDigest = digest(item.input.facts);
    const suppliedFacts = options.facts || item.input.facts;
    const suppliedDigest = digest(suppliedFacts);
    const input = {
      ...item.input,
      confidenceEvidence: {
        ...item.input.confidenceEvidence,
        inputDigest: suppliedDigest,
        registeredInputDigest: canonicalDigest,
      },
    };
    const result = orchestrator.run(input);
    return Object.freeze({
      fixtureId: item.id,
      fixtureOnly: true,
      simulationOnly: true,
      publicClinicalExecutionAllowed: false,
      automaticPrescriptionAllowed: false,
      inputDigest: suppliedDigest,
      result,
    });
  }

  return Object.freeze({
    version: VERSION,
    fixtureCount: FIXTURES.length,
    buildEngineGateSuite,
    runFixture,
    digest,
  });
});
