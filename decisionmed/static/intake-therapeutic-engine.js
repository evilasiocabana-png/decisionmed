(function exposeDecisionMedTherapeuticEngine(root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.DecisionMedTherapeuticEngine = api;
})(typeof globalThis === "object" ? globalThis : this, function createTherapeuticEngine() {
  "use strict";

  const VERSION = "1.1.0";

  function unique(values) {
    return Object.freeze([...new Set(values.filter(Boolean))]);
  }

  function canonicalModuleId(value) {
    return (
      typeof value === "string" &&
      /^module\.[a-z0-9][a-z0-9.-]*$/.test(value)
    );
  }

  function validTexts(values) {
    return (
      Array.isArray(values) &&
      values.every(
        (value) => typeof value === "string" && value.trim().length > 0,
      )
    );
  }

  function treatmentBindingFor(candidate) {
    const binding = candidate?.treatmentBinding;
    if (!binding || typeof binding !== "object") {
      return Object.freeze({
        valid: false,
        reason: "missing_explicit_diagnostic_binding",
        binding: null,
      });
    }
    const sourceIds = Array.isArray(binding.sourceIds)
      ? binding.sourceIds
      : [];
    const valid =
      binding.scope === "diagnosis_specific" &&
      binding.status === "validated" &&
      binding.hypothesisKey === candidate.key &&
      binding.hypothesisName === candidate.name &&
      canonicalModuleId(binding.moduleId) &&
      typeof binding.contentVersion === "string" &&
      binding.contentVersion.trim().length > 0 &&
      binding.moduleStatus === "validated" &&
      binding.contentRecordStatus === "validated" &&
      binding.sourceBindingValidated === true &&
      sourceIds.length > 0 &&
      validTexts(sourceIds) &&
      validTexts(binding.initialTreatment) &&
      validTexts(binding.definitiveTreatment) &&
      binding.initialTreatment.length + binding.definitiveTreatment.length > 0;
    return Object.freeze({
      valid,
      reason: valid ? null : "explicit_diagnostic_binding_not_validated",
      binding: valid ? binding : null,
    });
  }

  function syndromicSupportPlan(syndrome) {
    return Object.freeze({
      planId: `syndromic-support:${syndrome.key}`,
      scope: "syndromic_shared_support",
      syndromeKey: syndrome.key,
      syndromeName: syndrome.name,
      safety: unique([
        ...(syndrome.safetyConduct || []),
        ...(syndrome.redFlags || []),
      ]),
      physicalExam: unique(syndrome.physicalExam || []),
      tests: Object.freeze(
        (syndrome.tests || []).map((test) =>
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
      contraindicationsAndLimits: unique([
        ...(syndrome.stopConditions || []),
        ...(syndrome.boundaries ? [syndrome.boundaries] : []),
      ]),
      postExamReassessment: unique(syndrome.postExamReassessment || []),
      destinationReturnFollowup: unique(
        syndrome.destinationReturnFollowup || [],
      ),
      sourceIds: unique([
        ...(syndrome.sourceIds || []),
        ...(syndrome.contentSourceIds || []),
      ]),
      diagnosisSpecificTreatmentIncluded: false,
    });
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
    const supportPlans = Object.freeze(selected.map(syndromicSupportPlan));
    const supportBySyndromeName = new Map(
      supportPlans.map((item) => [item.syndromeName, item]),
    );
    const candidates = Array.isArray(input.diagnostic?.candidates)
      ? input.diagnostic.candidates
      : [];
    const plan = candidates.map((candidate) => {
      const candidateSupportPlans = candidate.originatingSyndromes
        .map((name) => supportBySyndromeName.get(name))
        .filter(Boolean);
      const bindingResult = treatmentBindingFor(candidate);
      const binding = bindingResult.binding;
      return Object.freeze({
        hypothesisKey: candidate.key,
        hypothesisName: candidate.name,
        hypothesisGroup: candidate.group,
        originatingSyndromes: unique(candidate.originatingSyndromes),
        contentScope: binding ? "diagnosis_specific" : "unbound",
        syndromicSupportPlanIds: unique(
          candidateSupportPlans.map((item) => item.planId),
        ),
        supportScope: "syndromic_shared_support",
        safety: unique(
          candidateSupportPlans.flatMap((item) => item.safety),
        ),
        physicalExam: unique(
          candidateSupportPlans.flatMap((item) => item.physicalExam),
        ),
        tests: Object.freeze(
          candidateSupportPlans.flatMap((item) => item.tests),
        ),
        treatmentBindingStatus: binding ? "validated" : "unbound",
        treatmentBindingReason: bindingResult.reason,
        treatmentModuleId: binding?.moduleId || null,
        treatmentContentVersion: binding?.contentVersion || null,
        initialTreatment: unique(binding?.initialTreatment || []),
        definitiveTreatment: unique(binding?.definitiveTreatment || []),
        treatmentSourceIds: unique(binding?.sourceIds || []),
        contraindicationsAndLimits: unique([
          ...candidateSupportPlans.flatMap(
            (item) => item.contraindicationsAndLimits,
          ),
        ]),
        postExamReassessment: unique(
          candidateSupportPlans.flatMap(
            (item) => item.postExamReassessment,
          ),
        ),
        destinationReturnFollowup: unique(
          candidateSupportPlans.flatMap(
            (item) => item.destinationReturnFollowup,
          ),
        ),
        syndromicSupportSourceIds: unique(
          candidateSupportPlans.flatMap((item) => item.sourceIds),
        ),
        sourceIds: unique(binding?.sourceIds || []),
        status: binding
          ? "diagnosis_specific_treatment_review_only"
          : "treatment_unbound_review_only",
      });
    });
    const allTreatmentBindingsValidated =
      plan.length > 0 &&
      plan.every((item) => item.treatmentBindingStatus === "validated");

    return Object.freeze({
      engine: "DecisionMedTherapeuticEngine",
      version: VERSION,
      safetyLevel: reasoning.safety?.level || "continue",
      syndromicSupportPlans: supportPlans,
      plan: Object.freeze(plan),
      allContentValidated: allValidated,
      allTreatmentBindingsValidated,
      unboundTreatmentHypothesisKeys: Object.freeze(
        plan
          .filter((item) => item.treatmentBindingStatus !== "validated")
          .map((item) => item.hypothesisKey),
      ),
      professionalConfirmed,
      clinicalExecutionAllowed: catalogExecutionAllowed,
      deterministicSupportAllowed:
        allValidated && professionalConfirmed && catalogExecutionAllowed,
      diagnosisSpecificTreatmentSupportAllowed:
        allValidated &&
        allTreatmentBindingsValidated &&
        professionalConfirmed &&
        catalogExecutionAllowed,
      automaticTreatmentAllowed: false,
      automaticPrescriptionAllowed: false,
      status:
        allValidated &&
        allTreatmentBindingsValidated &&
        professionalConfirmed &&
        catalogExecutionAllowed
          ? "governed_deterministic_support"
          : "structural_review_only",
      disclaimer:
        allTreatmentBindingsValidated
          ? "Tratamento diagnóstico-específico vinculado para revisão profissional; prescrição automática permanece bloqueada."
          : "Apoio sindrômico disponível; tratamento diagnóstico-específico indisponível sem binding canônico validado.",
    });
  }

  return Object.freeze({ version: VERSION, analyze });
});
