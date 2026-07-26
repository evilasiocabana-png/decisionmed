(function exposeDecisionMedRoutingRules(root, factory) {
  const rules = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = rules;
  } else {
    root.DecisionMedRoutingRules = rules;
  }
})(typeof globalThis === "object" ? globalThis : this, function createRoutingRules() {
  "use strict";

  const VERSION = "0.1.0";
  const draftRoute = (ruleId, target, rationale, when, priority = false) => ({
    ruleId,
    version: VERSION,
    status: "draft",
    effect: "route",
    target,
    rationale,
    priority,
    sourceIds: [],
    when,
  });
  const equals = (fact, value) => ({ fact, operator: "equals", value });
  const contains = (value) => ({
    fact: "values",
    operator: "contains",
    value,
  });
  const containsAny = (values) => ({
    fact: "values",
    operator: "contains_any",
    values,
  });
  const countAtLeast = (values, threshold) => ({
    fact: "values",
    operator: "count_at_least",
    values,
    threshold,
  });

  const directRoutes = [
    ["Falta de ar", "pulmonology"],
    ["Tosse", "pulmonology"],
    ["Náusea / vômito", "abdominal"],
    ["Alteração urinária", "urology"],
    ["Alteração intestinal", "abdominal"],
    ["Pele", "dermatology"],
    ["Visão", "ophthalmology"],
    ["Neurológica", "neurology"],
    ["Ginecológica", "gynecology"],
    ["Gestação / pós-parto", "obstetrics"],
    ["Ossos / articulações", "orthopedics"],
    ["Humor / sono", "psychiatry"],
  ].map(([complaint, target]) =>
    draftRoute(
      `route.complaint.${target}.${complaint
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLocaleLowerCase("pt-BR")
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/^-|-$/g, "")}`,
      target,
      `Queixa principal: ${complaint}.`,
      equals("complaint", complaint),
    ),
  );

  const rules = [
    ...directRoutes,
    draftRoute(
      "route.pain.chest.cardiology",
      "cardiology",
      "Dor localizada no peito.",
      { all: [equals("complaint", "Dor"), contains("Peito")] },
    ),
    draftRoute(
      "route.pain.abdomen",
      "abdominal",
      "Dor localizada no abdome.",
      {
        all: [
          equals("complaint", "Dor"),
          containsAny(["Abdome superior", "Abdome inferior"]),
        ],
      },
    ),
    draftRoute(
      "route.pain.head.neurology",
      "neurology",
      "Dor localizada na cabeça.",
      { all: [equals("complaint", "Dor"), contains("Cabeça")] },
    ),
    draftRoute(
      "route.pain.eyes.ophthalmology",
      "ophthalmology",
      "Dor localizada nos olhos.",
      { all: [equals("complaint", "Dor"), contains("Olhos")] },
    ),
    draftRoute(
      "route.pain.skin.dermatology",
      "dermatology",
      "Dor associada à pele.",
      { all: [equals("complaint", "Dor"), contains("Pele")] },
    ),
    draftRoute(
      "route.pain.urinary-pelvic.urology",
      "urology",
      "Dor em região urinária ou pélvica.",
      {
        all: [
          equals("complaint", "Dor"),
          contains("Região urinária / pélvica"),
        ],
      },
    ),
    draftRoute(
      "route.pattern.possible-anginal-equivalent",
      "cardiology",
      "Combinação compatível com desconforto cardiovascular ou equivalente anginoso; exige revisão humana e não confirma diagnóstico.",
      {
        any: [
          {
            all: [
              containsAny([
                "Peito",
                "Braço / ombro",
                "Pescoço / mandíbula",
                "Costas",
                "Abdome superior",
              ]),
              countAtLeast(
                [
                  "Aperto / pressão",
                  "Peso / desconforto",
                  "Queimação",
                  "Esforço físico",
                  "Esforço piora",
                  "Repouso melhora",
                  "Falta de ar",
                  "Suor frio",
                  "Cansaço incomum",
                  "Náusea / vômito",
                  "Tontura / desmaio",
                ],
                2,
              ),
            ],
          },
          {
            all: [
              containsAny([
                "Esforço físico",
                "Esforço piora",
                "Repouso melhora",
                "Ao esforço",
              ]),
              containsAny([
                "Falta de ar",
                "Suor frio",
                "Cansaço incomum",
                "Náusea / vômito",
                "Tontura / desmaio",
                "Palpitação",
              ]),
              {
                any: [
                  containsAny([
                    "Peito",
                    "Braço / ombro",
                    "Pescoço / mandíbula",
                    "Costas",
                    "Abdome superior",
                  ]),
                  countAtLeast(
                    [
                      "Hipertensão",
                      "Diabetes",
                      "Doença cardíaca",
                      "Fuma atualmente",
                    ],
                    1,
                  ),
                ],
              },
            ],
          },
          {
            all: [
              equals("complaint", "Falta de ar"),
              containsAny([
                "Esforço físico",
                "Esforço piora",
                "Repouso melhora",
                "Ao esforço",
              ]),
              containsAny([
                "Cansaço incomum",
                "Tontura / desmaio",
                "Palpitação",
              ]),
            ],
          },
          {
            fact: "normalizedNote",
            operator: "matches",
            pattern:
              "(infarto|angina|anginos|coronar|isquemi|sudorese|suor frio|aperto no peito|pressao no peito)",
          },
        ],
      },
      true,
    ),
    draftRoute(
      "route.pattern.musculoskeletal",
      "orthopedics",
      "Localização combinada com trauma, movimento ou característica musculoesquelética.",
      {
        all: [
          equals("complaint", "Dor"),
          {
            any: [
              containsAny(["Trauma / queda", "Movimento piora"]),
              contains("Articulação específica"),
              {
                all: [
                  containsAny(["Braço / ombro", "Perna / quadril", "Costas"]),
                  containsAny(["Pontada", "Choque"]),
                ],
              },
            ],
          },
        ],
      },
    ),
    draftRoute(
      "route.review.respiratory",
      "pulmonology",
      "Alteração respiratória informada na revisão geral.",
      containsAny(["Respiratória", "Respiração"]),
    ),
    draftRoute(
      "route.review.urinary",
      "urology",
      "Alteração urinária informada na revisão geral.",
      containsAny(["Urinária", "Urina"]),
    ),
    draftRoute(
      "route.review.intestinal",
      "abdominal",
      "Alteração intestinal informada na revisão geral.",
      containsAny(["Intestinal", "Intestino"]),
    ),
    draftRoute(
      "route.review.skin",
      "dermatology",
      "Alteração de pele informada.",
      contains("Pele"),
    ),
    draftRoute(
      "route.review.visual",
      "ophthalmology",
      "Alteração visual informada.",
      contains("Visão"),
    ),
    draftRoute(
      "route.review.neurologic",
      "neurology",
      "Alteração neurológica informada.",
      contains("Neurológica"),
    ),
    draftRoute(
      "route.review.gynecologic",
      "gynecology",
      "Alteração ginecológica informada.",
      contains("Ginecológica"),
    ),
    draftRoute(
      "route.review.coloproctology",
      "coloproctology",
      "Sintoma anorretal ou sangramento nas fezes informado.",
      containsAny(["Sangue nas fezes", "Dor ao evacuar"]),
    ),
    draftRoute(
      "route.pattern.endocrine",
      "endocrinology",
      "Combinação de perda de peso e cansaço importante.",
      { all: [contains("Perda de peso"), contains("Cansaço importante")] },
    ),
    draftRoute(
      "route.pattern.systemic-inflammatory",
      "rheumatology",
      "Sinal sistêmico combinado com alteração de outro sistema.",
      {
        all: [
          containsAny(["Febre", "Perda de peso"]),
          containsAny(["Pele", "Urinária", "Respiratória"]),
        ],
      },
    ),
  ];

  return Object.freeze({
    version: VERSION,
    items: Object.freeze(rules.map((rule) => Object.freeze(rule))),
  });
});
