(function exposeDecisionMedPatient(root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  } else {
    root.DecisionMedPatient = api;
  }
})(typeof globalThis === "object" ? globalThis : this, function createPatientContext() {
  "use strict";

  const VERSION = "1.0.0";
  const MIN_NAME_LENGTH = 2;
  const MAX_NAME_LENGTH = 120;
  const MIN_AGE_YEARS = 0;
  const MAX_AGE_YEARS = 130;

  function normalizeName(value) {
    return String(value ?? "")
      .trim()
      .replace(/\s+/g, " ");
  }

  function parseAgeYears(value) {
    const raw = String(value ?? "").trim();
    if (!raw) return null;
    const age = Number(raw);
    return Number.isInteger(age) ? age : null;
  }

  function normalize(input = {}) {
    return {
      name: normalizeName(input.name),
      ageYears: parseAgeYears(input.ageYears),
      synthetic: Boolean(input.synthetic),
    };
  }

  function validate(input = {}) {
    const patient = normalize(input);
    const errors = [];

    if (patient.name.length < MIN_NAME_LENGTH) {
      errors.push({
        code: "patient_name_required",
        message: "Informe o nome, as iniciais ou o código do caso.",
      });
    } else if (patient.name.length > MAX_NAME_LENGTH) {
      errors.push({
        code: "patient_name_too_long",
        message: `Use no máximo ${MAX_NAME_LENGTH} caracteres na identificação.`,
      });
    }

    if (
      patient.ageYears === null ||
      patient.ageYears < MIN_AGE_YEARS ||
      patient.ageYears > MAX_AGE_YEARS
    ) {
      errors.push({
        code: "patient_age_invalid",
        message: `Informe a idade em anos, com um número inteiro entre ${MIN_AGE_YEARS} e ${MAX_AGE_YEARS}.`,
      });
    }

    return Object.freeze({
      valid: errors.length === 0,
      patient: Object.freeze(patient),
      errors: Object.freeze(errors.map((error) => Object.freeze(error))),
    });
  }

  function selectionIsValid(mode, selection = {}) {
    if (mode === "assisted") return Boolean(selection.complaint);
    if (mode === "direct") return Boolean(selection.directSyndrome);
    if (mode === "investigation") {
      const count = Array.isArray(selection.investigationSyndromes)
        ? selection.investigationSyndromes.length
        : 0;
      return count >= 2 && count <= 3;
    }
    return false;
  }

  function validateStart(mode, selection = {}, input = {}) {
    const patientResult = validate(input);
    const selectionValid = selectionIsValid(mode, selection);
    const errors = [...patientResult.errors];
    if (!selectionValid) {
      errors.push(
        Object.freeze({
          code: "clinical_selection_required",
          message: "Complete a seleção clínica desta porta para continuar.",
        }),
      );
    }
    return Object.freeze({
      valid: patientResult.valid && selectionValid,
      patient: patientResult.patient,
      patientValid: patientResult.valid,
      selectionValid,
      errors: Object.freeze(errors),
    });
  }

  function toAuditRecord(input = {}) {
    const result = validate(input);
    if (!result.valid) return null;
    return Object.freeze({
      display_name: result.patient.name,
      age_years: result.patient.ageYears,
      synthetic: result.patient.synthetic,
    });
  }

  return Object.freeze({
    version: VERSION,
    limits: Object.freeze({
      minNameLength: MIN_NAME_LENGTH,
      maxNameLength: MAX_NAME_LENGTH,
      minAgeYears: MIN_AGE_YEARS,
      maxAgeYears: MAX_AGE_YEARS,
    }),
    normalize,
    validate,
    validateStart,
    toAuditRecord,
  });
});
