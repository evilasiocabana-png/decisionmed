(function exposeDecisionMedCases(root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  } else {
    root.DecisionMedCases = api;
  }
})(typeof globalThis === "object" ? globalThis : this, function createCaseGenerator() {
  "use strict";

  const VERSION = "0.3.0";
  const SYNTHETIC_AGES = Object.freeze([
    62, 58, 34, 29, 51, 67, 46, 53, 38, 42, 31, 27, 45, 36, 54,
  ]);
  const TEMPLATES = Object.freeze([
    {
      id: "cardiac-equivalent",
      label: "Equivalente anginoso com dor no braço",
      complaint: "Dor",
      note: "Desconforto em peso no braço durante esforço, acompanhado de suor frio e náusea.",
      expectedModules: ["cardiology"],
      answers: {
        "safety.circulation": "Desconforto atual com suor frio ou náusea",
        "symptom.started": "Hoje",
        "symptom.onset": "De repente",
        "symptom.trigger": ["Esforço físico"],
        "symptom.location": "Braço / ombro",
        "symptom.quality": "Peso / desconforto",
        "symptom.intensity": "7",
        "symptom.radiation": ["Pescoço / mandíbula"],
        "symptom.pattern": "Contínuo",
        "symptom.modifiers": ["Esforço piora", "Repouso melhora"],
        "symptom.associated": ["Suor frio", "Náusea / vômito"],
        "symptom.trend": "Pior",
        "history.chronic": { values: ["Hipertensão", "Diabetes"], detail: "Em acompanhamento regular." },
        "module.cardiology.2": { values: ["Sim"], detail: "Desconforto relacionado ao esforço, com irradiação." },
      },
    },
    {
      id: "cardiac-chest-pressure",
      label: "Pressão torácica aos esforços",
      complaint: "Dor",
      note: "Pressão no peito ao caminhar, com falta de ar e alívio ao repouso.",
      expectedModules: ["cardiology"],
      answers: {
        "safety.circulation": "Desconforto persistente no peito",
        "symptom.location": "Peito",
        "symptom.quality": "Aperto / pressão",
        "symptom.trigger": ["Esforço físico"],
        "symptom.modifiers": ["Esforço piora", "Repouso melhora"],
        "symptom.associated": ["Falta de ar"],
        "symptom.intensity": "6",
        "module.cardiology.2": { values: ["Sim"], detail: "Falta de ar aos esforços." },
      },
    },
    {
      id: "respiratory-wheeze",
      label: "Falta de ar com chiado",
      complaint: "Falta de ar",
      note: "Falta de ar e chiado após exposição a poeira.",
      expectedModules: ["pulmonology"],
      answers: {
        "symptom.trigger": ["Outro"],
        "symptom.dyspnea_context": ["Ao esforço"],
        "symptom.associated": ["Nenhum"],
        "module.pulmonology.2": ["Com exposição / ambiente"],
        "module.pulmonology.6": { values: ["Sim"], detail: "Chiado percebido durante as crises." },
      },
    },
    {
      id: "urinary-dysuria",
      label: "Disúria e urgência urinária",
      complaint: "Alteração urinária",
      note: "Ardência para urinar, maior frequência e urgência.",
      expectedModules: ["urology"],
      answers: {
        "symptom.location": "Região urinária / pélvica",
        "symptom.urinary_type": ["Dor / ardência", "Maior frequência", "Urgência"],
        "module.urology.1": { values: ["Sim"], detail: "Ardência durante a micção." },
        "module.urology.3": { values: ["Sim"], detail: "Urgência de início recente." },
      },
    },
    {
      id: "intestinal-bleeding",
      label: "Alteração intestinal com sangue",
      complaint: "Alteração intestinal",
      note: "Mudança do hábito intestinal com sangue nas fezes.",
      expectedModules: ["abdominal", "coloproctology"],
      answers: {
        "symptom.location": "Abdome inferior",
        "symptom.bowel_type": ["Sangue nas fezes", "Mudança no formato das fezes"],
        "module.abdominal.7": { values: ["Sim"], detail: "Sangue observado nas fezes." },
        "module.coloproctology.3": { values: ["Sim"], detail: "Sangue vermelho observado." },
      },
    },
    {
      id: "neurologic-sudden-weakness",
      label: "Déficit neurológico súbito",
      complaint: "Neurológica",
      note: "Perda súbita de força e alteração da fala.",
      expectedModules: ["neurology"],
      answers: {
        "safety.neurologic": "Mais de um sinal",
        "symptom.onset": "De repente",
        "symptom.location": "Braço / ombro",
        "symptom.neuro_type": ["Perda de força", "Alteração da fala"],
        "module.neurology.1": { values: ["Sim"], detail: "Perda de força em um lado." },
        "module.neurology.2": { values: ["Sim"], detail: "Início percebido de repente." },
      },
    },
    {
      id: "skin-changing-lesion",
      label: "Lesão de pele em mudança",
      complaint: "Pele",
      note: "Mancha que cresceu e mudou de cor nas últimas semanas.",
      expectedModules: ["dermatology"],
      answers: {
        "symptom.location": "Pele",
        "symptom.skin_type": ["Mancha"],
        "module.dermatology.2": { values: ["Sim"], detail: "Mudança de cor percebida." },
        "module.dermatology.6": { values: ["Sim"], detail: "Crescimento progressivo." },
      },
    },
    {
      id: "visual-flashes",
      label: "Alteração visual com flashes",
      complaint: "Visão",
      note: "Manchas e flashes de início recente na visão.",
      expectedModules: ["ophthalmology"],
      answers: {
        "symptom.location": "Olhos",
        "symptom.vision_type": ["Manchas / flashes"],
        "module.ophthalmology.5": { values: ["Sim"], detail: "Flashes e manchas móveis." },
      },
    },
    {
      id: "orthopedic-trauma",
      label: "Dor articular após trauma",
      complaint: "Ossos / articulações",
      note: "Dor e limitação de movimento após queda.",
      expectedModules: ["orthopedics"],
      answers: {
        "symptom.trigger": ["Trauma / queda"],
        "symptom.location": "Articulação específica",
        "symptom.orthopedic_type": ["Dor", "Trauma / queda", "Limitação de movimento"],
        "symptom.modifiers": ["Movimento piora"],
        "module.orthopedics.3": { values: ["Sim"], detail: "Queda antes do início da dor." },
      },
    },
    {
      id: "gynecologic-bleeding",
      label: "Sangramento ginecológico fora do período",
      complaint: "Ginecológica",
      note: "Sangramento fora do período acompanhado de dor pélvica.",
      expectedModules: ["gynecology"],
      answers: {
        "symptom.location": "Região urinária / pélvica",
        "symptom.gyne_type": ["Sangramento fora do período", "Dor pélvica"],
        "module.gynecology.2": { values: ["Sim"], detail: "Sangramento fora da data esperada." },
      },
    },
    {
      id: "obstetric-bleeding",
      label: "Gestação com sangramento",
      complaint: "Gestação / pós-parto",
      note: "Gestação confirmada com sangramento vaginal.",
      expectedModules: ["obstetrics"],
      answers: {
        "safety.bleeding": "Quantidade moderada",
        "symptom.location": "Região urinária / pélvica",
        "symptom.obstetric_context": "Gestação confirmada",
        "symptom.associated": ["Sangramento"],
        "module.obstetrics.3": { values: ["Sim"], detail: "Sangramento vaginal durante a gestação." },
      },
    },
    {
      id: "mental-sleep",
      label: "Ansiedade e insônia",
      complaint: "Humor / sono",
      note: "Preocupação persistente e dificuldade para iniciar o sono.",
      expectedModules: ["psychiatry"],
      answers: {
        "symptom.trigger": ["Estresse"],
        "symptom.mental_type": ["Ansiedade / preocupação", "Insônia"],
        "module.psychiatry.1": { values: ["Sim"], detail: "Preocupação na maior parte dos dias." },
        "module.psychiatry.3": ["Dificuldade para iniciar"],
      },
    },
    {
      id: "endocrine-systemic",
      label: "Perda de peso e cansaço",
      complaint: "Outro sintoma",
      note: "Perda de peso não intencional e cansaço importante.",
      expectedModules: ["endocrinology"],
      answers: {
        "review.general": ["Perda de peso", "Cansaço importante"],
        "module.endocrinology.1": ["Perdeu peso"],
        "module.endocrinology.2": { values: ["Sim"], detail: "Cansaço persistente." },
      },
    },
    {
      id: "systemic-skin",
      label: "Febre e manifestações cutâneas",
      complaint: "Febre",
      note: "Febre medida acompanhada de manchas na pele.",
      expectedModules: ["dermatology", "rheumatology"],
      answers: {
        "symptom.fever_measurement": "38 a 38,9 °C",
        "symptom.associated": ["Febre"],
        "review.other": ["Pele"],
        "review.general": ["Febre"],
        "module.rheumatology.1": { values: ["Sim"], detail: "Febre medida nos últimos dias." },
        "module.rheumatology.2": { values: ["Sim"], detail: "Manchas recentes na pele." },
      },
    },
    {
      id: "unclassified-fatigue",
      label: "Sintoma ainda não classificado",
      complaint: "Outro sintoma",
      note: "Mal-estar inespecífico sem localização ou padrão definido.",
      expectedModules: ["generalmedicine"],
      answers: {},
    },
  ]);

  const SYNDROME_MODULES = Object.freeze({
    cardiovascular_discomfort: ["cardiology"],
    respiratory: ["pulmonology"],
    focal_neurologic: ["neurology"],
    lower_urinary_tract: ["urology"],
    abdominal: ["abdominal", "coloproctology"],
    cutaneous: ["dermatology"],
    visual: ["ophthalmology"],
    musculoskeletal: ["orthopedics"],
    gynecologic_pelvic: ["gynecology"],
    obstetric: ["obstetrics"],
    metabolic_endocrine: ["endocrinology"],
    systemic_inflammatory: ["rheumatology"],
    mental_health: ["psychiatry"],
    general_unclassified: ["generalmedicine"],
  });

  const PRIMARY_SYNDROMES = Object.freeze([
    "cardiovascular_discomfort",
    "cardiovascular_discomfort",
    "respiratory",
    "lower_urinary_tract",
    "abdominal",
    "focal_neurologic",
    "cutaneous",
    "visual",
    "musculoskeletal",
    "gynecologic_pelvic",
    "obstetric",
    "mental_health",
    "metabolic_endocrine",
    "systemic_inflammatory",
    "general_unclassified",
  ]);

  const INVESTIGATION_PAIRS = Object.freeze([
    ["cardiovascular_discomfort", "musculoskeletal"],
    ["cardiovascular_discomfort", "respiratory"],
    ["respiratory", "cardiovascular_discomfort"],
    ["lower_urinary_tract", "gynecologic_pelvic"],
    ["abdominal", "lower_urinary_tract"],
    ["focal_neurologic", "metabolic_endocrine"],
    ["cutaneous", "systemic_inflammatory"],
    ["visual", "focal_neurologic"],
    ["musculoskeletal", "systemic_inflammatory"],
    ["gynecologic_pelvic", "obstetric"],
    ["obstetric", "gynecologic_pelvic"],
    ["mental_health", "metabolic_endocrine"],
    ["metabolic_endocrine", "systemic_inflammatory"],
    ["systemic_inflammatory", "cutaneous"],
    ["general_unclassified", "metabolic_endocrine"],
  ]);

  function cloneTemplate(template, index) {
    const cycle = Math.floor(index / TEMPLATES.length) + 1;
    return {
      ...template,
      id: `${template.id}-${cycle}`,
      label: cycle === 1 ? template.label : `${template.label} · variação ${cycle}`,
      expectedModules: [...template.expectedModules],
      answers: Object.fromEntries(
        Object.entries(template.answers).map(([key, value]) => [
          key,
          value && typeof value === "object" && !Array.isArray(value)
            ? { ...value, values: [...value.values] }
            : Array.isArray(value)
              ? [...value]
              : value,
        ]),
      ),
    };
  }

  function safeQuantity(quantity) {
    const parsed = Number.parseInt(quantity, 10);
    return Number.isFinite(parsed)
      ? Math.min(100, Math.max(1, parsed))
      : 1;
  }

  function syntheticPatient(mode, index) {
    const prefixes = {
      assisted: "A",
      direct: "D",
      investigation: "I",
    };
    const cycle = Math.floor(index / TEMPLATES.length);
    return {
      name: `Paciente sintético ${prefixes[mode]}-${String(index + 1).padStart(3, "0")}`,
      ageYears: Math.min(
        95,
        SYNTHETIC_AGES[index % SYNTHETIC_AGES.length] + cycle,
      ),
      synthetic: true,
    };
  }

  function buildAssistedCases(quantity = 1) {
    return Array.from({ length: safeQuantity(quantity) }, (_, index) => {
      const base = cloneTemplate(TEMPLATES[index % TEMPLATES.length], index);
      return {
        ...base,
        id: `assisted-${base.id}`,
        flowMode: "assisted",
        syndromeKeys: [],
        patient: syntheticPatient("assisted", index),
      };
    });
  }

  function buildDirectCases(quantity = 1) {
    return Array.from({ length: safeQuantity(quantity) }, (_, index) => {
      const base = cloneTemplate(TEMPLATES[index % TEMPLATES.length], index);
      const syndromeKey = PRIMARY_SYNDROMES[index % PRIMARY_SYNDROMES.length];
      return {
        ...base,
        id: `direct-${base.id}`,
        label: `Direto · ${base.label}`,
        flowMode: "direct",
        syndromeKeys: [syndromeKey],
        expectedModules: [...SYNDROME_MODULES[syndromeKey]],
        patient: syntheticPatient("direct", index),
      };
    });
  }

  function buildInvestigationCases(quantity = 1) {
    return Array.from({ length: safeQuantity(quantity) }, (_, index) => {
      const base = cloneTemplate(TEMPLATES[index % TEMPLATES.length], index);
      const syndromeKeys = [...INVESTIGATION_PAIRS[index % INVESTIGATION_PAIRS.length]];
      return {
        ...base,
        id: `investigation-${base.id}`,
        label: `Investigação · ${base.label}`,
        flowMode: "investigation",
        syndromeKeys,
        patient: syntheticPatient("investigation", index),
        expectedModules: [
          ...new Set(syndromeKeys.flatMap((key) => SYNDROME_MODULES[key])),
        ],
      };
    });
  }

  function buildCases(quantity = 1) {
    return buildAssistedCases(quantity);
  }

  function buildSuite(quantityPerMode = 15, mode = "all") {
    const builders = {
      assisted: buildAssistedCases,
      direct: buildDirectCases,
      investigation: buildInvestigationCases,
    };
    if (mode in builders) return builders[mode](quantityPerMode);
    return [
      ...buildAssistedCases(quantityPerMode),
      ...buildDirectCases(quantityPerMode),
      ...buildInvestigationCases(quantityPerMode),
    ];
  }

  return Object.freeze({
    version: VERSION,
    templateCount: TEMPLATES.length,
    buildCases,
    buildSuite,
    buildAssistedCases,
    buildDirectCases,
    buildInvestigationCases,
    investigationPairCount: INVESTIGATION_PAIRS.length,
  });
});
