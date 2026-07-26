(function exposeDecisionMedDiagnosticEngine(root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.DecisionMedDiagnosticEngine = api;
})(typeof globalThis === "object" ? globalThis : this, function createDiagnosticEngine() {
  "use strict";

  const VERSION = "1.0.0";

  function unique(values) {
    return [...new Set(values.filter(Boolean))];
  }

  function normalizeReassessments(values) {
    return (Array.isArray(values) ? values : []).map((item) =>
      Object.freeze({
        hypothesis: item.hypothesis || null,
        impact: item.impact || null,
        examName: item.examName || item.examKind || null,
        finding: item.finding || null,
      }),
    );
  }

  function analyze(input = {}) {
    const reasoning = input.reasoning || { syndromes: [] };
    const syndromic = input.syndromic || { classifications: [] };
    const selectedKeys = new Set(syndromic.classifications.map((item) => item.key));
    const selected = (reasoning.syndromes || []).filter((item) => selectedKeys.has(item.key));
    const reassessments = normalizeReassessments(input.reassessments);
    const groups = [
      ["likely", "more_likely", "Mais provável"],
      ["cannotMiss", "cannot_miss", "Grave que não pode ser perdida"],
      ["mimics", "mimic", "Alternativa que imita o quadro"],
    ];
    const candidates = [];
    const byIdentity = new Map();

    selected.forEach((syndrome) => {
      groups.forEach(([field, group, groupLabel]) => {
        (syndrome.differential?.[field] || []).forEach((name) => {
          const identity = `${group}:${name}`;
          let candidate = byIdentity.get(identity);
          if (!candidate) {
            candidate = {
              key: identity,
              name,
              group,
              groupLabel,
              originatingSyndromes: [],
              criteria: { present: [], absentOrContrary: [], pending: [], conflicting: [] },
              reassessments: [],
            };
            byIdentity.set(identity, candidate);
            candidates.push(candidate);
          }
          candidate.originatingSyndromes.push(syndrome.name);
          candidate.criteria.present.push(...(syndrome.supports || []));
          candidate.criteria.absentOrContrary.push(...(syndrome.against || []));
          candidate.criteria.pending.push(...(syndrome.diagnosticCriteria || []));
          candidate.reassessments.push(
            ...reassessments.filter(
              (entry) => entry.hypothesis === name || entry.hypothesis === syndrome.name,
            ),
          );
          candidate.criteria.conflicting.push(
            ...candidate.reassessments
              .filter((entry) =>
                /reformular|contradit|incompat/i.test(
                  `${entry.impact || ""} ${entry.finding || ""}`,
                ),
              )
              .map(
                (entry) =>
                  `${entry.examName || "Reavaliação"}: ${entry.impact || entry.finding}`,
              ),
          );
        });
      });
    });

    const frozenCandidates = candidates.map((candidate) =>
      Object.freeze({
        ...candidate,
        originatingSyndromes: Object.freeze(unique(candidate.originatingSyndromes)),
        criteria: Object.freeze({
          present: Object.freeze(unique(candidate.criteria.present)),
          absentOrContrary: Object.freeze(unique(candidate.criteria.absentOrContrary)),
          pending: Object.freeze(unique(candidate.criteria.pending)),
          conflicting: Object.freeze(unique(candidate.criteria.conflicting)),
        }),
        criteriaScope: "shared_syndromic_evidence",
        referenceContraryFindings: Object.freeze(
          unique(
            selected
              .filter((syndrome) =>
                candidate.originatingSyndromes.includes(syndrome.name),
              )
              .flatMap((syndrome) => syndrome.contraryFindings || []),
          ),
        ),
        reassessments: Object.freeze(candidate.reassessments),
        automaticallyConfirmed: false,
      }),
    );
    const professionalImpression = input.professionalImpression || null;

    return Object.freeze({
      engine: "DecisionMedDiagnosticEngine",
      version: VERSION,
      candidates: Object.freeze(frozenCandidates),
      professionalImpression: professionalImpression
        ? Object.freeze({ ...professionalImpression })
        : null,
      confirmedByEngine: false,
      status: professionalImpression
        ? "professional_impression_recorded"
        : "differential_support_only",
      disclaimer:
        "O motor organiza hipóteses e critérios, mas nunca confirma diagnóstico automaticamente.",
    });
  }

  return Object.freeze({ version: VERSION, analyze });
});
