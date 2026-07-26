(function exposeDecisionMedRouting(root, factory) {
  let ruleEngine = root.DecisionMedRuleEngine;
  let routingRules = root.DecisionMedRoutingRules;
  if (typeof module === "object" && module.exports) {
    ruleEngine = require("./intake-rule-engine.js");
    routingRules = require("./intake-routing-rules.js");
    module.exports = factory(ruleEngine, routingRules);
  } else {
    root.DecisionMedRouting = factory(ruleEngine, routingRules);
  }
})(
  typeof globalThis === "object" ? globalThis : this,
  function createRoutingEngine(ruleEngine, routingRules) {
    "use strict";

    if (!ruleEngine || !routingRules) {
      throw new Error("DecisionMed routing dependencies are unavailable");
    }

    const VERSION = "0.3.0";
    const localRules = ruleEngine.compileRules(routingRules.items);
    let compiledRules = localRules;
    let ruleCatalogSource = "local_fallback";

    function configureRules(items) {
      if (items === undefined || items === null) {
        compiledRules = localRules;
        ruleCatalogSource = "local_fallback";
        return Object.freeze({
          count: compiledRules.length,
          source: ruleCatalogSource,
          clinicalExecutionAllowed: false,
        });
      }
      if (!Array.isArray(items)) {
        throw new TypeError("clinical rule catalog items must be an array");
      }
      const external = items
        .filter((item) => item && item.effect === "route")
        .map((item) => ({
          ruleId: item.rule_id,
          moduleId: item.module_id,
          version: item.version,
          status: item.status,
          effect: item.effect,
          target: item.output_key,
          priority: item.priority,
          rationale: item.rationale,
          sourceIds: item.source_ids,
          when: item.when,
        }));
      if (!external.length) {
        throw new TypeError("external clinical rule catalog is empty");
      }
      compiledRules = ruleEngine.compileRules(external);
      ruleCatalogSource = "governed_external";
      return Object.freeze({
        count: compiledRules.length,
        source: ruleCatalogSource,
        clinicalExecutionAllowed: false,
      });
    }

    function addSuggestion(suggestions, match) {
      const current = suggestions.get(match.target) || {
        reasons: [],
        priority: false,
        ruleIds: [],
        ruleVersions: [],
        ruleStatuses: [],
        moduleIds: [],
        sourceIds: [],
      };
      if (!current.reasons.includes(match.rationale)) {
        current.reasons.push(match.rationale);
      }
      if (!current.ruleIds.includes(match.ruleId)) {
        current.ruleIds.push(match.ruleId);
      }
      if (!current.ruleVersions.includes(match.ruleVersion)) {
        current.ruleVersions.push(match.ruleVersion);
      }
      if (!current.ruleStatuses.includes(match.ruleStatus)) {
        current.ruleStatuses.push(match.ruleStatus);
      }
      if (match.moduleId && !current.moduleIds.includes(match.moduleId)) {
        current.moduleIds.push(match.moduleId);
      }
      for (const sourceId of match.sourceIds) {
        if (!current.sourceIds.includes(sourceId)) {
          current.sourceIds.push(sourceId);
        }
      }
      current.priority = current.priority || match.priority;
      suggestions.set(match.target, current);
    }

    function suggestModules({ complaint = "", values = [], note = "" } = {}) {
      const facts = {
        complaint: String(complaint || ""),
        values: Array.isArray(values) ? [...new Set(values)] : [],
        normalizedNote: ruleEngine.normalizeText(note),
        normalized_note: ruleEngine.normalizeText(note),
      };
      const suggestions = new Map();
      for (const match of ruleEngine.evaluateRules(compiledRules, facts)) {
        addSuggestion(suggestions, match);
      }
      if (!suggestions.size) {
        addSuggestion(suggestions, {
          target: "generalmedicine",
          rationale:
            "Padrão ainda não classificado com segurança; requer revisão clínica ampliada.",
          priority: false,
          ruleId: "route.fallback.general-medicine",
          ruleVersion: VERSION,
          ruleStatus: "draft",
          sourceIds: [],
          moduleId: null,
        });
      }
      return [...suggestions].map(([key, value]) => ({
        key,
        reasons: [...value.reasons],
        priority: value.priority,
        ruleIds: [...value.ruleIds],
        ruleVersions: [...value.ruleVersions],
        ruleStatuses: [...value.ruleStatuses],
        moduleIds: [...value.moduleIds],
        sourceIds: [...value.sourceIds],
        clinicalExecutionAllowed: false,
      }));
    }

    return Object.freeze({
      version: VERSION,
      ruleEngineVersion: ruleEngine.version,
      ruleCatalogVersion: routingRules.version,
      configureRules,
      get ruleCatalogSource() {
        return ruleCatalogSource;
      },
      get ruleCount() {
        return compiledRules.length;
      },
      normalizeText: ruleEngine.normalizeText,
      suggestModules,
    });
  },
);
