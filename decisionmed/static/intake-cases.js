(function exposeDecisionMedCases(root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  } else {
    root.DecisionMedCases = api;
  }
})(typeof globalThis === "object" ? globalThis : this, function createCaseGenerator() {
  "use strict";

  const VERSION = "0.4.0";
  const COMPLETION_SCHEMA_VERSION = "1.0.0";
  const COMPLETION_STATUS = "simulation_only";
  const COMPLETION_SECTIONS = Object.freeze([
    "postExam",
    "reassessment",
    "impression",
    "conduct",
    "governance",
  ]);
  const SYNTHETIC_AGES = Object.freeze([
    62, 58, 34, 29, 51, 67, 46, 53, 38, 42, 31, 27, 45, 36, 54,
  ]);

  function uniqueSourceIds(sourceIds = []) {
    return [
      ...new Set(
        sourceIds.filter(
          (sourceId) =>
            typeof sourceId === "string" && sourceId.trim().length > 0,
        ),
      ),
    ];
  }

  function sourcedStatement(value, fallbackSourceIds) {
    const input =
      typeof value === "string"
        ? { text: value }
        : value && typeof value === "object"
          ? value
          : { text: "" };
    const explicitSourceIds = uniqueSourceIds(input.sourceIds || []);
    return {
      text: String(input.text || "").trim(),
      sourceIds: explicitSourceIds.length
        ? explicitSourceIds
        : uniqueSourceIds(fallbackSourceIds),
      simulationOnly: true,
    };
  }

  function syntheticCompletion(config) {
    const sourceIds = uniqueSourceIds(config.sourceIds);
    const statements = (items = []) =>
      items.map((item) => sourcedStatement(item, sourceIds));
    const postExamResults = (config.postExamResults || []).map(
      (result, index) => {
        const resultSourceIds = uniqueSourceIds(
          result.sourceIds && result.sourceIds.length
            ? result.sourceIds
            : sourceIds,
        );
        return {
          examId: result.examId || `synthetic.exam.${index + 1}`,
          name: String(result.name || "").trim(),
          finding: String(result.finding || "").trim(),
          findingOrigin: "synthetic_case",
          interpretation: String(result.interpretation || "").trim(),
          sourceIds: resultSourceIds,
          simulationOnly: true,
        };
      },
    );
    const impressionSourceIds = uniqueSourceIds(
      config.impression.sourceIds && config.impression.sourceIds.length
        ? config.impression.sourceIds
        : sourceIds,
    );

    return {
      schemaVersion: COMPLETION_SCHEMA_VERSION,
      status: COMPLETION_STATUS,
      simulationOnly: true,
      sourceIds,
      postExam: {
        status: "simulated_results_available",
        results: postExamResults,
        pending: statements(config.pendingExams),
        simulationOnly: true,
      },
      reassessment: {
        direction: config.reassessment.direction,
        summary: sourcedStatement(config.reassessment.summary, sourceIds),
        incompatibleFindings: statements(
          config.reassessment.incompatibleFindings,
        ),
        pendingQuestions: statements(config.reassessment.pendingQuestions),
        simulationOnly: true,
      },
      impression: {
        label: String(config.impression.label || "").trim(),
        certainty: config.impression.certainty,
        summary: String(config.impression.summary || "").trim(),
        sourceIds: impressionSourceIds,
        simulationOnly: true,
        professionalConfirmationRequired: true,
      },
      conduct: {
        immediate: statements(config.immediateActions),
        treatment: statements(config.treatments),
        destination: sourcedStatement(config.destination, sourceIds),
        returnPrecautions: statements(config.returnPrecautions),
        followUp: statements(config.followUp),
        sourceIds,
        simulationOnly: true,
        professionalConfirmationRequired: true,
        automaticTreatmentAllowed: false,
        automaticPrescriptionAllowed: false,
      },
      governance: {
        status: COMPLETION_STATUS,
        validationStatus: "not_validated",
        simulationOnly: true,
        clinicalExecutionAllowed: false,
        professionalConfirmationRequired: true,
        automaticTreatmentAllowed: false,
        automaticPrescriptionAllowed: false,
        llmUsed: false,
        disclaimer:
          "Caso sintético para teste do fluxo; não representa diagnóstico, prescrição nem conduta clínica executável.",
      },
    };
  }

  function cloneData(value) {
    if (Array.isArray(value)) return value.map((item) => cloneData(item));
    if (value && typeof value === "object") {
      return Object.fromEntries(
        Object.entries(value).map(([key, item]) => [key, cloneData(item)]),
      );
    }
    return value;
  }

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
      syntheticCompletion: syntheticCompletion({
        sourceIds: [
          "acc-aha.2021.chest-pain-guideline",
          "acc.2025.acute-coronary-syndromes",
        ],
        postExamResults: [
          {
            examId: "exam.synthetic.ecg.no-st-elevation",
            name: "Eletrocardiograma de 12 derivações",
            finding:
              "Traçado sintético sem supradesnivelamento persistente do segmento ST.",
            interpretation:
              "O traçado isolado não exclui síndrome coronariana aguda e deve ser correlacionado com clínica e marcadores seriados.",
          },
          {
            examId: "exam.synthetic.hs-troponin.dynamic-rise",
            name: "Troponina cardíaca de alta sensibilidade seriada",
            finding:
              "Resultado sintético com valor acima do percentil 99 e elevação na segunda coleta.",
            interpretation:
              "A dinâmica simulada aumenta a compatibilidade com lesão miocárdica aguda; a etiologia depende de avaliação profissional.",
          },
        ],
        pendingExams: [
          "Estratificação adicional e imagem ficam condicionadas à avaliação presencial e ao protocolo local.",
        ],
        reassessment: {
          direction: "increases",
          summary:
            "Os achados sintéticos aumentam a compatibilidade com uma síndrome coronariana aguda sem definir tratamento de forma automática.",
          incompatibleFindings: [
            "A ausência de supradesnivelamento persistente não sustenta a classificação de infarto com supradesnivelamento neste recorte simulado.",
          ],
          pendingQuestions: [
            "Confirmar tempo de início, contraindicações, risco hemorrágico e diagnósticos graves concorrentes.",
          ],
        },
        impression: {
          label: "Síndrome coronariana aguda sem supradesnivelamento — hipótese provável",
          certainty: "probable",
          summary:
            "Impressão sintética baseada em sintomas compatíveis e dinâmica simulada de troponina; exige confirmação médica.",
        },
        immediateActions: [
          "Manter avaliação urgente, monitorização clínica e eletrocardiográfica conforme recursos do serviço.",
          "Reavaliar imediatamente instabilidade, arritmia, insuficiência cardíaca e diagnósticos alternativos graves.",
        ],
        treatments: [
          "A terapia antitrombótica, anti-isquêmica e de prevenção secundária só pode ser selecionada pelo profissional após contraindicações, risco hemorrágico e diagnóstico diferencial.",
          "Nenhuma dose ou prescrição é liberada por este caso sintético.",
        ],
        destination:
          "Serviço de urgência com capacidade de avaliação cardiológica e manejo de síndrome coronariana aguda.",
        returnPrecautions: [
          "Dor ou desconforto persistente, dispneia, síncope, sudorese intensa ou piora clínica exigem atendimento imediato.",
        ],
        followUp: [
          "Registrar decisão profissional, resultados seriados e plano de seguimento após a fase aguda.",
        ],
      }),
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
      syntheticCompletion: syntheticCompletion({
        sourceIds: [
          "acc-aha.2021.chest-pain-guideline",
          "acc.2023.chronic-coronary-disease",
        ],
        postExamResults: [
          {
            examId: "exam.synthetic.ecg.nondiagnostic",
            name: "Eletrocardiograma de 12 derivações",
            finding:
              "Traçado sintético sem alteração isquêmica aguda conclusiva.",
            interpretation:
              "Um eletrocardiograma não diagnóstico não encerra a investigação quando a história permanece sugestiva.",
          },
          {
            examId: "exam.synthetic.hs-troponin.normal-series",
            name: "Troponina cardíaca de alta sensibilidade seriada",
            finding:
              "Série sintética sem elevação acima do limite informado pelo laboratório.",
            interpretation:
              "A série simulada reduz a compatibilidade com infarto agudo, mas não exclui isquemia sem necrose.",
          },
        ],
        pendingExams: [
          "A indicação de teste anatômico ou funcional depende de risco pré-teste, disponibilidade e decisão profissional.",
        ],
        reassessment: {
          direction: "changes",
          summary:
            "Infarto agudo fica menos compatível no cenário sintético, enquanto isquemia induzida por esforço permanece em investigação.",
          incompatibleFindings: [
            "Não há marcador sintético de necrose miocárdica nem alteração eletrocardiográfica aguda conclusiva.",
          ],
          pendingQuestions: [
            "Definir probabilidade clínica, capacidade funcional e risco cardiovascular global.",
          ],
        },
        impression: {
          label: "Isquemia miocárdica sem infarto — investigação necessária",
          certainty: "indeterminate",
          summary:
            "O padrão ao esforço mantém hipótese isquêmica, sem confirmação diagnóstica no conjunto sintético disponível.",
        },
        immediateActions: [
          "Confirmar estabilidade clínica e reavaliar qualquer recorrência ou mudança do padrão da dor.",
        ],
        treatments: [
          "Medidas farmacológicas e controle de fatores de risco dependem da avaliação cardiovascular, comorbidades e contraindicações.",
          "O caso não seleciona nem prescreve medicamento automaticamente.",
        ],
        destination:
          "Avaliação cardiológica prioritária; urgência imediata se houver sintomas atuais, instabilidade ou sinais de alarme.",
        returnPrecautions: [
          "Procurar urgência diante de desconforto em repouso, piora, dispneia, síncope, sudorese ou náusea importante.",
        ],
        followUp: [
          "Documentar o exame escolhido para esclarecer isquemia e revisar o resultado em consulta definida.",
        ],
      }),
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
      syntheticCompletion: syntheticCompletion({
        sourceIds: [
          "gina.2026.strategy-report",
          "ms-conitec.2026.asthma-pcdt",
        ],
        postExamResults: [
          {
            examId: "exam.synthetic.peak-flow.variable",
            name: "Medida de fluxo expiratório",
            finding:
              "Registro sintético com redução durante os sintomas e melhora posterior da medida.",
            interpretation:
              "A variabilidade simulada apoia limitação variável do fluxo aéreo, mas a técnica e o contexto precisam ser confirmados.",
          },
          {
            examId: "exam.synthetic.oxygen-saturation.stable",
            name: "Oximetria e sinais vitais",
            finding:
              "Saturação sintética de 96% em ar ambiente, sem sinal vital crítico informado.",
            interpretation:
              "O resultado não indica hipoxemia neste momento simulado e não substitui avaliação da gravidade clínica.",
          },
        ],
        pendingExams: [
          "Espirometria com avaliação de variabilidade ou resposta broncodilatadora permanece indicada quando viável e clinicamente apropriada.",
        ],
        reassessment: {
          direction: "increases",
          summary:
            "Exposição desencadeante, sibilância e variabilidade sintética aumentam a compatibilidade com síndrome obstrutiva variável.",
          incompatibleFindings: [],
          pendingQuestions: [
            "Excluir diagnósticos alternativos e classificar controle, risco de exacerbação e técnica inalatória.",
          ],
        },
        impression: {
          label: "Asma ou outra limitação variável do fluxo aéreo — hipótese provável",
          certainty: "probable",
          summary:
            "A hipótese é provável no caso sintético, sem dispensar confirmação funcional e avaliação profissional.",
        },
        immediateActions: [
          "Avaliar gravidade, fala, esforço respiratório, saturação e resposta clínica antes de definir o local de cuidado.",
        ],
        treatments: [
          "O profissional pode selecionar tratamento inalatório conforme diagnóstico, gravidade, técnica, adesão e contraindicações.",
          "Orientação de técnica e plano de ação fazem parte do cuidado, sem prescrição automática pelo gerador.",
        ],
        destination:
          "Atendimento ambulatorial se estável; serviço de urgência se houver dificuldade para falar, exaustão, cianose ou piora rápida.",
        returnPrecautions: [
          "Piora rápida, dificuldade para falar, sonolência, cianose ou pouca resposta ao tratamento prescrito exigem urgência.",
        ],
        followUp: [
          "Revisar sintomas, técnica inalatória, adesão, exposições e função pulmonar em prazo definido pelo profissional.",
        ],
      }),
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
      syntheticCompletion: syntheticCompletion({
        sourceIds: ["nice.2026.guidance-library"],
        postExamResults: [
          {
            examId: "exam.synthetic.urinalysis.inflammatory",
            name: "Urina tipo 1",
            finding:
              "Resultado sintético com leucocitúria e teste de nitrito positivo.",
            interpretation:
              "O conjunto aumenta a compatibilidade com infecção bacteriana do trato urinário no contexto clínico apropriado.",
          },
          {
            examId: "exam.synthetic.urine-culture.pending",
            name: "Urocultura",
            finding: "Coleta sintética registrada; resultado ainda pendente.",
            interpretation:
              "A cultura pode identificar agente e suscetibilidade quando indicada, sem justificar atraso em situações que exigem tratamento imediato.",
          },
        ],
        pendingExams: [
          "Resultado de urocultura e avaliação de função renal permanecem pendentes quando clinicamente indicados.",
        ],
        reassessment: {
          direction: "increases",
          summary:
            "Sintomas urinários baixos e urinálise sintética aumentam a compatibilidade com infecção urinária baixa.",
          incompatibleFindings: [
            "Não foram simulados febre, dor lombar ou instabilidade que sustentem pielonefrite neste recorte.",
          ],
          pendingQuestions: [
            "Confirmar gestação, sexo biológico relevante ao manejo, recorrência, função renal, alergias e sinais de complicação.",
          ],
        },
        impression: {
          label: "Infecção do trato urinário baixo — hipótese provável",
          certainty: "probable",
          summary:
            "A impressão sintética permanece sujeita à avaliação de fatores de complicação e diagnósticos alternativos.",
        },
        immediateActions: [
          "Verificar sinais de pielonefrite, sepse, obstrução, gestação e outras condições que mudem a urgência.",
        ],
        treatments: [
          "A seleção de antimicrobiano, dose e duração depende do perfil do paciente, resistência local, função renal, alergias e decisão profissional.",
          "Medidas sintomáticas podem ser consideradas pelo profissional; o gerador não emite prescrição.",
        ],
        destination:
          "Atendimento ambulatorial se estável e sem complicadores; urgência se houver febre alta, dor lombar, vômitos, gestação com sinais de alarme ou deterioração.",
        returnPrecautions: [
          "Febre, dor lombar, vômitos, redução importante de urina, confusão ou piora exigem reavaliação rápida.",
        ],
        followUp: [
          "Revisar resposta clínica e cultura quando coletada, ajustando o plano somente por decisão profissional.",
        ],
      }),
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
      syntheticCompletion: syntheticCompletion({
        sourceIds: ["nice.2026.guidance-library"],
        postExamResults: [
          {
            examId: "exam.synthetic.cbc.no-severe-anemia",
            name: "Hemograma",
            finding:
              "Resultado sintético sem anemia grave, com hemoglobina a ser acompanhada conforme evolução.",
            interpretation:
              "Um valor inicial sem anemia grave não exclui sangramento relevante nem define sua origem.",
          },
          {
            examId: "exam.synthetic.endoscopy.pending",
            name: "Avaliação endoscópica dirigida",
            finding:
              "Exame sintético ainda não realizado; indicação depende da estabilidade, idade, padrão do sangramento e risco.",
            interpretation:
              "A investigação deve localizar a fonte e avaliar causas inflamatórias, vasculares, neoplásicas e anorretais conforme o contexto.",
          },
        ],
        pendingExams: [
          "Avaliação endoscópica e exames laboratoriais adicionais permanecem condicionados à estratificação profissional.",
        ],
        reassessment: {
          direction: "maintains",
          summary:
            "O sangramento intestinal permanece confirmado como manifestação, mas sua causa continua indeterminada no cenário sintético.",
          incompatibleFindings: [
            "A ausência de anemia grave no primeiro resultado não elimina perda recente ou intermitente.",
          ],
          pendingQuestions: [
            "Quantificar sangramento, verificar instabilidade, anticoagulantes, dor, perda ponderal e mudança persistente do hábito intestinal.",
          ],
        },
        impression: {
          label: "Sangramento gastrointestinal baixo — etiologia indeterminada",
          certainty: "indeterminate",
          summary:
            "A manifestação exige localização e investigação etiológica; o caso não atribui causa específica.",
        },
        immediateActions: [
          "Avaliar estabilidade hemodinâmica, volume do sangramento, hemograma seriado quando indicado e medicamentos que alterem coagulação.",
        ],
        treatments: [
          "Reposição volêmica, hemoderivados, suspensão ou reversão de fármacos e terapia específica dependem de gravidade e decisão presencial.",
          "Não há tratamento etiológico automático sem identificar a fonte.",
        ],
        destination:
          "Urgência se houver sangramento volumoso, síncope, instabilidade ou piora; investigação digestiva prioritária se estável.",
        returnPrecautions: [
          "Aumento do sangramento, tontura, desmaio, palidez, dor intensa, febre ou fraqueza importante exigem atendimento imediato.",
        ],
        followUp: [
          "Registrar evolução do sangramento e revisar o resultado da investigação endoscópica ou coloproctológica.",
        ],
      }),
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
      syntheticCompletion: syntheticCompletion({
        sourceIds: [
          "ms-conitec.2023.acute-ischemic-stroke-pcdt",
          "aha.2023.transient-ischemic-attack",
        ],
        postExamResults: [
          {
            examId: "exam.synthetic.head-ct.no-hemorrhage",
            name: "Tomografia de crânio sem contraste",
            finding:
              "Imagem sintética sem hemorragia intracraniana aguda identificada.",
            interpretation:
              "A ausência simulada de hemorragia permite prosseguir na investigação de isquemia, sem confirmar sozinha o diagnóstico.",
          },
          {
            examId: "exam.synthetic.glucose.normal",
            name: "Glicemia capilar",
            finding:
              "Valor sintético dentro do intervalo informado pelo serviço.",
            interpretation:
              "O achado reduz a possibilidade de alteração glicêmica como imitador imediato do déficit focal.",
          },
        ],
        pendingExams: [
          "Imagem vascular, perfusão e exames etiológicos dependem de tempo de início, disponibilidade e avaliação da equipe de AVC.",
        ],
        reassessment: {
          direction: "increases",
          summary:
            "Déficit focal persistente, início súbito e ausência sintética de hemorragia aumentam a compatibilidade com AVC isquêmico agudo.",
          incompatibleFindings: [],
          pendingQuestions: [
            "Confirmar último momento bem, escala neurológica, anticoagulantes, contraindicações e elegibilidade para reperfusão.",
          ],
        },
        impression: {
          label: "Acidente vascular cerebral isquêmico agudo — hipótese provável",
          certainty: "probable",
          summary:
            "Hipótese sintética provável que exige confirmação imediata por equipe habilitada e protocolo local.",
        },
        immediateActions: [
          "Ativar fluxo de AVC, registrar o último momento conhecido sem déficit e manter avaliação neurológica e fisiológica urgente.",
          "Não atrasar encaminhamento por etapas do formulário ou por exames não essenciais à decisão imediata.",
        ],
        treatments: [
          "Trombólise ou trombectomia só podem ser indicadas por equipe habilitada após critérios temporais, de imagem e contraindicações.",
          "Pressão arterial, glicemia, oxigenação, deglutição e prevenção de complicações devem seguir decisão profissional e protocolo do serviço.",
        ],
        destination:
          "Emergência com protocolo de AVC e acesso a neuroimagem e terapia de reperfusão.",
        returnPrecautions: [
          "Qualquer déficit focal súbito, alteração da fala, assimetria facial, perda visual ou piora neurológica é emergência.",
        ],
        followUp: [
          "Após a fase aguda, documentar etiologia investigada, prevenção secundária e plano de reabilitação.",
        ],
      }),
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
      syntheticCompletion: syntheticCompletion({
        sourceIds: ["aad.2026.guideline-library"],
        postExamResults: [
          {
            examId: "exam.synthetic.dermoscopy.suspicious",
            name: "Dermatoscopia",
            finding:
              "Registro sintético com assimetria e estruturas pigmentadas irregulares.",
            interpretation:
              "Os achados simulados justificam avaliação especializada e possível confirmação histopatológica; não estabelecem diagnóstico isoladamente.",
          },
          {
            examId: "exam.synthetic.skin-biopsy.pending",
            name: "Histopatologia",
            finding:
              "Amostra sintética ainda não coletada; resultado inexistente.",
            interpretation:
              "A decisão sobre técnica de biópsia ou excisão depende do exame dermatológico e da localização da lesão.",
          },
        ],
        pendingExams: [
          "Confirmação histopatológica permanece pendente caso o dermatologista indique coleta.",
        ],
        reassessment: {
          direction: "increases",
          summary:
            "Mudança evolutiva e padrão dermatoscópico sintético aumentam a suspeita de lesão melanocítica relevante.",
          incompatibleFindings: [],
          pendingQuestions: [
            "Confirmar evolução, dimensões, localização, exposição solar, história pessoal e familiar e exame cutâneo completo.",
          ],
        },
        impression: {
          label: "Lesão pigmentada suspeita — diagnóstico histológico indeterminado",
          certainty: "indeterminate",
          summary:
            "O caso sintético indica necessidade de avaliação dermatológica sem afirmar melanoma ou outra etiologia.",
        },
        immediateActions: [
          "Documentar localização, tamanho, imagem clínica autorizada e evolução sem atrasar avaliação especializada.",
        ],
        treatments: [
          "Não realizar tratamento destrutivo empírico antes de decisão diagnóstica quando houver suspeita de neoplasia.",
          "Biópsia, excisão e margens dependem da avaliação dermatológica e do resultado histopatológico.",
        ],
        destination:
          "Dermatologia em caráter prioritário, com urgência maior se houver crescimento rápido, sangramento ou ulceração.",
        returnPrecautions: [
          "Crescimento acelerado, sangramento espontâneo, ulceração ou aparecimento de novos sinais sistêmicos exigem reavaliação.",
        ],
        followUp: [
          "Revisar histopatologia quando realizada e registrar plano definitivo e vigilância cutânea.",
        ],
      }),
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
      syntheticCompletion: syntheticCompletion({
        sourceIds: ["nice.2026.guidance-library"],
        postExamResults: [
          {
            examId: "exam.synthetic.dilated-fundus.suspected-tear",
            name: "Exame de fundo de olho sob dilatação",
            finding:
              "Registro sintético com área periférica suspeita de rotura retiniana, sem conclusão definitiva.",
            interpretation:
              "Flashes, moscas volantes e suspeita de rotura exigem avaliação oftalmológica urgente para prevenir progressão.",
          },
          {
            examId: "exam.synthetic.visual-acuity.preserved",
            name: "Acuidade visual",
            finding:
              "Acuidade sintética preservada no momento do registro.",
            interpretation:
              "Acuidade preservada não exclui rotura periférica nem risco de descolamento de retina.",
          },
        ],
        pendingExams: [
          "Avaliação completa da retina periférica por oftalmologista permanece pendente.",
        ],
        reassessment: {
          direction: "increases",
          summary:
            "O padrão de sintomas e o achado sintético aumentam a suspeita de rotura retiniana.",
          incompatibleFindings: [],
          pendingQuestions: [
            "Confirmar campo visual, efeito de cortina, miopia, trauma, cirurgia ocular prévia e lateralidade.",
          ],
        },
        impression: {
          label: "Rotura retiniana — hipótese provável, sem confirmação",
          certainty: "probable",
          summary:
            "A hipótese sintética requer confirmação oftalmológica imediata antes de qualquer procedimento.",
        },
        immediateActions: [
          "Encaminhar para avaliação oftalmológica urgente e registrar início, lateralidade e perda de campo visual.",
        ],
        treatments: [
          "Laser, crioterapia ou cirurgia somente podem ser definidos pelo oftalmologista após exame completo.",
          "O gerador não recomenda colírios ou procedimentos automáticos.",
        ],
        destination:
          "Serviço oftalmológico de urgência no mesmo dia, especialmente se houver sombra, cortina ou perda visual.",
        returnPrecautions: [
          "Sombra em cortina, aumento súbito de manchas, perda de campo ou redução visual exigem atendimento imediato.",
        ],
        followUp: [
          "Registrar avaliação da retina contralateral e seguimento definido pelo especialista.",
        ],
      }),
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
      syntheticCompletion: syntheticCompletion({
        sourceIds: ["aaos.2026.cpg-library"],
        postExamResults: [
          {
            examId: "exam.synthetic.radiograph.no-fracture",
            name: "Radiografia dirigida",
            finding:
              "Imagem sintética sem fratura ou luxação evidente no segmento avaliado.",
            interpretation:
              "A radiografia simulada reduz a suspeita de lesão óssea deslocada, mas não exclui fratura oculta ou lesão ligamentar.",
          },
          {
            examId: "exam.synthetic.neurovascular.intact",
            name: "Exame neurovascular distal",
            finding:
              "Registro sintético com perfusão, sensibilidade e força distal preservadas.",
            interpretation:
              "O achado reduz a preocupação imediata com comprometimento neurovascular, devendo ser reavaliado se houver mudança.",
          },
        ],
        pendingExams: [
          "Imagem avançada só deve ser considerada diante de suspeita persistente, instabilidade ou evolução incompatível.",
        ],
        reassessment: {
          direction: "changes",
          summary:
            "Sem fratura evidente e com exame neurovascular preservado, lesão de partes moles torna-se mais compatível no cenário sintético.",
          incompatibleFindings: [
            "O recorte não mostra luxação, fratura deslocada ou déficit neurovascular.",
          ],
          pendingQuestions: [
            "Confirmar capacidade de apoio, instabilidade, ponto de dor óssea e critérios específicos do segmento.",
          ],
        },
        impression: {
          label: "Lesão musculoesquelética pós-trauma — hipótese provável",
          certainty: "probable",
          summary:
            "A hipótese de partes moles é provável, mas fratura oculta permanece possível conforme exame e evolução.",
        },
        immediateActions: [
          "Proteger o segmento, reavaliar dor, edema, função e estado neurovascular.",
        ],
        treatments: [
          "Analgesia e medidas locais podem ser definidas pelo profissional conforme contraindicações, tolerância e tipo de lesão.",
          "Imobilização e liberação de carga dependem do segmento e da estabilidade clínica.",
        ],
        destination:
          "Seguimento ambulatorial se estável; ortopedia ou urgência se houver deformidade, incapacidade de apoio, déficit neurovascular ou dor desproporcional.",
        returnPrecautions: [
          "Dormência, extremidade fria ou pálida, dor crescente, edema tenso, febre ou perda funcional exigem reavaliação.",
        ],
        followUp: [
          "Reexaminar se a dor persistir e considerar nova imagem quando houver suspeita de fratura oculta.",
        ],
      }),
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
      syntheticCompletion: syntheticCompletion({
        sourceIds: ["acog.2026.clinical-guidance"],
        postExamResults: [
          {
            examId: "exam.synthetic.pregnancy-test.negative",
            name: "Teste de gravidez",
            finding: "Resultado sintético negativo.",
            interpretation:
              "O resultado reduz a possibilidade de causa gestacional no momento testado, considerando tempo e sensibilidade do método.",
          },
          {
            examId: "exam.synthetic.pelvic-ultrasound.nonspecific",
            name: "Ultrassonografia pélvica",
            finding:
              "Imagem sintética sem massa anexial aguda e sem etiologia única definida para o sangramento.",
            interpretation:
              "A ultrassonografia não específica mantém a necessidade de correlação com padrão menstrual, exame e fatores de risco endometrial.",
          },
        ],
        pendingExams: [
          "Hemograma, avaliação cervical e investigação endometrial dependem do volume, idade, persistência e fatores de risco.",
        ],
        reassessment: {
          direction: "maintains",
          summary:
            "Sangramento uterino anormal permanece como síndrome, com etiologia ainda não definida no caso sintético.",
          incompatibleFindings: [
            "Não foi simulada massa anexial aguda nem gravidez detectável.",
          ],
          pendingQuestions: [
            "Caracterizar ciclo, volume, contracepção, medicamentos, anemia, exame cervical e fatores de risco.",
          ],
        },
        impression: {
          label: "Sangramento uterino anormal — etiologia indeterminada",
          certainty: "indeterminate",
          summary:
            "O caso reconhece a síndrome, sem atribuir causa estrutural, ovulatória ou sistêmica.",
        },
        immediateActions: [
          "Quantificar sangramento, avaliar estabilidade, anemia, dor intensa e possibilidade de gestação conforme o momento do teste.",
        ],
        treatments: [
          "Tratamento hormonal, antifibrinolítico, procedimento ou reposição de ferro dependem da causa, gravidade, riscos e decisão profissional.",
          "Nenhuma terapia é selecionada automaticamente neste caso.",
        ],
        destination:
          "Ginecologia prioritária se estável; urgência se houver sangramento intenso, instabilidade, síncope ou dor importante.",
        returnPrecautions: [
          "Sangramento que encharca absorventes rapidamente, desmaio, falta de ar, palidez ou dor intensa exige atendimento urgente.",
        ],
        followUp: [
          "Revisar exames, persistência do sangramento e resultado de investigação endometrial quando indicada.",
        ],
      }),
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
      syntheticCompletion: syntheticCompletion({
        sourceIds: [
          "acog.2026.clinical-guidance",
          "who.2026.guideline-library",
        ],
        postExamResults: [
          {
            examId: "exam.synthetic.obstetric-ultrasound.viable-iup",
            name: "Ultrassonografia obstétrica",
            finding:
              "Imagem sintética de gestação intrauterina com atividade cardíaca presente no momento do exame.",
            interpretation:
              "O achado confirma localização intrauterina e viabilidade naquele momento, mas não explica sozinho o sangramento nem garante evolução.",
          },
          {
            examId: "exam.synthetic.cbc.stable",
            name: "Hemograma e avaliação hemodinâmica",
            finding:
              "Registro sintético sem instabilidade e sem anemia importante.",
            interpretation:
              "Estabilidade atual permite estratificação, mas exige reavaliação se o volume ou os sintomas mudarem.",
          },
        ],
        pendingExams: [
          "Tipagem sanguínea, fator Rh e outros exames dependem da idade gestacional, história e protocolo obstétrico.",
        ],
        reassessment: {
          direction: "changes",
          summary:
            "Gestação intrauterina viável no exame sintético reduz algumas hipóteses, mas o sangramento obstétrico continua exigindo avaliação etiológica.",
          incompatibleFindings: [
            "Não foram simuladas instabilidade hemodinâmica ou ausência de atividade cardíaca.",
          ],
          pendingQuestions: [
            "Confirmar idade gestacional, dor, volume, colo uterino, fator Rh e eventos prévios.",
          ],
        },
        impression: {
          label: "Sangramento na gestação com viabilidade atual — causa indeterminada",
          certainty: "indeterminate",
          summary:
            "O caso sintético não confirma perda gestacional nem define a origem do sangramento.",
        },
        immediateActions: [
          "Avaliar prontamente estabilidade, dor, volume do sangramento e idade gestacional em ambiente obstétrico.",
        ],
        treatments: [
          "Imunoprofilaxia, progesterona, procedimento ou outra intervenção dependem de indicação individual e protocolo profissional.",
          "Não há tratamento ou prescrição automática para sangramento na gestação.",
        ],
        destination:
          "Avaliação obstétrica no mesmo dia; emergência se houver sangramento intenso, dor forte, síncope ou instabilidade.",
        returnPrecautions: [
          "Aumento do sangramento, dor intensa ou unilateral, desmaio, febre ou piora clínica exige atendimento imediato.",
        ],
        followUp: [
          "Revisar evolução clínica e ultrassonográfica no prazo definido pela equipe obstétrica.",
        ],
      }),
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
      syntheticCompletion: syntheticCompletion({
        sourceIds: ["who.2023.mhgap-guideline"],
        postExamResults: [
          {
            examId: "exam.synthetic.mental-health-risk-screen",
            name: "Avaliação estruturada de segurança",
            finding:
              "Registro sintético sem ideação suicida atual, plano, psicose ou agitação grave.",
            interpretation:
              "A ausência registrada reduz o risco imediato aparente, mas não elimina necessidade de avaliação clínica e plano de segurança.",
          },
          {
            examId: "exam.synthetic.anxiety-screen.positive",
            name: "Instrumento de rastreio de ansiedade",
            finding:
              "Pontuação sintética acima do ponto de rastreio informado pelo instrumento.",
            interpretation:
              "Rastreio positivo indica necessidade de avaliação diagnóstica; não confirma transtorno por si só.",
          },
        ],
        pendingExams: [
          "Causas clínicas, substâncias, medicamentos e transtornos concorrentes devem ser avaliados conforme história e exame.",
        ],
        reassessment: {
          direction: "increases",
          summary:
            "Preocupação persistente, insônia e rastreio sintético aumentam a compatibilidade com síndrome ansiosa.",
          incompatibleFindings: [
            "Não foram simulados mania, psicose ou risco suicida agudo.",
          ],
          pendingQuestions: [
            "Confirmar duração, prejuízo funcional, uso de substâncias, sintomas depressivos, mania, trauma e risco.",
          ],
        },
        impression: {
          label: "Síndrome ansiosa com insônia — hipótese provável",
          certainty: "probable",
          summary:
            "A formulação sintética é sindrômica e requer entrevista clínica para diagnóstico e comorbidades.",
        },
        immediateActions: [
          "Reavaliar risco de autoagressão, violência, intoxicação, abstinência, mania ou psicose antes do manejo ambulatorial.",
        ],
        treatments: [
          "Intervenções psicossociais, higiene do sono e psicoterapia podem integrar o plano definido pelo profissional.",
          "Medicamentos exigem diagnóstico, avaliação de riscos, interações e acompanhamento; não há prescrição automática.",
        ],
        destination:
          "Cuidado ambulatorial programado se risco baixo e suporte adequado; urgência diante de risco, psicose, mania ou incapacidade grave.",
        returnPrecautions: [
          "Ideação suicida, agitação intensa, perda de contato com a realidade, incapacidade de autocuidado ou piora abrupta exigem urgência.",
        ],
        followUp: [
          "Reavaliar sintomas, funcionamento, sono, adesão e segurança em intervalo definido pelo profissional.",
        ],
      }),
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
      syntheticCompletion: syntheticCompletion({
        sourceIds: [
          "ada.2026.standards-of-care",
          "nice.2026.guidance-library",
        ],
        postExamResults: [
          {
            examId: "exam.synthetic.thyroid-profile.thyrotoxic",
            name: "TSH e tiroxina livre",
            finding:
              "Resultado sintético com TSH reduzido e tiroxina livre elevada.",
            interpretation:
              "O padrão laboratorial simulado é compatível com tireotoxicose bioquímica, cuja causa ainda precisa ser definida.",
          },
          {
            examId: "exam.synthetic.glucose.not-diagnostic",
            name: "Glicemia",
            finding:
              "Valor sintético sem critério diagnóstico de hiperglicemia no momento avaliado.",
            interpretation:
              "O achado torna hiperglicemia manifesta menos explicativa neste recorte, sem encerrar avaliação metabólica.",
          },
        ],
        pendingExams: [
          "Investigação etiológica da tireotoxicose e avaliação de repercussões dependem de história, exame e decisão profissional.",
        ],
        reassessment: {
          direction: "changes",
          summary:
            "O perfil tireoidiano sintético direciona a investigação para tireotoxicose, sem determinar sua etiologia.",
          incompatibleFindings: [
            "Não há hiperglicemia manifesta simulada para explicar o conjunto de sintomas.",
          ],
          pendingQuestions: [
            "Confirmar palpitações, tremor, bócio, dor cervical, medicamentos, gestação e sinais de descompensação.",
          ],
        },
        impression: {
          label: "Tireotoxicose bioquímica — etiologia indeterminada",
          certainty: "probable",
          summary:
            "O estado bioquímico é provável no cenário sintético; doença de base e gravidade permanecem pendentes.",
        },
        immediateActions: [
          "Avaliar frequência cardíaca, temperatura, estado mental, insuficiência cardíaca e outros sinais de gravidade.",
        ],
        treatments: [
          "Controle sintomático e terapia etiológica dependem da causa, comorbidades, gestação, contraindicações e decisão profissional.",
          "Antitireoidianos ou outros fármacos não são selecionados automaticamente pelo caso.",
        ],
        destination:
          "Avaliação clínica/endocrinológica prioritária; urgência se houver febre alta, alteração mental, arritmia ou insuficiência cardíaca.",
        returnPrecautions: [
          "Palpitação sustentada, dor torácica, falta de ar, febre, confusão ou fraqueza extrema exigem atendimento imediato.",
        ],
        followUp: [
          "Repetir e complementar avaliação laboratorial conforme etiologia e revisar resposta ao plano profissional.",
        ],
      }),
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
      syntheticCompletion: syntheticCompletion({
        sourceIds: ["acr.2026.guideline-library"],
        postExamResults: [
          {
            examId: "exam.synthetic.inflammatory-markers.elevated",
            name: "Hemograma e marcadores inflamatórios",
            finding:
              "Resultado sintético com elevação inespecífica de marcadores inflamatórios.",
            interpretation:
              "Marcadores elevados sustentam inflamação, mas não distinguem infecção, autoimunidade, vasculite ou outras causas.",
          },
          {
            examId: "exam.synthetic.urinalysis.hematuria-proteinuria",
            name: "Urina tipo 1 e função renal",
            finding:
              "Registro sintético com hematúria microscópica e proteinúria, sem falência renal informada.",
            interpretation:
              "O achado sugere possível envolvimento renal e aumenta a urgência da investigação sistêmica.",
          },
        ],
        pendingExams: [
          "Sorologias, autoanticorpos, imagem e biópsia devem ser selecionados pela apresentação e hipótese, evitando painel indiscriminado.",
        ],
        reassessment: {
          direction: "increases",
          summary:
            "Febre, lesões cutâneas e alteração urinária sintética aumentam a suspeita de doença inflamatória sistêmica com possível órgão-alvo.",
          incompatibleFindings: [],
          pendingQuestions: [
            "Excluir infecção, exposição medicamentosa e comprometimento pulmonar, neurológico, gastrointestinal e renal.",
          ],
        },
        impression: {
          label: "Doença inflamatória sistêmica ou vasculite — hipótese indeterminada",
          certainty: "indeterminate",
          summary:
            "O padrão sintético justifica investigação urgente, sem confirmar subtipo de vasculite ou etiologia autoimune.",
        },
        immediateActions: [
          "Avaliar função renal, pressão arterial, oxigenação, sintomas neurológicos e sinais de infecção ou hemorragia.",
        ],
        treatments: [
          "Imunossupressão não deve ser iniciada automaticamente; decisão depende de gravidade, órgão-alvo, exclusão de infecção e avaliação especializada.",
          "Suporte clínico e tratamento etiológico devem seguir o quadro presencial.",
        ],
        destination:
          "Avaliação urgente e especializada; emergência se houver comprometimento renal agudo, pulmonar, neurológico ou instabilidade.",
        returnPrecautions: [
          "Falta de ar, sangue ao tossir, redução de urina, confusão, fraqueza focal, dor intensa ou piora rápida exigem emergência.",
        ],
        followUp: [
          "Revisar tendência renal, marcadores, investigação etiológica e plano de monitorização de órgão-alvo.",
        ],
      }),
    },
    {
      id: "unclassified-fatigue",
      label: "Sintoma ainda não classificado",
      complaint: "Outro sintoma",
      note: "Mal-estar inespecífico sem localização ou padrão definido.",
      expectedModules: ["generalmedicine"],
      answers: {},
      syntheticCompletion: syntheticCompletion({
        sourceIds: [
          "nice.2026.guidance-library",
          "who.2026.guideline-library",
        ],
        postExamResults: [
          {
            examId: "exam.synthetic.basic-assessment.nonspecific",
            name: "Avaliação clínica e exames básicos dirigidos",
            finding:
              "Resultados sintéticos sem alteração focal ou sinal de disfunção orgânica aguda.",
            interpretation:
              "Resultados inespecíficos não definem causa e devem ser interpretados segundo duração, contexto e evolução.",
          },
          {
            examId: "exam.synthetic.vitals.stable",
            name: "Sinais vitais",
            finding:
              "Registro sintético sem instabilidade fisiológica no momento avaliado.",
            interpretation:
              "Estabilidade atual permite investigação estruturada, mantendo orientação de retorno se surgirem sinais de alarme.",
          },
        ],
        pendingExams: [
          "Exames adicionais devem responder a hipóteses surgidas na história e no exame, sem bateria indiscriminada.",
        ],
        reassessment: {
          direction: "insufficient",
          summary:
            "Os dados sintéticos permanecem insuficientes para reconhecer uma síndrome específica.",
          incompatibleFindings: [
            "Não há, neste recorte, achado focal ou sinal de disfunção orgânica aguda que direcione uma hipótese única.",
          ],
          pendingQuestions: [
            "Revisar cronologia, medicamentos, sono, humor, nutrição, exposições, infecções, sintomas sistêmicos e função.",
          ],
        },
        impression: {
          label: "Quadro clínico ainda não classificado",
          certainty: "indeterminate",
          summary:
            "A impressão sintética permanece aberta e não deve ser convertida em diagnóstico por ausência de achados.",
        },
        immediateActions: [
          "Repetir história e exame dirigidos, confirmar sinais vitais e procurar sinais de alarme ou perda funcional.",
        ],
        treatments: [
          "Evitar tratamento etiológico empírico sem hipótese sustentada; medidas de suporte dependem da avaliação profissional.",
          "O gerador não propõe prescrição automática para sintomas inespecíficos.",
        ],
        destination:
          "Acompanhamento clínico programado se estável, com urgência diante de novos sinais de alarme ou deterioração.",
        returnPrecautions: [
          "Febre persistente, falta de ar, dor importante, déficit neurológico, sangramento, desmaio ou piora funcional exigem reavaliação.",
        ],
        followUp: [
          "Definir prazo curto para reavaliação, revisar evolução e atualizar hipóteses antes de ampliar exames.",
        ],
      }),
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
    const clone = cloneData(template);
    return {
      ...clone,
      id: `${template.id}-${cycle}`,
      label: cycle === 1 ? template.label : `${template.label} · variação ${cycle}`,
      expectedModules: [...template.expectedModules],
      answers: cloneData(template.answers),
      syntheticCompletion: cloneData(template.syntheticCompletion),
    };
  }

  function safeQuantity(quantity) {
    const parsed = Number.parseInt(quantity, 10);
    return Number.isFinite(parsed)
      ? Math.min(100, Math.max(1, parsed))
      : 1;
  }

  function collectSourceIds(value, target = new Set()) {
    if (Array.isArray(value)) {
      value.forEach((item) => collectSourceIds(item, target));
      return target;
    }
    if (!value || typeof value !== "object") return target;
    if (Array.isArray(value.sourceIds)) {
      uniqueSourceIds(value.sourceIds).forEach((sourceId) =>
        target.add(sourceId),
      );
    }
    Object.values(value).forEach((item) => collectSourceIds(item, target));
    return target;
  }

  function sourceIdsForCase(scenario) {
    return [
      ...collectSourceIds(
        scenario && scenario.syntheticCompletion
          ? scenario.syntheticCompletion
          : {},
      ),
    ];
  }

  function isSyntheticCompletionComplete(completion) {
    if (
      !completion ||
      completion.schemaVersion !== COMPLETION_SCHEMA_VERSION ||
      completion.status !== COMPLETION_STATUS ||
      completion.simulationOnly !== true
    ) {
      return false;
    }
    if (
      !COMPLETION_SECTIONS.every(
        (section) => completion[section] && completion[section].simulationOnly,
      )
    ) {
      return false;
    }
    if (
      !Array.isArray(completion.postExam.results) ||
      completion.postExam.results.length === 0 ||
      !completion.postExam.results.every(
        (result) =>
          result.simulationOnly === true &&
          result.findingOrigin === "synthetic_case" &&
          result.name &&
          result.finding &&
          result.interpretation &&
          result.sourceIds.length > 0,
      )
    ) {
      return false;
    }
    if (
      !["increases", "reduces", "maintains", "changes", "insufficient"].includes(
        completion.reassessment.direction,
      ) ||
      !completion.reassessment.summary.text ||
      completion.reassessment.summary.sourceIds.length === 0
    ) {
      return false;
    }
    if (
      !["probable", "indeterminate"].includes(
        completion.impression.certainty,
      ) ||
      !completion.impression.label ||
      !completion.impression.summary ||
      completion.impression.sourceIds.length === 0 ||
      completion.impression.professionalConfirmationRequired !== true
    ) {
      return false;
    }
    if (
      !["immediate", "treatment", "returnPrecautions", "followUp"].every(
        (key) =>
          Array.isArray(completion.conduct[key]) &&
          completion.conduct[key].length > 0 &&
          completion.conduct[key].every(
            (item) =>
              item.simulationOnly === true &&
              item.text &&
              item.sourceIds.length > 0,
          ),
      ) ||
      !completion.conduct.destination.text ||
      completion.conduct.destination.sourceIds.length === 0
    ) {
      return false;
    }
    return (
      completion.governance.status === COMPLETION_STATUS &&
      completion.governance.validationStatus === "not_validated" &&
      completion.governance.clinicalExecutionAllowed === false &&
      completion.governance.automaticTreatmentAllowed === false &&
      completion.governance.automaticPrescriptionAllowed === false &&
      completion.governance.llmUsed === false &&
      completion.governance.professionalConfirmationRequired === true &&
      completion.conduct.automaticTreatmentAllowed === false &&
      completion.conduct.automaticPrescriptionAllowed === false &&
      completion.conduct.professionalConfirmationRequired === true
    );
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
    completionSchemaVersion: COMPLETION_SCHEMA_VERSION,
    completionStatus: COMPLETION_STATUS,
    completionSections: [...COMPLETION_SECTIONS],
    templateCount: TEMPLATES.length,
    buildCases,
    buildSuite,
    buildAssistedCases,
    buildDirectCases,
    buildInvestigationCases,
    investigationPairCount: INVESTIGATION_PAIRS.length,
    isSyntheticCompletionComplete,
    sourceIdsForCase,
  });
});
