(function exposeDecisionMedRuleEngine(root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  } else {
    root.DecisionMedRuleEngine = api;
  }
})(typeof globalThis === "object" ? globalThis : this, function createRuleEngine() {
  "use strict";

  const VERSION = "0.2.0";
  const EFFECTS = new Set(["support", "oppose", "alarm", "route"]);
  const OPERATORS = new Set([
    "equals",
    "contains",
    "contains_any",
    "contains_all",
    "count_at_least",
    "matches",
    "present",
  ]);

  function fail(message) {
    throw new TypeError(`DecisionMedRuleEngine: ${message}`);
  }

  function normalizeText(value) {
    return String(value || "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLocaleLowerCase("pt-BR");
  }

  function normalizeArray(value) {
    return Array.isArray(value) ? value : value == null ? [] : [value];
  }

  function validateCondition(condition, path) {
    if (!condition || typeof condition !== "object" || Array.isArray(condition)) {
      fail(`${path} must be an object`);
    }
    const groupKeys = ["all", "any", "none"].filter((key) => key in condition);
    const isGroup = groupKeys.length > 0;
    if (isGroup) {
      if ("fact" in condition || "operator" in condition) {
        fail(`${path} cannot mix a group with a fact condition`);
      }
      for (const key of groupKeys) {
        if (!Array.isArray(condition[key]) || !condition[key].length) {
          fail(`${path}.${key} must be a non-empty array`);
        }
        condition[key].forEach((item, index) =>
          validateCondition(item, `${path}.${key}[${index}]`),
        );
      }
      return;
    }
    if (typeof condition.fact !== "string" || !condition.fact) {
      fail(`${path}.fact is required`);
    }
    if (!OPERATORS.has(condition.operator)) {
      fail(`${path}.operator is unsupported`);
    }
    if (
      condition.operator === "count_at_least" &&
      (!Number.isInteger(condition.threshold) || condition.threshold < 1)
    ) {
      fail(`${path}.threshold must be a positive integer`);
    }
    if (
      condition.operator === "matches" &&
      (typeof condition.pattern !== "string" || !condition.pattern)
    ) {
      fail(`${path}.pattern is required`);
    }
  }

  function compileRules(input) {
    if (!Array.isArray(input)) fail("rules must be an array");
    const ids = new Set();
    const rules = input.map((rule, index) => {
      const path = `rules[${index}]`;
      if (!rule || typeof rule !== "object" || Array.isArray(rule)) {
        fail(`${path} must be an object`);
      }
      if (typeof rule.ruleId !== "string" || !rule.ruleId) {
        fail(`${path}.ruleId is required`);
      }
      if (ids.has(rule.ruleId)) fail(`duplicate rule id: ${rule.ruleId}`);
      ids.add(rule.ruleId);
      if (!EFFECTS.has(rule.effect)) fail(`${path}.effect is unsupported`);
      if (typeof rule.target !== "string" || !rule.target) {
        fail(`${path}.target is required`);
      }
      if (typeof rule.rationale !== "string" || !rule.rationale.trim()) {
        fail(`${path}.rationale is required`);
      }
      validateCondition(rule.when, `${path}.when`);
      return Object.freeze({
        ruleId: rule.ruleId,
        moduleId:
          typeof rule.moduleId === "string" ? rule.moduleId : null,
        version: typeof rule.version === "string" ? rule.version : "0.1.0",
        status: typeof rule.status === "string" ? rule.status : "draft",
        effect: rule.effect,
        target: rule.target,
        strength:
          typeof rule.strength === "string" ? rule.strength : "moderate",
        priority: rule.priority === true,
        rationale: rule.rationale,
        sourceIds: Object.freeze(
          Array.isArray(rule.sourceIds) ? [...rule.sourceIds] : [],
        ),
        when: rule.when,
        clinicalExecutionAllowed: false,
      });
    });
    return Object.freeze(rules);
  }

  function valueFor(facts, fact) {
    return String(fact)
      .split(".")
      .reduce(
        (value, key) =>
          value && typeof value === "object" ? value[key] : undefined,
        facts,
      );
  }

  function evaluateFact(condition, facts) {
    const actual = valueFor(facts, condition.fact);
    const expectedValues = normalizeArray(condition.values);
    const actualValues = normalizeArray(actual);
    switch (condition.operator) {
      case "equals":
        return actual === condition.value;
      case "contains":
        return actualValues.includes(condition.value);
      case "contains_any":
        return expectedValues.some((value) => actualValues.includes(value));
      case "contains_all":
        return expectedValues.every((value) => actualValues.includes(value));
      case "count_at_least":
        return (
          expectedValues.filter((value) => actualValues.includes(value)).length >=
          condition.threshold
        );
      case "matches":
        return new RegExp(condition.pattern, condition.flags || "").test(
          String(actual || ""),
        );
      case "present":
        return Array.isArray(actual)
          ? actual.length > 0
          : actual !== undefined && actual !== null && actual !== "";
      default:
        return false;
    }
  }

  function evaluateCondition(condition, facts) {
    const hasGroups = ["all", "any", "none"].some((key) => key in condition);
    if (!hasGroups) return evaluateFact(condition, facts);
    const allPass =
      !condition.all ||
      condition.all.every((item) => evaluateCondition(item, facts));
    const anyPass =
      !condition.any ||
      condition.any.some((item) => evaluateCondition(item, facts));
    const nonePass =
      !condition.none ||
      condition.none.every((item) => !evaluateCondition(item, facts));
    return allPass && anyPass && nonePass;
  }

  function evaluateRules(compiledRules, facts = {}) {
    if (!Array.isArray(compiledRules)) {
      fail("compiled rules must be an array");
    }
    return Object.freeze(
      compiledRules
        .filter((rule) => evaluateCondition(rule.when, facts))
        .map((rule) =>
          Object.freeze({
            ruleId: rule.ruleId,
            moduleId: rule.moduleId,
            ruleVersion: rule.version,
            ruleStatus: rule.status,
            effect: rule.effect,
            target: rule.target,
            strength: rule.strength,
            priority: rule.priority,
            rationale: rule.rationale,
            sourceIds: rule.sourceIds,
            clinicalExecutionAllowed: false,
          }),
        ),
    );
  }

  return Object.freeze({
    version: VERSION,
    normalizeText,
    compileRules,
    evaluateRules,
  });
});
