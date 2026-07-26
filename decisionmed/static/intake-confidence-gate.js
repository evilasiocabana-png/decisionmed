(function exposeDecisionMedConfidenceGate(root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.DecisionMedConfidenceGate = api;
})(typeof globalThis === "object" ? globalThis : this, function createConfidenceGate() {
  "use strict";

  const VERSION = "1.0.0";
  const HIGH_CONFIDENCE_THRESHOLD = 0.95;
  const REQUIRED_PROVENANCE = Object.freeze([
    "method",
    "modelVersion",
    "validationSetId",
    "calibratedAt",
    "reviewedBy",
  ]);

  function provenanceComplete(provenance) {
    return Boolean(
      provenance &&
        REQUIRED_PROVENANCE.every(
          (field) => typeof provenance[field] === "string" && provenance[field].trim(),
        ),
    );
  }

  function evaluate(input = {}) {
    const syndromic = input.syndromic || { classifications: [], safety: {} };
    const diagnostic = input.diagnostic || { candidates: [] };
    const therapeutic = input.therapeutic || {};
    const evidence = input.confidenceEvidence || {};
    const score = Number(evidence.score);
    const scoreDeclared =
      typeof evidence.score === "number" &&
      Number.isFinite(score) &&
      score >= 0 &&
      score <= 1;
    const provenanceValid = provenanceComplete(evidence.provenance);
    const calibrationValidated = evidence.calibrationStatus === "validated";
    const calibrated =
      evidence.calibrated === true &&
      calibrationValidated &&
      provenanceValid &&
      scoreDeclared;
    const dominantHypothesis =
      typeof evidence.dominantHypothesis === "string" &&
      evidence.dominantHypothesis.trim()
        ? evidence.dominantHypothesis.trim()
        : null;
    const dominantMatches = diagnostic.candidates.some(
      (item) => item.name === dominantHypothesis,
    );
    const stable = syndromic.safety?.level === "continue";
    const criteriaSufficient = evidence.criteriaSufficient === true;
    const noCriticalConflict = evidence.unresolvedCriticalConflict === false;
    const cannotMissExcluded = evidence.cannotMissExcluded === true;
    const noCriticalEvidencePending = evidence.criticalEvidencePending === false;
    const noPostExamConflict = evidence.postExamConflict === false;
    const competitionResolved = evidence.unresolvedCompetition === false;
    const contentComplete = evidence.contentComplete === true;
    const sourceBindingValidated = evidence.sourceBindingValidated === true;
    const governanceAuthorized =
      evidence.governanceAuthority === "registered_fixture" ||
      evidence.governanceAuthority === "validated_runtime";
    const inputIntegrity =
      typeof evidence.inputDigest === "string" &&
      evidence.inputDigest.length > 0 &&
      evidence.inputDigest === evidence.registeredInputDigest;
    const modulesValidated =
      syndromic.classifications.length > 0 &&
      syndromic.classifications.every((item) => item.moduleStatus === "validated");
    const contentValidated =
      syndromic.classifications.length > 0 &&
      syndromic.classifications.every((item) => item.contentRecordStatus === "validated");
    const executionAllowed = therapeutic.clinicalExecutionAllowed === true;
    const professionalConfirmed = therapeutic.professionalConfirmed === true;
    const scoreAboveThreshold = calibrated && score > HIGH_CONFIDENCE_THRESHOLD;

    const checks = Object.freeze([
      Object.freeze({ key: "calibrated_score_missing", passed: scoreDeclared, detail: "Score calibrado ausente ou inválido" }),
      Object.freeze({ key: "confidence_provenance_missing", passed: provenanceValid, detail: "Proveniência da confiança ausente ou incompleta" }),
      Object.freeze({ key: "calibration_not_validated", passed: calibrationValidated, detail: "Calibração ainda não validada pela governança" }),
      Object.freeze({ key: "confidence_not_above_threshold", passed: scoreAboveThreshold, detail: `Score não é estritamente maior que ${HIGH_CONFIDENCE_THRESHOLD}` }),
      Object.freeze({ key: "dominant_hypothesis", passed: Boolean(dominantHypothesis && dominantMatches), detail: "Hipótese dominante ausente ou fora do diferencial calculado" }),
      Object.freeze({ key: "unresolved_competition", passed: competitionResolved, detail: "Competição entre hipóteses ainda não resolvida" }),
      Object.freeze({ key: "clinical_instability", passed: stable, detail: "Triagem indica prioridade ou instabilidade" }),
      Object.freeze({ key: "criteria_insufficient", passed: criteriaSufficient, detail: "Critérios diagnósticos ainda insuficientes" }),
      Object.freeze({ key: "severe_conflict_present", passed: noCriticalConflict, detail: "Existe conflito crítico não resolvido" }),
      Object.freeze({ key: "cannot_miss_not_excluded", passed: cannotMissExcluded, detail: "Hipóteses graves relevantes ainda não foram excluídas" }),
      Object.freeze({ key: "critical_evidence_pending", passed: noCriticalEvidencePending, detail: "Existe evidência crítica pendente" }),
      Object.freeze({ key: "post_exam_conflict", passed: noPostExamConflict, detail: "Existe conflito na reavaliação pós-exame" }),
      Object.freeze({ key: "content_incomplete", passed: contentComplete, detail: "Conteúdo necessário para a decisão está incompleto" }),
      Object.freeze({ key: "source_binding_missing", passed: sourceBindingValidated, detail: "Fontes do conteúdo não foram vinculadas e validadas" }),
      Object.freeze({ key: "module_not_validated", passed: modulesValidated, detail: "Um ou mais módulos clínicos ainda não foram validados" }),
      Object.freeze({ key: "content_not_validated", passed: contentValidated, detail: "Um ou mais conteúdos clínicos ainda não foram validados" }),
      Object.freeze({ key: "clinical_execution_blocked", passed: executionAllowed, detail: "Execução clínica continua bloqueada pela governança" }),
      Object.freeze({ key: "professional_confirmation_missing", passed: professionalConfirmed, detail: "Confirmação profissional ainda não foi registrada" }),
      Object.freeze({ key: "governance_authority_missing", passed: governanceAuthorized, detail: "Autoridade de governança ausente ou inválida" }),
      Object.freeze({ key: "input_integrity_failed", passed: inputIntegrity, detail: "Integridade dos fatos de entrada não foi confirmada" }),
    ]);
    const eligible = checks.every((check) => check.passed);

    return Object.freeze({
      engine: "DecisionMedConfidenceGate",
      version: VERSION,
      threshold: HIGH_CONFIDENCE_THRESHOLD,
      comparison: "strictly_greater_than",
      score: calibrated ? score : null,
      calibrated,
      provenance: calibrated ? Object.freeze({ ...evidence.provenance }) : null,
      compatibilityUsedAsProbability: false,
      checks,
      eligible,
      route: eligible ? "deterministic_no_llm" : "complex_case_llm_standby",
      reasons: Object.freeze(
        checks.filter((check) => !check.passed).map((check) => check.detail),
      ),
      reasonCodes: Object.freeze(
        checks.filter((check) => !check.passed).map((check) => check.key),
      ),
    });
  }

  return Object.freeze({
    version: VERSION,
    HIGH_CONFIDENCE_THRESHOLD,
    REQUIRED_PROVENANCE,
    evaluate,
  });
});
