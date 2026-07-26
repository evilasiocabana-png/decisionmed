(function exposeDecisionMedTherapeuticEngine(root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.DecisionMedTherapeuticEngine = api;
})(typeof globalThis === "object" ? globalThis : this, function createTherapeuticEngine() {
  "use strict";

  const VERSION = "1.0.0";

  function unique(values) {
    return Object.freeze([...new Set(values.filter(Boolean))]);
  }

  function analyze(input = {}) {
    const reasoning = input.reasoning || { syndromes: [], safety: { level: "continue" } };
    const syndromic = input.syndromic || { classifications: [] };
    const selectedKeys = new Set(syndromic.classifications.map((item) => item.key));
    const selected = (reasoning.syndromes || []).filter((item) => selectedKeys.has(item.key));
    const professionalConfirmed = Boolean(input.professionalConfirmation);
    const allValidated =
      selected.length > 0 &&
      selected.every(
        (item) =>
          item.moduleStatus === "validated" &&
          item.contentRecordStatus === "validated",
      );
    const catalogExecutionAllowed = Boolean(input.clinicalExecutionAllowed);
    const byName = new Map(selected.map((item) => [item.name, item]));
    const candidates = Array.isArray(input.diagnostic?.candidates)
      ? input.diagnostic.candidates
      : [];
    const plan = candidates.map((candidate) => {
      const origins = candidate.originatingSyndromes
        .map((name) => byName.get(name))
        .filter(Boolean);
      return Object.freeze({
        hypothesisKey: candidate.key,
        hypothesisName: candidate.name,
        hypothesisGroup: candidate.group,
        originatingSyndromes: unique(candidate.originatingSyndromes),
        contentScope: "shared_from_originating_syndrome",
        safety: unique(origins.flatMap((item) => [...(item.safetyConduct || []), ...(item.redFlags || [])])),
        physicalExam: unique(origins.flatMap((item) => item.physicalExam || [])),
        tests: Object.freeze(
          origins.flatMap((item) => item.tests || []).map((test) =>
            Object.freeze({
              examId: test.examId || null,
              name: test.name,
              question: test.question,
              when: test.when,
              limitations: test.limitations || null,
              sourceIds: unique(test.sourceIds || []),
            }),
          ),
        ),
        initialTreatment: unique(origins.flatMap((item) => item.initialTreatment || [])),
        definitiveTreatment: unique(origins.flatMap((item) => item.definitiveTreatment || [])),
        contraindicationsAndLimits: unique([
          ...origins.flatMap((item) => item.stopConditions || []),
          ...origins.flatMap((item) => item.boundaries ? [item.boundaries] : []),
        ]),
        postExamReassessment: unique(origins.flatMap((item) => item.postExamReassessment || [])),
        destinationReturnFollowup: unique(origins.flatMap((item) => item.destinationReturnFollowup || [])),
        sourceIds: unique(origins.flatMap((item) => [...(item.sourceIds || []), ...(item.contentSourceIds || [])])),
        status:
          origins.length > 0 &&
          origins.every((item) => item.moduleStatus === "validated" && item.contentRecordStatus === "validated")
            ? "validated"
            : "draft_review_only",
      });
    });

    return Object.freeze({
      engine: "DecisionMedTherapeuticEngine",
      version: VERSION,
      safetyLevel: reasoning.safety?.level || "continue",
      plan: Object.freeze(plan),
      allContentValidated: allValidated,
      professionalConfirmed,
      clinicalExecutionAllowed: catalogExecutionAllowed,
      deterministicSupportAllowed:
        allValidated && professionalConfirmed && catalogExecutionAllowed,
      automaticTreatmentAllowed: false,
      automaticPrescriptionAllowed: false,
      status:
        allValidated && professionalConfirmed && catalogExecutionAllowed
          ? "governed_deterministic_support"
          : "structural_review_only",
      disclaimer:
        "Plano estrutural para validação profissional; prescrição automática permanece bloqueada.",
    });
  }

  return Object.freeze({ version: VERSION, analyze });
});
