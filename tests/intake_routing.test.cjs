"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const ruleEngine = require("../decisionmed/static/intake-rule-engine.js");
const routingRules = require("../decisionmed/static/intake-routing-rules.js");
const routing = require("../decisionmed/static/intake-routing.js");
const sequences = require("../decisionmed/static/intake-sequences.js");
const cases = require("../decisionmed/static/intake-cases.js");
const reasoning = require("../decisionmed/static/intake-reasoning.js");

reasoning.configureRules([
  {
    rule_id: "support.test.cardiovascular.reproducible",
    module_id: "module.cardiology.acute-thoracic-syndrome",
    version: "0.1.0",
    status: "draft",
    effect: "support",
    strength: "moderate",
    output_value: "Dor musculoesquelética da parede torácica",
    priority: false,
    rationale: "Reprodução à palpação favorece origem musculoesquelética.",
    source_ids: [],
    when: {
      fact: "answer_values.cardiovascular_reproducible",
      operator: "contains",
      value: "Ao apertar o local",
    },
  },
  {
    rule_id: "alarm.test.neurologic",
    module_id: "module.neurology.acute-focal-neurological-deficit",
    version: "0.1.0",
    status: "draft",
    effect: "alarm",
    strength: "critical",
    output_value: "Sinal neurológico agudo informado na triagem.",
    priority: true,
    rationale: "Déficit focal exige avaliação imediata.",
    source_ids: [],
    when: {
      fact: "values",
      operator: "contains",
      value: "Fraqueza de um lado",
    },
  },
]);

test("DM-300 phase zero inventory matches the legacy reasoning catalog", () => {
  const inventory = JSON.parse(
    fs.readFileSync(
      path.join(
        __dirname,
        "..",
        "docs",
        "baselines",
        "dm300-phase0-module-inventory.json",
      ),
      "utf8",
    ),
  );
  assert.equal(inventory.reasoning_engine_version, "0.2.0");
  assert.equal(inventory.entry_count, reasoning.syndromeCatalog.length);
  assert.deepEqual(
    inventory.entries.map((item) => item.legacy_key),
    reasoning.syndromeCatalog.map((item) => item.key),
  );
  assert.deepEqual(
    inventory.entries.map((item) => item.entity_type),
    reasoning.syndromeCatalog.map((item) => item.entityType),
  );
});

test("external catalog hydrates identities without changing legacy routing keys", () => {
  const item = {
    module_id: "module.cardiology.acute-thoracic-syndrome",
    version: "1.0.0",
    display_name: "Síndrome torácica aguda governada",
    entity_type: "initial_syndrome",
    legacy_keys: ["cardiovascular_discomfort"],
    terminology_status: "candidate",
    content_status: "skeleton",
    status: "draft",
    sources: [{ source_id: "source.acc-aha.chest-pain.2021" }],
  };

  const result = reasoning.configureCatalog([item]);
  const catalogEntry = reasoning.syndromeCatalog.find(
    (entry) => entry.key === "cardiovascular_discomfort",
  );
  const analysisEntry = reasoning.analyze({
    complaint: "Dor",
    selectedModules: ["cardiology"],
    answers: [
      {
        id: "symptom.location",
        section: "symptom",
        module: "general",
        question: "Onde?",
        values: ["Peito"],
      },
    ],
  }).syndromes[0];

  assert.equal(result.matched, 1);
  assert.equal(result.complete, false);
  assert.equal(
    catalogEntry.moduleId,
    "module.cardiology.acute-thoracic-syndrome",
  );
  assert.equal(catalogEntry.name, "Síndrome torácica aguda governada");
  assert.equal(catalogEntry.status, "draft");
  assert.equal(analysisEntry.moduleId, catalogEntry.moduleId);
  assert.equal(analysisEntry.moduleStatus, "draft");
  assert.deepEqual(analysisEntry.sourceIds, [
    "source.acc-aha.chest-pain.2021",
  ]);
  assert.equal(analysisEntry.key, "cardiovascular_discomfort");

  reasoning.configureCatalog([]);
});

test("external content replaces the legacy prototype payload by module id", () => {
  reasoning.configureCatalog([
    {
      module_id: "module.cardiology.acute-thoracic-syndrome",
      version: "0.2.0",
      display_name: "Síndrome torácica aguda",
      entity_type: "initial_syndrome",
      legacy_keys: ["cardiovascular_discomfort"],
      terminology_status: "candidate",
      content_status: "partial",
      status: "draft",
      sources: [],
    },
  ]);
  const hydration = reasoning.configureContent([
    {
      module_id: "module.cardiology.acute-thoracic-syndrome",
      version: "0.1.0",
      status: "draft",
      content_status: "partial",
      anchor_values: ["Peito"],
      likely_hypotheses: ["Hipótese externa"],
      cannot_miss_hypotheses: ["Grave externa"],
      mimics: ["Imitador externo"],
      discriminators: [
        {
          question_id: "discriminator.external.duration",
          text: "Pergunta externa?",
          options: ["Sim", "Não"],
          rationale: null,
          detail_on_positive: false,
          detail_required: false,
          source_ids: [],
        },
      ],
      physical_examination: ["Exame externo"],
      complementary_exams: [
        {
          exam_id: "exam.external",
          name: "Exame externo",
          clinical_question: "Pergunta clínica externa?",
          when: "Quando indicado.",
          limitations: null,
          source_ids: [],
        },
      ],
      source_ids: [],
    },
  ]);
  const result = reasoning.analyze({
    complaint: "Dor",
    selectedModules: ["cardiology"],
    answers: [
      {
        id: "symptom.location",
        section: "symptom",
        module: "general",
        question: "Onde?",
        values: ["Peito"],
      },
    ],
  }).syndromes[0];

  assert.equal(hydration.matched, 1);
  assert.equal(result.contentVersion, "0.1.0");
  assert.equal(result.contentRecordStatus, "draft");
  assert.deepEqual(result.differential.likely, ["Hipótese externa"]);
  assert.deepEqual(result.physicalExam, ["Exame externo"]);
  assert.equal(result.tests[0].name, "Exame externo");
  assert.equal(
    reasoning.discriminatorQuestions(["cardiovascular_discomfort"])[0].id,
    "discriminator.external.duration",
  );

  reasoning.configureCatalog([]);
  reasoning.configureContent([]);
});

test("governed runtime exposes 300 modules and selects an exact direct entry", () => {
  const catalog = Array.from({ length: 300 }, (_, index) => ({
    module_id: `module.test.item-${index + 1}`,
    version: "0.1.0",
    display_name: `Módulo sintético ${index + 1}`,
    entity_type: index % 2 ? "diagnosis" : "clinical_presentation",
    primary_specialty: "internal-medicine",
    legacy_keys: index === 0 ? ["cardiovascular_discomfort"] : [],
    terminology_status: "candidate",
    content_status: "partial",
    status: "draft",
    sources: [],
  }));
  const content = catalog.map((item, index) => ({
    module_id: item.module_id,
    version: "0.1.0",
    status: "draft",
    content_status: "partial",
    anchor_values: [`Âncora ${index + 1}`],
    likely_hypotheses: [item.display_name],
    cannot_miss_hypotheses: ["Hipótese grave concorrente"],
    mimics: ["Imitador"],
    discriminators: [
      {
        question_id: `question.test.item-${index + 1}`,
        text: "Pergunta discriminadora?",
        options: ["Sim", "Não"],
        rationale: "Teste estrutural.",
        detail_on_positive: false,
        detail_required: false,
        source_ids: [],
      },
    ],
    physical_examination: ["Exame dirigido"],
    complementary_exams: [
      {
        exam_id: `exam.test.item-${index + 1}`,
        name: "Exame dirigido",
        clinical_question: "Muda a hipótese?",
        when: "Quando indicado.",
        limitations: "Interpretar no contexto.",
        source_ids: [],
      },
    ],
    source_ids: [],
  }));

  const catalogHydration = reasoning.configureCatalog(catalog);
  const contentHydration = reasoning.configureContent(content);
  const targetKey = "module.test.item-300";
  const result = reasoning.analyze({
    complaint: "Confirmação direta",
    selectedSyndromeKeys: [targetKey],
    selectedModules: ["generalmedicine"],
    answers: [],
  });

  assert.equal(catalogHydration.catalogCount, 300);
  assert.equal(contentHydration.matched, 300);
  assert.equal(reasoning.syndromeCatalog.length, 300);
  assert.equal(result.syndromes.length, 1);
  assert.equal(result.syndromes[0].key, targetKey);
  assert.equal(result.syndromes[0].moduleId, targetKey);

  reasoning.configureCatalog([]);
  reasoning.configureContent([]);
});

function resultFor(input) {
  return routing.suggestModules(input);
}

function keysFor(input) {
  return resultFor(input).map((item) => item.key);
}

function moduleFor(input, key) {
  return resultFor(input).find((item) => item.key === key);
}

test("declarative engine evaluates nested all, any and none conditions", () => {
  const compiled = ruleEngine.compileRules([
    {
      ruleId: "test.route.nested",
      version: "0.1.0",
      status: "draft",
      effect: "route",
      target: "cardiology",
      rationale: "Regra sintética.",
      when: {
        all: [
          { fact: "complaint", operator: "equals", value: "Dor" },
          {
            any: [
              {
                fact: "values",
                operator: "contains",
                value: "Peito",
              },
              {
                fact: "values",
                operator: "contains",
                value: "Braço / ombro",
              },
            ],
          },
        ],
        none: [
          {
            fact: "values",
            operator: "contains",
            value: "Dado incompatível",
          },
        ],
      },
    },
  ]);

  assert.equal(
    ruleEngine.evaluateRules(compiled, {
      complaint: "Dor",
      values: ["Braço / ombro"],
    }).length,
    1,
  );
  assert.equal(
    ruleEngine.evaluateRules(compiled, {
      complaint: "Dor",
      values: ["Peito", "Dado incompatível"],
    }).length,
    0,
  );
});

test("declarative engine fails closed for duplicate or invalid rules", () => {
  const valid = {
    ruleId: "test.route.valid",
    effect: "route",
    target: "generalmedicine",
    rationale: "Regra de teste.",
    when: { fact: "complaint", operator: "present" },
  };
  assert.throws(
    () => ruleEngine.compileRules([valid, { ...valid }]),
    /duplicate rule id/,
  );
  assert.throws(
    () =>
      ruleEngine.compileRules([
        { ...valid, ruleId: "test.route.invalid", when: {} },
      ]),
    /fact is required/,
  );
});

test("routing exposes fired rule ids and blocks clinical execution", () => {
  const cardiac = moduleFor(
    {
      complaint: "Dor",
      values: ["Peito", "Aperto / pressão", "Suor frio"],
    },
    "cardiology",
  );

  assert.ok(routingRules.items.length > 20);
  assert.ok(cardiac.ruleIds.includes("route.pain.chest.cardiology"));
  assert.ok(
    cardiac.ruleIds.includes("route.pattern.possible-anginal-equivalent"),
  );
  assert.equal(cardiac.clinicalExecutionAllowed, false);
  assert.ok(cardiac.ruleStatuses.every((status) => status === "draft"));
});

test("routing hydrates governed external rules and preserves local fallback", () => {
  const hydration = routing.configureRules([
    {
      rule_id: "route.external.dyspnea",
      module_id: "module.pulmonology.dyspnea-presentation",
      version: "0.1.0",
      status: "draft",
      effect: "route",
      output_key: "pulmonology",
      priority: false,
      rationale: "Regra externa de teste.",
      source_ids: [],
      when: {
        fact: "complaint",
        operator: "equals",
        value: "Falta de ar",
      },
    },
  ]);
  const result = moduleFor({ complaint: "Falta de ar" }, "pulmonology");

  assert.equal(hydration.count, 1);
  assert.equal(routing.ruleCatalogSource, "governed_external");
  assert.deepEqual(result.ruleIds, ["route.external.dyspnea"]);
  assert.deepEqual(result.moduleIds, [
    "module.pulmonology.dyspnea-presentation",
  ]);
  assert.equal(result.clinicalExecutionAllowed, false);

  const reset = routing.configureRules();
  assert.equal(reset.source, "local_fallback");
  assert.ok(routing.ruleCount > 20);
});

test("routes an atypical anginal-equivalent pattern to cardiology", () => {
  const input = {
    complaint: "Dor",
    values: [
      "Braço / ombro",
      "Peso / desconforto",
      "Esforço piora",
      "Náusea / vômito",
      "Suor frio",
    ],
  };
  const result = resultFor(input);

  assert.ok(result.some((item) => item.key === "cardiology"));
  assert.equal(moduleFor(input, "cardiology").priority, true);
  assert.ok(!result.some((item) => item.key === "orthopedics"));
});

test("free-text cardiovascular terms may only expand routing", () => {
  for (const note of [
    "infarto atípico",
    "equivalente anginoso",
    "suspeita de isquemia",
    "angina",
    "sudorese com mal-estar",
  ]) {
    const result = moduleFor({ complaint: "Outro sintoma", note }, "cardiology");
    assert.ok(result, note);
    assert.equal(result.priority, true, note);
  }
});

test("robot covers upper-body anginal-equivalent combinations", () => {
  const locations = [
    "Peito",
    "Braço / ombro",
    "Pescoço / mandíbula",
    "Costas",
    "Abdome superior",
  ];
  const patterns = ["Esforço físico", "Esforço piora", "Repouso melhora"];
  const associated = [
    "Falta de ar",
    "Suor frio",
    "Cansaço incomum",
    "Náusea / vômito",
    "Tontura / desmaio",
  ];

  for (const location of locations) {
    for (const pattern of patterns) {
      for (const symptom of associated) {
        const result = moduleFor(
          {
            complaint: "Dor",
            values: [location, pattern, symptom],
          },
          "cardiology",
        );
        assert.ok(result, `${location} + ${pattern} + ${symptom}`);
        assert.equal(result.priority, true);
      }
    }
  }
});

test("robot separates musculoskeletal patterns from isolated limb location", () => {
  assert.deepEqual(
    keysFor({ complaint: "Dor", values: ["Braço / ombro"] }),
    ["generalmedicine"],
  );

  for (const values of [
    ["Braço / ombro", "Trauma / queda"],
    ["Costas", "Movimento piora"],
    ["Perna / quadril", "Pontada"],
    ["Articulação específica"],
  ]) {
    const keys = keysFor({ complaint: "Dor", values });
    assert.ok(keys.includes("orthopedics"), values.join(" + "));
    assert.ok(!keys.includes("cardiology"), values.join(" + "));
  }
});

test("ambiguous combinations preserve all relevant modules", () => {
  const keys = keysFor({
    complaint: "Dor",
    values: [
      "Braço / ombro",
      "Movimento piora",
      "Esforço piora",
      "Suor frio",
    ],
  });

  assert.ok(keys.includes("cardiology"));
  assert.ok(keys.includes("orthopedics"));
});

test("direct complaints and unclassified patterns remain covered", () => {
  const direct = [
    ["Alteração urinária", "urology"],
    ["Alteração intestinal", "abdominal"],
    ["Pele", "dermatology"],
    ["Visão", "ophthalmology"],
    ["Neurológica", "neurology"],
    ["Ginecológica", "gynecology"],
    ["Gestação / pós-parto", "obstetrics"],
    ["Ossos / articulações", "orthopedics"],
    ["Humor / sono", "psychiatry"],
  ];

  for (const [complaint, expected] of direct) {
    assert.ok(keysFor({ complaint }).includes(expected), complaint);
  }
  assert.deepEqual(keysFor({ complaint: "Febre" }), ["generalmedicine"]);
  assert.deepEqual(keysFor({ complaint: "Outro sintoma" }), ["generalmedicine"]);
});

test("sequence generator covers every registered complaint without duplicate ids", () => {
  for (const complaint of sequences.complaints) {
    const sequence = sequences.buildSymptomQuestions(complaint);
    const ids = sequence.map((item) => item.id);

    assert.ok(sequence.length >= 9, complaint);
    assert.equal(new Set(ids).size, ids.length, complaint);
    assert.equal(ids[0], "symptom.started", complaint);
    assert.equal(ids.at(-1), "symptom.trend", complaint);
    assert.ok(sequence.every((item) => item.section === "symptom"), complaint);
  }
});

test("sequence generator changes questions according to the chief complaint", () => {
  const painIds = sequences.buildSymptomQuestions("Dor").map((item) => item.id);
  assert.ok(painIds.includes("symptom.location"));
  assert.ok(painIds.includes("symptom.quality"));
  assert.ok(painIds.includes("symptom.radiation"));

  const generalizedCases = [
    ["Febre", "symptom.fever_measurement"],
    ["Falta de ar", "symptom.dyspnea_context"],
    ["Tosse", "symptom.cough_type"],
    ["Humor / sono", "symptom.mental_type"],
  ];
  for (const [complaint, expected] of generalizedCases) {
    const ids = sequences
      .buildSymptomQuestions(complaint)
      .map((item) => item.id);
    assert.ok(ids.includes(expected), complaint);
    assert.ok(!ids.includes("symptom.location"), complaint);
  }
});

test("generated sequences are independent copies", () => {
  const first = sequences.buildSymptomQuestions("Dor");
  first[0].options.push("Mutação de teste");
  const second = sequences.buildSymptomQuestions("Dor");

  assert.ok(!second[0].options.includes("Mutação de teste"));
});

test("local case generator respects quantity and returns independent cases", () => {
  assert.equal(cases.buildCases(0).length, 1);
  assert.equal(cases.buildCases(7).length, 7);
  assert.equal(cases.buildCases(150).length, 100);

  const firstSuite = cases.buildCases(20);
  const secondSuite = cases.buildCases(20);
  firstSuite[0].answers["symptom.started"] = "Mutação de teste";

  assert.notEqual(
    secondSuite[0].answers["symptom.started"],
    "Mutação de teste",
  );
  assert.equal(new Set(secondSuite.map((scenario) => scenario.id)).size, 20);
});

test("case generator builds 15 cases for each of the three entry modes", () => {
  const suite = cases.buildSuite(15, "all");
  const counts = suite.reduce((result, scenario) => {
    result[scenario.flowMode] = (result[scenario.flowMode] || 0) + 1;
    return result;
  }, {});

  assert.equal(suite.length, 45);
  assert.deepEqual(counts, {
    assisted: 15,
    direct: 15,
    investigation: 15,
  });
  assert.equal(new Set(suite.map((scenario) => scenario.id)).size, 45);
  assert.ok(
    suite.every(
      (scenario) =>
        scenario.expectedModules.length &&
        Array.isArray(scenario.syndromeKeys),
    ),
  );
});

test("direct and investigation batteries use valid catalog syndromes", () => {
  const direct = cases.buildDirectCases(15);
  const investigation = cases.buildInvestigationCases(15);
  const validKeys = new Set(reasoning.syndromeKeys);

  assert.equal(
    new Set(direct.flatMap((scenario) => scenario.syndromeKeys)).size,
    reasoning.syndromeKeys.length,
  );
  assert.ok(
    direct.every(
      (scenario) =>
        scenario.syndromeKeys.length === 1 &&
        scenario.syndromeKeys.every((key) => validKeys.has(key)),
    ),
  );
  assert.ok(
    investigation.every(
      (scenario) =>
        scenario.syndromeKeys.length >= 2 &&
        scenario.syndromeKeys.length <= 3 &&
        new Set(scenario.syndromeKeys).size === scenario.syndromeKeys.length &&
        scenario.syndromeKeys.every((key) => validKeys.has(key)),
    ),
  );
});

test("every synthetic template reaches all modules declared for coverage", () => {
  for (const scenario of cases.buildCases(cases.templateCount)) {
    const values = Object.entries(scenario.answers)
      .filter(([key]) => !key.startsWith("module."))
      .flatMap(([, value]) =>
        Array.isArray(value)
          ? value
          : value && typeof value === "object"
            ? value.values
            : [value],
      )
      .filter(Boolean);
    const actual = keysFor({
      complaint: scenario.complaint,
      note: scenario.note,
      values,
    });

    for (const expected of scenario.expectedModules) {
      assert.ok(actual.includes(expected), `${scenario.id} -> ${expected}`);
    }
  }
});

test("reasoning engine creates representation, syndrome and three differential groups", () => {
  const result = reasoning.analyze({
    complaint: "Dor",
    note: "Peso no braço aos esforços com suor frio.",
    selectedModules: ["cardiology"],
    answers: [
      { id: "symptom.location", section: "symptom", module: "general", question: "Onde?", values: ["Braço / ombro"] },
      { id: "symptom.quality", section: "symptom", module: "general", question: "Como?", values: ["Peso / desconforto"] },
      { id: "symptom.modifiers", section: "symptom", module: "general", question: "Modificadores?", values: ["Esforço piora", "Repouso melhora"] },
      { id: "symptom.associated", section: "symptom", module: "general", question: "Associados?", values: ["Suor frio"] },
    ],
  });

  assert.match(result.representation, /braço \/ ombro/i);
  assert.equal(result.syndromes[0].key, "cardiovascular_discomfort");
  assert.ok(result.syndromes[0].supports.length >= 3);
  assert.ok(result.syndromes[0].differential.likely.length);
  assert.ok(result.syndromes[0].differential.cannotMiss.length);
  assert.ok(result.syndromes[0].differential.mimics.length);
  assert.ok(result.syndromes[0].physicalExam.length);
  assert.ok(result.syndromes[0].tests.every((item) => item.question));
  assert.ok(result.syndromes[0].tests.every((item) => item.when));
  assert.ok(
    result.syndromes[0].tests.some((item) =>
      item.name.includes("Troponina cardíaca de alta sensibilidade"),
    ),
  );
});

test("safety checkpoint distinguishes stable and immediate patterns", () => {
  const stable = reasoning.analyze({
    complaint: "Outro sintoma",
    answers: [
      { id: "safety.consciousness", section: "safety", module: "safety", question: "Consciência", values: ["Alerta e conversando normalmente"] },
      { id: "safety.breathing", section: "safety", module: "safety", question: "Respiração", values: ["Não"] },
    ],
  });
  const immediate = reasoning.analyze({
    complaint: "Neurológica",
    answers: [
      { id: "safety.neurologic", section: "safety", module: "safety", question: "Neurológico", values: ["Fraqueza de um lado"] },
    ],
  });

  assert.equal(stable.safety.level, "continue");
  assert.equal(immediate.safety.level, "immediate");
  assert.deepEqual(immediate.safety.ruleIds, ["alarm.test.neurologic"]);
});

test("only confirmed syndromes generate discriminator questions", () => {
  const cardiac = reasoning.discriminatorQuestions([
    "cardiovascular_discomfort",
  ]);
  const selected = reasoning.discriminatorQuestions(
    ["cardiovascular_discomfort", "respiratory"],
    ["discriminator.cardiovascular.duration"],
  );

  assert.ok(
    cardiac.every((question) =>
      question.id.startsWith("discriminator.cardiovascular."),
    ),
  );
  assert.ok(
    !selected.some(
      (question) => question.id === "discriminator.cardiovascular.duration",
    ),
  );
  assert.ok(
    selected.some((question) =>
      question.id.startsWith("discriminator.respiratory."),
    ),
  );
});

test("one catalog supports assisted, direct and investigation entry points", () => {
  assert.ok(reasoning.syndromeCatalog.length >= 10);
  assert.equal(
    new Set(reasoning.syndromeCatalog.map((item) => item.key)).size,
    reasoning.syndromeCatalog.length,
  );
  assert.ok(
    reasoning.syndromeCatalog.every(
      (item) =>
        item.key &&
        item.name &&
        item.entityType &&
        item.entityTypeLabel &&
        item.modules.length,
    ),
  );

  const selected = reasoning.syndromeCatalog.slice(0, 3).map((item) => item.key);
  const comparisonQuestions = reasoning.discriminatorQuestions(selected);
  assert.equal(
    new Set(comparisonQuestions.map((item) => item.id)).size,
    comparisonQuestions.length,
  );
  assert.ok(
    comparisonQuestions.every((item) => selected.includes(item.syndrome)),
  );
});

test("acute thoracic syndrome uses standardized diagnostic hypotheses", () => {
  const thoracic = reasoning.analyze({
    complaint: "Dor",
    selectedModules: ["cardiology"],
    answers: [
      { id: "symptom.location", section: "symptom", module: "general", question: "Onde?", values: ["Peito"] },
    ],
  }).syndromes[0];
  const hypotheses = [
    ...thoracic.differential.likely,
    ...thoracic.differential.cannotMiss,
    ...thoracic.differential.mimics,
  ];

  assert.equal(thoracic.key, "cardiovascular_discomfort");
  assert.equal(thoracic.name, "Síndrome torácica aguda");
  assert.equal(thoracic.entityType, "initial_syndrome");
  assert.equal(thoracic.entityTypeLabel, "Síndrome clínica inicial");
  [
    "Síndrome coronariana aguda (SCA)",
    "Isquemia miocárdica sem infarto: angina; ANOCA/INOCA conforme investigação",
    "Dissecção aguda de aorta",
    "Embolia pulmonar",
    "Pericardite aguda",
    "Tamponamento cardíaco",
    "Pneumotórax hipertensivo",
    "Dor musculoesquelética da parede torácica",
    "Doença esofágica",
    "Ansiedade ou síndrome de hiperventilação",
  ].forEach((name) => assert.ok(hypotheses.includes(name), name));
});

test("discriminator selections refine the ordered differential", () => {
  const result = reasoning.analyze({
    complaint: "Dor",
    selectedModules: ["cardiology"],
    answers: [
      { id: "symptom.location", section: "symptom", module: "general", question: "Onde?", values: ["Peito"] },
      { id: "discriminator.cardiovascular.reproducible", section: "discriminator", module: "cardiovascular_discomfort", question: "Reproduz?", values: ["Ao apertar o local"] },
    ],
  });

  assert.equal(
    result.syndromes[0].differential.likely[0],
    "Dor musculoesquelética da parede torácica",
  );
  assert.equal(
    result.syndromes[0].differential.rules[0].ruleId,
    "support.test.cardiovascular.reproducible",
  );
  assert.ok(
    result.syndromes[0].differential.likely.includes(
      "Síndrome coronariana aguda (SCA)",
    ),
  );
});

test("neutral discriminator answers are not counted as supporting evidence", () => {
  const result = reasoning.analyze({
    complaint: "Confirmação direta",
    selectedModules: ["cardiology"],
    answers: [
      {
        id: "discriminator.cardiovascular.duration",
        section: "discriminator",
        module: "cardiovascular_discomfort",
        question: "Quanto dura cada episódio?",
        values: ["Segundos"],
      },
    ],
  });

  assert.ok(
    !result.syndromes[0].supports.some((item) =>
      item.startsWith("Discriminador:"),
    ),
  );
});
