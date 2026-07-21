const COMMON_PHENOTYPES = [
  "Ansiedade",
  "Depressao",
  "Dor",
  "Insonia",
  "Baixa energia",
  "Lentificacao",
  "Irritabilidade",
  "Compulsividade",
  "Psicose",
  "Humor elevado",
];

const COMMON_SYMPTOMS = [
  "Humor deprimido",
  "Anedonia",
  "Ansiedade",
  "Tensao",
  "Insonia inicial",
  "Insonia terminal",
  "Dor",
  "Fadiga",
  "Baixa concentracao",
  "Irritabilidade",
  "Impulsividade",
  "Compulsao",
  "Craving/uso de substancias",
  "Sintomas psicoticos",
  "Instabilidade do humor",
  "Disfuncao sexual",
  "Ganho de peso",
  "Ideacao suicida",
  "Efeitos adversos",
];

const ESSENTIAL_SAFETY_ASSESSMENTS = [
  ["suicide", "Risco suicida"],
  ["aggression", "Risco de agressividade"],
  ["mania_or_hypomania", "Ativacao, mania ou hipomania"],
  ["substances", "Alcool, substancias ou medicacao sem controle"],
  ["delirium", "Delirium ou alteracao aguda da consciencia"],
  ["intoxication", "Intoxicacao"],
  ["withdrawal", "Abstinencia"],
  ["allergies", "Alergias medicamentosas"],
  ["severe_adverse_reaction", "Reacao adversa grave previa"],
  ["interactions", "Interacoes medicamentosas relevantes"],
  ["qt_risk", "Risco de prolongamento do QT"],
  ["metabolic_risk", "Risco metabolico relevante"],
];

const SUICIDE_SAFETY_DETAILS = [
  ["suicide_plan", "Plano atual"],
  ["suicide_intent", "Intencao atual"],
  ["suicide_means_access", "Acesso a meios"],
  ["suicide_recent_attempt", "Tentativa recente"],
];

const CLINICAL_AXES = [
  "humor/TEPT",
  "sono/sedacao",
  "ansiedade/resgate",
  "impulsividade/irritabilidade",
  "compulsividade/TOC",
  "substancias/craving",
  "dor/sintomas somaticos",
  "energia/cognicao",
  "libido/funcao sexual",
  "peso/metabolico",
  "estabilizacao do humor",
  "psicose/organizacao do pensamento",
  "efeito adverso/contramedicacao",
];

const PREFERRED_MEDICATIONS_BY_AXIS = {
  "humor/TEPT": ["fluoxetina", "sertralina", "escitalopram", "venlafaxina", "duloxetina"],
  "sono/sedacao": ["trazodona", "mirtazapina", "quetiapina", "zolpidem"],
  "ansiedade/resgate": ["clonazepam", "bromazepam", "diazepam", "alprazolam", "lorazepam"],
  "impulsividade/irritabilidade": ["divalproato", "carbamazepina", "quetiapina", "risperidona"],
  "compulsividade/TOC": ["fluvoxamina", "sertralina", "fluoxetina", "clomipramina"],
  "substancias/craving": ["naltrexona", "acamprosato", "buprenorfina", "bupropiona"],
  "dor/sintomas somaticos": ["duloxetina", "amitriptilina", "nortriptilina", "venlafaxina"],
  "energia/cognicao": ["bupropiona", "venlafaxina", "desvenlafaxina", "metilfenidato IR", "metilfenidato LP"],
  "libido/funcao sexual": ["bupropiona", "agomelatina", "vortioxetina"],
  "peso/metabolico": ["bupropiona", "agomelatina", "fluoxetina"],
  "estabilizacao do humor": ["litio", "lamotrigina", "divalproato", "carbamazepina"],
  "psicose/organizacao do pensamento": ["quetiapina", "risperidona", "olanzapina", "aripiprazol", "haloperidol"],
  "efeito adverso/contramedicacao": ["biperideno", "prometazina", "propranolol"],
};

const TEST_SIGNALS_BY_AXIS = {
  "humor/TEPT": {phenotypes: {"Depressao": 3, "Ansiedade": 2}, symptoms: ["Humor deprimido", "Anedonia"]},
  "sono/sedacao": {phenotypes: {"Insonia": 4, "Ansiedade": 2}, symptoms: ["Insonia inicial", "Insonia terminal"]},
  "ansiedade/resgate": {phenotypes: {"Ansiedade": 4}, symptoms: ["Ansiedade", "Tensao"]},
  "impulsividade/irritabilidade": {phenotypes: {"Irritabilidade": 4}, symptoms: ["Irritabilidade", "Impulsividade"]},
  "compulsividade/TOC": {phenotypes: {"Compulsividade": 4, "Ansiedade": 2}, symptoms: ["Compulsao", "Ansiedade"]},
  "substancias/craving": {phenotypes: {"Compulsividade": 4, "Ansiedade": 2}, symptoms: ["Craving/uso de substancias", "Compulsao"]},
  "dor/sintomas somaticos": {phenotypes: {"Dor": 4, "Depressao": 2}, symptoms: ["Dor", "Fadiga"]},
  "energia/cognicao": {phenotypes: {"Baixa energia": 4, "Lentificacao": 3}, symptoms: ["Fadiga", "Baixa concentracao"]},
  "libido/funcao sexual": {phenotypes: {"Depressao": 2}, symptoms: ["Disfuncao sexual"]},
  "peso/metabolico": {phenotypes: {"Depressao": 2}, symptoms: ["Ganho de peso"]},
  "estabilizacao do humor": {phenotypes: {"Humor elevado": 3, "Irritabilidade": 3}, symptoms: ["Instabilidade do humor", "Irritabilidade", "Impulsividade"]},
  "psicose/organizacao do pensamento": {phenotypes: {"Psicose": 4}, symptoms: ["Sintomas psicoticos", "Baixa concentracao"]},
  "efeito adverso/contramedicacao": {phenotypes: {"Ansiedade": 2}, symptoms: ["Efeitos adversos"]},
};

function clinicalSignalsForAxes(blueprint, axes) {
  const phenotypes = {...(blueprint?.phenotypes || {})};
  const symptoms = new Set(blueprint?.symptoms || []);
  (axes || []).forEach((axis) => {
    const signals = TEST_SIGNALS_BY_AXIS[axis];
    if (!signals) return;
    Object.entries(signals.phenotypes || {}).forEach(([name, intensity]) => {
      phenotypes[name] = Math.max(Number(phenotypes[name] || 0), Number(intensity || 0));
    });
    (signals.symptoms || []).forEach((symptom) => symptoms.add(symptom));
  });
  return {phenotypes, symptoms: Array.from(symptoms)};
}

const PRESENTATIONS = {
  "Primeira consulta": {
    profile: ["boa tolerabilidade", "baixo prejuizo cognitivo", "compatibilidade com seguranca"],
    strategies: ["investigar", "observar", "otimizar", "trocar", "associar", "reavaliar diagnostico"],
  },
  "Seguimento": {
    profile: ["boa tolerabilidade", "manutencao longitudinal", "baixo prejuizo cognitivo"],
    strategies: ["observar", "otimizar", "trocar", "associar", "corrigir adesao"],
  },
  "Crise": {
    profile: ["seguranca imediata", "rapida estabilizacao", "monitorizacao intensiva"],
    strategies: ["avaliacao urgente", "corrigir risco", "encaminhar", "otimizar", "associar"],
  },
  "Segunda opiniao": {
    profile: ["alternativas rastreaveis", "boa tolerabilidade", "rastreabilidade da escolha"],
    strategies: ["revisar historico", "reavaliar diagnostico", "otimizar", "trocar", "associar"],
  },
  "Revisao medicamentosa": {
    profile: ["revisar carga medicamentosa", "reduzir efeitos adversos", "preservar resposta"],
    strategies: ["otimizar", "trocar", "reduzir carga", "retirar gradual", "corrigir adesao"],
  },
};

const CARD_ORDER = [
  "presentation",
  "population",
  "diagnosis",
  "phenotype",
  "symptoms",
  "objective",
  "medication",
  "safety-review",
  "acute-safety",
  "profile",
  "restrictions",
  "decision",
  "monitoring",
];

let currentMedicationItems = [];
let currentMedicationDetails = [];
let medicationOptionNames = [];
let medicationClassByName = new Map();
let acuteToxidromeSignals = [];
let nextRandomCaseIndex = 0;
let pendingScenarioClinicalContextIds = [];
let activeScenarioSequenceLabel = "";

let RANDOM_CASES = [];

const PRESCRIPTION_EXAMPLE_CASE = {
  patient: "Sr. Carlsson",
  birthDate: "1980-01-01",
  diagnosis: "Transtorno de estresse pos-traumatico",
  presentation: "Revisao medicamentosa",
  phenotypes: {
    "Ansiedade": 4,
    "Depressao": 4,
    "Irritabilidade": 4,
    "Compulsividade": 3,
    "Insonia": 2,
  },
  symptoms: [
    "Ansiedade",
    "Irritabilidade",
    "Impulsividade",
    "Ideacao suicida",
    "Compulsao",
    "Insonia inicial",
  ],
  clinicalAxes: [
    "humor/TEPT",
    "sono/sedacao",
    "ansiedade/resgate",
    "impulsividade/irritabilidade",
    "substancias/craving",
  ],
  secondaryObjectives: [
    "reduzir sedacao",
    "melhorar cognicao",
    "minimizar interacoes",
  ],
  restrictions: [
    "Alcool/drogas ou medicacao sem controle",
    "Interacoes relevantes",
    "Risco cardiovascular",
  ],
  medications: [
    {
      name: "Naltrexona",
      reason_for_use: "substancias/craving",
      dose_value: "50",
      dose_prescribed: "50",
      dose_unit: "mg",
      frequency: "1x/dia",
      duration: "mais de 8 semanas",
      adherence: "Irregular",
      response: "Resposta parcial",
      tolerability: "Boa",
    },
    {
      name: "Trazodona",
      reason_for_use: "sono/sedacao",
      dose_value: "50",
      dose_prescribed: "50",
      dose_unit: "mg",
      frequency: "noite",
      duration: "mais de 8 semanas",
      adherence: "Irregular",
      response: "Resposta parcial",
      tolerability: "Boa",
    },
    {
      name: "Fluoxetina",
      reason_for_use: "humor/TEPT",
      dose_value: "20",
      dose_prescribed: "20",
      dose_unit: "mg",
      frequency: "1x/dia",
      duration: "mais de 8 semanas",
      adherence: "Irregular",
      response: "Resposta parcial",
      tolerability: "Boa",
    },
    {
      name: "Clonazepam",
      reason_for_use: "ansiedade/resgate",
      dose_value: "0.25",
      dose_prescribed: "0.25",
      dose_unit: "mg",
      frequency: "1x/dia",
      duration: "mais de 8 semanas",
      adherence: "Irregular",
      response: "Resposta parcial",
      tolerability: "Boa",
    },
    {
      name: "Bromazepam",
      reason_for_use: "ansiedade/resgate",
      dose_value: "6",
      dose_prescribed: "6",
      dose_unit: "mg",
      frequency: "1x/dia",
      duration: "mais de 8 semanas",
      adherence: "Irregular",
      response: "Resposta parcial",
      tolerability: "Boa",
    },
  ],
};

const CLINICAL_THEORY = {
  depression: {
    characterization: "Humor deprimido e/ou perda de interesse ou prazer, acompanhados por alteracoes cognitivas, somaticas e comportamentais. A avaliacao deve considerar duracao, curso, gravidade, prejuizo funcional, sintomas psicoticos e risco de suicidio.",
    differentials: "Transtorno bipolar; reacao de luto ou transtorno de adaptacao; transtornos de ansiedade e relacionados a trauma; uso, abstinencia ou efeito de substancias/medicamentos; causas clinicas, incluindo alteracoes tireoidianas; transtornos psicoticos quando houver psicose.",
    sources: [
      ["WHO-CDDR", "https://www.who.int/publications/i/item/9789240077263/"],
      ["NICE-NG222", "https://www.nice.org.uk/guidance/ng222/chapter/Recommendations"],
      ["NIMH-DEP", "https://www.nimh.nih.gov/health/publications/depression"],
    ],
  },
  bipolar: {
    characterization: "Episodios definidos de mudanca do humor, energia e atividade, com mania ou hipomania e possiveis episodios depressivos. O curso longitudinal, a reducao da necessidade de sono, a desinibicao e a elevacao de atividade ajudam a reconhecer o espectro.",
    differentials: "Espectro da esquizofrenia; depressao unipolar; transtornos de personalidade; TDAH; uso de alcool, drogas ou medicamentos; causas clinicas como hipo ou hipertireoidismo.",
    sources: [
      ["WHO-CDDR", "https://www.who.int/publications/i/item/9789240077263/"],
      ["NICE-CG185", "https://www.nice.org.uk/guidance/cg185/chapter/recommendations"],
      ["NIMH-BD", "https://www.nimh.nih.gov/health/publications/bipolar-disorder"],
    ],
  },
  anxiety: {
    characterization: "Ansiedade ou preocupacao excessiva, dificil de controlar, associada a tensao, inquietacao, fadiga, dificuldade de concentracao, irritabilidade ou alteracao do sono. No panico, destacam-se crises inesperadas recorrentes e preocupacao persistente com novas crises ou suas consequencias.",
    differentials: "Depressao; outros transtornos de ansiedade; TEPT; TOC; uso ou abstinencia de substancias; efeitos medicamentosos; doencas cardiacas, respiratorias, endocrinas ou neurologicas capazes de produzir sintomas semelhantes.",
    sources: [
      ["WHO-CDDR", "https://www.who.int/publications/i/item/9789240077263/"],
      ["NICE-CG113", "https://www.nice.org.uk/guidance/cg113/chapter/Recommendations"],
    ],
  },
  trauma: {
    characterization: "Quadro relacionado a exposicao traumatica, caracterizado por revivencia do evento, evitacao, percepcao persistente de ameaca ou hiperativacao e alteracoes emocionais/cognitivas, com sofrimento ou prejuizo funcional.",
    differentials: "Reacao aguda ao estresse; transtorno de adaptacao; depressao; transtornos de ansiedade; transtornos dissociativos; uso de substancias; lesao cerebral ou outras causas clinicas; psicose quando a fenomenologia nao estiver ligada ao trauma.",
    sources: [
      ["WHO-CDDR", "https://www.who.int/publications/i/item/9789240077263/"],
      ["NICE-NG116", "https://www.nice.org.uk/guidance/ng116/chapter/recommendations"],
    ],
  },
  obsessive: {
    characterization: "Obsessoes recorrentes e/ou compulsoes realizadas para reduzir ansiedade ou prevenir consequencias temidas, geralmente percebidas como excessivas em algum grau e associadas a sofrimento, consumo de tempo ou prejuizo funcional.",
    differentials: "Preocupacao do TAG; ruminacao depressiva; transtorno dismorfico corporal; transtorno de personalidade obsessivo-compulsiva; tiques; transtornos psicoticos quando as crencas forem delirantes; comportamentos repetitivos relacionados ao autismo.",
    sources: [
      ["WHO-CDDR", "https://www.who.int/publications/i/item/9789240077263/"],
      ["NICE-CG31", "https://www.nice.org.uk/guidance/cg31/chapter/Recommendations"],
    ],
  },
  psychosis: {
    characterization: "Delirios, alucinacoes, desorganizacao do pensamento ou comportamento e/ou sintomas negativos, avaliados junto ao curso, funcionamento, humor, cognicao e risco.",
    differentials: "Transtorno bipolar ou depressao com sintomas psicoticos; uso de substancias ou medicamentos; delirium; epilepsia e outras condicoes neurologicas; doencas metabolicas, endocrinas, infecciosas ou autoimunes; transtornos relacionados a trauma.",
    sources: [
      ["WHO-CDDR", "https://www.who.int/publications/i/item/9789240077263/"],
      ["NICE-CG178", "https://www.nice.org.uk/guidance/cg178/chapter/Recommendations"],
    ],
  },
  substance: {
    characterization: "Padrao de uso associado a perda de controle, prioridade crescente da substancia, persistencia apesar de danos e, conforme o caso, tolerancia, craving ou abstinencia. Deve-se distinguir intoxicacao, abstinencia e transtorno persistente.",
    differentials: "Transtornos primarios de humor, ansiedade ou psicose; sintomas induzidos por substancias/medicamentos; dor e outras condicoes clinicas; uso terapeutico inadequado; comportamentos compulsivos sem substancia.",
    sources: [["WHO-CDDR", "https://www.who.int/publications/i/item/9789240077263/"]],
  },
  other: {
    characterization: "O item selecionado funciona como contexto clinico ou indicacao. A caracterizacao deve ser confirmada pela historia, exame, curso temporal, prejuizo funcional e criterios diagnosticos aplicaveis.",
    differentials: "Revisar causas clinicas, efeitos de medicamentos ou substancias, comorbidades psiquiatricas e outras condicoes que expliquem melhor o conjunto de sintomas.",
    sources: [["WHO-CDDR", "https://www.who.int/publications/i/item/9789240077263/"]],
  },
};

function clinicalTheoryKey(condition) {
  const value = String(condition || "").toLowerCase();
  if (!value || value.includes("nao informado")) return "";
  if (/bipolar|mania|hipomania|anticonvulsivante/.test(value)) return "bipolar";
  if (/psicose|esquizofrenia|agitacao/.test(value)) return "psychosis";
  if (/estresse pos-traumatico|tept|f43/.test(value)) return "trauma";
  if (/obsessivo|toc|compuls/.test(value)) return "obsessive";
  if (/ansiedade|panico|fobia/.test(value)) return "anxiety";
  if (/alcool|opioide|tabagismo|substancia/.test(value)) return "substance";
  if (/depress|disforico/.test(value)) return "depression";
  return "other";
}

function renderClinicalConditionTheory() {
  const target = document.getElementById("clinical-condition-theory");
  if (!target) return;
  const condition = document.getElementById("diagnosis-context")?.value || "";
  const key = clinicalTheoryKey(condition);
  if (!key) {
    target.textContent = "Selecione uma condicao para ver caracterizacao e diagnosticos diferenciais.";
    return;
  }
  const theory = CLINICAL_THEORY[key] || CLINICAL_THEORY.other;
  const sourceLinks = theory.sources.map(([label, url]) =>
    `<a href="${escapeHTML(url)}" target="_blank" rel="noopener noreferrer">${escapeHTML(label)}</a>`
  ).join(" · ");
  target.innerHTML = `
    <span class="theory-block"><b>Como se caracteriza:</b> ${escapeHTML(theory.characterization)}</span>
    <span class="theory-block"><b>Diagnosticos diferenciais:</b> ${escapeHTML(theory.differentials)}</span>
    <span class="theory-sources"><b>Fontes:</b> ${sourceLinks}</span>
  `;
}

function conditionBlueprint(condition) {
  const text = condition.toLowerCase();
  const base = {
    phenotypes: {"Depressao": 3, "Ansiedade": 2},
    symptoms: ["Humor deprimido", "Ansiedade", "Fadiga"],
    objective: "Remissao",
    secondaryObjectives: ["evitar ganho de peso", "minimizar interacoes"],
    restrictions: [],
    medicationName: "Sertralina",
  };
  if (text.includes("ansiedade") || text.includes("panico") || text.includes("estresse") || text.includes("fobia")) {
    return {...base, phenotypes: {"Ansiedade": 4, "Insonia": 2, "Depressao": 2}, symptoms: ["Ansiedade", "Tensao", "Insonia inicial", "Baixa concentracao"], objective: "reduzir ansiedade", secondaryObjectives: ["preservar libido", "evitar ganho de peso"], medicationName: "Sertralina"};
  }
  if (text.includes("toc") || text.includes("obsessivo")) {
    return {...base, phenotypes: {"Compulsividade": 4, "Ansiedade": 4, "Depressao": 2}, symptoms: ["Compulsao", "Ansiedade", "Tensao", "Baixa concentracao"], objective: "reduzir ansiedade", secondaryObjectives: ["preservar libido", "minimizar interacoes"], medicationName: "Sertralina"};
  }
  if (text.includes("fadiga") || text.includes("baixa energia")) {
    return {...base, phenotypes: {"Depressao": 4, "Baixa energia": 4, "Lentificacao": 3}, symptoms: ["Humor deprimido", "Anedonia", "Fadiga", "Baixa concentracao"], objective: "melhorar energia", secondaryObjectives: ["melhorar cognicao", "reduzir sedacao"], medicationName: "Bupropiona"};
  }
  if (text.includes("insonia") || text.includes("perda de peso")) {
    return {...base, phenotypes: {"Insonia": 4, "Ansiedade": 3, "Depressao": 2}, symptoms: ["Insonia inicial", "Insonia terminal", "Ansiedade", "Irritabilidade"], objective: "melhorar sono", secondaryObjectives: ["evitar ganho de peso", "minimizar interacoes"], restrictions: ["Risco de quedas"], medicationName: "Mirtazapina"};
  }
  if (text.includes("dor") || text.includes("fibromialgia") || text.includes("enxaqueca")) {
    return {...base, phenotypes: {"Dor": 4, "Depressao": 3, "Ansiedade": 2}, symptoms: ["Dor", "Humor deprimido", "Fadiga", "Ansiedade"], objective: "Remissao", secondaryObjectives: ["reduzir dor", "melhorar energia"], medicationName: "Duloxetina"};
  }
  if (text.includes("bipolar") || text.includes("mania") || text.includes("anticonvulsivantes")) {
    return {...base, phenotypes: {"Humor elevado": 4, "Irritabilidade": 3, "Insonia": 3}, symptoms: ["Irritabilidade", "Impulsividade", "Insonia inicial"], objective: "Estabilizacao", secondaryObjectives: ["reduzir sedacao", "minimizar interacoes"], restrictions: ["Interacoes relevantes"], medicationName: "Litio"};
  }
  if (text.includes("psicose") || text.includes("esquizofrenia") || text.includes("agitacao")) {
    return {...base, phenotypes: {"Psicose": 4, "Irritabilidade": 3, "Insonia": 2}, symptoms: ["Impulsividade", "Irritabilidade", "Baixa concentracao"], objective: "controlar psicose", secondaryObjectives: ["reduzir sedacao", "minimizar interacoes"], restrictions: ["QT prolongado"], medicationName: "Risperidona"};
  }
  if (text.includes("alcool")) {
    return {...base, phenotypes: {"Compulsividade": 4, "Ansiedade": 3, "Insonia": 2}, symptoms: ["Compulsao", "Ansiedade", "Insonia inicial"], objective: "Estabilizacao", secondaryObjectives: ["minimizar interacoes", "reduzir sedacao"], restrictions: ["Doenca hepatica", "Alcool/drogas ou medicacao sem controle"], medicationName: "Naltrexona"};
  }
  if (text.includes("opioides")) {
    return {...base, phenotypes: {"Compulsividade": 4, "Ansiedade": 3, "Irritabilidade": 2}, symptoms: ["Compulsao", "Ansiedade", "Irritabilidade"], objective: "Estabilizacao", secondaryObjectives: ["minimizar interacoes", "reduzir sedacao"], restrictions: ["Alcool/drogas ou medicacao sem controle"], medicationName: "Buprenorfina"};
  }
  if (text.includes("tabagismo")) {
    return {...base, phenotypes: {"Compulsividade": 3, "Ansiedade": 2, "Baixa energia": 2}, symptoms: ["Compulsao", "Ansiedade", "Irritabilidade"], objective: "melhorar energia", secondaryObjectives: ["evitar ganho de peso", "preservar libido"], medicationName: "Bupropiona"};
  }
  if (text.includes("alimentar") || text.includes("bulimia") || text.includes("anorexia")) {
    return {...base, phenotypes: {"Compulsividade": 3, "Ansiedade": 3, "Depressao": 2}, symptoms: ["Compulsao", "Ansiedade", "Efeitos adversos"], objective: "Estabilizacao", secondaryObjectives: ["evitar ganho de peso", "minimizar interacoes"], restrictions: ["Risco cardiovascular"], medicationName: "Fluoxetina"};
  }
  return base;
}

function medicationForState(medicationName, state, doseValue = "50", axis = "") {
  if (state === "sem_medicacao") return [];
  const stateMap = {
    resposta_parcial: {duration: "8 semanas", adherence: "Boa", response: "Resposta parcial", tolerability: "Boa", dose: doseValue},
    sem_resposta: {duration: "mais de 8 semanas", adherence: "Boa", response: "Sem resposta", tolerability: "Boa", dose: doseValue},
    efeito_adverso: {duration: "mais de 8 semanas", adherence: "Boa", response: "Boa resposta", tolerability: "Ruim / efeitos relevantes", dose: doseValue},
  };
  const item = stateMap[state] || stateMap.resposta_parcial;
  return [{
    name: medicationName,
    reason_for_use: axis,
    dose_value: item.dose,
    dose_prescribed: item.dose,
    dose_unit: "mg",
    frequency: "1x/dia",
    duration: item.duration,
    adherence: item.adherence,
    response: item.response,
    tolerability: item.tolerability,
  }];
}

function medicationDetailText(detail) {
  return [
    detail?.drug_class,
    detail?.therapeutic_targets,
    detail?.preferred_contexts,
    detail?.name,
  ].filter(Boolean).join(" ").toLowerCase();
}

function conditionForMedicationDetail(detail) {
  const text = medicationDetailText(detail);
  if (text.includes("psicose") || text.includes("antipsicotico") || text.includes("esquizofrenia")) {
    return "Esquizofrenia e transtornos psicoticos";
  }
  if (text.includes("bipolar") || text.includes("mania") || text.includes("estabilizador") || text.includes("anticonvulsivante")) {
    return "Transtorno bipolar - manutencao";
  }
  if (text.includes("dor") || text.includes("fibromialgia")) {
    return "Dor neuropatica ou sindromes dolorosas";
  }
  if (text.includes("sono") || text.includes("hipnotico") || text.includes("sedativo")) {
    return "Insonia";
  }
  if (text.includes("benzodiazepinico") && text.includes("ansiedade")) {
    return "Transtorno de ansiedade generalizada";
  }
  if (text.includes("dependencia") || text.includes("alcool")) {
    return "Transtorno por uso de alcool";
  }
  if (text.includes("opioide")) {
    return "Transtorno por uso de opioides";
  }
  if (text.includes("tdah") || text.includes("estimulante")) {
    return "Outro contexto ja conhecido / nao cadastrado";
  }
  if (text.includes("compuls")) {
    return "Transtorno obsessivo-compulsivo";
  }
  if (text.includes("ansiedade")) {
    return "Transtorno de ansiedade generalizada";
  }
  return "Transtorno depressivo maior";
}

function axisForMedicationDetail(detail, condition = "") {
  const text = `${medicationDetailText(detail)} ${condition || ""}`.toLowerCase();
  if (text.includes("dor") || text.includes("fibromialgia") || text.includes("neuropatica") || text.includes("somatico")) {
    return "dor/sintomas somaticos";
  }
  if (text.includes("tdah") || text.includes("estimulante") || text.includes("baixa energia") || text.includes("cognicao")) {
    return "energia/cognicao";
  }
  if (text.includes("toc") || text.includes("obsessivo") || text.includes("compuls")) {
    return "compulsividade/TOC";
  }
  if (text.includes("naltrexona") || text.includes("unialtrex") || text.includes("alcool") || text.includes("opioide") || text.includes("dependencia") || text.includes("craving")) {
    return "substancias/craving";
  }
  if (text.includes("trazodona") || text.includes("zolpidem") || text.includes("zopiclona") || text.includes("sono") || text.includes("hipnotico") || text.includes("sedativo")) {
    return "sono/sedacao";
  }
  if (text.includes("rivotril") || text.includes("clonazepam") || text.includes("lexotan") || text.includes("bromazepam") || text.includes("diazepam") || text.includes("alprazolam") || text.includes("lorazepam") || text.includes("benzodiazepinico")) {
    return "ansiedade/resgate";
  }
  if (text.includes("litio") || text.includes("lamotrigina") || text.includes("valproato") || text.includes("carbamazepina") || text.includes("estabilizador") || text.includes("bipolar") || text.includes("mania")) {
    return "estabilizacao do humor";
  }
  if (text.includes("antipsicotico") || text.includes("quetiapina") || text.includes("risperidona") || text.includes("olanzapina") || text.includes("aripiprazol") || text.includes("haloperidol") || text.includes("amisulprida") || text.includes("psicose") || text.includes("esquizofrenia")) {
    return "psicose/organizacao do pensamento";
  }
  if (text.includes("impulsividade") || text.includes("irritabilidade") || text.includes("agressividade")) {
    return "impulsividade/irritabilidade";
  }
  if (text.includes("fluoxetina") || text.includes("sertralina") || text.includes("escitalopram") || text.includes("citalopram") || text.includes("paroxetina") || text.includes("fluvoxamina") || text.includes("isrs") || text.includes("ssri") || text.includes("snri") || text.includes("irsn") || text.includes("depress") || text.includes("ansiedade") || text.includes("tept")) {
    return "humor/TEPT";
  }
  return "outro eixo";
}

function testMedicationDose(detail) {
  const text = medicationDetailText(detail);
  const name = normalizeMedicationKey(detail?.name || "");
  const namedDoses = {
    agomelatina: "25",
    alprazolam: "0.5",
    bromazepam: "3",
    clonazepam: "0.5",
    diazepam: "5",
    duloxetina: "30",
    escitalopram: "10",
    fluoxetina: "20",
    lorazepam: "1",
    mirtazapina: "15",
    naltrexona: "50",
    quetiapina: "25",
    sertralina: "50",
    trazodona: "50",
    zolpidem: "5",
    zopiclona: "3.75",
  };
  if (namedDoses[name]) return namedDoses[name];
  if (text.includes("antipsicotico")) return "5";
  if (text.includes("benzodiazepinico") || text.includes("hipnotico")) return "1";
  if (text.includes("estabilizador") || text.includes("anticonvulsivante")) return "300";
  if (text.includes("estimulante")) return "10";
  return "50";
}

function doseBandLines(detail) {
  const lines = String(detail?.dose_band || "")
    .split(/\n+/)
    .map((line) => line.trim())
    .filter(Boolean)
    .filter((line) => /\d/.test(line))
    .filter((line) => !/^faixa usual/i.test(line) && !/^faixa antidepressiva usual/i.test(line));
  return lines.length ? lines : [""];
}

function doseValueFromBand(detail, bandLine) {
  const match = String(bandLine || "").match(/(\d+(?:[,.]\d+)?)/);
  if (!match) return testMedicationDose(detail);
  return match[1].replace(",", ".");
}

function shortDoseBandLabel(bandLine) {
  if (!bandLine) return "faixa unica";
  const firstSentence = bandLine.split(/[.;]/)[0].trim();
  return firstSentence || "faixa cadastrada";
}

function medicationCoverageScenario(detail, index, bandLine = "") {
  const condition = conditionForMedicationDetail(detail);
  const blueprint = conditionBlueprint(condition);
  const axis = axisForMedicationDetail(detail, condition);
  const signals = clinicalSignalsForAxes(blueprint, [axis]);
  const states = ["resposta_parcial", "sem_resposta", "efeito_adverso"];
  const state = states[index % states.length];
  const bandLabel = shortDoseBandLabel(bandLine);
  return {
    patient: `Caso teste - Medicacao ${index + 1} - ${detail.name} - ${bandLabel}`,
    birthDate: "1980-01-01",
    diagnosis: condition,
    presentation: "Revisao medicamentosa",
    phenotypes: signals.phenotypes,
    symptoms: signals.symptoms,
    clinicalAxes: [axis],
    secondaryObjectives: blueprint.secondaryObjectives,
    medications: medicationForState(detail.name, state, doseValueFromBand(detail, bandLine), axis),
    restrictions: blueprint.restrictions,
  };
}

function associationCoverageScenarios(details) {
  const associationCandidates = details.filter((detail) => String(detail.association_fit || "").trim());
  if (!associationCandidates.length) return [];
  const anchor =
    details.find((detail) => /sertralina/i.test(detail.name)) ||
    details.find((detail) => /ssri|isrs|serotonergico/i.test(detail.drug_class || "")) ||
    details[0];
  return associationCandidates.map((candidate, index) => {
    const condition = conditionForMedicationDetail(candidate);
    const blueprint = conditionBlueprint(condition);
    const axes = Array.from(new Set([axisForMedicationDetail(anchor, condition), axisForMedicationDetail(candidate, condition)]));
    const signals = clinicalSignalsForAxes(blueprint, axes);
    return {
      patient: `Caso teste - Associacao ${index + 1} - ${anchor.name} + ${candidate.name}`,
      birthDate: "1980-01-01",
      diagnosis: condition,
      presentation: "Revisao medicamentosa",
      phenotypes: signals.phenotypes,
      symptoms: signals.symptoms,
      clinicalAxes: axes,
      secondaryObjectives: Array.from(new Set([...blueprint.secondaryObjectives, "minimizar interacoes"])),
      medications: [
        ...medicationForState(anchor.name, "resposta_parcial", testMedicationDose(anchor), axisForMedicationDetail(anchor, condition)),
        ...medicationForState(candidate.name, "resposta_parcial", testMedicationDose(candidate), axisForMedicationDetail(candidate, condition)),
      ],
      restrictions: blueprint.restrictions,
    };
  });
}

function firstDetailByAxis(details, axis, offset = 0) {
  const matches = details.filter((detail) => axisForMedicationDetail(detail, conditionForMedicationDetail(detail)) === axis);
  return matches.length ? matches[offset % matches.length] : null;
}

function detailByPreferredName(details, names, fallbackAxis, offset = 0) {
  const preferred = names.flatMap((name) => {
    const normalizedName = normalizeMedicationKey(name);
    return details.filter((detail) => {
      const detailName = normalizeMedicationKey(detail.name || "");
      return detailName === normalizedName || detailName.includes(normalizedName);
    });
  });
  if (preferred.length) return preferred[offset % preferred.length];
  return firstDetailByAxis(details, fallbackAxis, offset);
}

function prescriptionMedicationItem(details, axis, offset, state = "resposta_parcial") {
  const detail = detailByPreferredName(details, PREFERRED_MEDICATIONS_BY_AXIS[axis] || [], axis, offset);
  if (!detail) return null;
  return medicationForState(detail.name, state, testMedicationDose(detail), axis)[0];
}

function prescriptionItemsForAxes(details, axes, index) {
  const states = ["resposta_parcial", "sem_resposta", "efeito_adverso"];
  const prescriptionAxes = axes.length === 1 ? [axes[0], axes[0]] : axes;
  const seen = new Set();
  return prescriptionAxes
    .map((axis, axisIndex) => {
      const item = prescriptionMedicationItem(details, axis, index + axisIndex, states[(index + axisIndex) % states.length]);
      if (!item) return null;
      const key = `${item.name}|${item.dose_value}|${item.reason_for_use}`;
      if (seen.has(key)) {
        return prescriptionMedicationItem(details, axis, index + axisIndex + 3, states[(index + axisIndex + 1) % states.length]);
      }
      seen.add(key);
      return item;
    })
    .filter(Boolean);
}

function prescriptionBasedCoverageScenarios(details) {
  const prescriptionPatterns = [
    {
      label: "Humor isolado com receita combinada do mesmo eixo",
      diagnosis: "Transtorno depressivo maior",
      axes: ["humor/TEPT"],
      restrictions: [],
    },
    {
      label: "Humor e ansiedade",
      diagnosis: "Transtorno de ansiedade generalizada",
      axes: ["humor/TEPT", "ansiedade/resgate"],
      restrictions: [],
    },
    {
      label: "Depressao ansiosa com insonia",
      diagnosis: "Transtorno depressivo maior",
      axes: ["humor/TEPT", "ansiedade/resgate", "sono/sedacao"],
      restrictions: [],
    },
    {
      label: "TEPT com sono, resgate e substancias",
      diagnosis: "TEPT / F43.1",
      axes: ["humor/TEPT", "sono/sedacao", "ansiedade/resgate", "substancias/craving"],
      restrictions: ["Alcool/drogas ou medicacao sem controle"],
    },
    {
      label: "TEPT complexo com cinco eixos",
      diagnosis: "Transtorno de estresse pos-traumatico",
      axes: ["humor/TEPT", "sono/sedacao", "ansiedade/resgate", "impulsividade/irritabilidade", "substancias/craving"],
      restrictions: ["Alcool/drogas ou medicacao sem controle", "Interacoes relevantes"],
    },
    {
      label: "Toxicidade medicamentosa aguda suspeita",
      diagnosis: "Toxicidade medicamentosa aguda em investigacao",
      axes: ["humor/TEPT", "sono/sedacao"],
      medications: [
        ["Sertralina", "humor/TEPT"],
        ["Trazodona", "sono/sedacao"],
      ],
      acuteToxicitySignals: [
        "Febre ou hipertermia com agitacao",
        "Clonus hiperreflexia tremor ou mioclonia",
        "Taquicardia pressao instavel ou sudorese intensa",
      ],
      restrictions: ["Interacoes relevantes"],
    },
    {
      label: "Intoxicacao ou exposicao excessiva suspeita",
      diagnosis: "Intoxicacao medicamentosa aguda em investigacao",
      axes: ["ansiedade/resgate"],
      medications: [
        ["Clonazepam", "ansiedade/resgate"],
        ["Bromazepam", "ansiedade/resgate"],
      ],
      acuteToxicitySignals: [
        "Superdose ingestao excessiva ou mudanca abrupta recente",
        "Rebaixamento de consciencia ou dificuldade para despertar",
        "Respiracao lenta superficial ou dificil",
      ],
      restrictions: ["Interacoes relevantes", "Risco de quedas"],
    },
  ];
  const cases = [];
  for (let index = 0; index < 160; index += 1) {
    const pattern = prescriptionPatterns[index % prescriptionPatterns.length];
    const blueprint = conditionBlueprint(pattern.diagnosis);
    const signals = clinicalSignalsForAxes(blueprint, pattern.axes);
    const medications = pattern.medications
      ? pattern.medications.map(([name, axis]) => medicationItemByName(details, name, axis))
      : prescriptionItemsForAxes(details, pattern.axes, index);
    cases.push({
      patient: `Caso teste receita clinica ${index + 1} - ${pattern.axes.length} eixo - ${pattern.label}`,
      birthDate: "1980-01-01",
      diagnosis: pattern.diagnosis,
      presentation: "Revisao medicamentosa",
      phenotypes: signals.phenotypes,
      symptoms: signals.symptoms,
      clinicalAxes: pattern.axes,
      secondaryObjectives: Array.from(new Set([...blueprint.secondaryObjectives, "minimizar interacoes"])),
      medications,
      acuteToxicitySignals: pattern.acuteToxicitySignals || ["Nenhum sinal agudo identificado"],
      restrictions: pattern.restrictions,
    });
  }
  return cases;
}

function guidedFeatureScenarios(details) {
  const definitions = [
    {
      group: "P1 Idade",
      label: "Crianca",
      birthDate: "2017-01-01",
      diagnosis: "Transtorno depressivo maior",
      axes: ["humor/TEPT"],
      medications: [["Sertralina", "humor/TEPT"]],
    },
    {
      group: "P1 Idade",
      label: "Adolescente",
      birthDate: "2011-01-01",
      diagnosis: "Transtorno obsessivo-compulsivo",
      axes: ["compulsividade/TOC"],
      medications: [["Clomipramina", "compulsividade/TOC"]],
    },
    {
      group: "P1 Idade",
      label: "Adulto",
      birthDate: "1980-01-01",
      diagnosis: "Transtorno depressivo maior",
      axes: ["humor/TEPT"],
      medications: [["Agomelatina", "humor/TEPT"]],
    },
    {
      group: "P1 Idade",
      label: "Idoso",
      birthDate: "1950-01-01",
      diagnosis: "Transtorno de ansiedade generalizada",
      axes: ["ansiedade/resgate"],
      medications: [["Bromazepam", "ansiedade/resgate"]],
      restrictions: ["Risco de quedas"],
    },
    {
      group: "P1 Populacao especial",
      label: "Gestacao",
      birthDate: "1994-01-01",
      sexContext: "female",
      diagnosis: "Transtorno depressivo maior",
      axes: ["humor/TEPT"],
      medications: [["Sertralina", "humor/TEPT"]],
      restrictions: ["Gestacao"],
    },
    {
      group: "P1 Populacao especial",
      label: "Lactacao",
      birthDate: "1992-01-01",
      sexContext: "female",
      diagnosis: "Transtorno depressivo maior",
      axes: ["humor/TEPT"],
      medications: [["Sertralina", "humor/TEPT"]],
      restrictions: ["Lactacao"],
    },
    {
      group: "P1 Populacao especial",
      label: "Periodo pos-parto",
      birthDate: "1990-01-01",
      sexContext: "female",
      diagnosis: "Transtorno depressivo maior",
      axes: ["humor/TEPT"],
      medications: [["Sertralina", "humor/TEPT"]],
      restrictions: ["Periodo pos-parto"],
    },
    {
      group: "P1 Populacao especial",
      label: "Funcao renal alterada",
      birthDate: "1975-01-01",
      diagnosis: "Transtorno por uso de alcool",
      axes: ["substancias/craving"],
      medications: [["Acamprosato", "substancias/craving"]],
      restrictions: ["Doenca renal"],
    },
    {
      group: "P1 Populacao especial",
      label: "Funcao hepatica alterada",
      birthDate: "1972-01-01",
      diagnosis: "Transtorno depressivo maior",
      axes: ["humor/TEPT"],
      medications: [["Agomelatina", "humor/TEPT"]],
      restrictions: ["Doenca hepatica"],
    },
    {
      group: "P2 Contexto clinico",
      label: "Sindrome adversa",
      birthDate: "1985-01-01",
      diagnosis: "Esquizofrenia e transtornos psicoticos",
      axes: ["psicose/organizacao do pensamento"],
      medications: [["Risperidona", "psicose/organizacao do pensamento"]],
      clinicalContextIds: ["AKATHISIA"],
    },
    {
      group: "P2 Contexto clinico",
      label: "Substancias",
      birthDate: "1982-01-01",
      diagnosis: "Transtorno por uso de alcool",
      axes: ["substancias/craving"],
      medications: [["Naltrexona", "substancias/craving"]],
      clinicalContextIds: ["ALCOHOL_CONTEXT"],
    },
    {
      group: "P2 Contexto clinico",
      label: "Limite diagnostico",
      birthDate: "1948-01-01",
      diagnosis: "Outro contexto ja conhecido / nao cadastrado",
      axes: ["energia/cognicao"],
      medications: [["Rivastigmina", "energia/cognicao"]],
      clinicalContextIds: ["NEUROCOGNITIVE_CONTEXT"],
    },
    {
      group: "P2 Contexto clinico",
      label: "Limite populacional",
      birthDate: "1991-01-01",
      sexContext: "female",
      diagnosis: "Transtorno depressivo maior",
      axes: ["humor/TEPT"],
      medications: [["Sertralina", "humor/TEPT"]],
      restrictions: ["Periodo pos-parto"],
      clinicalContextIds: ["PERINATAL_CONTEXT"],
    },
    {
      group: "P3 Governanca farmacologica",
      label: "Interacao conhecida",
      birthDate: "1980-01-01",
      diagnosis: "Transtorno depressivo maior",
      axes: ["humor/TEPT", "sono/sedacao"],
      medications: [["Sertralina", "humor/TEPT"], ["Trazodona", "sono/sedacao"]],
      restrictions: ["Interacoes relevantes"],
    },
    {
      group: "P3 Governanca farmacologica",
      label: "Perfil de interacao pendente",
      birthDate: "1980-01-01",
      diagnosis: "Transtorno depressivo maior",
      axes: ["humor/TEPT"],
      medications: [["Sertralina", "humor/TEPT"], ["Medicamento externo", "humor/TEPT"]],
      restrictions: ["Interacoes relevantes"],
    },
    {
      group: "P3 Monitorizacao oficial",
      label: "Litio",
      birthDate: "1980-01-01",
      diagnosis: "Transtorno bipolar - manutencao",
      axes: ["estabilizacao do humor"],
      medications: [["Litio", "estabilizacao do humor"]],
    },
    {
      group: "P3 Monitorizacao oficial",
      label: "Antipsicotico",
      birthDate: "1980-01-01",
      diagnosis: "Esquizofrenia e transtornos psicoticos",
      axes: ["psicose/organizacao do pensamento"],
      medications: [["Risperidona", "psicose/organizacao do pensamento"]],
    },
    {
      group: "P4 Cobertura canonica",
      label: "Tema coberto",
      birthDate: "1980-01-01",
      diagnosis: "Transtorno depressivo maior",
      axes: ["humor/TEPT"],
      medications: [["Fluoxetina", "humor/TEPT"]],
    },
    {
      group: "P4 Cobertura canonica",
      label: "Contexto explicito fora da matriz",
      birthDate: "1980-01-01",
      diagnosis: "Outro contexto ja conhecido / nao cadastrado",
      axes: ["humor/TEPT"],
      medications: [["Sertralina", "humor/TEPT"]],
    },
    {
      group: "P5 Integracao",
      label: "Caso completo multi-eixos",
      birthDate: "1980-01-01",
      diagnosis: "Transtorno de estresse pos-traumatico",
      axes: ["humor/TEPT", "sono/sedacao", "ansiedade/resgate", "impulsividade/irritabilidade", "substancias/craving"],
      medications: [
        ["Fluoxetina", "humor/TEPT"],
        ["Trazodona", "sono/sedacao"],
        ["Clonazepam", "ansiedade/resgate"],
        ["Quetiapina", "impulsividade/irritabilidade"],
        ["Naltrexona", "substancias/craving"],
      ],
      restrictions: ["Interacoes relevantes"],
      clinicalContextIds: ["ALCOHOL_CONTEXT"],
    },
  ];

  return definitions.map((definition) => {
    const blueprint = conditionBlueprint(definition.diagnosis);
    const signals = clinicalSignalsForAxes(blueprint, definition.axes);
    return {
      patient: `Caso guiado - ${definition.group} - ${definition.label}`,
      demonstrationGroup: definition.group,
      demonstrationLabel: definition.label,
      birthDate: definition.birthDate,
      sexContext: definition.sexContext || "not_informed",
      diagnosis: definition.diagnosis,
      presentation: "Revisao medicamentosa",
      phenotypes: signals.phenotypes,
      symptoms: signals.symptoms,
      clinicalAxes: definition.axes,
      secondaryObjectives: Array.from(new Set([...blueprint.secondaryObjectives, "minimizar interacoes"])),
      medications: definition.medications.map(([name, axis]) => medicationItemByName(details, name, axis)),
      restrictions: definition.restrictions || [],
      clinicalContextIds: definition.clinicalContextIds || [],
    };
  });
}

function medicationItemByName(details, name, axis, state = "resposta_parcial") {
  const detail = detailByPreferredName(details, [name], axis, 0) || {name};
  return medicationForState(detail.name || name, state, testMedicationDose(detail), axis)[0];
}

function interactionCoverageScenarios(details) {
  const interactionPatterns = [
    {
      label: "Serotonergica ISRS + SARI",
      diagnosis: "Depressao ansiosa com insonia",
      axes: ["humor/TEPT", "sono/sedacao"],
      medications: [
        ["Sertralina", "humor/TEPT"],
        ["Trazodona", "sono/sedacao"],
      ],
      restrictions: ["Interacoes relevantes"],
    },
    {
      label: "ISRS + triciclico sensivel CYP2D6",
      diagnosis: "Depressao com dor e ansiedade",
      axes: ["humor/TEPT", "dor/sintomas somaticos"],
      medications: [
        ["Fluoxetina", "humor/TEPT"],
        ["Amitriptilina", "dor/sintomas somaticos"],
      ],
      restrictions: ["Interacoes relevantes"],
    },
    {
      label: "Sedacao combinada antipsicotico + benzodiazepinico",
      diagnosis: "TEPT com insonia e resgate ansioso",
      axes: ["sono/sedacao", "ansiedade/resgate"],
      medications: [
        ["Quetiapina", "sono/sedacao"],
        ["Clonazepam", "ansiedade/resgate"],
      ],
      restrictions: ["Risco de quedas", "Interacoes relevantes"],
    },
    {
      label: "Risco QT combinado",
      diagnosis: "Depressao ansiosa com risco QT",
      axes: ["humor/TEPT", "psicose/organizacao do pensamento"],
      medications: [
        ["Escitalopram", "humor/TEPT"],
        ["Quetiapina", "psicose/organizacao do pensamento"],
      ],
      restrictions: ["QT prolongado", "Interacoes relevantes"],
    },
    {
      label: "Valproato + lamotrigina",
      diagnosis: "Transtorno bipolar - manutencao",
      axes: ["estabilizacao do humor", "impulsividade/irritabilidade"],
      medications: [
        ["Divalproato", "estabilizacao do humor"],
        ["Lamotrigina", "estabilizacao do humor"],
      ],
      restrictions: ["Interacoes relevantes"],
    },
    {
      label: "Indutor CYP3A4 + substrato CYP3A4",
      diagnosis: "Transtorno bipolar com psicose",
      axes: ["estabilizacao do humor", "psicose/organizacao do pensamento"],
      medications: [
        ["Carbamazepina", "estabilizacao do humor"],
        ["Quetiapina", "psicose/organizacao do pensamento"],
      ],
      restrictions: ["Interacoes relevantes"],
    },
    {
      label: "Litio + agente serotoninergico",
      diagnosis: "Depressao bipolar em manutencao",
      axes: ["estabilizacao do humor", "humor/TEPT"],
      medications: [
        ["Litio", "estabilizacao do humor"],
        ["Sertralina", "humor/TEPT"],
      ],
      restrictions: ["Interacoes relevantes"],
    },
    {
      label: "Medicamento fora da base",
      diagnosis: "Revisao medicamentosa com farmaco externo",
      axes: ["humor/TEPT", "sono/sedacao"],
      medications: [
        ["Sertralina", "humor/TEPT"],
        ["Medicamento externo", "sono/sedacao"],
      ],
      restrictions: ["Interacoes relevantes"],
    },
  ];
  return interactionPatterns.map((pattern, index) => {
    const blueprint = conditionBlueprint(pattern.diagnosis);
    const signals = clinicalSignalsForAxes(blueprint, pattern.axes);
    return {
      patient: `Caso teste interacao ${index + 1} - ${pattern.label}`,
      birthDate: "1980-01-01",
      diagnosis: pattern.diagnosis,
      presentation: "Revisao medicamentosa",
      phenotypes: signals.phenotypes,
      symptoms: signals.symptoms,
      clinicalAxes: pattern.axes,
      secondaryObjectives: Array.from(new Set([...blueprint.secondaryObjectives, "minimizar interacoes"])),
      medications: pattern.medications.map(([name, axis]) => medicationItemByName(details, name, axis)),
      restrictions: pattern.restrictions,
    };
  });
}

function buildMedicationCoverageTestCases(details = []) {
  const validDetails = details.filter((detail) => detail?.name);
  if (!validDetails.length) {
    const fallback = conditionBlueprint("Transtorno depressivo maior");
    return [{
      patient: "Caso teste - Sem base de medicamentos carregada",
      birthDate: "1980-01-01",
      diagnosis: "Transtorno depressivo maior",
      presentation: "Revisao medicamentosa",
      phenotypes: fallback.phenotypes,
      symptoms: fallback.symptoms,
      clinicalAxes: ["humor/TEPT"],
      secondaryObjectives: fallback.secondaryObjectives,
      medications: [],
      restrictions: fallback.restrictions,
    }];
  }
  const prescriptionCases = prescriptionBasedCoverageScenarios(validDetails);
  return [
    ...prescriptionCases.slice(0, 7),
    ...guidedFeatureScenarios(validDetails),
    ...prescriptionCases.slice(7),
    ...interactionCoverageScenarios(validDetails),
    ...validDetails.flatMap((detail, medicationIndex) =>
      doseBandLines(detail).map((bandLine, bandIndex) =>
        medicationCoverageScenario(detail, medicationIndex + bandIndex, bandLine)
      )
    ),
    ...associationCoverageScenarios(validDetails),
  ];
}

RANDOM_CASES = buildMedicationCoverageTestCases();

function setText(id, value) {
  const node = document.getElementById(id);
  if (node) node.textContent = value;
}

function setHTML(id, value) {
  const node = document.getElementById(id);
  if (node) node.innerHTML = value;
}

function escapeHTML(value) {
  return String(value || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function selectedSingle(name) {
  return document.querySelector(`[data-single="${name}"] button.active`)?.textContent.trim() || "";
}

function selectedGroup(name) {
  return Array.from(document.querySelectorAll(`[data-group="${name}"] button.active`))
    .map((button) => button.textContent.trim());
}

function selectedAcuteToxicitySignals() {
  return selectedGroup("acute-toxicity-signals").filter(
    (label) => label !== "Nenhum sinal agudo identificado"
  );
}

function selectedClinicalContextIds() {
  return Array.from(document.querySelectorAll('[data-group="clinical-contexts"] button.active'))
    .map((button) => button.dataset.contextId)
    .filter(Boolean);
}

function populationState(id) {
  return document.getElementById(id)?.value || "not_assessed";
}

function populationComplete() {
  const birthDate = document.getElementById("patient-birthdate")?.value || "";
  const required = ["pregnancy-status", "lactation-status", "postpartum-status", "renal-status", "hepatic-status"];
  return Boolean(birthDate) && required.every((id) => populationState(id) !== "not_assessed");
}

function calculateAgeForDisplay() {
  const value = document.getElementById("patient-birthdate")?.value || "";
  if (!value) return null;
  const born = new Date(`${value}T00:00:00`);
  const now = new Date();
  if (Number.isNaN(born.getTime()) || born > now) return null;
  let age = now.getFullYear() - born.getFullYear();
  const beforeBirthday = now.getMonth() < born.getMonth() || (now.getMonth() === born.getMonth() && now.getDate() < born.getDate());
  if (beforeBirthday) age -= 1;
  return age >= 0 && age <= 130 ? age : null;
}

function populationSummary() {
  const age = calculateAgeForDisplay();
  if (age === null) return "Idade nao avaliada";
  const band = age < 12 ? "crianca" : age < 18 ? "adolescente" : age < 65 ? "adulto" : "idoso";
  return `${age} anos (${band})`;
}

function populationAgeBandForDisplay() {
  const age = calculateAgeForDisplay();
  if (age === null) return "UNKNOWN";
  if (age < 12) return "CHILD";
  if (age < 18) return "ADOLESCENT";
  if (age < 65) return "ADULT";
  return "OLDER_ADULT";
}

function populationReviewNoticeHTML(ageBand) {
  if (ageBand === "CHILD") {
    return [
      '<div class="population-review-notice">',
      "<b>Revisao pediatrica obrigatoria</b>",
      "<span>Crianca identificada pela data de nascimento. As fontes abaixo sao informativas por idade e nao liberam dose pediatrica automatica.</span>",
      "</div>",
    ].join("");
  }
  if (ageBand === "ADOLESCENT") {
    return [
      '<div class="population-review-notice">',
      "<b>Revisao de adolescente obrigatoria</b>",
      "<span>Adolescente identificado pela data de nascimento. As fontes abaixo sao informativas por idade e nao liberam dose pediatrica automatica.</span>",
      "</div>",
    ].join("");
  }
  return "";
}

function renderPopulationOptions() {
  const perinatalOptions = `
    <option value="not_assessed">Nao avaliado</option>
    <option value="Negado">Negado apos avaliacao</option>
    <option value="Presente">Presente</option>
    <option value="unknown">Desconhecido</option>
    <option value="Nao aplicavel">Nao aplicavel</option>
  `;
  ["pregnancy-status", "lactation-status", "postpartum-status"].forEach((id) => {
    const select = document.getElementById(id);
    if (select) select.innerHTML = perinatalOptions;
  });
  const organOptions = `
    <option value="not_assessed">Nao avaliada</option>
    <option value="Preservada">Preservada</option>
    <option value="Alterada">Alterada</option>
    <option value="unknown">Desconhecida</option>
    <option value="Nao aplicavel">Nao aplicavel</option>
  `;
  ["renal-status", "hepatic-status"].forEach((id) => {
    const select = document.getElementById(id);
    if (select) select.innerHTML = organOptions;
  });
  updatePopulationStatus();
}

function updatePopulationStatus() {
  const status = document.getElementById("population-required-status");
  const ageDisplay = document.getElementById("patient-age-display");
  const age = calculateAgeForDisplay();
  if (ageDisplay) ageDisplay.textContent = age === null ? "Nao calculada" : `${age} anos`;
  if (!status) return;
  const complete = populationComplete();
  status.classList.toggle("ready", complete);
  status.classList.toggle("pending", !complete);
  status.textContent = complete
    ? `Contexto populacional registrado: ${populationSummary()}. O motor confirmara a faixa etaria.`
    : "Nascimento ou contexto populacional ainda nao avaliado; o motor nao presumira uma populacao adulta.";
}

function combinedPerinatalSafetyState() {
  const states = [populationState("pregnancy-status"), populationState("lactation-status")];
  if (states.includes("Presente")) return "Presente";
  if (states.includes("not_assessed")) return "not_assessed";
  if (states.includes("unknown")) return "unknown";
  return "Negado";
}

function populationRestrictions() {
  const restrictions = [];
  if (populationState("pregnancy-status") === "Presente") restrictions.push("Gestacao");
  if (populationState("lactation-status") === "Presente") restrictions.push("Lactacao");
  if (populationState("postpartum-status") === "Presente") restrictions.push("Periodo pos-parto");
  if (populationState("renal-status") === "Alterada") restrictions.push("Doenca renal");
  if (populationState("hepatic-status") === "Alterada") restrictions.push("Doenca hepatica");
  const age = calculateAgeForDisplay();
  if (age !== null && age >= 65) restrictions.push("Idoso");
  return restrictions;
}

function safetyState(field) {
  return document.querySelector(`.essential-safety-state[data-safety-field="${field}"]`)?.value || "not_assessed";
}

function suicideDetailState(field) {
  return document.querySelector(`.suicide-safety-detail-state[data-safety-field="${field}"]`)?.value || "not_assessed";
}

function essentialSafetyComplete() {
  return ESSENTIAL_SAFETY_ASSESSMENTS.every(([field]) => safetyState(field) !== "not_assessed");
}

function essentialSafetySummary() {
  const unresolved = ESSENTIAL_SAFETY_ASSESSMENTS.filter(([field]) => safetyState(field) === "not_assessed");
  if (unresolved.length) return `${unresolved.length} dominio(s) nao avaliado(s)`;
  const present = ESSENTIAL_SAFETY_ASSESSMENTS.filter(([field]) => safetyState(field) === "Presente");
  return present.length ? `Risco presente em ${present.length} dominio(s)` : "Avaliacao essencial concluida";
}

function safetyStateOptions() {
  return `
    <option value="not_assessed">Nao avaliado</option>
    <option value="Negado">Negado apos avaliacao</option>
    <option value="Presente">Presente</option>
    <option value="unknown">Desconhecido</option>
    <option value="Nao aplicavel">Nao aplicavel</option>
  `;
}

function renderEssentialSafetyAssessment() {
  const target = document.getElementById("essential-safety-list");
  if (target) {
    target.innerHTML = ESSENTIAL_SAFETY_ASSESSMENTS.map(([field, label]) => `
      <label class="intensity-row">
        <span>${label}</span>
        <select class="essential-safety-state" data-safety-field="${field}">${safetyStateOptions()}</select>
      </label>
    `).join("");
  }
  const details = document.getElementById("suicide-safety-detail-list");
  if (details) {
    details.innerHTML = SUICIDE_SAFETY_DETAILS.map(([field, label]) => `
      <label class="intensity-row">
        <span>${label}</span>
        <select class="suicide-safety-detail-state" data-safety-field="${field}">${safetyStateOptions()}</select>
      </label>
    `).join("");
  }
  updateEssentialSafetyStatus();
}

function updateEssentialSafetyStatus() {
  const status = document.getElementById("essential-safety-status");
  if (!status) return;
  const complete = essentialSafetyComplete();
  status.classList.toggle("ready", complete);
  status.classList.toggle("pending", !complete);
  status.textContent = complete
    ? essentialSafetySummary()
    : "Existem dominios nao avaliados. Ausencia de marcacao nao equivale a ausencia de risco.";
}

function acuteSafetySummary() {
  const selected = selectedGroup("acute-toxicity-signals");
  if (!selected.length) return "Nao avaliada";
  if (selected.includes("Nenhum sinal agudo identificado")) return "Nenhum sinal agudo identificado";
  return `Prioridade de urgencia: ${selected.join(", ")}`;
}

function createButton(label) {
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = label;
  return button;
}

function renderOptions(container, values) {
  if (!container) return;
  container.innerHTML = "";
  values.forEach((value) => container.appendChild(createButton(value)));
  bindDirectSelectableButtons(container);
}

function renderAcuteToxidromeOptions(signals) {
  const container = document.querySelector('[data-group="acute-toxicity-signals"]');
  if (!container) return;
  container.innerHTML = signals.map((signal) => `
    <button
      type="button"
      data-signal-id="${escapeHTML(signal.signal_id)}"
      data-toxidrome-definition="${escapeHTML(signal.toxidrome_definition || "")}"
      data-antidote-summary="${escapeHTML(signal.antidote_or_specific_measure || "")}"
      data-emergency-boundary="${escapeHTML(signal.emergency_boundary || "")}"
      data-source-id="${escapeHTML(signal.source_id || "")}"
      title="${escapeHTML(signal.pattern_hint)}"
    >
      ${escapeHTML(signal.ui_label)}
    </button>
  `).join("");
  bindDirectSelectableButtons(container);
  renderSelectedToxidromeDetails();
}

function selectedToxidromeSignalButtons() {
  return Array.from(document.querySelectorAll('[data-group="acute-toxicity-signals"] button.active'))
    .filter((button) => button.dataset.signalId !== "NONE");
}

function renderSelectedToxidromeDetails() {
  const target = document.getElementById("acute-toxidrome-details");
  if (!target) return;
  const selected = selectedToxidromeSignalButtons();
  if (!selected.length) {
    target.innerHTML = "Selecione um sinal para ver definicao e medida especifica, quando houver.";
    return;
  }
  target.innerHTML = `
    <ul class="axis-action-list toxidrome-detail-list">
      ${selected.map((button) => `
        <li>
          <b>${escapeHTML(button.textContent.trim())}</b>
          <em><strong>Definicao:</strong> ${escapeHTML(button.dataset.toxidromeDefinition || "Nao definida.")}</em>
          <em><strong>Antidoto/medida:</strong> ${escapeHTML(button.dataset.antidoteSummary || "Nao definida.")}</em>
          <em><strong>Limite:</strong> ${escapeHTML(button.dataset.emergencyBoundary || "Avaliacao urgente obrigatoria.")}</em>
          <em><strong>Fonte:</strong> ${escapeHTML(button.dataset.sourceId || "PENDENTE")}</em>
        </li>
      `).join("")}
    </ul>
  `;
}

function renderClinicalContextOptions(contexts) {
  const container = document.querySelector('[data-group="clinical-contexts"]');
  if (!container) return;
  const categoryLabels = {
    adverse_syndrome: "Sindromes adversas",
    substance_context: "Substancias",
    diagnostic_boundary: "Limites diagnosticos",
    population_boundary: "Populacoes especiais",
  };
  const visible = (contexts || []).filter((item) => item.category !== "acute_risk" && item.category !== "adverse_history");
  const groups = visible.reduce((result, item) => {
    (result[item.category] ||= []).push(item);
    return result;
  }, {});
  container.innerHTML = Object.entries(groups).map(([category, items]) => `
    <section class="generated-box clinical-context-group">
      <b>${escapeHTML(categoryLabels[category] || category)}</b>
      <div class="option-grid compact">
        ${items.map((item) => `<button type="button" data-context-id="${escapeHTML(item.context_id)}" title="${escapeHTML(item.clinical_boundary)}">${escapeHTML(item.label)}</button>`).join("")}
      </div>
    </section>
  `).join("");
  bindDirectSelectableButtons(container);
}

function updateAcuteSafetyStatus() {
  const status = document.getElementById("acute-safety-status");
  if (!status) return;
  const signals = selectedAcuteToxicitySignals();
  const evaluated = selectedGroup("acute-toxicity-signals").length > 0;
  status.classList.toggle("ready", evaluated);
  status.classList.toggle("pending", !evaluated);
  status.textContent = !evaluated
    ? 'Selecione "Nenhum sinal agudo identificado" ou marque todos os sinais presentes.'
    : signals.length
      ? `Prioridade de urgencia identificada: ${signals.join(", ")}. Interromper ranking de rotina e realizar avaliacao medica urgente.`
      : "Triagem concluida: nenhum sinal agudo identificado nesta etapa.";
}

function activeCardName() {
  return document.querySelector(".flow-card.active")?.dataset.card || CARD_ORDER[0];
}

function openCard(name) {
  document.querySelectorAll(".flow-card").forEach((card) => {
    const isActive = card.dataset.card === name;
    card.classList.toggle("active", isActive);
    card.classList.toggle("complete", !isActive && isCardComplete(card.dataset.card));
  });
  document.querySelectorAll("[data-jump]").forEach((button) => {
    button.classList.toggle("active", button.dataset.jump === name);
    button.classList.toggle("complete", isCardComplete(button.dataset.jump));
  });
  document.querySelector(`.flow-card[data-card="${name}"]`)?.scrollIntoView({
    behavior: "smooth",
    block: "start",
  });
}

function nextCard(name) {
  const index = CARD_ORDER.indexOf(name);
  return CARD_ORDER[Math.min(index + 1, CARD_ORDER.length - 1)];
}

function selectedPhenotypes() {
  return Array.from(document.querySelectorAll(".phenotype-intensity"))
    .map((select) => ({
      name: select.dataset.phenotype,
      intensity: Number(select.value || 0),
      label: select.options[select.selectedIndex]?.text || "",
    }))
    .filter((item) => item.intensity > 0);
}

function phenotypeSummary() {
  const values = selectedPhenotypes();
  return values.length
    ? values.map((item) => `${item.name} ${"+".repeat(item.intensity)}`).join(", ")
    : "Nao definido";
}

function isCardComplete(name) {
  if (name === "presentation") return Boolean(selectedSingle("presentation"));
  if (name === "population") return populationComplete();
  if (name === "diagnosis") return Boolean(document.getElementById("diagnosis-context")?.value);
  if (name === "phenotype") return selectedPhenotypes().length > 0;
  if (name === "symptoms") return selectedGroup("symptoms").length > 0;
  if (name === "objective") return selectedClinicalAxes().length > 0;
  if (name === "medication") return true;
  if (name === "safety-review") return essentialSafetyComplete();
  if (name === "acute-safety") return selectedGroup("acute-toxicity-signals").length > 0;
  if (name === "profile") return Boolean(buildProfile().length);
  if (name === "restrictions") return true;
  if (name === "decision") return document.getElementById("physician-strategy")?.value !== "Selecionar";
  if (name === "monitoring") return selectedGroup("monitoring").length > 0 || selectedSingle("reassessment") !== "";
  return false;
}

function initializePresentationOptions() {
  renderOptions(document.querySelector('[data-single="presentation"]'), Object.keys(PRESENTATIONS));
}

function renderPhenotypeIntensityList() {
  const target = document.getElementById("phenotype-intensity-list");
  if (!target) return;
  target.innerHTML = COMMON_PHENOTYPES.map((name) => `
    <label class="intensity-row">
      <span>${name}</span>
      <select class="phenotype-intensity" data-phenotype="${name}">
        <option value="0">-</option>
        <option value="1">+</option>
        <option value="2">++</option>
        <option value="3">+++</option>
        <option value="4">++++</option>
      </select>
    </label>
  `).join("");
}

function handleSelectableButton(button) {
  const single = button.closest("[data-single]");
  const group = button.closest("[data-group]");
  if (group) {
    if (group.dataset.group === "acute-toxicity-signals") {
      if (button.dataset.signalId === "NONE") {
        group.querySelectorAll("button").forEach((item) => item.classList.remove("active"));
        button.classList.add("active");
      } else {
        group.querySelector('[data-signal-id="NONE"]')?.classList.remove("active");
        button.classList.toggle("active");
      }
      updateAcuteSafetyStatus();
      renderSelectedToxidromeDetails();
    } else {
      button.classList.toggle("active");
    }
    if (group.dataset.group === "symptoms") {
      resetClinicalAxesFromCurrentState();
    }
  } else if (single) {
    single.querySelectorAll("button").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    if (single.dataset.single === "presentation") {
      refreshDependentOptions();
      openCard("population");
    }
  } else {
    return false;
  }
  renderProfile();
  updateSummary();
  updatePhysicianDecisionPreview();
  return true;
}

function bindDirectSelectableButtons(root = document) {
  root.querySelectorAll("[data-single] button, [data-group] button").forEach((button) => {
    if (button.dataset.selectableBound === "true") return;
    button.dataset.selectableBound = "true";
    button.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      handleSelectableButton(button);
    });
  });
}

function suggestedClinicalAxes() {
  const values = new Set();
  const text = [
    document.getElementById("diagnosis-context")?.value || "",
    ...secondaryObjectives(),
    ...selectedGroup("symptoms"),
    ...selectedPhenotypes().map((item) => item.name),
  ].join(" ").toLowerCase();

  if (/depress|humor deprimido|anedonia|fadiga|baixa energia|tept|estresse/.test(text)) {
    values.add("humor/TEPT");
  }
  if (/insonia|sono|sedacao/.test(text)) {
    values.add("sono/sedacao");
  }
  if (/ansiedade|tensao|panico|fobia|resgate/.test(text)) {
    values.add("ansiedade/resgate");
  }
  if (/irritabilidade|impulsividade|agressividade|baixo limiar/.test(text)) {
    values.add("impulsividade/irritabilidade");
  }
  if (/toc|obsess|compulsao|compulsividade/.test(text)) {
    values.add("compulsividade/TOC");
  }
  if (/substancia|alcool|droga|craving|compulsao|vicio|opioide|tabagismo/.test(text)) {
    values.add("substancias/craving");
  }
  if (/dor|fibromialgia|somatico|enxaqueca/.test(text)) {
    values.add("dor/sintomas somaticos");
  }
  if (/baixa energia|fadiga|lentificacao|cognicao|concentracao|energia/.test(text)) {
    values.add("energia/cognicao");
  }
  if (/libido|sexual/.test(text)) {
    values.add("libido/funcao sexual");
  }
  if (/peso|metabolico|obesidade|diabetes|apetite/.test(text)) {
    values.add("peso/metabolico");
  }
  if (/bipolar|mania|hipomania|humor elevado|estabilizacao/.test(text)) {
    values.add("estabilizacao do humor");
  }
  if (/psicose|delirio|alucin|organizacao do pensamento/.test(text)) {
    values.add("psicose/organizacao do pensamento");
  }
  if (/efeitos adversos|tolerabilidade|contramedicacao/.test(text)) {
    values.add("efeito adverso/contramedicacao");
  }
  return Array.from(values);
}

function renderClinicalAxisOptions() {
  const container = document.querySelector('[data-group="clinical-axes"]');
  if (!container) return;
  const previous = new Set(selectedGroup("clinical-axes"));
  const suggested = new Set(suggestedClinicalAxes());
  renderOptions(container, CLINICAL_AXES);
  const selected = previous.size ? previous : suggested;
  container.querySelectorAll("button").forEach((button) => {
    button.classList.toggle("active", selected.has(button.textContent.trim()));
  });
}

function resetClinicalAxesFromCurrentState() {
  const container = document.querySelector('[data-group="clinical-axes"]');
  if (!container) return;
  container.querySelectorAll("button").forEach((button) => button.classList.remove("active"));
  renderClinicalAxisOptions();
}

function selectedClinicalAxes() {
  const selected = selectedGroup("clinical-axes");
  return selected.length ? selected : suggestedClinicalAxes();
}

function refreshDependentOptions() {
  renderPhenotypeIntensityList();
  renderOptions(document.querySelector('[data-group="symptoms"]'), COMMON_SYMPTOMS);
  renderClinicalAxisOptions();
}

function secondaryObjectives() {
  return selectedGroup("secondary-objectives");
}

function therapeuticObjectiveFromAxes() {
  const axes = selectedClinicalAxes();
  if (axes.includes("ansiedade/resgate")) return "reduzir ansiedade";
  if (axes.includes("sono/sedacao")) return "melhorar sono";
  if (axes.includes("dor/sintomas somaticos")) return "reduzir dor";
  if (axes.includes("energia/cognicao")) return "melhorar energia";
  if (axes.includes("compulsividade/TOC")) return "reduzir ansiedade";
  if (axes.includes("humor/TEPT")) return "Remissao";
  if (axes.includes("estabilizacao do humor")) return "Estabilizacao";
  if (axes.includes("psicose/organizacao do pensamento")) return "controlar psicose";
  if (axes.includes("substancias/craving")) return "Estabilizacao";
  if (axes.includes("impulsividade/irritabilidade")) return "Estabilizacao";
  return secondaryObjectives()[0] || "";
}

function buildProfile() {
  const presentation = selectedSingle("presentation");
  const objective = therapeuticObjectiveFromAxes();
  const symptoms = selectedGroup("symptoms");
  const phenotypes = selectedPhenotypes();
  const axes = selectedClinicalAxes();
  const data = PRESENTATIONS[presentation];
  if (!data || !objective || !symptoms.length || !phenotypes.length) return [];

  const profile = new Set(data.profile);
  axes.forEach((axis) => profile.add(`Eixo ${axis}`));
  phenotypes.forEach((item) => {
    if (item.intensity >= 3) profile.add(`${item.name}: alvo predominante`);
    if (item.intensity === 2) profile.add(`${item.name}: alvo secundario`);
  });
  if (objective.includes("ansiedade")) profile.add("forte acao ansiolitica");
  if (objective.includes("energia")) profile.add("baixa sedacao diurna");
  if (objective.includes("sono")) profile.add("boa acao sobre sono");
  if (objective.includes("psicose")) profile.add("acao antipsicotica");
  if (objective.includes("Remissao")) profile.add("potencia suficiente para resposta sustentada");
  secondaryObjectives().forEach((item) => profile.add(item));
  if (symptoms.some((item) => item.includes("Insonia"))) profile.add("boa acao sobre sono");
  if (symptoms.some((item) => item.includes("Fadiga"))) profile.add("baixa sedacao diurna");
  if (symptoms.some((item) => item.includes("Dor"))) profile.add("acao em sintomas somaticos");
  return Array.from(profile);
}

function restrictionText() {
  const restrictions = selectedGroup("restrictions");
  return restrictions.length ? restrictions.join(", ") : "Nenhuma restricao selecionada";
}

function renderProfile() {
  const profile = buildProfile();
  const target = document.getElementById("profile-output");
  if (!target) return;
  if (!profile.length) {
    target.textContent = "Aguardando apresentacao, fenotipo, sintomas e objetivo.";
    setText("summary-profile", "Aguardando selecoes.");
    return;
  }
  target.innerHTML = profile.map((item) => `<span>${item}</span>`).join("");
  setText("summary-profile", profile.join("; "));
}

function strategyOptions() {
  const presentation = selectedSingle("presentation");
  const data = PRESENTATIONS[presentation];
  const base = data ? data.strategies : ["observar", "reavaliar diagnostico"];
  const restrictions = selectedGroup("restrictions");
  const options = new Set(base);
  if (restrictions.length) options.add("refinar por seguranca");
  if (currentMedicationItems.length) options.add("revisar receita atual");
  return Array.from(options);
}

function suggestedStrategy() {
  if (!buildProfile().length) return "";
  const options = strategyOptions();
  if (currentMedicationItems.length && options.includes("revisar receita atual")) return "revisar receita atual";
  return options[0] || "observar";
}

function summaryRows() {
  const profile = buildProfile();
  const restrictions = selectedGroup("restrictions");
  const presentation = selectedSingle("presentation");
  const strategy = suggestedStrategy();
  if (!strategy || !profile.length) return [];
  return [
    {label: "Opcao compativel", text: `${presentation}: procurar opcao alinhada a ${profile.slice(0, 3).join(" + ")}.`},
    {label: "Compativel com ressalvas", text: restrictions.length ? `Refinar pela restricao: ${restrictions.slice(0, 3).join(", ")}.` : "Sem restricao marcada; revisar comorbidades antes de finalizar."},
    {label: "Receita atual", text: currentMedicationItems.length ? currentMedicationItems.map((item) => `${item.name} ${item.dose_value || "?"} ${item.dose_unit || ""}`).join("; ") : "Sem medicacao atual registrada."},
    {label: "Bloqueada", text: "Bloquear quando houver risco, interacao, contraindicacao ou informacao essencial ausente."},
  ];
}

function updateSummary() {
  const presentation = selectedSingle("presentation") || "Nao definida";
  const condition = document.getElementById("diagnosis-context")?.value || "Nao informada / em investigacao";
  const phenotype = phenotypeSummary();
  const symptoms = selectedGroup("symptoms");
  const axes = selectedClinicalAxes();
  const therapeuticObjective = therapeuticObjectiveFromAxes() || "Nao definido";
  const profile = buildProfile();
  const restrictions = selectedGroup("restrictions");
  const strategy = suggestedStrategy();

  setText("summary-presentation", presentation);
  setText("summary-population", populationSummary());
  setText("summary-condition", condition);
  setText("summary-phenotype", phenotype);
  setText("summary-symptoms", symptoms.length ? symptoms.join(", ") : "Nenhum");
  setText("summary-clinical-axes", axes.length ? axes.join(", ") : "Nao definidos");
  setText("summary-objective", `${therapeuticObjective}${secondaryObjectives().length ? ` + ${secondaryObjectives().join(", ")}` : ""}`);
  setText("summary-acute-safety", acuteSafetySummary());
  setText("summary-essential-safety", essentialSafetySummary());
  setText("summary-restrictions", restrictions.length ? restrictions.join(", ") : "Nenhuma");
  renderClinicalConditionTheory();
  const missing = missingClosureInputs();
  updatePracticalAdvice(
    practicalReadinessLabel(),
    missing.length ? `Pendencias: ${missing.join(", ")}.` : "Dados essenciais preenchidos.",
    "Gerar conselho do motor",
    "Aguardando conselho",
    objectiveSummaryHTML()
  );
  updateMedicationRequiredStatus();
  setText("decision-support-advice", strategy ? `Conselho sugerido: ${strategy}.` : "Preencha o fluxo progressivo.");
  setText(
    "decision-support-rationale",
    profile.length
      ? `Perfil construido por ${presentation}, vetor ${phenotype}, sintomas ${symptoms.join(", ")} e objetivo ${therapeuticObjective}.`
      : "Aguardando apresentacao, fenotipo, sintomas e objetivo."
  );
  setText(
    "decision-support-substitution",
    strategy ? summaryRows().map((row) => `${row.label}: ${row.text}`).join(" ") : "Aguardando conselho do motor."
  );
  setText("decision-support-disease-use", "Aguardando uso por doenca.");
  setText("decision-support-population-evidence", "Aguardando cruzamento por idade e medicamento.");
  setText("decision-support-association", restrictionText());
  setText("decision-support-pharmacology", profile.length ? profile.join("; ") : "Aguardando perfil.");
  setText("decision-support-target", symptoms.join(", "));
  setText("decision-support-evidence", "Base local: fluxo clinico estruturado + Tabela Motor quando o conselho for executado.");
  setText("decision-support-evidence-map", "Cada opcao deve ser revisada com perfil desejado, restricoes, seguranca, tolerabilidade e historico.");
  setText("level-1-strategy", strategy || "Aguardando estrategia");
  setText("level-2-target", profile.join("; "));
  setText("level-3-status", strategy ? "Pronto para revisao medica" : "Aguardando fluxo");
}

function practicalReadinessLabel() {
  if (noCurrentMedicationSelected() && buildProfile().length) {
    return "Pronto para opcao inicial";
  }
  return medicationResponseStability() ? "Pronto para conselho" : "Aguardando dados";
}

function updatePhysicianDecisionPreview() {
  const strategy = document.getElementById("physician-strategy")?.value || "Selecionar";
  const medication = document.getElementById("physician-medication")?.value.trim() || "";
  const doseNumber = document.getElementById("physician-dose-number")?.value.trim() || "";
  const doseUnit = document.getElementById("physician-dose-unit")?.value || "mg";
  const frequency = document.getElementById("physician-frequency")?.value || "1x/dia";
  const target = document.getElementById("physician-decision-preview");
  if (!target) return;
  if (strategy === "Selecionar" && !medication && !doseNumber) {
    target.textContent = "Aguardando decisao do medico.";
    return;
  }
  const med = medication || "medicamento nao informado";
  const dose = doseNumber ? `${doseNumber} ${doseUnit}, ${frequency}` : "dose nao informada";
  target.textContent = `Decisao registrada pelo medico: ${strategy} | ${med} | ${dose}.`;
}

function setFieldValue(id, value) {
  const node = document.getElementById(id);
  if (node) node.value = value || "";
}

function setSingleSelection(name, value) {
  const container = document.querySelector(`[data-single="${name}"]`);
  if (!container) return;
  container.querySelectorAll("button").forEach((button) => {
    button.classList.toggle("active", button.textContent.trim() === value);
  });
}

function setGroupSelection(name, values) {
  const selected = new Set(values || []);
  const container = document.querySelector(`[data-group="${name}"]`);
  if (!container) return;
  container.querySelectorAll("button").forEach((button) => {
    button.classList.toggle("active", selected.has(button.textContent.trim()));
  });
}

function setClinicalContextSelection(contextIds) {
  pendingScenarioClinicalContextIds = [...(contextIds || [])];
  const selected = new Set(pendingScenarioClinicalContextIds);
  document.querySelectorAll('[data-group="clinical-contexts"] button[data-context-id]').forEach((button) => {
    button.classList.toggle("active", selected.has(button.dataset.contextId));
  });
}

function setPhenotypeVector(vector) {
  document.querySelectorAll(".phenotype-intensity").forEach((select) => {
    select.value = String(vector?.[select.dataset.phenotype] || 0);
  });
}

function clearClinicalSelections() {
  document.querySelectorAll("[data-single] button.active, [data-group] button.active").forEach((button) => {
    button.classList.remove("active");
  });
  document.querySelectorAll(".phenotype-intensity").forEach((select) => {
    select.value = "0";
  });
  document.querySelectorAll(".essential-safety-state, .suicide-safety-detail-state, .population-required-state").forEach((select) => {
    select.value = "not_assessed";
  });
  [
    "patient-name",
    "patient-birthdate",
    "patient-weight-kg",
    "current-medication-status",
    "current-medication-name",
    "current-medication-dose-number",
    "current-medication-duration",
    "current-medication-adherence",
    "current-medication-response",
    "current-medication-tolerability",
    "physician-medication",
    "physician-dose-number",
  ].forEach((id) => setFieldValue(id, ""));
  setFieldValue("patient-sex-context", "not_informed");
  setFieldValue("physician-strategy", "Selecionar");
  setFieldValue("diagnosis-context", "Nao informado / em investigacao");
  setFieldValue("current-medication-dose-unit", "mg");
  setFieldValue("current-medication-frequency", "");
  setFieldValue("physician-dose-unit", "mg");
  setFieldValue("physician-frequency", "1x/dia");
  currentMedicationItems = [];
  pendingScenarioClinicalContextIds = [];
  activeScenarioSequenceLabel = "";
}

function resetDecisionSupportOutput() {
  setText("decision-support-practical-action", "Aguardando");
  setText("decision-support-practical-current", "Aguardando dados");
  setHTML("decision-support-practical-target", "Completar fluxo");
  setHTML("decision-support-practical-dose-range", "Aguardando alvo");
  setHTML("decision-support-practical-next", "Aguardando objetivo");
  setHTML("decision-support-advice", "Preencha o fluxo progressivo.");
  setHTML("decision-support-rationale", "Nenhum raciocinio gerado.");
  setHTML("clinical-condition-theory", "Selecione uma condicao para ver caracterizacao e diagnosticos diferenciais.");
  setHTML("decision-support-current-medication", "Nenhuma receita atual informada.");
  setHTML("decision-support-interactions", "Aguardando receita para cruzar interacoes.");
  setHTML("decision-support-substitution", "Aguardando estrategia escolhida.");
  setHTML("decision-support-disease-use", "Uso por quadro ainda nao calculado.");
  setHTML("decision-support-population-evidence", "Aguardando cruzamento por idade e medicamento.");
  setHTML("decision-support-association", "Nenhuma restricao selecionada.");
  setHTML("decision-support-pharmacology", "Aguardando perfil.");
  setHTML("decision-support-target", "Aguardando.");
  setHTML("decision-support-evidence", "Aguardando.");
  setHTML("decision-support-evidence-map", "Aguardando.");
  setHTML("decision-support-source-legend", sourceLegendHTML());
  setText("decision-support-status", "Campos limpos. Pronto para nova consulta.");
  setText("level-1-strategy", "sem acao");
  setText("level-2-target", "sem alvo");
  setText("level-3-status", "sem status");
}

function clearClinicalForm() {
  clearClinicalSelections();
  renderClinicalAxisOptions();
  renderMedicationList();
  renderProfile();
  updatePopulationStatus();
  updateEssentialSafetyStatus();
  updateSummary();
  updateMedicationRequiredStatus();
  updatePhysicianDecisionPreview();
  resetDecisionSupportOutput();
  updateRandomCaseButton();
  openCard("presentation");
}

function updateRandomCaseButton() {
  const button = document.getElementById("fill-random-case");
  if (!button) return;
  if (nextRandomCaseIndex >= RANDOM_CASES.length) {
    button.textContent = "Todos os casos foram testados";
    button.disabled = true;
    setText("test-case-sequence-label", "Sequencia concluida: todos os grupos e casos exaustivos foram apresentados.");
    return;
  }
  const nextScenario = RANDOM_CASES[nextRandomCaseIndex];
  const nextGroup = nextScenario.demonstrationGroup || "Cobertura exaustiva";
  const nextLabel = nextScenario.demonstrationLabel || nextScenario.patient || "Caso clinico";
  button.disabled = false;
  button.textContent = `Gerar caso teste ${nextRandomCaseIndex + 1}/${RANDOM_CASES.length}`;
  const currentPrefix = activeScenarioSequenceLabel ? `Atual: ${activeScenarioSequenceLabel}. ` : "";
  setText("test-case-sequence-label", `${currentPrefix}Proximo: ${nextRandomCaseIndex + 1}/${RANDOM_CASES.length} - ${nextGroup} - ${nextLabel}`);
}

function applyScenarioToForm(scenario) {
  clearClinicalSelections();
  setFieldValue("patient-name", scenario.patient);
  setFieldValue("patient-birthdate", scenario.birthDate);
  setFieldValue("patient-sex-context", scenario.sexContext || "not_informed");
  setFieldValue("patient-weight-kg", scenario.weightKg || "");
  setFieldValue("diagnosis-context", scenario.diagnosis);
  setSingleSelection("presentation", scenario.presentation);
  setPhenotypeVector(scenario.phenotypes);
  setGroupSelection("symptoms", scenario.symptoms);
  renderClinicalAxisOptions();
  setGroupSelection("clinical-axes", scenario.clinicalAxes || suggestedClinicalAxes());
  setGroupSelection("secondary-objectives", scenario.secondaryObjectives);
  setClinicalContextSelection(scenario.clinicalContextIds || []);
  const scenarioRestrictions = scenario.restrictions || [];
  setFieldValue("pregnancy-status", scenarioRestrictions.includes("Gestacao") ? "Presente" : "Nao aplicavel");
  setFieldValue("lactation-status", scenarioRestrictions.includes("Lactacao") ? "Presente" : "Nao aplicavel");
  setFieldValue("postpartum-status", scenarioRestrictions.includes("Periodo pos-parto") ? "Presente" : "Nao aplicavel");
  setFieldValue("renal-status", scenarioRestrictions.includes("Doenca renal") ? "Alterada" : "Preservada");
  setFieldValue("hepatic-status", scenarioRestrictions.includes("Doenca hepatica") ? "Alterada" : "Preservada");
  updatePopulationStatus();
  const scenarioSafety = {
    suicide: (scenario.symptoms || []).includes("Ideacao suicida") ? "Presente" : "Negado",
    aggression: "Negado",
    mania_or_hypomania: Number(scenario.phenotypes?.["Humor elevado"] || 0) >= 2 ? "Presente" : "Negado",
    substances: scenarioRestrictions.includes("Alcool/drogas ou medicacao sem controle") ? "Presente" : "Negado",
    delirium: "Negado",
    intoxication: "Negado",
    withdrawal: "Negado",
    allergies: scenarioRestrictions.includes("Alergia ou reacao grave anterior") ? "Presente" : "Negado",
    severe_adverse_reaction: scenarioRestrictions.includes("Alergia ou reacao grave anterior") ? "Presente" : "Negado",
    interactions: scenarioRestrictions.includes("Interacoes relevantes") ? "Presente" : "Negado",
    qt_risk: scenarioRestrictions.includes("QT prolongado") ? "Presente" : "Negado",
    pregnancy_or_lactation: scenarioRestrictions.some((item) => ["Gestacao", "Lactacao"].includes(item)) ? "Presente" : "Nao aplicavel",
    metabolic_risk: scenarioRestrictions.some((item) => ["Obesidade", "Diabetes"].includes(item)) ? "Presente" : "Negado",
    ...(scenario.safety || {}),
  };
  Object.entries(scenarioSafety).forEach(([field, value]) => {
    const select = document.querySelector(`.essential-safety-state[data-safety-field="${field}"]`);
    if (select) select.value = value;
  });
  updateEssentialSafetyStatus();
  setGroupSelection(
    "acute-toxicity-signals",
    scenario.acuteToxicitySignals || ["Nenhum sinal agudo identificado"]
  );
  updateAcuteSafetyStatus();
  setGroupSelection("restrictions", scenarioRestrictions);
  currentMedicationItems = (scenario.medications || []).map((item) => ({...item}));
  setFieldValue(
    "current-medication-status",
    currentMedicationItems.length ? "has_current_medication" : "no_current_medication"
  );
  renderMedicationList();
  renderProfile();
  updateSummary();
  updatePhysicianDecisionPreview();
}

function fillRandomCase() {
  if (nextRandomCaseIndex >= RANDOM_CASES.length) {
    setText("decision-support-status", "Todos os casos de teste desta sessao ja foram gerados. Recarregue a pagina para recomecar do zero.");
    updateRandomCaseButton();
    return;
  }
  const scenarioNumber = nextRandomCaseIndex + 1;
  const scenario = RANDOM_CASES[nextRandomCaseIndex];
  nextRandomCaseIndex += 1;
  applyScenarioToForm(scenario);
  const group = scenario.demonstrationGroup || "Cobertura exaustiva";
  const label = scenario.demonstrationLabel || scenario.patient || "Caso clinico";
  activeScenarioSequenceLabel = `${scenarioNumber}/${RANDOM_CASES.length} - ${group} - ${label}`;
  updateRandomCaseButton();
  setText("decision-support-status", `Caso teste ${scenarioNumber}/${RANDOM_CASES.length} - ${group} - ${label}. Gerando conselho local...`);
  requestDecisionSupport();
}

function fillPrescriptionExampleCase() {
  applyScenarioToForm(PRESCRIPTION_EXAMPLE_CASE);
  activeScenarioSequenceLabel = "Exemplo de receita real";
  updateRandomCaseButton();
  setText("decision-support-status", "Caso exemplo com receita combinada preenchido. Gerando conselho local...");
  requestDecisionSupport();
}

function medicationDraftFromFields() {
  const name = document.getElementById("current-medication-name")?.value.trim() || "";
  if (!name) return null;
  const doseNumber = document.getElementById("current-medication-dose-number")?.value.trim() || "";
  const doseUnit = document.getElementById("current-medication-dose-unit")?.value || "mg";
  const frequency = document.getElementById("current-medication-frequency")?.value || "";
  return {
    name,
    dose_value: doseNumber,
    dose_prescribed: doseNumber,
    dose_unit: doseUnit,
    frequency,
    duration: document.getElementById("current-medication-duration")?.value || "",
    adherence: document.getElementById("current-medication-adherence")?.value || "",
    response: document.getElementById("current-medication-response")?.value || "",
    tolerability: document.getElementById("current-medication-tolerability")?.value || "",
  };
}

function currentMedicationPayload() {
  if (noCurrentMedicationSelected()) return [];
  const draft = medicationDraftFromFields();
  const items = [...currentMedicationItems];
  if (draft && !items.some((item) => item.name === draft.name && item.dose_value === draft.dose_value)) {
    items.push(draft);
  }
  return items;
}

function noCurrentMedicationSelected() {
  return document.getElementById("current-medication-status")?.value === "no_current_medication";
}

function hasCurrentMedicationSelected() {
  return document.getElementById("current-medication-status")?.value === "has_current_medication";
}

function renderMedicationList() {
  const target = document.getElementById("current-medication-list");
  if (!target) return;
  if (noCurrentMedicationSelected()) {
    target.innerHTML = "<span>Paciente sem medicacao atual.</span>";
    return;
  }
  if (!currentMedicationItems.length) {
    target.innerHTML = "<span>Nenhuma medicacao adicionada.</span>";
    return;
  }
  target.innerHTML = currentMedicationItems.map((item, index) => `
    <article>
      <strong>${index + 1}. ${item.name}</strong>
      <span>${item.reason_for_use ? `${item.reason_for_use} | ` : ""}${item.dose_value || "?"} ${item.dose_unit || ""} ${item.frequency || ""} | ${item.duration || "tempo nao informado"} | ${item.response || "resposta nao informada"}</span>
      <button type="button" data-remove-medication="${index}">Remover</button>
    </article>
  `).join("");
}

function clearMedicationFields() {
  [
    "current-medication-name",
    "current-medication-dose-number",
    "current-medication-duration",
    "current-medication-adherence",
    "current-medication-response",
    "current-medication-tolerability",
  ].forEach((id) => {
    const node = document.getElementById(id);
    if (node) node.value = "";
  });
  hideMedicationSuggestions();
}

function hideMedicationSuggestions() {
  document.getElementById("current-medication-suggestions")?.classList.remove("open");
}

function renderMedicationSuggestions(query = "") {
  const target = document.getElementById("current-medication-suggestions");
  if (!target) return;
  const normalizedQuery = normalizeMedicationKey(query);
  const resultLimit = window.matchMedia("(max-width: 680px)").matches ? 80 : 14;
  const matches = medicationOptionNames
    .filter((name) => {
      if (!normalizedQuery) return true;
      return normalizeMedicationKey(name).includes(normalizedQuery);
    })
    .slice(0, resultLimit);

  if (!matches.length) {
    target.innerHTML = `<button type="button" disabled>Nenhum medicamento encontrado</button>`;
    target.classList.add("open");
    return;
  }

  target.innerHTML = matches
    .map((name) => `<button type="button" data-medication-suggestion="${escapeHTML(name)}">${escapeHTML(name)}</button>`)
    .join("");
  target.classList.add("open");
}

function selectMedicationSuggestion(name) {
  const field = document.getElementById("current-medication-name");
  if (!field) return;
  field.value = name;
  hideMedicationSuggestions();
  renderProfile();
  updateSummary();
  updateMedicationRequiredStatus();
}

function addCurrentMedication() {
  if (noCurrentMedicationSelected()) {
    setText("decision-support-status", "Altere o status da receita para usar medicacao atual antes de adicionar.");
    return;
  }
  const draft = medicationDraftFromFields();
  if (!draft) {
    setText("decision-support-status", "Informe o medicamento atual antes de adicionar.");
    return;
  }
  currentMedicationItems.push(draft);
  const status = document.getElementById("current-medication-status");
  if (status) status.value = "has_current_medication";
  clearMedicationFields();
  renderMedicationList();
  updateSummary();
}

function continueFromOptionalCard(cardName) {
  if (cardName === "population" && !populationComplete()) {
    setText("decision-support-status", "Informe nascimento e avalie os contextos populacionais obrigatorios antes de continuar.");
    return;
  }
  if (cardName === "phenotype" && !selectedPhenotypes().length) {
    setText("decision-support-status", "Selecione pelo menos um fenotipo antes de continuar.");
    return;
  }
  if (cardName === "symptoms" && !selectedGroup("symptoms").length) {
    setText("decision-support-status", "Selecione pelo menos um sintoma antes de continuar.");
    return;
  }
  if (cardName === "objective" && !selectedClinicalAxes().length) {
    setText("decision-support-status", "Selecione pelo menos um eixo do tratamento antes de continuar.");
    return;
  }
  if (cardName === "profile" && !buildProfile().length) {
    setText("decision-support-status", "Complete apresentacao, fenotipo, sintomas e objetivo para gerar o perfil.");
    return;
  }
  if (cardName === "safety-review" && !essentialSafetyComplete()) {
    setText("decision-support-status", "Avalie explicitamente todos os dominios de seguranca essencial antes de continuar.");
    return;
  }
  if (cardName === "acute-safety" && !selectedGroup("acute-toxicity-signals").length) {
    setText("decision-support-status", "Informe se existe algum sinal agudo antes de continuar.");
    return;
  }
  const targets = {
    population: "diagnosis",
    diagnosis: "phenotype",
    phenotype: "symptoms",
    symptoms: "objective",
    objective: "medication",
    medication: "safety-review",
    "safety-review": "acute-safety",
    "acute-safety": "profile",
    profile: "restrictions",
    restrictions: "decision",
  };
  if (cardName === "restrictions") {
    requestDecisionSupport().then(() => openCard("decision"));
    return;
  }
  openCard(targets[cardName] || nextCard(cardName));
}

function adverseEffectSafetyValue(tolerability) {
  const value = String(tolerability || "").toLowerCase();
  if (!value) return "Nao avaliado";
  if (value.includes("ruim") || value.includes("relevante")) return "Relevantes";
  return "Ausentes";
}

function buildDecisionSupportRequest() {
  const symptoms = selectedGroup("symptoms");
  const clinicalAxes = selectedClinicalAxes();
  const profile = buildProfile();
  const medications = currentMedicationPayload();
  const currentMedication = medications[0] || {};
  const comorbidities = Array.from(new Set([...selectedGroup("restrictions"), ...populationRestrictions()]));
  return {
    patient_label: document.getElementById("patient-name")?.value.trim() || "",
    birth_date: document.getElementById("patient-birthdate")?.value || "",
    pregnancy_status: populationState("pregnancy-status"),
    lactation_status: populationState("lactation-status"),
    postpartum_status: populationState("postpartum-status"),
    sex_context: document.getElementById("patient-sex-context")?.value || "not_informed",
    weight_kg: document.getElementById("patient-weight-kg")?.value || "",
    renal_status: populationState("renal-status"),
    hepatic_status: populationState("hepatic-status"),
    diagnostic_context: document.getElementById("diagnosis-context")?.value || "",
    clinical_presentation: selectedSingle("presentation"),
    current_state: selectedSingle("presentation"),
    therapeutic_objective: therapeuticObjectiveFromAxes(),
    pharmacological_profile: profile,
    clinical_axes: clinicalAxes,
    clinical_context_ids: selectedClinicalContextIds(),
    symptoms,
    observed_signs: selectedPhenotypes().map((item) => `${item.name} ${"+".repeat(item.intensity)}`),
    impairment_domains: [therapeuticObjectiveFromAxes(), ...secondaryObjectives(), ...clinicalAxes].filter(Boolean),
    impairment_severity: "Nao definido",
    stability: medicationResponseStability() || "Nao definido",
    comorbidities,
    current_medications: medications,
    safety: {
      suicide: safetyState("suicide"),
      suicide_plan: suicideDetailState("suicide_plan"),
      suicide_intent: suicideDetailState("suicide_intent"),
      suicide_means_access: suicideDetailState("suicide_means_access"),
      suicide_recent_attempt: suicideDetailState("suicide_recent_attempt"),
      aggression: safetyState("aggression"),
      mania_or_hypomania: safetyState("mania_or_hypomania"),
      substances: safetyState("substances"),
      delirium: safetyState("delirium"),
      intoxication: safetyState("intoxication"),
      withdrawal: safetyState("withdrawal"),
      allergies: safetyState("allergies"),
      severe_adverse_reaction: safetyState("severe_adverse_reaction"),
      interactions: safetyState("interactions"),
      qt_risk: safetyState("qt_risk"),
      pregnancy_or_lactation: combinedPerinatalSafetyState(),
      metabolic_risk: safetyState("metabolic_risk"),
      adherence: medications.length ? (currentMedication.adherence || "Nao avaliado") : "Nao aplicavel",
      adverse_effects: medications.length ? adverseEffectSafetyValue(currentMedication.tolerability) : "Nao aplicavel",
      acute_toxicity: !selectedGroup("acute-toxicity-signals").length
        ? "not_assessed"
        : selectedAcuteToxicitySignals().length ? "Presente" : "Negado",
      toxidrome_signals: selectedAcuteToxicitySignals(),
    },
  };
}

function cleanCandidateName(name) {
  return String(name || "")
    .replace(/\s+\(score\s+\d+\)$/i, "")
    .replace(/\s+\(pontuacao\s+\d+\)$/i, "");
}

function normalizeMedicationKey(name) {
  return String(name || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/\s+xr$/i, "")
    .replace(/\s+xl$/i, "")
    .trim();
}

function displayDrugClass(drugClass) {
  const normalized = String(drugClass || "").trim();
  const labels = {
    SSRI: "ISRS",
    SNRI: "IRSN",
    NDRI: "IRND",
    TCA: "Triciclico",
    MAOI: "IMAO",
  };
  return labels[normalized.toUpperCase()] || normalized;
}

function classForMedication(name) {
  const cleanName = cleanCandidateName(name);
  return medicationClassByName.get(cleanName) || medicationClassByName.get(normalizeMedicationKey(cleanName)) || "";
}

function formatMedicationWithClass(name, drugClass = "", axis = "") {
  const cleanName = cleanCandidateName(name);
  const classLabel = displayDrugClass(drugClass || classForMedication(cleanName));
  const axisLabel = String(axis || "").trim();
  const labelParts = [classLabel, axisLabel].filter(Boolean);
  if (!cleanName || !labelParts.length) return cleanName;
  const label = labelParts.join(" - ");
  if (cleanName.includes(`(${label})`)) return cleanName;
  return `${cleanName} (${label})`;
}

function sourceAbbreviation(citation) {
  const text = [
    citation?.source_id,
    citation?.title,
    citation?.organization,
    citation?.section,
  ].filter(Boolean).join(" ").toUpperCase();
  if (text.includes("DAILYMED") || /(^|\W)DM($|\W)/.test(text)) return "DM";
  if (text.includes("EUROPEAN MEDICINES AGENCY") || /(^|\W)EMA($|\W)/.test(text)) return "EMA";
  if (text.includes("HEALTH CANADA") || /(^|\W)HC($|\W)/.test(text)) return "HC";
  if (text.includes("ANVISA")) return "ANVISA";
  if (text.includes("NICE")) return "NICE";
  if (text.includes("PSYCHRX") || text.includes("TABELA MOTOR")) return "TM";
  return "PENDENTE";
}

function parenthesizedSource(line) {
  const text = String(line || "").trim();
  if (!text) return text;
  return text.replace(/\s*Fonte:\s*([^.]*)\.?$/i, (_, sources) => ` (${sources.trim()})`);
}

function formatCandidates(options) {
  if (!options || !options.length) return "Nenhum candidato retornado pela matriz.";
  return options.map((option, index) => {
    const evidence = option.evidence?.[0];
    const source = sourceAbbreviation(evidence);
    const cautions = option.safety_notes?.length ? ` Cautelas: ${option.safety_notes.join(", ")}.` : "";
    return `${index + 1}. ${formatMedicationWithClass(option.name, option.drug_class, option.reason_for_use || primaryClinicalAxis())} - ${option.reason}${cautions} (${source})`;
  }).join("\n");
}

function formatEvidence(items) {
  if (!items || !items.length) return "Evidencia local nao retornada.";
  return items.map((item) => {
    const citations = item.citations?.map(sourceAbbreviation).filter(Boolean);
    const sources = Array.from(new Set(citations || [])).join("/");
    return `${item.action}: ${item.rationale}${sources ? ` (${sources})` : ""}`;
  }).join("\n");
}

function formatInteractionSummary(items) {
  const lines = Array.isArray(items) ? items.filter(Boolean) : [];
  if (!lines.length) return "Sem interacao prioritaria retornada pelo motor.";
  const cards = lines.slice(0, 6).map((line) => `<li>${escapeHTML(parenthesizedSource(line))}</li>`).join("");
  return `<ul class="axis-action-list interaction-list">${cards}</ul>`;
}

function formatDiseaseUse(items) {
  if (!items || !items.length) return "Uso por doenca nao cadastrado para o medicamento avaliado.";
  const rows = items.slice(0, 4).map((item) => `<li>${escapeHTML(item)}</li>`).join("");
  return `<ul class="axis-action-list disease-use-list">${rows}</ul>`;
}

function formatPopulationEvidence(items) {
  const ageBand = populationAgeBandForDisplay();
  const notice = populationReviewNoticeHTML(ageBand);
  if (!items || !items.length) {
    return notice || "Nenhuma evidencia populacional aplicavel ao resultado atual.";
  }
  const rows = items.slice(0, 5).map((item) => `<li>${escapeHTML(item)}</li>`).join("");
  return `${notice}<ul class="axis-action-list population-evidence-list">${rows}</ul>`;
}

function populationRangeUnderAdultHTML(response) {
  const items = response?.population_evidence_summary || [];
  if (!items.length) return "";
  return [
    '<div class="population-range-under-adult">',
    '<span class="dose-profile-heading"><b>Faixa etaria do paciente</b></span>',
    formatPopulationEvidence(items),
    "</div>",
  ].join("");
}

function hasDefinedDiagnosis() {
  const value = String(document.getElementById("diagnosis-context")?.value || "").toLowerCase();
  return Boolean(value && !value.includes("nao informado") && !value.includes("investigacao"));
}

function diseaseUseLabel(response) {
  if (hasDefinedDiagnosis()) return "Uso por doenca";
  const phenotype = (response.phenotype_summary || []).join(" ").toLowerCase();
  return phenotype.includes("unspecified") ? "Uso por quadro" : "Uso por quadro clinico";
}

function phenotypeDecisionBase(response) {
  const phenotype = response.phenotype_summary?.[0]?.replace("Fenotipo principal: ", "") || "";
  return hasDefinedDiagnosis()
    ? `Base: diagnostico informado; ${phenotype || "fenotipo nao calculado"}.`
    : `Base: quadro clinico/fenotipo; diagnostico ainda nao confirmado. ${phenotype || ""}`;
}

function eligibilityLine(response) {
  const eligible = response.eligibility_summary || [];
  const excluded = response.excluded_medications || [];
  if (eligible.length) return eligible[0];
  if (excluded.length) return `Sem candidato principal apos filtro. ${excluded[0]}`;
  return "Elegibilidade ainda nao calculada.";
}

function actionLabel(action) {
  const labels = {
    maintain: "Manter",
    optimize_current: "Revisar tratamento atual",
    increase_dose: "Otimizar dose",
    decrease_dose: "Reduzir dose",
    substitute: "Substituir medicacao",
    associate: "Potencializar",
    taper_or_withdraw: "Suspender/retirar",
    select_candidate: "Iniciar opcao",
    investigate_before_change: "Prioridade de seguranca",
    insufficient_information: "Aguardar dados",
  };
  return labels[action] || "Revisar";
}

function practicalActionLabel(response) {
  const action = response?.recommended_action || "";
  if (action !== "insufficient_information") return actionLabel(action);
  const missing = missingClosureInputs();
  if (!missing.length) return "Aguardar dados: revisar campos obrigatorios.";
  return `Aguardar dados: faltam ${missing.join(", ")}.`;
}

function safetyFriendlyText(value) {
  return String(value || "")
    .replace(
      /Conselho suspenso:\s*resolver seguranca antes de estrategia\.?/gi,
      "Prioridade de seguranca identificada. A revisao farmacologica continua em paralelo.",
    )
    .replace(
      /A tabela local bloqueou estrategia porque/gi,
      "A tabela local identificou prioridade de seguranca porque",
    )
    .replace(/Fluxo obrigatorio:/gi, "Sequencia recomendada:")
    .replace(
      /Nao aplicavel enquanto seguranca estiver bloqueada\.?/gi,
      "Revisar em conjunto com as prioridades de seguranca.",
    )
    .replace(/\b(?:bloqueado|bloqueada|suspenso|suspensa|pausado|pausada)\b/gi, "em revisao de seguranca");
}

function confidenceLabel(value, safetyPriority = false) {
  const normalized = String(value || "").toLowerCase();
  if (safetyPriority && normalized.includes("high")) return "alta para prioridade de seguranca";
  if (normalized.includes("high")) return "alta";
  if (normalized.includes("moderate")) return "moderada";
  if (normalized.includes("low")) return "baixa";
  return value || "nao calculada";
}

function currentMedicationAssessmentFallback(response) {
  const medications = currentMedicationPayload();
  if (!medications.length) return "Sem medicacao atual registrada.";
  return medications.map((item) => {
    const axis = item.reason_for_use || primaryClinicalAxis();
    const suggested = suggestedMedicationForAxis(axis);
    const row = bestMotor2RowForMedication(item.name, axis);
    const comparison = doseComparisonLabel(item, row);
    const action = practicalActionForMedication(item, row, response, suggested);
    return `${medicationSummaryItem(item)}. Quadro: ${comparisonConditionLabel(row, axis)}. ${comparison} ${action}`;
  }).join("\n");
}

function axisCandidatesFallback() {
  const axes = Array.from(new Set(selectedClinicalAxes()));
  if (!axes.length) return "Defina os eixos do tratamento para calcular candidatos.";
  return axes.map((axis, index) => {
    const candidate = suggestedMedicationForAxis(axis);
    return `${index + 1}. ${axisDisplayLabel(axis)}: ${candidate.label}`;
  }).join("\n");
}

function diseaseUseFallback(response) {
  const rows = therapeuticRangeRows(response);
  if (!rows.length) return "Nenhum medicamento disponivel para cruzar com o quadro informado.";
  return rows.map((row) => {
    const condition = row.condition || axisDisplayLabel(row.primaryContext);
    return `${row.medication}: ${condition}`;
  }).join(" | ");
}

function currentMedicationSummary() {
  if (noCurrentMedicationSelected()) return "Sem medicacao atual";
  const medications = currentMedicationPayload();
  if (!medications.length) return "Sem receita registrada";
  return medications.map((item) => medicationSummaryItem(item)).join("; ");
}

function currentMedicationsForAxis(axis) {
  return currentMedicationPayload().filter((item) => item.reason_for_use === axis);
}

function suggestedMedicationForAxis(axis, offset = 0) {
  const detail = detailByPreferredName(
    currentMedicationDetails,
    PREFERRED_MEDICATIONS_BY_AXIS[axis] || [],
    axis,
    offset
  );
  if (!detail) {
    return {
      name: "",
      label: `pendente pesquisar para ${axis}`,
    };
  }
  return {
    name: detail.name,
    label: formatMedicationWithClass(detail.name, detail.drug_class, axis),
  };
}

function detailForMedicationName(name) {
  const normalized = normalizeMedicationKey(name);
  if (!normalized) return null;
  return currentMedicationDetails.find((detail) => normalizeMedicationKey(detail.name || "") === normalized)
    || currentMedicationDetails.find((detail) => normalizeMedicationKey(detail.name || "").includes(normalized))
    || null;
}

function doseBandForMedication(name) {
  const detail = detailForMedicationName(name);
  return String(detail?.dose_band || "").trim() || "faixa nao cadastrada";
}

const AXIS_CONDITION_HINTS = {
  "humor/TEPT": ["tept", "transtorno de estresse", "depressao", "humor"],
  "sono/sedacao": ["insonia", "sono", "sedacao"],
  "ansiedade/resgate": ["ansiedade", "tag", "panico", "resgate"],
  "impulsividade/irritabilidade": ["mania", "hipomania", "impulsividade", "irritabilidade", "agitacao"],
  "substancias/craving": ["alcool", "substancia", "craving", "vicio", "dependencia"],
  "estabilizacao do humor": ["bipolar", "mania", "hipomania", "manutencao"],
  "psicose/organizacao do pensamento": ["psicose", "psicotico", "esquizofrenia", "agitacao"],
  "compulsividade/TOC": ["toc", "compulsao"],
  "dor/sintomas somaticos": ["dor", "fibromialgia", "somatico", "enxaqueca"],
  "energia/cognicao": ["energia", "fadiga", "cognicao", "depressao"],
  "libido/funcao sexual": ["libido", "sexual"],
  "peso/metabolico": ["peso", "metabolico"],
};

const MOTOR2_UI_FALLBACK_RANGES = {
  clonazepam: [
    {
      condition: "Transtorno do panico",
      condition_key: "panico",
      condition_range: "0,5-1 mg/dia (DM)",
      condition_range_min: "0.5",
      condition_range_max: "1",
      range_source: "DM - panico/ansiedade-resgate",
      dose_effect_band: "0,25 mg 2x/dia: inicio em transtorno do panico; 1 mg/dia: alvo usual no panico; 2-4 mg/dia: maior exposicao e mais eventos adversos. (DM)",
    },
  ],
  bromazepam: [
    {
      condition: "Ansiedade aguda",
      condition_key: "TAG",
      condition_range: "6-18 mg/dia (HC)",
      condition_range_min: "6",
      condition_range_max: "18",
      range_source: "HC - ansiedade/resgate",
      dose_effect_band: "6-18 mg/dia em doses divididas: faixa adulta usual; doses maiores aumentam sedacao, prejuizo psicomotor e dependencia. (HC/ST-E/GG)",
    },
  ],
  trazodona: [
    {
      condition: "Insonia",
      condition_key: "insonia",
      condition_range: "25-100 mg a noite (DM/ST-E/GG)",
      condition_range_min: "25",
      condition_range_max: "100",
      range_source: "DM/ST-E/GG - dose-efeito/sono",
      dose_effect_band: "25-100 mg a noite: predominam antagonismo H1, alfa-1 e 5-HT2A, com sedacao e auxilio do sono. (DM/ST-E/GG)",
    },
  ],
};

function numericDose(value) {
  const match = String(value || "").replace(",", ".").match(/\d+(?:\.\d+)?/);
  return match ? Number.parseFloat(match[0]) : null;
}

function registeredMotorRange(row) {
  const range = String(row?.condition_range || "").trim();
  return range && !/nao cadastrad|pendente/i.test(range);
}

function registeredDoseEffectRange(row) {
  const band = String(row?.dose_effect_band || "").trim();
  const low = String(row?.dose_effect_min || "").trim();
  const high = String(row?.dose_effect_max || "").trim();
  if (!band || /nao cadastrad|pendente[_\s-]*pesquisar/i.test(band)) return false;
  return Boolean(low && high);
}

function registeredDoseEffectText(row) {
  const band = String(row?.dose_effect_band || "").trim();
  return Boolean(band && !/nao cadastrad|pendente[_\s-]*pesquisar/i.test(band));
}

function sourceAbbreviationsForRow(row) {
  const text = [
    row?.range_source || "",
    row?.dose_effect_source || "",
    row?.dose_effect_band || "",
  ].join(" ");
  const known = ["DM", "HC", "EMA", "ANVISA", "ST-E", "ST-PG", "GG", "CANMAT", "APA", "NICE", "MAUDSLEY", "TM"];
  const found = known.filter((abbr) => new RegExp(`\\b${abbr}\\b`, "i").test(text));
  return found.length ? Array.from(new Set(found)).join("/") : "fonte cadastrada";
}

function motorComparableRange(row) {
  if (registeredMotorRange(row)) {
    return {
      kind: "condition",
      range: row.condition_range,
      min: row.condition_range_min,
      max: row.condition_range_max,
      label: `Faixa por quadro: ${row.condition_range}`,
    };
  }
  if (registeredDoseEffectRange(row)) {
    const low = String(row.dose_effect_min).replace(".", ",");
    const high = String(row.dose_effect_max).replace(".", ",");
    const same = low === high;
    const range = same ? `${low} mg/dia` : `${low}-${high} mg/dia`;
    return {
      kind: "dose_effect",
      range,
      min: row.dose_effect_min,
      max: row.dose_effect_max,
      label: `Faixa por dose-efeito: ${range} (${sourceAbbreviationsForRow(row)})`,
    };
  }
  if (registeredDoseEffectText(row)) {
    return {
      kind: "dose_effect_text",
      range: row.dose_effect_band,
      min: "",
      max: "",
      label: `Faixa contextual por dose-efeito: ${row.dose_effect_band}`,
    };
  }
  return null;
}

function motor2RowsForMedication(name) {
  const detail = detailForMedicationName(name);
  const apiRows = Array.isArray(detail?.motor2_ranges) ? detail.motor2_ranges : [];
  if (apiRows.length) return apiRows;
  return MOTOR2_UI_FALLBACK_RANGES[normalizeMedicationKey(name)] || [];
}

function motor2ComparisonContext(axis) {
  return [
    document.getElementById("diagnosis-context")?.value || "",
    axis,
    ...selectedGroup("symptoms"),
    ...selectedPhenotypes().map((item) => item.name),
  ].join(" ").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
}

function motor2RowScore(row, axis) {
  const context = motor2ComparisonContext(axis);
  const rowText = `${row.condition || ""} ${row.condition_key || ""}`
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
  let score = registeredMotorRange(row) ? 10 : -5;
  rowText.split(/\s+/).forEach((token) => {
    if (token.length > 3 && context.includes(token)) score += 1;
  });
  (AXIS_CONDITION_HINTS[axis] || []).forEach((hint) => {
    if (rowText.includes(hint)) score += 2;
  });
  return score;
}

function bestMotor2RowForMedication(name, axis) {
  const rows = motor2RowsForMedication(name);
  if (!rows.length) return null;
  return rows
    .slice()
    .sort((left, right) => motor2RowScore(right, axis) - motor2RowScore(left, axis))[0];
}

function doseStatusAgainstRange(item, row) {
  const comparable = motorComparableRange(row);
  if (!row || !comparable) return "range_missing";
  if (comparable.kind === "dose_effect_text") return "qualitative_range";
  const dose = numericDose(item.dose_value);
  const low = numericDose(comparable.min);
  const high = numericDose(comparable.max);
  if (dose === null || low === null || high === null) return "dose_indeterminate";
  if (dose < low) return "below";
  if (dose > high) return "above";
  return "within";
}

function currentDoseLabel(item) {
  const dose = [item.dose_value, item.dose_unit].filter(Boolean).join(" ");
  return dose || "dose atual nao informada";
}

function motorRangeLabel(row) {
  const comparable = motorComparableRange(row);
  if (!comparable) return "faixa nao cadastrada";
  return comparable.label;
}

function axisDisplayLabel(axis) {
  const labels = {
    "humor/TEPT": "Humor/TEPT",
    "sono/sedacao": "Sono/sedacao",
    "ansiedade/resgate": "Ansiedade/resgate",
    "impulsividade/irritabilidade": "Impulsividade/irritabilidade",
    "compulsividade/TOC": "Compulsividade/TOC",
    "substancias/craving": "Substancias/craving",
    "dor/sintomas somaticos": "Dor/sintomas somaticos",
    "energia/cognicao": "Energia/cognicao",
    "libido/funcao sexual": "Libido/funcao sexual",
    "peso/metabolico": "Peso/metabolico",
    "estabilizacao do humor": "Estabilizacao do humor",
    "psicose/organizacao do pensamento": "Psicose/organizacao do pensamento",
    "efeito adverso/contramedicacao": "Efeito adverso/contramedicacao",
  };
  return labels[axis] || axis || "Quadro nao informado";
}

function comparisonConditionLabel(row, axis) {
  const axisLabel = axisDisplayLabel(axis);
  if (!row?.condition) return axisLabel;
  const condition = String(row.condition);
  const context = motor2ComparisonContext(axis);
  if (axis === "ansiedade/resgate" && /panico/i.test(condition) && !context.includes("panico")) {
    return `${axisLabel} (referencia cadastrada: ${condition})`;
  }
  return condition;
}

function doseComparisonLabel(item, row) {
  const status = doseStatusAgainstRange(item, row);
  const current = currentDoseLabel(item);
  const comparable = motorComparableRange(row);
  const range = comparable?.label || "faixa nao cadastrada";
  if (status === "range_missing") {
    return `Dose atual ${current}. Faixa cadastrada: nao encontrada para este medicamento/eixo.`;
  }
  if (status === "dose_indeterminate") {
    return `Dose atual ${current}. ${range}. Dose incompleta para comparar.`;
  }
  if (status === "qualitative_range") {
    return `Dose atual ${current}. ${range}. Resultado: faixa qualitativa/contextual; comparar por via, indicacao, seguranca e resposta, nao por corte numerico simples.`;
  }
  if (status === "below") {
    return `Dose atual ${current}. ${range}. Resultado: abaixo da faixa.`;
  }
  if (status === "above") {
    return `Dose atual ${current}. ${range}. Resultado: acima da faixa.`;
  }
  return `Dose atual ${current}. ${range}. Resultado: dentro da faixa.`;
}

function doseComparisonResultLabel(item, row) {
  const status = doseStatusAgainstRange(item, row);
  if (status === "range_missing") return "faixa nao cadastrada";
  if (status === "dose_indeterminate") return "dose incompleta";
  if (status === "qualitative_range") return "faixa contextual";
  if (status === "below") return "abaixo da faixa";
  if (status === "above") return "acima da faixa";
  return "dentro da faixa";
}

function residualTargetSummary(response) {
  const explicit = (response?.clinical_rationale || [])
    .map((item) => String(item).trim())
    .find((item) => item.startsWith("Alvo residual"));
  return explicit || "Alvo residual nao definido: registrar quais sintomas ou prejuizos persistem antes de discutir troca ou associacao.";
}

function practicalActionForMedication(item, row, response, suggested) {
  const status = doseStatusAgainstRange(item, row);
  const responseText = String(item.response || "").toLowerCase();
  const comparable = motorComparableRange(row);
  const range = comparable?.range || "faixa nao cadastrada";
  const sameAsRobot = normalizeMedicationKey(item.name) === normalizeMedicationKey(suggested.name);
  if (status === "range_missing") {
    return "Conduta sugerida: nao definir aumento, reducao ou troca pela faixa; falta cadastrar faixa ou dose-efeito revisavel para este eixo.";
  }
  if (status === "dose_indeterminate") {
    return "Conduta sugerida: completar a dose atual antes de decidir manter, aumentar, reduzir ou trocar.";
  }
  if (status === "qualitative_range") {
    return "Conduta sugerida: nao decidir aumento/reducao por corte numerico; usar a faixa contextual, resposta, seguranca, via/formulacao e objetivo clinico.";
  }
  if (status === "below") {
    const basis = comparable?.kind === "dose_effect" ? "faixa por dose-efeito" : "faixa por quadro";
    return `Conduta sugerida: avaliar otimizacao gradual ate a ${basis} ${range}, se seguranca, adesao e tolerabilidade permitirem.`;
  }
  if (status === "above") {
    const basis = comparable?.kind === "dose_effect" ? "faixa por dose-efeito" : "faixa por quadro";
    return `Conduta sugerida: revisar reducao ou seguranca, pois a dose esta acima da ${basis} ${range}.`;
  }
  if (responseText.includes("boa resposta")) {
    return "Conduta sugerida: manter e monitorar.";
  }
  if (responseText.includes("sem resposta")) {
    return "Conduta sugerida: avaliar substituicao ou revisao diagnostica, pois ja esta em faixa e sem resposta.";
  }
  if (responseText.includes("parcial")) {
    return sameAsRobot
      ? `Conduta sugerida: manter a faixa atual enquanto se confirma a resposta. ${residualTargetSummary(response)} Troca ou associacao depende dessa confirmacao, do prejuizo funcional, tempo, adesao e tolerabilidade.`
      : `Conduta sugerida: comparar com o candidato do robo (${suggested.label}) somente depois de confirmar quais sintomas ou prejuizos permanecem.`;
  }
  return "Conduta sugerida: definir a resposta clinica para decidir manter, associar ou trocar.";
}

function medicationComparisonLine(item, axis, response, suggested) {
  const row = bestMotor2RowForMedication(item.name, axis);
  const condition = row?.condition ? `Quadro: ${row.condition}. ` : "";
  return {
    medication: medicationSummaryItem(item),
    candidate: suggested.label,
    condition: comparisonConditionLabel(row, axis),
    currentDose: currentDoseLabel(item),
    targetRange: motorRangeLabel(row),
    result: doseComparisonResultLabel(item, row),
    comparison: `${condition}${doseComparisonLabel(item, row)}`,
    action: practicalActionForMedication(item, row, response, suggested),
  };
}

function shortAxisActionSummary(medicationActions, suggested) {
  if (!medicationActions.length) {
    return `avaliar inclusao de ${suggested.label}.`;
  }
  return medicationActions
    .map((item) => {
      const medication = item.medication.split(" ").slice(0, 2).join(" ");
      return `${medication}: ${item.action.replace(/^(Acao|Conduta sugerida):\s*/i, "")}`;
    })
    .join(" ");
}

function effectiveRobotCandidateForAxis(axis, currentForAxis, suggested) {
  const suggestedKey = normalizeMedicationKey(suggested.name);
  if (suggestedKey) {
    const sameMedication = currentForAxis.find((item) => normalizeMedicationKey(item.name) === suggestedKey);
    if (sameMedication) {
      return {
        name: sameMedication.name,
        label: formatMedicationWithClass(sameMedication.name, "", axis),
        source: "current_matching_robot",
      };
    }
  }
  if (currentForAxis.length) {
    const primaryCurrent = currentForAxis[0];
    return {
      name: primaryCurrent.name,
      label: formatMedicationWithClass(primaryCurrent.name, "", axis),
      source: "current_axis_coverage",
    };
  }
  return suggested;
}

function therapeuticRangeRows(response) {
  const rows = [];
  const rowByMedication = new Map();
  const axes = Array.from(new Set(selectedClinicalAxes()));

  const addContext = (row, context) => {
    const contexts = String(row.context || "")
      .split(" / ")
      .map((item) => item.trim())
      .filter(Boolean);
    if (context && !contexts.includes(context)) contexts.push(context);
    row.context = contexts.join(" / ");
  };

  axes.forEach((axis) => {
    const suggested = suggestedMedicationForAxis(axis);
    const key = normalizeMedicationKey(suggested.name);
    if (!key) return;
    const existing = rowByMedication.get(key);
    if (existing) {
      addContext(existing, axis);
      return;
    }
    const row = {
      name: suggested.name,
      primaryContext: axis,
      context: axis,
      medication: suggested.label,
      status: "sugerido pelo robo",
    };
    rowByMedication.set(key, row);
    rows.push(row);
  });

  currentMedicationPayload().forEach((item) => {
    const key = normalizeMedicationKey(item.name);
    if (!key) return;
    const existing = rowByMedication.get(key);
    if (existing) {
      existing.medication = medicationSummaryItem(item);
      addContext(existing, item.reason_for_use);
      existing.status = "sugerido pelo robo / na receita atual";
      return;
    }
    const row = {
      name: item.name,
      primaryContext: item.reason_for_use || "receita atual",
      context: item.reason_for_use || "receita atual",
      medication: medicationSummaryItem(item),
      status: "na receita atual",
    };
    rowByMedication.set(key, row);
    rows.push(row);
  });

  return rows.map((row) => {
    const motorRow = bestMotor2RowForMedication(row.name, row.primaryContext);
    const targetRange = motorRangeLabel(motorRow).replace(
      /^Faixa (?:por quadro|por dose-efeito|contextual por dose-efeito):\s*/i,
      "",
    );
    return {
      ...row,
      condition: comparisonConditionLabel(motorRow, row.primaryContext),
      targetRange,
      doseEffect: doseBandForMedication(row.name)
        || String(motorRow?.dose_effect_band || "").trim(),
    };
  });
}

function axisMedicationComparison(axis, response) {
  const suggested = suggestedMedicationForAxis(axis);
  const currentForAxis = currentMedicationsForAxis(axis);
  const suggestedKey = normalizeMedicationKey(suggested.name);
  const currentLabels = currentForAxis.map((item) => medicationSummaryItem(item)).join("; ");
  const sameMedication = suggestedKey
    ? currentForAxis.find((item) => normalizeMedicationKey(item.name) === suggestedKey)
    : null;

  if (!currentForAxis.length) {
    return `${axis}: receita atual nao cobre; robo sugere ${suggested.label}.`;
  }
  if (sameMedication) {
    return `${axis}: ja coberto por ${medicationSummaryItem(sameMedication)}; comparar dose atual, tempo, resposta e tolerabilidade com a faixa do motor.`;
  }
  return `${axis}: receita atual usa ${currentLabels}; robo sugere ${suggested.label}. Comparar substituicao, associacao ou manutencao conforme resposta e tolerabilidade.`;
}

function axisMedicationComparisonData(axis, response) {
  const suggested = suggestedMedicationForAxis(axis);
  const currentForAxis = currentMedicationsForAxis(axis);
  const suggestedKey = normalizeMedicationKey(suggested.name);
  const sameMedication = suggestedKey
    ? currentForAxis.find((item) => normalizeMedicationKey(item.name) === suggestedKey)
    : null;
  const currentAxisLabel = currentForAxis.map((item) => medicationSummaryItem(item)).join("; ");
  const effectiveCandidate = effectiveRobotCandidateForAxis(axis, currentForAxis, suggested);
  const medicationActions = currentForAxis.map((item) => medicationComparisonLine(item, axis, response, effectiveCandidate));
  const actionSummary = shortAxisActionSummary(medicationActions, effectiveCandidate);
  if (!currentForAxis.length) {
    return {
      axis,
      candidate: suggested.label,
      status: "Nao coberto",
      note: "Receita atual nao cobre este eixo.",
      medications: [],
    };
  }
  if (sameMedication) {
    return {
      axis,
      candidate: currentAxisLabel,
      status: "Ja coberto",
      note: `Candidato do robo: ${effectiveCandidate.label}. Conduta: ${actionSummary}`,
      medications: medicationActions,
    };
  }
  return {
    axis,
    candidate: effectiveCandidate.label,
    status: "Comparar troca/associacao",
    note: `Receita atual: ${currentForAxis.map((item) => medicationSummaryItem(item)).join("; ")}. Conduta: ${actionSummary}`,
    medications: medicationActions,
  };
}

function pauseReasonText(response) {
  const blockers = actionBlockers(response);
  return blockers.length ? blockers.join("; ") : "seguranca/fechamento pendente";
}

function pauseActionText(response) {
  if (hasAcuteToxicityBlocker(response)) {
    return "Interromper o ranking farmacologico de rotina e realizar avaliacao medica urgente. Os sinais registrados sugerem possivel toxicidade/intoxicacao aguda, sem estabelecer uma toxindrome especifica.";
  }
  if (hasSuicideBlocker(response)) {
    const substanceText = hasSubstanceBlocker(response)
      ? " Tambem revisar substancias ou medicacao sem controle antes de comparar receita."
      : "";
    return `Resolver seguranca imediata: risco suicida presente. Definir intervencao de crise e tratamento da condicao de base pelo medico.${substanceText}`;
  }
  const reason = pauseReasonText(response);
  return `Resolver antes da comparacao: ${reason}.`;
}

function robotRegimenStrategy(response) {
  const axes = Array.from(new Set(selectedClinicalAxes()));
  if (!axes.length) return "Defina os eixos do tratamento antes de gerar a receita sugerida pelo robo.";
  const lines = axes.map((axis) => axisMedicationComparison(axis, response));
  return `Receita sugerida pelo robo por eixo. ${lines.join(" ")}`;
}

function robotRegimenStrategyHTML(response, intro = "") {
  const axes = Array.from(new Set(selectedClinicalAxes()));
  if (!axes.length) {
    return `<div class="strategy-readout"><p>Defina os eixos do tratamento antes de gerar a receita sugerida pelo robo.</p></div>`;
  }
  const items = axes
    .map((axis) => axisMedicationComparisonData(axis, response))
    .map((item) => `
      <li>
        <span>${escapeHTML(item.axis)}</span>
        ${item.medications?.length ? `
          <ul class="axis-action-list">
            ${item.medications.map((medication) => `
              <li>
                <b>Medicamento atual: ${escapeHTML(medication.medication)}</b>
                <em>Candidato do robo: ${escapeHTML(medication.candidate)}</em>
                <em>Quadro: ${escapeHTML(medication.condition)}</em>
                <em>Faixa usada na comparacao: ${escapeHTML(medication.targetRange)}</em>
                <em>Leitura da dose: ${escapeHTML(medication.currentDose)} - ${escapeHTML(medication.result)}</em>
                <em>${escapeHTML(medication.action)}</em>
              </li>
            `).join("")}
          </ul>
        ` : `
          <ul class="axis-action-list">
            <li>
              <b>Candidato do robo: ${escapeHTML(item.candidate)}</b>
              <em>${escapeHTML(item.status)}</em>
              <em>${escapeHTML(item.note)}</em>
            </li>
          </ul>
        `}
      </li>
    `)
    .join("");
  return `
    <div class="strategy-readout">
      ${intro ? `<p class="strategy-alert">${escapeHTML(intro)}</p>` : ""}
      <p class="strategy-heading">Receita sugerida pelo robo por eixo</p>
      <ul class="axis-medication-list">${items}</ul>
    </div>
  `;
}

function strategyActionHTML(text) {
  return `<p class="strategy-action">${escapeHTML(text)}</p>`;
}

function conciseMedicationReason(value) {
  const reason = String(value || "Nao informado.")
    .replace(/^(Favorecida para discussao medica|Favorecida|Condicionalmente favorecida|Condicional|Nao favorecida automaticamente|Nao favorecida de imediato|Nao favorecida antes da revisao|Nao favorecida como estrategia isolada|Nao favorecida|Nao avaliavel agora|Nao avaliavel):\s*/i, "")
    .trim();
  const clauses = reason.split(/;\s*/).filter(Boolean);
  return clauses.slice(0, 2).join("; ") || "Revisar os dados clinicos disponiveis.";
}

function replacementCandidateForMedication(item, response) {
  const currentName = String(item?.medication_name || "");
  const current = currentMedicationPayload().find(
    (medication) => normalizeMedicationKey(medication.name) === normalizeMedicationKey(currentName)
  );
  const axis = current?.reason_for_use || primaryClinicalAxis(currentName);
  const option = item?.substitution_candidate;
  const candidateName = cleanCandidateName(option?.name);
  if (
    !candidateName
    || option?.unresolved_reason
    || /pendente/i.test(candidateName)
    || normalizeMedicationKey(candidateName) === normalizeMedicationKey(currentName)
  ) return "";
  return formatMedicationWithClass(
    candidateName,
    option.drug_class,
    axis
  );
}

function doseGuidanceForReplacement(item) {
  const option = item?.substitution_candidate;
  if (!option || option.unresolved_reason) return "";
  return String(option.dose_guidance || "").trim();
}

function doseGuidanceSourceForReplacement(item) {
  const source = (item?.substitution_candidate?.evidence || []).find(
    (citation) => citation?.source_id && citation?.title
  );
  return source ? sourceAbbreviation(source) : "";
}

function doseGuidanceDisplay(value) {
  return String(value || "")
    .replace(/^MDD:\s*/i, "Depressao em adultos: ")
    .replace(/\bstart\b/gi, "inicio")
    .replace(/\btarget\b/gi, "alvo")
    .replace(/\bmax\b/gi, "maximo")
    .replace(/\bonce daily\b/gi, "1x/dia")
    .replace(/\btwice daily\b/gi, "2x/dia")
    .replace(/\bnightly\b/gi, "a noite")
    .replace(/\bmay be used for\b/gi, "pode ser usada por")
    .replace(/\bin some patients\b/gi, "em alguns pacientes")
    .replace(/\bmg\/day\b/gi, "mg/dia")
    .replace(/\bas (?=\d)/gi, "em ")
    .replace(/\bor\b/gi, "ou")
    .replace(/\bdays\b/gi, "dias")
    .trim();
}

function replacementDosePlan(value) {
  const raw = String(value || "").trim();
  if (!raw) return null;
  const usualStart = raw.match(/\bstart\s+(\d+(?:[.,]\d+)?)\s*mg\s+once daily/i);
  const gradualStart = raw.match(
    /(\d+(?:[.,]\d+)?)\s*mg\s+once daily\s+may be used for\s+(\d+(?:\s*-\s*\d+)?)\s*days/i
  );
  const maximum = raw.match(/\bmax\s+(\d+(?:[.,]\d+)?)\s*mg\/day/i);
  const usualStartLabel = usualStart ? `${usualStart[1].replace(".", ",")} mg 1x/dia` : "";
  const gradualStartLabel = gradualStart ? `${gradualStart[1].replace(".", ",")} mg 1x/dia` : "";
  const durationLabel = gradualStart ? `${gradualStart[2].replace(/\s/g, "")} dias` : "";
  const maximumLabel = maximum ? `${maximum[1].replace(".", ",")} mg/dia` : "";
  return {
    usualStart: usualStartLabel,
    gradualStart: gradualStartLabel,
    duration: durationLabel,
    evolution: gradualStartLabel && durationLabel && usualStartLabel
      ? `Apos ${durationLabel}, reavaliar progressao para ${usualStartLabel}`
      : "",
    referenceRange: usualStartLabel && maximumLabel
      ? `${usualStart[1].replace(".", ",")}-${maximum[1].replace(".", ",")} mg/dia`
      : "",
    fullText: doseGuidanceDisplay(raw),
  };
}

function dailyQuantityLabel(frequency) {
  const normalized = String(frequency || "").trim().toLowerCase();
  const labels = {
    "1x/dia": "1 administracao/dia",
    "2x/dia": "2 administracoes/dia",
    "3x/dia": "3 administracoes/dia",
    manha: "1 administracao/dia, pela manha",
    noite: "1 administracao/dia, a noite",
  };
  return labels[normalized] || (frequency ? String(frequency) : "nao informada");
}

function dailyQuantityFromDoseGuidance(value) {
  const normalized = String(value || "").toLowerCase();
  if (/\b(?:once daily|1x\/dia)\b/.test(normalized)) return "1 administracao/dia";
  if (/\b(?:twice daily|2x\/dia)\b/.test(normalized)) return "2 administracoes/dia";
  if (/\b(?:three times daily|3x\/dia)\b/.test(normalized)) return "3 administracoes/dia";
  if (/\bnightly\b|\ba noite\b/.test(normalized)) return "1 administracao/dia, a noite";
  return "nao cadastrada na fonte estruturada";
}

function medicationDoseDecisionDetails(item) {
  const current = currentMedicationPayload().find(
    (medication) => normalizeMedicationKey(medication.name) === normalizeMedicationKey(item?.medication_name)
  );
  if (!current) {
    return {
      currentLabel: "Medicamento nao identificado",
      currentDose: "nao informada",
      currentRegimen: "Dose e frequencia nao informadas",
      dailyQuantity: "nao informada",
      comparisonRange: "faixa nao cadastrada",
    };
  }
  const axis = current.reason_for_use || primaryClinicalAxis(current.name);
  const row = bestMotor2RowForMedication(current.name, axis);
  const currentDose = currentDoseLabel(current);
  return {
    currentLabel: formatMedicationWithClass(current.name, "", axis),
    currentDose,
    currentRegimen: `${currentDose} | ${current.frequency || "frequencia nao informada"}`,
    dailyQuantity: dailyQuantityLabel(current.frequency),
    comparisonRange: motorRangeLabel(row).replace(/^Faixa por quadro:\s*/i, ""),
  };
}

function medicationPrimaryDecision(item, response) {
  const options = [
    {label: "Manter", reason: item.maintain_reason},
    {label: "Otimizar dose", reason: item.increase_reason},
    {label: "Substituir", reason: item.substitute_reason},
    {label: "Potencializar", reason: item.associate_reason},
  ];
  const safetyReason = options.find(({reason}) => /prioridade de seguranca|safety first/i.test(String(reason || "")));
  if (safetyReason) {
    return {
      label: "Seguranca primeiro",
      reason: "Resolver a prioridade de seguranca antes de alterar a medicacao.",
      showReason: true,
    };
  }
  const favored = options.find(({reason}) => /^Favorecida(?:\s|:)/i.test(String(reason || "")));
  if (favored) {
    const replacement = favored.label === "Substituir"
      ? replacementCandidateForMedication(item, response)
      : "";
    return {
      label: favored.label === "Substituir"
        ? (replacement ? `Substituir por ${replacement}` : "Revisar substituicao")
        : favored.label,
      reason: favored.label === "Substituir" && !replacement
        ? "O motor identificou motivo para troca, mas nao encontrou candidato comparavel."
        : conciseMedicationReason(favored.reason),
      showReason: favored.label !== "Manter",
    };
  }
  const conditionallyFavored = options.find(({reason}) => /^Condicionalmente favorecida/i.test(String(reason || "")));
  if (conditionallyFavored) {
    const replacement = conditionallyFavored.label === "Substituir"
      ? replacementCandidateForMedication(item, response)
      : "";
    return {
      label: conditionallyFavored.label === "Substituir"
        ? (replacement ? `Substituir por ${replacement}` : "Revisar substituicao")
        : conditionallyFavored.label,
      reason: conditionallyFavored.label === "Substituir" && !replacement
        ? "O motor identificou possibilidade de troca, mas nao encontrou candidato comparavel."
        : conciseMedicationReason(conditionallyFavored.reason),
      showReason: conditionallyFavored.label !== "Manter",
    };
  }
  return {label: "Manter", reason: "", showReason: false};
}

function medicationActionExplanationsHTML(response) {
  const explanations = response?.medication_action_explanations || [];
  if (!explanations.length) return "";
  const items = explanations.map((item) => {
    const decision = medicationPrimaryDecision(item, response);
    const doseDetails = medicationDoseDecisionDetails(item);
    const replacementDoseGuidance = doseGuidanceForReplacement(item);
    const replacementDoseSource = doseGuidanceSourceForReplacement(item);
    const replacementPlan = replacementDosePlan(replacementDoseGuidance);
    const replacementLabel = replacementCandidateForMedication(item, response);
    const isSubstitution = decision.label.startsWith("Substituir");
    const decisionLabel = isSubstitution ? "Substituir" : decision.label;
    const reason = decision.showReason
      ? `<p class="medication-decision-reason"><strong>${isSubstitution ? "Motivo da troca" : "Por que alterar"}:</strong> ${escapeHTML(decision.reason)}</p>`
      : "";
    const currentDoseDetails = isSubstitution
      ? `
          <div class="medication-decision-section medication-current-base">
            <small>Base atual</small>
            <strong>${escapeHTML(doseDetails.currentLabel)}</strong>
            <p>${escapeHTML(doseDetails.currentRegimen)}</p>
            <p><strong>Faixa cadastrada para o quadro:</strong> ${escapeHTML(doseDetails.comparisonRange)}</p>
          </div>
        `
      : `
          <p><strong>Dose atual:</strong> ${escapeHTML(doseDetails.currentDose)}</p>
          <p><strong>Quantidade/dia atual:</strong> ${escapeHTML(doseDetails.dailyQuantity)}</p>
          <p><strong>Faixa diaria para revisao:</strong> ${escapeHTML(doseDetails.comparisonRange)}</p>
        `;
    const replacementDose = isSubstitution
      ? `
          <div class="medication-decision-section medication-replacement-candidate">
            <small>Candidato do motor</small>
            <strong>${escapeHTML(replacementLabel || "Candidato ainda nao definido")}</strong>
            ${replacementPlan?.gradualStart ? `<p><strong>Inicio gradual:</strong> ${escapeHTML(replacementPlan.gradualStart)}</p>` : ""}
            ${replacementPlan?.duration ? `<p><strong>Tempo nessa etapa:</strong> ${escapeHTML(replacementPlan.duration)}, quando aplicavel</p>` : ""}
            ${replacementPlan?.evolution ? `<p><strong>Evolucao para faixa terapeutica:</strong> ${escapeHTML(replacementPlan.evolution)}</p>` : ""}
            ${replacementPlan?.referenceRange ? `<p><strong>Faixa terapeutica de referencia:</strong> ${escapeHTML(replacementPlan.referenceRange)}</p>` : ""}
            ${replacementPlan && !replacementPlan.gradualStart ? `<p><strong>Referencia de dose:</strong> ${escapeHTML(replacementPlan.fullText)}</p>` : ""}
            ${replacementDoseSource ? `<p class="medication-dose-source"><strong>Fonte:</strong> ${escapeHTML(replacementDoseSource)}</p>` : ""}
          </div>
        `
      : "";
    return `
      <li class="medication-decision-card">
        <span class="medication-decision-name">${escapeHTML(item.medication_name || "Medicamento nao identificado")}</span>
        <div class="medication-decision-summary">
          <small>Decisao</small>
          <strong>${escapeHTML(decisionLabel)}</strong>
          ${currentDoseDetails}
          ${replacementDose}
          ${reason}
        </div>
      </li>
    `;
  }).join("");
  return `
    <div class="strategy-readout medication-action-explanations">
      <p class="strategy-heading">Conduta por medicamento</p>
      <ul class="axis-medication-list">${items}</ul>
    </div>
  `;
}
function medicationResponseStability() {
  const response = currentMedicationPayload().find((item) => item.response)?.response || "";
  const normalized = response.toLowerCase();
  if (normalized.includes("boa resposta")) return "Estavel";
  if (normalized.includes("resposta parcial")) return "Resposta parcial";
  if (normalized.includes("sem resposta")) return "Sem resposta";
  if (normalized.includes("piora")) return "Piora clinica";
  return "";
}

function missingPracticalInputs() {
  if (!document.getElementById("current-medication-status")?.value) {
    return ["status da receita"];
  }
  if (noCurrentMedicationSelected()) return [];
  const medications = currentMedicationPayload();
  if (!medications.length) return ["medicamento atual"];
  const first = medications[0];
  const missing = [];
  if (hasCurrentMedicationSelected() && !first.name) missing.push("medicamento atual");
  if (!first.response) missing.push("resposta percebida");
  if (!first.duration) missing.push("tempo de uso");
  if (!first.adherence) missing.push("adesao");
  if (!first.tolerability) missing.push("tolerabilidade");
  return missing;
}

function missingClosureInputs() {
  const missing = [];
  if (!selectedSingle("presentation")) missing.push("contexto da consulta");
  if (!populationComplete()) missing.push("contexto populacional");
  if (!selectedPhenotypes().length) missing.push("fenotipo/intensidade");
  if (!selectedGroup("symptoms").length) missing.push("sintomas predominantes");
  if (!selectedClinicalAxes().length) missing.push("eixos do tratamento");
  if (!essentialSafetyComplete()) missing.push("seguranca essencial");
  if (!selectedGroup("acute-toxicity-signals").length) missing.push("seguranca aguda");
  missing.push(...missingPracticalInputs());
  return Array.from(new Set(missing));
}

function updateMedicationRequiredStatus() {
  const target = document.getElementById("medication-required-status");
  if (!target) return;
  const missing = missingPracticalInputs();
  target.classList.toggle("ready", missing.length === 0);
  target.classList.toggle("pending", missing.length > 0);
  target.textContent = missing.length
    ? `Obrigatorio para o resumo do motor: ${missing.join(", ")}.`
    : "Receita suficiente para gerar resumo pratico do conselho.";
}

function primaryClinicalAxis() {
  const axes = selectedClinicalAxes();
  if (axes.length) return axes[0];
  const medicationAxis = currentMedicationPayload().find((item) => item.reason_for_use)?.reason_for_use;
  return medicationAxis || "";
}

function firstCandidateName(options) {
  if (!options || !options.length) return "";
  return formatMedicationWithClass(options[0].name, options[0].drug_class, options[0].reason_for_use || primaryClinicalAxis());
}

function doseTargetSummary(response) {
  const target = response.pharmacological_targets?.[0];
  const doseTarget = String(target?.therapeutic_dose_target || "").trim();
  if (!doseTarget) return "alvo de dose nao retornado pela matriz";
  return doseTarget.split(" Caminhos rastreados na Tabela Motor:")[0].trim();
}

function medicationNameFromDoseRange(response) {
  const summary = doseTargetSummary(response);
  if (!summary || /nao|pausada|bloqueada|aplicavel/i.test(summary)) return "";
  const candidate = summary
    .replace(/^faixa por quadro:\s*/i, "")
    .split("/")[0]
    .trim();
  return candidate && !/\d/.test(candidate) ? candidate : "";
}

function medicationSummaryItem(item) {
  const dose = [item.dose_value, item.dose_unit].filter(Boolean).join(" ");
  const frequency = item.frequency ? ` ${item.frequency}` : "";
  return `${formatMedicationWithClass(item.name, "", item.reason_for_use)}${dose ? ` ${dose}` : ""}${frequency}`;
}

function medicationFocusForDoseRange(response) {
  const targetName = medicationNameFromDoseRange(response);
  if (!targetName) return currentMedicationSummary();
  const normalizedTarget = normalizeMedicationKey(targetName);
  const match = currentMedicationPayload().find((item) => normalizeMedicationKey(item.name) === normalizedTarget);
  if (match) return medicationSummaryItem(match);
  const current = currentMedicationSummary();
  return current
    ? `${current} (faixa do motor retornou ${formatMedicationWithClass(targetName, "", primaryClinicalAxis())})`
    : formatMedicationWithClass(targetName, "", primaryClinicalAxis());
}

function doseSourceLabel(response) {
  const source = response.pharmacological_targets?.[0]?.dose_source;
  if (!source) return "";
  const sourceId = String(source.source_id || "");
  const section = String(source.section || "");
  if (sourceId.startsWith("PSYCHRX-ABA1-DOSE")) return "TM";
  if (section.toLowerCase().includes("aba 1 dose range not registered")) {
    return "TM";
  }
  if (sourceId === "PSYCHRX-LOCAL-RULE-TABLE") return "TM";
  return sourceAbbreviation(source);
}

function doseTargetDisplay(response) {
  const range = doseTargetSummary(response);
  const source = doseSourceLabel(response);
  const normalized = range.toLowerCase();
  const cleanRange = normalized.includes("faixa por quadro: nao cadastrado")
    ? "nao cadastrada"
    : range;
  return source ? `${cleanRange} (${source})` : cleanRange;
}

function doseProfileDisplay(response) {
  const profile = String(response.pharmacological_targets?.[0]?.dose_dependent_profile || "").trim();
  return profile || "Dose - efeito: pendente pesquisar.";
}

function cleanDoseProfileText(response) {
  return doseProfileDisplay(response)
    .replace(/^(Perfil por dose|Dose - efeito):\s*/i, "")
    .replace(/Classificacao do motor:/i, "\nClassificacao:")
    .replace(/Mecanismo\/alvo:/i, "\nMecanismo:")
    .replace(/\.\s*Classificacao:/i, "\nClassificacao:")
    .replace(/\.\s*Mecanismo:/i, "\nMecanismo:")
    .replaceAll("PERFIL_CLINICO_DEPENDENTE_DA_DOSE_COM_EVIDENCIA_LIMITADA", "perfil clinico dependente da dose; evidencia limitada")
    .replaceAll("MUDANCA_FARMACOLOGICA_RELEVANTE_COM_A_DOSE", "mudanca farmacologica relevante com a dose")
    .replaceAll("MUDANCA_CLINICA_RELEVANTE_COM_A_DOSE", "mudanca clinica relevante com a dose")
    .replaceAll("MESMO_MECANISMO_MAIOR_EXPOSICAO", "mesmo mecanismo; maior exposicao")
    .replaceAll("SEM_MUDANCA_QUALITATIVA", "sem mudanca qualitativa")
    .replaceAll("SEM_MUDANCA_QUALITATIVA_COMPROVADA", "sem mudanca qualitativa comprovada")
    .replaceAll("INDICACAO_DEPENDENTE_DA_DOSE", "indicacao dependente da dose")
    .replaceAll("INDICACAO_E_EXPOSICAO_DEPENDENTES_DA_DOSE", "indicacao e exposicao dependentes da dose")
    .replaceAll("GUIADO_POR_RESPOSTA_NIVEL_E_INTERACOES", "guiado por resposta, nivel e interacoes")
    .replaceAll("GUIADO_POR_PESO_E_NIVEL_SERICO", "guiado por peso e nivel serico")
    .replaceAll("OBRIGATORIAMENTE_GUIADO_POR_LITEMIA", "obrigatoriamente guiado por litemia")
    .replaceAll("TITULACAO_DEPENDENTE_DE_INTERACOES", "titulacao dependente de interacoes")
    .replaceAll("SEM_PERFIL_RECEPTORIAL_POR_DOSE", "sem perfil receptorial por dose")
    .replaceAll("NIVEL_SERICO_OBRIGATORIO_QUANDO_INDICADO", "nivel serico obrigatorio quando indicado")
    .replaceAll("GUIADO_POR_NIVEL_E_TOXICIDADE", "guiado por nivel e toxicidade")
    .replaceAll("RESTRITO_ALTO_RISCO", "restrito / alto risco")
    .replaceAll("MESMO_MECANISMO_MAIOR_OCUPACAO_D2", "mesmo mecanismo; maior ocupacao D2");
}

function doseProfileHTML(response) {
  const lines = cleanDoseProfileText(response)
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
  return lines.map((line) => `<span class="dose-profile-line">${escapeHTML(line)}</span>`).join("");
}

function therapeuticRangeListHTML(response) {
  const rows = therapeuticRangeRows(response);
  if (!rows.length) {
    return `<span class="dose-profile-line">Nenhum medicamento selecionado ou sugerido para exibir faixa.</span>`;
  }
  const items = rows.map((row) => `
    <li>
      <span>${escapeHTML(row.context)} · ${escapeHTML(row.status)}</span>
      <strong>${escapeHTML(row.medication)}</strong>
      <small>${escapeHTML(row.doseEffect || row.range)}</small>
    </li>
  `).join("");
  return `<ul class="therapeutic-range-list">${items}</ul>`;
}

function sourceLegendHTML() {
  return `
    <div class="source-legend" aria-label="Legenda das fontes">
      <b>Legenda:</b>
      <span>DM = DailyMed/FDA</span>
      <span>NICE = National Institute for Health and Care Excellence</span>
      <span>HC = Health Canada</span>
      <span>ST-E = Stahl Essential</span>
      <span>ST-PG = Stahl Prescriber's Guide</span>
      <span>GG = Goodman &amp; Gilman</span>
      <span>BNF = British National Formulary/NICE</span>
      <span>EMA = European Medicines Agency</span>
      <span>ANVISA = regulacao brasileira</span>
      <span>UK-SMPC = informacao oficial de produto do Reino Unido</span>
      <span>TM/T1-T8 = tabelas locais</span>
      <span>PENDENTE = fonte de suporte ainda nao confirmada</span>
    </div>
  `;
}

function actionBlockers(response) {
  const warnings = (response.safety_warnings || [])
    .map((item) => String(item).trim())
    .filter(Boolean);
  if (warnings.length) return warnings;
  const missing = missingClosureInputs();
  if (missing.length) return missing;
  return (response.clinical_rationale || [])
    .map((item) => String(item).trim())
    .filter((item) => /seguranca|adesao|efeito|diagnostico|risco|instabilidade/i.test(item))
    .slice(0, 3);
}

function hasSuicideBlocker(response) {
  return actionBlockers(response).some((item) => /suicidio|suicida/i.test(item));
}

function hasSubstanceBlocker(response) {
  return actionBlockers(response).some((item) => /alcool|droga|substancia|medicacao sem controle/i.test(item));
}

function hasAcuteToxicityBlocker(response) {
  return actionBlockers(response).some((item) => /toxicidade|intoxicacao aguda/i.test(item));
}

function doseTargetDisplayHTML(response) {
  if (hasAcuteToxicityBlocker(response)) {
    return [
      "<span><b>Prioridade toxicológica:</b> as faixas terapeuticas ficam somente como contexto e nao devem orientar aumento, reducao, troca ou associacao durante a avaliacao aguda.</span>",
      "<span><b>Conduta:</b> realizar avaliacao medica urgente e confirmar a causa dos sinais registrados.</span>",
      sourceLegendHTML(),
    ].join("");
  }
  if (response.recommended_action === "investigate_before_change" || response.status === "blocked") {
    const blockers = actionBlockers(response);
    const blockerText = blockers.length ? blockers.join("; ") : "revisao de seguranca necessaria";
    return [
      `<span><b>Prioridade de seguranca:</b> ${escapeHTML(blockerText)}. As faixas permanecem disponiveis para revisao medica.</span>`,
      `<span class="dose-profile-heading"><b>Medicamentos por eixo</b></span>`,
      therapeuticRangeListHTML(response),
      populationRangeUnderAdultHTML(response),
      sourceLegendHTML(),
    ].join("");
  }
  return [
    `<span class="dose-profile-heading"><b>Medicamentos por eixo</b></span>`,
    therapeuticRangeListHTML(response),
    populationRangeUnderAdultHTML(response),
    sourceLegendHTML(),
  ].join("");
}

function strategyDoseRange(response) {
  const range = doseTargetDisplay(response);
  if (!range || range.toLowerCase().includes("nao cadastrada")) return "";
  return range.replace(/\s*\(fonte:.*?\)\s*$/i, "");
}

function practicalStrategy(response) {
  if (hasAcuteToxicityBlocker(response)) {
    return strategyActionHTML(
      "Acao agora: interromper a estrategia farmacologica de rotina e realizar avaliacao medica urgente. Os sinais registrados podem ser compativeis com toxicidade ou intoxicacao aguda, mas nao definem uma toxindrome especifica."
    );
  }
  const action = response.recommended_action || "";
  const regimen = () => robotRegimenStrategyHTML(response);
  const actionsRenderedPerMedication = new Set([
    "maintain",
    "increase_dose",
    "optimize_current",
    "decrease_dose",
    "substitute",
    "select_candidate",
    "associate",
    "taper_or_withdraw",
  ]);
  if (actionsRenderedPerMedication.has(action)) {
    return regimen();
  }
  if (action === "investigate_before_change") {
    const blockers = actionBlockers(response);
    if (hasSuicideBlocker(response)) {
      const substanceText = hasSubstanceBlocker(response)
        ? " Revisar tambem substancias e medicacao sem controle."
        : "";
      return `${robotRegimenStrategyHTML(response, `Prioridade de seguranca: ${pauseReasonText(response)}. A comparacao da receita continua disponivel abaixo.`)}${strategyActionHTML(`Acao imediata: avaliar risco suicida e definir manejo de crise pelo medico. Em paralelo, revisar as condutas calculadas para cada eixo.${substanceText}`)}`;
    }
    return blockers.length
      ? `${robotRegimenStrategyHTML(response, `Prioridade de seguranca: ${pauseReasonText(response)}. A comparacao da receita continua disponivel abaixo.`)}${strategyActionHTML(`Acao imediata: revisar ${blockers.join("; ")}. As condutas por eixo podem ser analisadas em paralelo pelo medico.`)}`
      : `${regimen()}${strategyActionHTML("Acao imediata: completar a revisao clinica e analisar as condutas calculadas por eixo.")}`;
  }
  const missing = missingPracticalInputs();
  return missing.length
    ? strategyActionHTML(`Faltou: ${missing.join(", ")}.`)
    : strategyActionHTML("Completar dados essenciais antes de definir acao.");
}

function practicalJustificationHTML(response) {
  const medications = currentMedicationPayload();
  const items = [];
  if (medications.length) {
    const axes = Array.from(new Set(medications.map((item) => item.reason_for_use).filter(Boolean)));
    const responses = Array.from(new Set(medications.map((item) => item.response).filter(Boolean)));
    const adherence = Array.from(new Set(medications.map((item) => item.adherence).filter(Boolean)));
    const tolerability = Array.from(new Set(medications.map((item) => item.tolerability).filter(Boolean)));
    items.push(`Receita: ${medications.length} medicamento(s)`);
    items.push(`Eixos cobertos: ${axes.length ? axes.join(", ") : "nao informados"}`);
    items.push(`Resposta: ${responses.length ? responses.join(", ") : "nao informada"}`);
    items.push(`Adesao/tolerabilidade: ${[adherence.join(", "), tolerability.join(", ")].filter(Boolean).join(" / ") || "nao informada"}`);
  } else {
    items.push("Sem medicacao atual");
    items.push("Escolha guiada por sintomas e objetivo");
  }
  if (response.safety_warnings?.length) {
    items.push(`Cautela: ${response.safety_warnings[0]}`);
  }
  if (response.phenotype_summary?.length) {
    items.push(response.phenotype_summary[0].replace("Fenotipo principal: ", "Fenotipo: "));
  }
  if (response.clinical_context_summary?.length) {
    items.push(`Contextos: ${response.clinical_context_summary.join("; ")}`);
  }
  return `<ul class="practical-list">${items.slice(0, 4).map((item) => `<li>${item}</li>`).join("")}</ul>`;
}

function objectiveSummaryHTML() {
  const objectives = [therapeuticObjectiveFromAxes(), ...secondaryObjectives()].filter(Boolean);
  if (!objectives.length) return "Aguardando objetivo";
  return `<ul class="practical-list">${objectives.slice(0, 5).map((item) => `<li>${item}</li>`).join("")}</ul>`;
}

function updatePracticalAdvice(action, justification, strategy, doseRange, objective) {
  setText("decision-support-practical-action", action);
  setHTML("decision-support-practical-current", justification);
  setHTML("decision-support-practical-target", strategy);
  setHTML("decision-support-practical-dose-range", doseRange);
  setHTML("decision-support-practical-next", objective);
}

function renderDecisionSupportResponse(response) {
  const substitution = response.substitution_options || [];
  const association = response.association_options || [];
  const pharmacologicalTarget = response.pharmacological_targets?.[0];
  const safetyPriority = response.status === "blocked" || response.recommended_action === "investigate_before_change";
  const acuteToxicityPriority = hasAcuteToxicityBlocker(response);
  const warnings = (response.safety_warnings || []).filter(Boolean);
  const governance = (response.evidence_governance_summary || []).filter(Boolean);
  const currentMedicationAssessment = (response.clinical_rationale || [])
    .filter((line) => String(line).startsWith("Avaliacao da medicacao atual:"))
    .join(" ");
  updatePracticalAdvice(
    practicalActionLabel(response),
    practicalJustificationHTML(response),
    `${practicalStrategy(response)}${medicationActionExplanationsHTML(response)}`,
    doseTargetDisplayHTML(response),
    objectiveSummaryHTML()
  );
  const advice = acuteToxicityPriority
    ? "Prioridade toxicológica: interromper o ranking farmacologico de rotina e realizar avaliacao medica urgente. Esta triagem nao estabelece diagnostico de toxindrome."
    : safetyPriority
    ? `Prioridade de seguranca: ${warnings.join("; ") || "revisao clinica necessaria"}. A comparacao da receita, das faixas e dos candidatos permanece disponivel.`
    : response.summary || "Sem resumo retornado.";
  setText("decision-support-advice", `${safetyFriendlyText(advice)} ${phenotypeDecisionBase(response)}`);
  setText(
    "decision-support-rationale",
    `${safetyFriendlyText((response.clinical_rationale || []).join(" "))} Contextos: ${safetyFriendlyText((response.clinical_context_summary || []).join("; ") || "nenhum adicional")}. ${(response.coverage_summary || []).join(" ")} Elegibilidade: ${eligibilityLine(response)}`
  );
  setText(
    "decision-support-current-medication",
    acuteToxicityPriority
      ? `Receita atual registrada: ${currentMedicationSummary()}. Comparacao de dose e conduta pausadas durante a avaliacao aguda.`
      : safetyFriendlyText(currentMedicationAssessment || currentMedicationAssessmentFallback(response)),
  );
  setHTML("decision-support-interactions", formatInteractionSummary(response.interaction_summary || []));
  setText(
    "decision-support-substitution",
    acuteToxicityPriority
      ? "Ranking pausado durante a avaliacao aguda."
      : substitution.length ? formatCandidates(substitution) : axisCandidatesFallback(),
  );
  setText("decision-support-disease-use-label", diseaseUseLabel(response));
  setHTML(
    "decision-support-disease-use",
    acuteToxicityPriority
      ? "Uso por quadro mantido fora da decisao ate concluir a avaliacao aguda."
      : response.disease_use_summary?.length ? formatDiseaseUse(response.disease_use_summary) : diseaseUseFallback(response),
  );
  setHTML(
    "decision-support-population-evidence",
    formatPopulationEvidence(response.population_evidence_summary || []),
  );
  setText(
    "decision-support-association",
    acuteToxicityPriority
      ? "Nenhuma associacao, troca ou ajuste de dose e proposto durante a prioridade aguda."
      : association.length ? formatCandidates(association) : "Associacao nao priorizada neste ranking.",
  );
  setText(
    "decision-support-pharmacology",
    acuteToxicityPriority
      ? "Revisao farmacologica pausada durante a prioridade aguda. Medicamentos e faixas permanecem registrados apenas como contexto para a avaliacao medica."
      : safetyPriority
      ? `Alvos por eixo: ${selectedClinicalAxes().map(axisDisplayLabel).join(", ") || "nao informados"}. Consulte as faixas terapeuticas calculadas acima.`
      : pharmacologicalTarget
      ? safetyFriendlyText(`${pharmacologicalTarget.pharmacological_target}. Dose/faixa informativa: ${pharmacologicalTarget.therapeutic_dose_target}`)
      : `Alvos por eixo: ${selectedClinicalAxes().map(axisDisplayLabel).join(", ") || "nao informados"}. Consulte as faixas terapeuticas calculadas acima.`
  );
  setText("decision-support-target", (response.impairment_targets || []).join(", "));
  const evidenceText = acuteToxicityPriority
    ? "Triagem de sinais agudos: HHS-CHEMM, CDC-OD, DM-SS e DM-NMS. Consulte a legenda de fontes da etapa Seguranca aguda."
    : `${formatEvidence(response.action_evidence || [])} Governanca cientifica: ${governance.join("; ") || "nao avaliada"}. Governanca de monitorizacao: ${(response.monitoring_governance_summary || []).join("; ") || "nao avaliada"}.`;
  setText("decision-support-evidence", evidenceText);
  setText("decision-support-evidence-map", evidenceText);
  setHTML("decision-support-source-legend", sourceLegendHTML());
  setText("level-1-strategy", response.recommended_action || "sem acao");
  setText("level-2-target", pharmacologicalTarget?.pharmacological_target || "sem alvo");
  setText("level-3-status", safetyPriority ? "prioridade de seguranca" : response.status || "sem status");
  setText(
    "decision-support-status",
    `${safetyPriority ? "Prioridade de seguranca identificada" : "Resposta recebida"} | prontidao cientifica: ${response.scientific_readiness || "nao avaliada"} | confianca: ${confidenceLabel(response.confidence, safetyPriority)}`,
  );
}

async function requestDecisionSupport() {
  updateSummary();
  const ready = selectedSingle("presentation") && populationComplete() && selectedPhenotypes().length && selectedGroup("symptoms").length && selectedClinicalAxes().length && essentialSafetyComplete() && selectedGroup("acute-toxicity-signals").length;
  if (!ready) {
    setText("decision-support-status", "Complete apresentacao, populacao, fenotipo, sintomas, eixos, seguranca essencial e seguranca aguda antes do conselho.");
    return;
  }
  setText("decision-support-status", "Consultando matriz farmacologica local...");
  try {
    const response = await fetch("/api/decision-support", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(buildDecisionSupportRequest()),
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    renderDecisionSupportResponse(await response.json());
  } catch (error) {
    setText("decision-support-status", `Falha ao consultar matriz local: ${error.message}`);
  }
}

function bindSelectableButtons() {
  document.body.addEventListener("click", (event) => {
    const button = event.target.closest("button");
    if (!button) return;
    if (button.id === "fill-random-case") {
      fillRandomCase();
      return;
    }
    if (button.id === "fill-prescription-example") {
      fillPrescriptionExampleCase();
      return;
    }
    if (button.id === "clear-clinical-form") {
      clearClinicalForm();
      return;
    }
    if (button.id === "add-current-medication") {
      addCurrentMedication();
      return;
    }
    if (button.dataset.medicationSuggestion !== undefined) {
      selectMedicationSuggestion(button.dataset.medicationSuggestion);
      return;
    }
    if (button.dataset.removeMedication !== undefined) {
      currentMedicationItems.splice(Number(button.dataset.removeMedication), 1);
      renderMedicationList();
      updateSummary();
      return;
    }
    const directFlow = {
      "continue-population": "population",
      "continue-diagnosis": "diagnosis",
      "continue-phenotype": "phenotype",
      "continue-symptoms": "symptoms",
      "continue-objective": "objective",
      "continue-medication": "medication",
      "continue-safety-review": "safety-review",
      "continue-acute-safety": "acute-safety",
      "continue-profile": "profile",
      "continue-restrictions": "restrictions",
    };
    if (directFlow[button.id]) {
      continueFromOptionalCard(directFlow[button.id]);
      return;
    }
    handleSelectableButton(button);
  });

  bindDirectSelectableButtons(document);

  document.querySelectorAll("[data-jump]").forEach((button) => {
    button.addEventListener("click", () => openCard(button.dataset.jump));
  });

  document.querySelectorAll("input, select").forEach((field) => {
    field.addEventListener("input", () => {
      renderProfile();
      updateSummary();
      updatePhysicianDecisionPreview();
    });
    field.addEventListener("change", () => {
      renderProfile();
      updateSummary();
      updatePhysicianDecisionPreview();
      if (field.classList.contains("phenotype-intensity") && selectedPhenotypes().length === 1) {
        setText("decision-support-status", "Fenotipo registrado. Voce pode continuar ou marcar outros pesos.");
      }
      if (field.classList.contains("phenotype-intensity")) {
        resetClinicalAxesFromCurrentState();
      }
      if (field.classList.contains("essential-safety-state") || field.classList.contains("suicide-safety-detail-state")) {
        updateEssentialSafetyStatus();
      }
      if (field.classList.contains("population-required-state") || field.id === "patient-birthdate") {
        updatePopulationStatus();
      }
    });
  });

  const medicationNameField = document.getElementById("current-medication-name");
  medicationNameField?.addEventListener("focus", () => renderMedicationSuggestions(medicationNameField.value));
  medicationNameField?.addEventListener("input", () => renderMedicationSuggestions(medicationNameField.value));
  document.addEventListener("click", (event) => {
    if (event.target.closest(".medication-search-field")) return;
    hideMedicationSuggestions();
  });

  document.getElementById("request-decision-support")?.addEventListener("click", requestDecisionSupport);
}

async function loadAppState() {
  const response = await fetch("/api/app-state");
  if (!response.ok) throw new Error("app_state_unavailable");
  return response.json();
}

async function loadMedicationOptions() {
  const target = document.getElementById("medication-options");
  if (!target) return;
  try {
    const response = await fetch("/api/medications");
    if (!response.ok) throw new Error("medications_unavailable");
    const payload = await response.json();
    const medications = payload.medications || [];
    medicationOptionNames = medications;
    currentMedicationDetails = payload.medication_details || [];
    medicationClassByName = new Map();
    currentMedicationDetails.forEach((item) => {
      if (!item.name) return;
      medicationClassByName.set(item.name, item.drug_class || "");
      medicationClassByName.set(normalizeMedicationKey(item.name), item.drug_class || "");
    });
    RANDOM_CASES = buildMedicationCoverageTestCases(currentMedicationDetails);
    nextRandomCaseIndex = 0;
    updateRandomCaseButton();
    target.innerHTML = medications
      .map((name) => `<option value="${String(name).replace(/"/g, "&quot;")}"></option>`)
      .join("");
  } catch {
    currentMedicationDetails = [];
    medicationOptionNames = [];
    RANDOM_CASES = buildMedicationCoverageTestCases();
    nextRandomCaseIndex = 0;
    updateRandomCaseButton();
    medicationClassByName = new Map();
    target.innerHTML = "";
  }
}

async function loadToxidromeScreeningOptions() {
  try {
    const response = await fetch("/api/toxidrome-screening");
    if (!response.ok) throw new Error("toxidrome_screening_unavailable");
    const payload = await response.json();
    acuteToxidromeSignals = payload.signals || [];
    renderAcuteToxidromeOptions(acuteToxidromeSignals);
  } catch {
    acuteToxidromeSignals = [{
      signal_id: "NONE",
      ui_label: "Nenhum sinal agudo identificado",
      pattern_hint: "Opcao operacional de triagem",
    }];
    renderAcuteToxidromeOptions(acuteToxidromeSignals);
  }
  updateAcuteSafetyStatus();
}

async function loadClinicalContexts() {
  try {
    const response = await fetch("/api/clinical-contexts");
    if (!response.ok) throw new Error("clinical_contexts_unavailable");
    const payload = await response.json();
    renderClinicalContextOptions(payload.contexts || []);
    setClinicalContextSelection(pendingScenarioClinicalContextIds);
  } catch {
    renderClinicalContextOptions([]);
  }
}

async function loadClinicalCoverage() {
  try {
    const response = await fetch("/api/clinical-coverage");
    if (!response.ok) throw new Error("clinical_coverage_unavailable");
    const payload = await response.json();
    const summary = payload.summary || {};
    setText(
      "coverage-audit-summary",
      `${payload.topic_count || 0} temas: ${summary.covered || 0} cobertos, ${summary.partial || 0} parciais, ${summary.relevant_gap || 0} lacunas relevantes e ${summary.contextual_only || 0} apenas contextuais.`
    );
  } catch {
    setText("coverage-audit-summary", "Matriz de cobertura indisponivel.");
  }
}

function initializeClinicalFlow() {
  initializePresentationOptions();
  refreshDependentOptions();
  renderPopulationOptions();
  renderEssentialSafetyAssessment();
  document.querySelectorAll("[data-single] button.active, [data-group] button.active").forEach((button) => {
    button.classList.remove("active");
  });
  document.querySelectorAll(".phenotype-intensity").forEach((select) => {
    select.value = "0";
  });
  renderMedicationList();
  bindSelectableButtons();
  renderProfile();
  updateSummary();
  updatePhysicianDecisionPreview();
  updateRandomCaseButton();
  setHTML("decision-support-source-legend", sourceLegendHTML());
  openCard("presentation");
  loadMedicationOptions();
  loadToxidromeScreeningOptions();
  loadClinicalContexts();
  loadClinicalCoverage();
}

loadAppState()
  .then((state) => {
    setText("app-mode", state.status?.mode || "Clinical Support");
    setText("app-version", state.status?.version || "v1");
    initializeClinicalFlow();
  })
  .catch(initializeClinicalFlow);
