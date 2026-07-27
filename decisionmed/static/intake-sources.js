(function exposeDecisionMedSources(root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.DecisionMedSources = api;
})(typeof globalThis === "object" ? globalThis : this, function createSourcesPresenter() {
  "use strict";

  const VERSION = "1.0.0";
  let registry = new Map();

  const STATUS_LABELS = Object.freeze({
    draft: "Referência vinculada · revisão clínica pendente",
    candidate: "Terminologia candidata · revisão clínica pendente",
    partial: "Conteúdo parcialmente estruturado · revisão clínica pendente",
    skeleton: "Estrutura inicial · revisão clínica pendente",
    validated: "Validada para o escopo governado",
    retired: "Referência retirada de uso",
    unknown: "Estado de revisão não informado",
    draft_review_only: "Conteúdo em revisão · somente para conferência profissional",
    structural_review_only: "Plano estrutural em revisão · uso clínico automático bloqueado",
    differential_support_only: "Apoio à organização do diagnóstico diferencial",
    professional_impression_recorded: "Impressão registrada pelo profissional",
    provisional_classification: "Classificação clínica provisória",
    unclassified: "Classificação ainda não formada",
    governed_deterministic_support: "Apoio determinístico governado",
    treatment_binding_missing: "Tratamento diagnóstico-específico ainda não vinculado",
    unbound: "Sem vínculo diagnóstico-específico",
    module_level: "Fonte vinculada ao módulo",
    field_level: "Fonte vinculada diretamente ao campo",
    case_fact: "Informação fornecida no caso",
  });

  function clean(value) {
    return typeof value === "string" ? value.trim() : "";
  }

  function safeLocator(value) {
    const locator = clean(value);
    return /^https?:\/\//i.test(locator) ? locator : null;
  }

  function unique(values) {
    return [...new Set((Array.isArray(values) ? values : []).filter(Boolean))];
  }

  function configure(items = []) {
    if (!Array.isArray(items)) throw new TypeError("source items must be an array");
    const next = new Map();
    for (const item of items) {
      if (!item || typeof item !== "object") continue;
      const sourceId = clean(item.source_id);
      if (!sourceId || next.has(sourceId)) continue;
      next.set(
        sourceId,
        Object.freeze({
          sourceId,
          citationLabel: clean(item.citation_label) || "Fonte vinculada",
          title: clean(item.title) || "Referência bibliográfica ainda não disponível",
          publisher: clean(item.publisher) || null,
          publicationYear:
            Number.isInteger(item.publication_year) || typeof item.publication_year === "string"
              ? String(item.publication_year)
              : null,
          version: clean(item.version) || null,
          status: clean(item.status) || "unknown",
          locator: safeLocator(item.locator),
          reviewedOn: clean(item.reviewed_on) || null,
          reviewDueOn: clean(item.review_due_on) || null,
          evidenceQuality: clean(item.evidence_quality) || null,
          recommendationStrength: clean(item.recommendation_strength) || null,
          clinicalApplicability: clean(item.clinical_applicability) || null,
          knownConflicts: clean(item.known_conflicts) || null,
        }),
      );
    }
    registry = next;
    return Object.freeze({ count: registry.size, complete: registry.size === items.length });
  }

  function get(sourceId) {
    return registry.get(sourceId) || null;
  }

  function displayStatus(code) {
    const normalized = clean(code) || "unknown";
    return STATUS_LABELS[normalized] || "Estado técnico registrado na trilha de auditoria";
  }

  function citationLabel(sourceId) {
    return get(sourceId)?.citationLabel || "Fonte vinculada";
  }

  function citationText(sourceIds = [], kind = "clinical") {
    if (kind === "case") return "[CASO]";
    const ids = unique(sourceIds);
    if (!ids.length) return "[FONTE ESPECÍFICA PENDENTE]";
    return ids.map((sourceId) => `[${citationLabel(sourceId)}]`).join(" ");
  }

  function anchorId(sourceId) {
    const normalized = clean(sourceId)
      .toLocaleLowerCase("pt-BR")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "");
    return `fonte-${normalized || "vinculada"}`;
  }

  function legendEntries(sourceIds = []) {
    return unique(sourceIds).map((sourceId) => {
      const source = get(sourceId);
      if (source) return source;
      return Object.freeze({
        sourceId,
        citationLabel: "Fonte vinculada",
        title: "Referência bibliográfica ainda não disponível para exibição",
        publisher: null,
        publicationYear: null,
        version: null,
        status: "unknown",
        locator: null,
        reviewedOn: null,
        reviewDueOn: null,
        evidenceQuality: null,
        recommendationStrength: null,
        clinicalApplicability: null,
        knownConflicts: null,
      });
    });
  }

  function claim(text, sourceIds = [], bindingScope = "module_level", kind = "clinical") {
    return Object.freeze({
      text: String(text || ""),
      sourceIds: Object.freeze(unique(sourceIds)),
      bindingScope,
      kind,
      cited: kind === "case" || unique(sourceIds).length > 0,
    });
  }

  function claims(values = [], sourceIds = [], bindingScope = "module_level", kind = "clinical") {
    return (Array.isArray(values) ? values : []).map((value) =>
      typeof value === "object" && value !== null && "text" in value
        ? claim(
            value.text,
            value.sourceIds || sourceIds,
            value.bindingScope || bindingScope,
            value.kind || kind,
          )
        : claim(value, sourceIds, bindingScope, kind),
    );
  }

  return Object.freeze({
    version: VERSION,
    configure,
    get,
    displayStatus,
    citationLabel,
    citationText,
    anchorId,
    legendEntries,
    claim,
    claims,
  });
});
