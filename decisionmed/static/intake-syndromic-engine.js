(function exposeDecisionMedSyndromicEngine(root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.DecisionMedSyndromicEngine = api;
})(typeof globalThis === "object" ? globalThis : this, function createSyndromicEngine() {
  "use strict";

  const VERSION = "1.0.0";

  function freezeList(values) {
    return Object.freeze([...(Array.isArray(values) ? values : [])]);
  }

  function analyze(input = {}) {
    const reasoning = input.reasoning || {};
    const available = Array.isArray(reasoning.syndromes) ? reasoning.syndromes : [];
    const selectedKeys = new Set(
      Array.isArray(input.selectedSyndromeKeys) && input.selectedSyndromeKeys.length
        ? input.selectedSyndromeKeys
        : available.map((item) => item.key),
    );
    const classifications = available
      .filter((item) => selectedKeys.has(item.key))
      .map((item) =>
        Object.freeze({
          key: item.key,
          moduleId: item.moduleId || null,
          name: item.name,
          entityType: item.entityType || null,
          entityTypeLabel: item.entityTypeLabel || null,
          compatibility: item.compatibility || "não classificada",
          supports: freezeList(item.supports),
          against: freezeList(item.against),
          redFlags: freezeList(item.redFlags),
          stopConditions: freezeList(item.stopConditions),
          sourceIds: freezeList([...(item.sourceIds || []), ...(item.contentSourceIds || [])]),
          moduleVersion: item.moduleVersion || null,
          moduleStatus: item.moduleStatus || "unknown",
          contentVersion: item.contentVersion || null,
          contentRecordStatus: item.contentRecordStatus || "unknown",
          terminologyStatus: item.terminologyStatus || "unknown",
        }),
      );

    return Object.freeze({
      engine: "DecisionMedSyndromicEngine",
      version: VERSION,
      representation: String(reasoning.representation || "Representação do problema indisponível."),
      safety: Object.freeze({ ...(reasoning.safety || { level: "continue", reasons: [] }) }),
      classifications: Object.freeze(classifications),
      status: classifications.length ? "provisional_classification" : "unclassified",
      probabilityCalibrated: false,
      disclaimer:
        "Compatibilidade sindrômica é qualitativa e não representa probabilidade diagnóstica.",
    });
  }

  return Object.freeze({ version: VERSION, analyze });
});
