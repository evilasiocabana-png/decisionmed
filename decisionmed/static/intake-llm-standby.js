(function exposeDecisionMedLlmStandby(root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.DecisionMedLlmStandby = api;
})(typeof globalThis === "object" ? globalThis : this, function createLlmStandby() {
  "use strict";

  const VERSION = "1.0.0";

  function status(input = {}) {
    return Object.freeze({
      adapter: "DecisionMedLlmStandby",
      version: VERSION,
      route: input.route || "complex_case_llm_standby",
      disabled: true,
      provider: null,
      invoked: false,
      transmitted: false,
      tokenUsage: 0,
      purpose: "Explicação, justificativa ou apoio futuro em caso complexo.",
      reasons: Object.freeze([...(input.reasons || [])]),
      message:
        "LLM em standby. Nenhuma chamada, transmissão de dados ou consumo de tokens foi realizado.",
    });
  }

  function invoke() {
    return Object.freeze({
      ok: false,
      code: "llm_standby_disabled",
      invoked: false,
      transmitted: false,
      tokenUsage: 0,
    });
  }

  return Object.freeze({ version: VERSION, status, invoke });
});
