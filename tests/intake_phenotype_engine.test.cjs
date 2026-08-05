"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const phenotypeEngine = require("../decisionmed/static/intake-phenotype-engine.js");
const diagnosticEngine = require("../decisionmed/static/intake-diagnostic-engine.js");

const modules = [
  {
    module_id: "module.cardiology.acute-thoracic-syndrome",
    display_name: "Síndrome torácica aguda",
    entity_type: "initial_syndrome",
    primary_specialty: "cardiology",
    legacy_keys: ["cardiovascular_discomfort"],
  },
  {
    module_id: "module.orthopedics.musculoskeletal-presentation",
    display_name: "Quadro musculoesquelético em investigação",
    entity_type: "clinical_presentation",
    primary_specialty: "orthopedics",
    legacy_keys: ["musculoskeletal"],
  },
  {
    module_id: "module.cardiology.acute-coronary-syndrome",
    display_name: "Síndrome coronariana aguda",
    entity_type: "standardized_syndrome",
    primary_specialty: "cardiology",
    legacy_keys: [],
  },
  {
    module_id: "module.cardiology.stemi",
    display_name: "Infarto agudo do miocárdio com supradesnivelamento do segmento ST",
    entity_type: "diagnosis",
    primary_specialty: "cardiology",
    legacy_keys: [],
  },
  {
    module_id: "module.obstetrics.hypertensive-disorder-of-pregnancy",
    display_name: "Síndrome hipertensiva da gestação",
    entity_type: "standardized_syndrome",
    primary_specialty: "obstetrics",
    legacy_keys: [],
  },
];

const content = [
  {
    module_id: "module.cardiology.acute-thoracic-syndrome",
    anchor_values: [
      "Braço / ombro",
      "Aperto / pressão",
      "Esforço piora",
      "Suor frio",
    ],
    likely_hypotheses: ["Síndrome coronariana aguda (SCA)"],
    cannot_miss_hypotheses: ["Embolia pulmonar"],
    mimics: ["Dor musculoesquelética da parede torácica"],
    discriminators: [
      {
        question_id: "discriminator.cardiovascular.reproducible",
        text: "O desconforto é reproduzido ao apertar o local?",
        options: ["Não", "Ao apertar o local"],
      },
      {
        question_id: "discriminator.cardiovascular.duration",
        text: "Quanto dura cada episódio?",
        options: ["Segundos", "Mais de 20 minutos"],
      },
    ],
  },
  {
    module_id: "module.orthopedics.musculoskeletal-presentation",
    anchor_values: ["Braço / ombro", "Movimento piora", "Trauma / queda"],
    likely_hypotheses: ["Dor musculoesquelética"],
    cannot_miss_hypotheses: ["Síndrome compartimental"],
    mimics: ["Dor referida"],
    discriminators: [],
  },
  {
    module_id: "module.cardiology.acute-coronary-syndrome",
    anchor_values: ["Aperto / pressão", "Esforço piora", "Suor frio"],
    likely_hypotheses: ["Infarto agudo do miocárdio com supradesnivelamento do segmento ST"],
    cannot_miss_hypotheses: ["Instabilidade hemodinâmica"],
    mimics: ["Pericardite"],
    discriminators: [],
  },
  {
    module_id: "module.cardiology.stemi",
    anchor_values: ["dor ou desconforto"],
    diagnostic_criteria: ["Confirmar critérios eletrocardiográficos e clínicos."],
    discriminators: [
      {
        question_id: "question.cardiology.stemi.central",
        text: "Os critérios centrais para infarto com supra estão presentes?",
        options: ["Sim", "Não"],
      },
    ],
    source_ids: ["source.test.stemi"],
  },
  {
    module_id: "module.obstetrics.hypertensive-disorder-of-pregnancy",
    anchor_values: ["Dor"],
    likely_hypotheses: ["Síndrome hipertensiva da gestação"],
    cannot_miss_hypotheses: ["Eclâmpsia"],
    mimics: [],
    discriminators: [],
  },
];

phenotypeEngine.configureCatalog(modules, content);
phenotypeEngine.configureRules([
  {
    rule_id: "support.test.musculoskeletal",
    module_id: "module.cardiology.acute-thoracic-syndrome",
    version: "0.1.0",
    status: "draft",
    effect: "support",
    strength: "moderate",
    output_value: "Dor musculoesquelética da parede torácica",
    rationale: "Reprodução favorece origem musculoesquelética sem excluir causas graves.",
    source_ids: [],
    when: {
      fact: "answer_values.cardiovascular_reproducible",
      operator: "contains",
      value: "Ao apertar o local",
    },
  },
]);

function answer(id, values, question = id, section = "symptom") {
  return { id, values, question, section, module: "general" };
}

test("click selections form a phenotype without treating unknown or absent as present", () => {
  const phenotype = phenotypeEngine.buildPhenotype({
    complaint: "Dor",
    answers: [
      answer("symptom.location", ["Braço / ombro"]),
      answer("symptom.quality", ["Aperto / pressão"]),
      answer("symptom.associated", ["Suor frio", "Nenhum"]),
      answer("symptom.previous", ["Não sabe informar"]),
    ],
  });
  assert.ok(phenotype.present.some((item) => item.label === "Braço / ombro"));
  assert.ok(phenotype.present.some((item) => item.label === "Suor frio"));
  assert.ok(phenotype.absent.some((item) => item.label === "Nenhum"));
  assert.ok(phenotype.unknown.some((item) => item.label === "Não sabe informar"));
});

test("atypical ischemic phenotype ranks the thoracic syndrome before orthopedics", () => {
  const result = phenotypeEngine.rankSyndromes({
    complaint: "Dor",
    selectedModules: ["cardiology", "orthopedics"],
    answers: [
      answer("symptom.location", ["Braço / ombro"]),
      answer("symptom.quality", ["Aperto / pressão"]),
      answer("symptom.modifiers", ["Esforço piora"]),
      answer("symptom.associated", ["Suor frio"]),
    ],
  });
  assert.equal(result.candidates[0].key, "cardiovascular_discomfort");
  assert.equal(result.candidates[0].name, "Síndrome torácica aguda");
  assert.equal(result.probabilityCalibrated, false);
  assert.ok(result.trace.some((item) => item.applied));
});

test("generic pain cannot override the clinical area confirmed by routing", () => {
  const result = phenotypeEngine.rankSyndromes({
    complaint: "Dor",
    selectedModules: ["cardiology"],
    answers: [
      answer("symptom.location", ["Braço / ombro"]),
      answer("symptom.quality", ["Peso / desconforto"]),
      answer("symptom.modifiers", ["Esforço piora"]),
      answer("symptom.associated", ["Suor frio"]),
    ],
  });
  assert.equal(result.candidates[0].key, "cardiovascular_discomfort");
  assert.ok(result.candidates.every((item) => item.specialty === "cardiology"));
  assert.ok(
    result.trace.some(
      (item) => item.featureId === "confirmed-clinical-area" && item.applied,
    ),
  );
});

test("differential question plan is finite and begins with syndrome questions", () => {
  const plan = phenotypeEngine.planDifferentiation({
    syndromeKeys: ["cardiovascular_discomfort"],
    baseQuestions: content[0].discriminators.map((item) => ({
      id: item.question_id,
      text: item.text,
      options: item.options,
      module: "cardiovascular_discomfort",
      section: "discriminator",
    })),
    maxQuestions: 6,
  });
  assert.ok(plan.questions.length <= 6);
  assert.equal(plan.questions[0].questionOrigin, "confirmed_syndrome");
  assert.equal(plan.questions[0].phase, "differential");
  assert.match(plan.stopRule, /exame físico|Limite de perguntas/);
});

test("pathology effects are individual and cannot-miss hypotheses remain preserved", () => {
  const syndrome = {
    name: "Síndrome torácica aguda",
    supports: ["Aperto relacionado ao esforço."],
    sourceIds: [],
    contentSourceIds: [],
    differential: {
      likely: ["Síndrome coronariana aguda (SCA)"],
      cannotMiss: ["Embolia pulmonar"],
      mimics: ["Dor musculoesquelética da parede torácica"],
    },
  };
  const assessment = phenotypeEngine.analyzeDifferentials({
    syndromes: [syndrome],
    answers: [
      {
        ...answer(
          "discriminator.cardiovascular.reproducible",
          ["Ao apertar o local"],
          "O desconforto é reproduzido ao apertar o local?",
          "discriminator",
        ),
        module: "cardiovascular_discomfort",
      },
    ],
  });
  const musculoskeletal = assessment.profiles.find((item) =>
    item.name.includes("musculoesquelética"),
  );
  const embolism = assessment.profiles.find((item) => item.name === "Embolia pulmonar");
  assert.equal(musculoskeletal.assessmentStatus, "supported");
  assert.ok(musculoskeletal.present.length > 0);
  assert.equal(embolism.cannotMissPreserved, true);
  assert.equal(assessment.confirmedByEngine, false);

  const diagnostic = diagnosticEngine.analyze({
    reasoning: { syndromes: [] },
    syndromic: { classifications: [] },
    diagnosticProfiles: assessment,
  });
  assert.equal(diagnostic.status, "pathology_specific_differential_support");
  assert.equal(diagnostic.confirmedByEngine, false);
  assert.equal(
    diagnostic.candidates.find((item) => item.name === "Embolia pulmonar")
      .cannotMissPreserved,
    true,
  );
  assert.equal(
    diagnostic.candidates.find((item) => item.name.includes("musculoesquelética"))
      .criteriaScope,
    "pathology_specific_where_bound",
  );
});
