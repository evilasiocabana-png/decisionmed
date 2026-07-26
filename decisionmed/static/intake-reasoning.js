(function exposeDecisionMedReasoning(root, factory) {
  let ruleEngine = root.DecisionMedRuleEngine;
  if (typeof module === "object" && module.exports) {
    ruleEngine = require("./intake-rule-engine.js");
  }
  const api = factory(ruleEngine);
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  } else {
    root.DecisionMedReasoning = api;
  }
})(
  typeof globalThis === "object" ? globalThis : this,
  function createReasoningEngine(ruleEngine) {
  "use strict";

  if (!ruleEngine) {
    throw new Error("DecisionMed reasoning rule engine is unavailable");
  }

  const VERSION = "0.6.0";
  const ENTITY_TYPE_LABELS = Object.freeze({
    manifestation: "Manifestação",
    clinical_context: "Contexto clínico",
    initial_syndrome: "Síndrome clínica inicial",
    clinical_presentation: "Apresentação clínica em investigação",
    standardized_syndrome: "Síndrome padronizada",
    diagnosis: "Diagnóstico",
    risk_condition: "Condição de risco",
  });
  let EXTERNAL_IDENTITIES = new Map();
  let MODULE_ID_TO_LEGACY = new Map();
  let EXTERNAL_CONTENT = new Map();
  let EXTERNAL_MODULES = [];
  let EXTERNAL_CONTENT_BY_MODULE = new Map();
  let CLINICAL_RULES = Object.freeze([]);
  const SPECIALTY_MODULE_GROUP = Object.freeze({
    cardiology: "cardiology",
    pulmonology: "pulmonology",
    neurology: "neurology",
    gastroenterology: "abdominal",
    hepatology: "abdominal",
    nephrology: "urology",
    urology: "urology",
    endocrinology: "endocrinology",
    "infectious-diseases": "generalmedicine",
    rheumatology: "rheumatology",
    hematology: "generalmedicine",
    dermatology: "dermatology",
    psychiatry: "psychiatry",
    gynecology: "gynecology",
    obstetrics: "obstetrics",
    pediatrics: "generalmedicine",
    orthopedics: "orthopedics",
    emergency: "generalmedicine",
    trauma: "orthopedics",
    ophthalmology: "ophthalmology",
    "internal-medicine": "generalmedicine",
  });
  const LEGACY_MODULE_IDS = Object.freeze({
    cardiovascular_discomfort:
      "module.cardiology.acute-thoracic-syndrome",
    respiratory: "module.pulmonology.dyspnea-presentation",
    focal_neurologic:
      "module.neurology.acute-focal-neurological-deficit",
    abdominal:
      "module.gastroenterology.acute-abdominal-pain-presentation",
    lower_urinary_tract: "module.urology.lower-urinary-tract-symptoms",
    metabolic_endocrine:
      "module.endocrinology.metabolic-endocrine-change",
    systemic_inflammatory:
      "module.rheumatology.systemic-inflammatory-disease-suspicion",
    cutaneous: "module.dermatology.skin-lesion-presentation",
    mental_health: "module.psychiatry.mood-sleep-thought-change",
    gynecologic_pelvic:
      "module.gynecology.pelvic-gynecologic-change",
    obstetric: "module.obstetrics.obstetric-signs-symptoms",
    musculoskeletal:
      "module.orthopedics.musculoskeletal-presentation",
    visual: "module.ophthalmology.visual-ocular-change",
    general_unclassified:
      "module.internal-medicine.unclassified-clinical-presentation",
  });
  const NEGATIVE_VALUES = new Set([
    "Não",
    "Nunca",
    "Nenhum",
    "Nenhuma",
    "Não se aplica",
    "Não sabe informar",
    "Nada percebido",
    "Não conhece alergia",
    "Sem mudança",
    "Sem tosse",
    "Normal",
  ]);

  const SYNDROME_DEFINITIONS = Object.freeze([
    {
      key: "cardiovascular_discomfort",
      name: "Síndrome torácica aguda",
      entityType: "initial_syndrome",
      modules: ["cardiology"],
      anchorValues: ["Peito", "Braço / ombro", "Pescoço / mandíbula", "Aperto / pressão", "Peso / desconforto", "Esforço piora", "Suor frio", "Falta de ar"],
      likely: [
        "Síndrome coronariana aguda (SCA)",
        "Isquemia miocárdica sem infarto: angina; ANOCA/INOCA conforme investigação",
        "Pericardite aguda",
      ],
      cannotMiss: [
        "Dissecção aguda de aorta",
        "Embolia pulmonar",
        "Tamponamento cardíaco",
        "Pneumotórax hipertensivo",
      ],
      mimics: [
        "Dor musculoesquelética da parede torácica",
        "Doença esofágica",
        "Ansiedade ou síndrome de hiperventilação",
      ],
      exam: ["Sinais vitais completos e estado geral", "Ausculta cardíaca e pulmonar", "Pulsos periféricos e simetria", "Reprodução do desconforto à palpação ou ao movimento"],
      tests: [
        ["ECG de 12 derivações", "Identificar isquemia, lesão ou alteração do ritmo; comparar com traçados prévios e repetir se a suspeita persistir.", "Exame inicial na suspeita cardiovascular aguda. Não deve atrasar encaminhamento quando houver instabilidade."],
        ["Troponina cardíaca de alta sensibilidade seriada", "Detectar elevação ou variação compatível com lesão miocárdica usando o protocolo validado pelo serviço.", "Interpretar em série e junto com sintomas, tempo de início e ECG; elevação isolada não define a causa."],
        ["Ecocardiograma transtorácico dirigido", "Avaliar alteração de movimento da parede, função ventricular e diagnósticos estruturais alternativos.", "Condicional quando ECG não é diagnóstico, há instabilidade ou a avaliação clínica sugere alteração estrutural."],
      ],
      discriminators: [
        { id: "discriminator.cardiovascular.current", text: "O desconforto está presente agora?", options: ["Não está presente", "Presente e estável", "Presente e piorando", "Não sabe informar"] },
        { id: "discriminator.cardiovascular.duration", text: "Quanto dura cada episódio?", options: ["Segundos", "Menos de 5 minutos", "5 a 20 minutos", "Mais de 20 minutos", "Contínuo por horas", "Não sabe informar"] },
        { id: "discriminator.cardiovascular.reproducible", text: "O desconforto é reproduzido ao apertar o local ou movimentar o membro?", options: ["Não", "Ao apertar o local", "Ao movimentar", "Das duas formas", "Não foi verificado"] },
        { id: "discriminator.cardiovascular.pleuritic", text: "O desconforto piora ao respirar fundo ou tossir?", options: ["Não", "Ao respirar fundo", "Ao tossir", "Nas duas situações", "Não sabe informar"] },
      ],
    },
    {
      key: "respiratory",
      name: "Dispneia ou sintomas respiratórios em investigação",
      entityType: "clinical_presentation",
      modules: ["pulmonology"],
      anchorValues: ["Falta de ar", "Tosse", "Respiratória", "Respiração", "Ao esforço", "Em repouso", "Catarro com sangue"],
      likely: ["Doença obstrutiva de vias aéreas", "Infecção respiratória", "Congestão pulmonar conforme contexto"],
      cannotMiss: ["Insuficiência respiratória aguda", "Embolia pulmonar", "Pneumotórax", "Infecção respiratória grave"],
      mimics: ["Causa cardiovascular", "Anemia ou alteração metabólica", "Ansiedade ou hiperventilação"],
      exam: ["Frequência respiratória, saturação e esforço respiratório", "Capacidade de falar frases completas", "Ausculta pulmonar", "Sinais de congestão, trombose ou assimetria torácica"],
      tests: [
        ["Oximetria", "Quantificar oxigenação e acompanhar gravidade."],
        ["Imagem do tórax", "Investigar infiltrado, congestão, pneumotórax ou outra alteração estrutural."],
        ["Exames laboratoriais dirigidos", "Investigar infecção, anemia ou alteração metabólica conforme hipóteses."],
      ],
      discriminators: [
        { id: "discriminator.respiratory.speech", text: "Consegue falar frases completas sem parar para respirar?", options: ["Sim", "Precisa fazer pausas", "Não consegue", "Não foi observado"] },
        { id: "discriminator.respiratory.sudden", text: "A falta de ar atingiu intensidade máxima em poucos minutos?", options: ["Não", "Sim", "Não sabe informar"] },
        { id: "discriminator.respiratory.position", text: "Piora ao deitar ou acorda durante a noite com falta de ar?", options: ["Não", "Piora ao deitar", "Acorda durante a noite", "Ambos", "Não sabe informar"] },
      ],
    },
    {
      key: "focal_neurologic",
      name: "Déficit neurológico focal agudo",
      entityType: "clinical_presentation",
      modules: ["neurology"],
      anchorValues: ["Perda de força", "Alteração da fala", "Confusão", "Formigamento", "De repente"],
      likely: ["Evento vascular cerebral", "Crise epiléptica com déficit pós-ictal", "Enxaqueca com manifestação neurológica"],
      cannotMiss: ["Acidente vascular cerebral isquêmico ou hemorrágico", "Hemorragia intracraniana", "Infecção ou compressão aguda do sistema nervoso"],
      mimics: ["Hipoglicemia ou alteração metabólica", "Paralisia periférica", "Transtorno neurológico funcional"],
      exam: ["Sinais vitais e glicemia capilar", "Nível de consciência", "Face, fala, força, sensibilidade e coordenação", "Marcha e sinais meníngeos quando seguros e indicados"],
      tests: [
        ["Glicemia imediata", "Excluir alteração glicêmica que possa imitar déficit neurológico."],
        ["Neuroimagem", "Diferenciar causas estruturais, isquêmicas e hemorrágicas."],
        ["Avaliação vascular e cardíaca dirigida", "Investigar mecanismo conforme apresentação."],
      ],
      discriminators: [
        { id: "discriminator.neurologic.persistence", text: "A alteração neurológica ainda está presente?", options: ["Não, resolveu completamente", "Melhorou, mas persiste", "Permanece igual", "Está piorando", "Não sabe informar"] },
        { id: "discriminator.neurologic.side", text: "A alteração predomina em um lado do corpo?", options: ["Não", "Lado direito", "Lado esquerdo", "Não foi possível avaliar"] },
        { id: "discriminator.neurologic.face_speech", text: "Houve assimetria da face ou dificuldade para falar?", options: ["Não", "Assimetria da face", "Dificuldade para falar", "Ambas", "Não sabe informar"] },
      ],
    },
    {
      key: "lower_urinary_tract",
      name: "Sintomas do trato urinário inferior (STUI)",
      entityType: "clinical_presentation",
      modules: ["urology"],
      anchorValues: ["Dor / ardência", "Maior frequência", "Urgência", "Sangue", "Jato fraco", "Perda de urina", "Urina", "Urinária"],
      likely: ["Infecção urinária baixa", "Síndrome obstrutiva urinária", "Litíase urinária conforme padrão da dor"],
      cannotMiss: ["Infecção urinária alta ou complicada", "Obstrução urinária aguda", "Sangramento urinário relevante"],
      mimics: ["Infecção genital ou uretral", "Dor pélvica não urinária", "Irritação química ou medicamentosa"],
      exam: ["Sinais vitais e hidratação", "Exame abdominal e suprapúbico", "Punho-percussão lombar", "Exame genital ou pélvico somente quando indicado e consentido"],
      tests: [
        ["Urina tipo 1", "Investigar inflamação, sangue, glicose e outros achados urinários."],
        ["Cultura de urina", "Identificar agente quando indicada pelo contexto clínico."],
        ["Imagem do trato urinário", "Investigar obstrução, cálculo ou alteração estrutural quando indicada."],
      ],
      discriminators: [
        { id: "discriminator.urinary.fever_flank", text: "Há febre, calafrios ou dor forte nas costas/lateral do abdome?", options: ["Não", "Febre ou calafrios", "Dor nas costas/lateral", "Ambos", "Não sabe informar"] },
        { id: "discriminator.urinary.retention", text: "Consegue urinar ou sente a bexiga cheia sem conseguir esvaziar?", options: ["Urina normalmente", "Urina pouco", "Não consegue urinar", "Não sabe informar"] },
        { id: "discriminator.urinary.genital", text: "Há corrimento, ferida ou dor genital associada?", options: ["Não", "Corrimento", "Ferida", "Dor genital", "Mais de um", "Não sabe informar"] },
      ],
    },
    {
      key: "abdominal",
      name: "Dor abdominal ou alteração gastrointestinal em investigação",
      entityType: "clinical_presentation",
      modules: ["abdominal", "coloproctology"],
      anchorValues: ["Abdome superior", "Abdome inferior", "Náusea / vômito", "Diarreia", "Intestino preso", "Sangue nas fezes", "Intestino"],
      likely: ["Síndrome gastrointestinal inflamatória ou infecciosa", "Doença ácido-péptica, biliar ou pancreática conforme localização", "Alteração funcional ou do trânsito intestinal"],
      cannotMiss: ["Abdome agudo inflamatório ou perfurativo", "Obstrução intestinal", "Hemorragia digestiva", "Isquemia abdominal"],
      mimics: ["Causa urinária", "Causa ginecológica ou obstétrica", "Manifestação cardiovascular em abdome superior"],
      exam: ["Sinais vitais, hidratação e perfusão", "Inspeção, ausculta e palpação abdominal", "Pesquisa de defesa, rigidez e dor à descompressão", "Exame retal ou pélvico somente quando indicado e consentido"],
      tests: [
        ["Laboratório dirigido", "Investigar inflamação, anemia, função orgânica ou distúrbio metabólico."],
        ["Imagem abdominal dirigida", "Investigar inflamação, obstrução, cálculo ou alteração estrutural."],
        ["Pesquisa de sangramento", "Caracterizar e quantificar possível perda digestiva."],
      ],
      discriminators: [
        { id: "discriminator.abdominal.peritoneal", text: "A dor piora muito ao se mover, tossir ou quando o abdome é tocado?", options: ["Não", "Ao se mover", "Ao tossir", "Ao tocar", "Em mais de uma situação", "Não sabe informar"] },
        { id: "discriminator.abdominal.transit", text: "Consegue eliminar gases e evacuar?", options: ["Sim", "Não elimina gases", "Não evacua", "Não elimina gases nem evacua", "Não sabe informar"] },
        { id: "discriminator.abdominal.bleeding", text: "Como é o sangramento digestivo observado?", options: ["Não houve", "Vermelho vivo nas fezes", "Fezes negras", "Vômito com sangue", "Não sabe informar"] },
      ],
    },
    {
      key: "cutaneous",
      name: "Lesão cutânea em investigação",
      entityType: "clinical_presentation",
      modules: ["dermatology"],
      anchorValues: ["Pele", "Mancha", "Caroço", "Bolha", "Ferida", "Descamação", "Coceira", "Secreção"],
      likely: ["Dermatose inflamatória ou alérgica", "Infecção cutânea", "Lesão proliferativa ou pigmentada"],
      cannotMiss: ["Infecção cutânea rapidamente progressiva", "Reação mucocutânea grave", "Lesão suspeita de malignidade"],
      mimics: ["Manifestação cutânea de doença sistêmica", "Reação medicamentosa", "Lesão traumática ou vascular"],
      exam: ["Distribuição, simetria e extensão", "Cor, bordas, superfície e evolução", "Dor, calor, flutuação e secreção", "Mucosas, unhas e cabelos quando relacionados"],
      tests: [
        ["Dermatoscopia ou registro fotográfico clínico", "Documentar características e evolução quando indicado."],
        ["Coleta microbiológica", "Investigar agente infeccioso quando houver indicação."],
        ["Biópsia", "Esclarecer lesão persistente, atípica ou suspeita."],
      ],
      discriminators: [
        { id: "discriminator.skin.spread", text: "A alteração está se espalhando rapidamente?", options: ["Não", "Sim, em horas", "Sim, em dias", "Não sabe informar"] },
        { id: "discriminator.skin.mucosa", text: "Há feridas na boca, olhos ou genitais?", options: ["Não", "Boca", "Olhos", "Genitais", "Mais de um local", "Não sabe informar"] },
        { id: "discriminator.skin.systemic", text: "A lesão veio acompanhada de febre ou mal-estar importante?", options: ["Não", "Febre", "Mal-estar importante", "Ambos", "Não sabe informar"] },
      ],
    },
    {
      key: "visual",
      name: "Alteração visual ou ocular em investigação",
      entityType: "clinical_presentation",
      modules: ["ophthalmology"],
      anchorValues: ["Visão", "Olhos", "Perda de visão", "Visão dupla", "Manchas / flashes", "Dor ocular", "Olho vermelho"],
      likely: ["Alteração refrativa ou da superfície ocular", "Alteração retiniana ou vítrea", "Inflamação ocular"],
      cannotMiss: ["Perda visual aguda de causa vascular ou retiniana", "Glaucoma agudo", "Infecção ou trauma ocular grave"],
      mimics: ["Enxaqueca com fenômeno visual", "Alteração neurológica central", "Efeito medicamentoso ou metabólico"],
      exam: ["Acuidade visual de cada olho", "Pupilas, motilidade e campos visuais", "Inspeção externa e biomicroscopia quando disponível", "Pressão intraocular e fundo de olho quando indicados"],
      tests: [
        ["Avaliação oftalmológica dirigida", "Localizar a alteração em superfície, segmento anterior, retina ou nervo óptico."],
        ["Imagem ocular ou de órbita", "Investigar alteração estrutural selecionada pelo exame."],
        ["Avaliação neurológica", "Investigar origem central quando o padrão exigir."],
      ],
      discriminators: [
        { id: "discriminator.visual.eye", text: "A alteração ocorre em um olho ou nos dois?", options: ["Um olho", "Os dois olhos", "Não sabe informar"] },
        { id: "discriminator.visual.loss", text: "Houve perda súbita de visão ou sensação de cortina?", options: ["Não", "Perda súbita", "Sensação de cortina", "Ambas", "Não sabe informar"] },
        { id: "discriminator.visual.pain_redness", text: "Há dor ocular intensa acompanhada de olho vermelho?", options: ["Não", "Dor sem vermelhidão", "Vermelhidão sem dor", "Dor e vermelhidão", "Não sabe informar"] },
      ],
    },
    {
      key: "musculoskeletal",
      name: "Quadro musculoesquelético em investigação",
      entityType: "clinical_presentation",
      modules: ["orthopedics"],
      anchorValues: ["Articulação específica", "Trauma / queda", "Movimento piora", "Rigidez", "Limitação de movimento", "Inchaço"],
      likely: ["Lesão musculotendínea ou ligamentar", "Síndrome articular mecânica", "Fratura ou contusão conforme trauma"],
      cannotMiss: ["Fratura instável ou luxação", "Comprometimento neurovascular", "Infecção articular"],
      mimics: ["Dor referida de origem cardiovascular ou visceral", "Radiculopatia ou neuropatia", "Doença inflamatória sistêmica"],
      exam: ["Inspeção, deformidade, edema e pele", "Palpação e amplitude de movimento", "Força, sensibilidade, pulsos e perfusão distal", "Capacidade de sustentar peso quando seguro"],
      tests: [
        ["Radiografia dirigida", "Investigar fratura, luxação ou alteração óssea."],
        ["Ultrassonografia ou ressonância", "Investigar partes moles quando o exame justificar."],
        ["Laboratório inflamatório", "Investigar processo infeccioso ou inflamatório quando suspeito."],
      ],
      discriminators: [
        { id: "discriminator.musculoskeletal.weight", text: "Consegue apoiar ou usar normalmente o membro afetado?", options: ["Sim", "Com dificuldade", "Não consegue", "Não se aplica"] },
        { id: "discriminator.musculoskeletal.deformity", text: "Há deformidade, extremidade fria ou mudança de cor?", options: ["Não", "Deformidade", "Extremidade fria", "Mudança de cor", "Mais de um", "Não sabe informar"] },
        { id: "discriminator.musculoskeletal.passive", text: "O movimento passivo também provoca dor ou bloqueio?", options: ["Não", "Dor", "Bloqueio", "Dor e bloqueio", "Não foi examinado"] },
      ],
    },
    {
      key: "gynecologic_pelvic",
      name: "Dor pélvica ou alteração ginecológica em investigação",
      entityType: "clinical_presentation",
      modules: ["gynecology"],
      anchorValues: ["Ginecológica", "Sangramento fora do período", "Dor pélvica", "Corrimento / coceira", "Dor na relação", "Alteração menstrual"],
      likely: ["Sangramento uterino anormal", "Síndrome infecciosa genital ou pélvica", "Condição estrutural ginecológica"],
      cannotMiss: ["Gestação ectópica", "Hemorragia ginecológica importante", "Torção anexial", "Infecção pélvica grave"],
      mimics: ["Causa urinária", "Causa gastrointestinal", "Alteração hormonal ou medicamentosa"],
      exam: ["Sinais vitais e repercussão do sangramento", "Exame abdominal", "Exame ginecológico somente com indicação, consentimento e privacidade", "Caracterização objetiva do sangramento"],
      tests: [
        ["Teste de gestação", "Definir se causas relacionadas à gestação precisam ser priorizadas."],
        ["Hemograma", "Avaliar repercussão hematológica quando houver sangramento."],
        ["Ultrassonografia pélvica", "Investigar causas estruturais conforme contexto."],
      ],
      discriminators: [
        { id: "discriminator.gynecology.pregnancy", text: "Existe possibilidade de gestação?", options: ["Não", "Sim", "Gestação confirmada", "Não sabe informar"] },
        { id: "discriminator.gynecology.bleeding", text: "Qual é a intensidade do sangramento?", options: ["Não está sangrando", "Pequena quantidade", "Quantidade moderada", "Grande quantidade ou encharca absorventes", "Não sabe informar"] },
        { id: "discriminator.gynecology.instability", text: "O sangramento está associado a tontura, desmaio ou fraqueza intensa?", options: ["Não", "Tontura", "Desmaio", "Fraqueza intensa", "Mais de um", "Não sabe informar"] },
      ],
    },
    {
      key: "obstetric",
      name: "Sinais e sintomas obstétricos em investigação",
      entityType: "clinical_presentation",
      modules: ["obstetrics"],
      anchorValues: ["Gestação confirmada", "Suspeita de gestação", "Sangramento", "Dor pélvica", "Até 6 semanas após o parto"],
      likely: ["Alteração própria da gestação que necessita caracterização", "Síndrome gastrointestinal ou urinária associada à gestação", "Complicação hipertensiva conforme sinais associados"],
      cannotMiss: ["Gestação ectópica", "Hemorragia obstétrica", "Doença hipertensiva grave da gestação", "Infecção obstétrica"],
      mimics: ["Condição ginecológica não obstétrica", "Causa urinária", "Causa gastrointestinal"],
      exam: ["Sinais vitais, perfusão e estado geral", "Exame abdominal e obstétrico conforme idade gestacional", "Avaliação de sangramento e perda de líquido", "Avaliação fetal quando aplicável e disponível"],
      tests: [
        ["Confirmação e localização da gestação", "Definir presença, localização e evolução conforme contexto."],
        ["Hemograma e exames dirigidos", "Avaliar sangramento, infecção ou complicação hipertensiva."],
        ["Ultrassonografia obstétrica", "Responder à pergunta clínica definida pela avaliação."],
      ],
      discriminators: [
        { id: "discriminator.obstetric.stage", text: "Qual é a idade gestacional ou o tempo desde o parto?", options: ["Até 12 semanas", "13 a 27 semanas", "28 semanas ou mais", "Até 6 semanas após o parto", "Não sabe informar"] },
        { id: "discriminator.obstetric.bleeding", text: "Há sangramento, perda de líquido ou dor abdominal forte?", options: ["Não", "Sangramento", "Perda de líquido", "Dor abdominal forte", "Mais de um", "Não sabe informar"] },
        { id: "discriminator.obstetric.neuro", text: "Há dor de cabeça forte, alteração visual ou pressão muito elevada?", options: ["Não", "Dor de cabeça forte", "Alteração visual", "Pressão muito elevada", "Mais de um", "Não sabe informar"] },
      ],
    },
    {
      key: "metabolic_endocrine",
      name: "Alteração metabólica ou endócrina em investigação",
      entityType: "clinical_presentation",
      modules: ["endocrinology"],
      anchorValues: ["Perda de peso", "Cansaço importante", "Perdeu peso", "Ganhou peso", "Urina muito", "muita sede", "Palpitação", "tremor"],
      likely: ["Alteração glicêmica", "Disfunção tireoidiana", "Alteração hormonal ou metabólica sistêmica"],
      cannotMiss: ["Descompensação glicêmica aguda", "Crise tireotóxica ou insuficiência endócrina aguda", "Distúrbio hidroeletrolítico importante"],
      mimics: ["Infecção crônica", "Doença neoplásica", "Efeito medicamentoso", "Transtorno do humor ou do sono"],
      exam: ["Sinais vitais, hidratação e estado mental", "Peso, composição corporal e tendência temporal", "Tireoide, pele, pelos e tremor", "Sinais de alteração metabólica sistêmica"],
      tests: [
        ["Glicemia e avaliação metabólica", "Investigar alteração glicêmica e repercussões."],
        ["Função tireoidiana", "Investigar padrão de hipo ou hipertireoidismo."],
        ["Exames hormonais dirigidos", "Responder somente a uma hipótese clínica definida."],
      ],
      discriminators: [
        { id: "discriminator.endocrine.glucose", text: "Há muita sede, aumento importante da urina ou visão embaçada?", options: ["Não", "Muita sede", "Aumento da urina", "Visão embaçada", "Mais de um", "Não sabe informar"] },
        { id: "discriminator.endocrine.thyroid", text: "Predomina intolerância ao calor, ao frio, tremor ou alteração intestinal?", options: ["Nenhum", "Intolerância ao calor", "Intolerância ao frio", "Tremor", "Alteração intestinal", "Mais de um"] },
        { id: "discriminator.endocrine.medication", text: "Usa hormônio, corticoide ou suplemento capaz de interferir nesses sintomas?", options: ["Não", "Hormônio", "Corticoide", "Suplemento", "Não sabe informar"], detailOnPositive: true, detailRequired: true },
      ],
    },
    {
      key: "systemic_inflammatory",
      name: "Suspeita de doença inflamatória sistêmica ou vasculite",
      entityType: "clinical_presentation",
      modules: ["rheumatology"],
      anchorValues: ["Febre", "Perda de peso", "Suor noturno", "Pele", "Urinária", "Respiratória", "aftas"],
      likely: ["Processo infeccioso sistêmico", "Doença inflamatória ou autoimune", "Reação medicamentosa ou exposição sistêmica"],
      cannotMiss: ["Sepse ou infecção invasiva", "Vasculite com comprometimento de órgão", "Doença hematológica ou neoplásica"],
      mimics: ["Doença endócrina ou metabólica", "Infecção localizada", "Condição autolimitada"],
      exam: ["Sinais vitais e perfusão", "Pele, mucosas e articulações", "Avaliação respiratória, renal e neurológica", "Pesquisa de linfonodos e aumento de órgãos conforme contexto"],
      tests: [
        ["Hemograma e marcadores inflamatórios", "Caracterizar resposta sistêmica e citopenias."],
        ["Função renal, urina e função hepática", "Pesquisar comprometimento de órgãos."],
        ["Testes etiológicos dirigidos", "Investigar infecção, inflamação ou autoimunidade somente após definir hipóteses."],
      ],
      discriminators: [
        { id: "discriminator.systemic.organ", text: "Além dos sintomas gerais, qual órgão ou sistema parece mais afetado?", options: ["Nenhum definido", "Pele", "Articulações", "Respiração", "Urina/rins", "Sistema nervoso", "Mais de um"] },
        { id: "discriminator.systemic.exposure", text: "Houve infecção recente, viagem, medicamento novo ou exposição relevante?", options: ["Não", "Infecção recente", "Viagem", "Medicamento novo", "Outra exposição", "Não sabe informar"], detailOnPositive: true, detailRequired: true },
        { id: "discriminator.systemic.course", text: "Os sintomas gerais estão progredindo?", options: ["Melhorando", "Estáveis", "Piorando", "Oscilando", "Não sabe informar"] },
      ],
    },
    {
      key: "mental_health",
      name: "Alteração do humor, sono ou pensamento em investigação",
      entityType: "clinical_presentation",
      modules: ["psychiatry"],
      anchorValues: ["Ansiedade / preocupação", "Humor deprimido", "Irritabilidade", "Insônia", "Pensamentos repetitivos", "Memória / atenção"],
      likely: ["Síndrome ansiosa", "Síndrome depressiva", "Transtorno relacionado ao sono ou ao estresse"],
      cannotMiss: ["Risco de autoagressão ou suicídio", "Síndrome maniforme", "Psicose aguda", "Delirium, intoxicação ou abstinência"],
      mimics: ["Doença endócrina ou metabólica", "Efeito medicamentoso ou de substância", "Doença neurológica"],
      exam: ["Estado mental e nível de consciência", "Humor, pensamento, percepção e crítica", "Avaliação estruturada de risco de autoagressão e violência", "Sinais de intoxicação, abstinência ou causa orgânica"],
      tests: [
        ["Avaliação clínica e escalas validadas", "Quantificar sintomas sem substituir entrevista clínica."],
        ["Exames para causas orgânicas", "Investigar somente quando história ou exame sugerirem causa médica."],
        ["Avaliação toxicológica dirigida", "Investigar exposição quando clinicamente indicada."],
      ],
      discriminators: [
        { id: "discriminator.mental.self_harm", text: "Teve pensamentos de se machucar, morrer ou não querer continuar vivo?", options: ["Não", "Pensamento sem plano", "Pensamento com plano", "Tentativa recente", "Prefere não responder"] },
        { id: "discriminator.mental.mania", text: "Teve período de energia muito aumentada, pouca necessidade de sono e comportamento fora do habitual?", options: ["Não", "Sim", "Não sabe informar"], detailOnPositive: true, detailRequired: true },
        { id: "discriminator.mental.psychosis", text: "Percebeu vozes, visões ou crenças que outras pessoas não compartilham?", options: ["Não", "Sim", "Não sabe informar"], detailOnPositive: true, detailRequired: true },
      ],
    },
    {
      key: "general_unclassified",
      name: "Quadro clínico ainda não classificado",
      entityType: "clinical_presentation",
      modules: ["generalmedicine"],
      anchorValues: [],
      likely: ["Condição clínica inespecífica ainda em caracterização"],
      cannotMiss: ["Condição aguda tempo-dependente definida por sinais de alarme"],
      mimics: ["Efeito medicamentoso", "Alteração metabólica", "Manifestação inicial de doença sistêmica"],
      exam: ["Sinais vitais e estado geral", "Exame físico completo orientado pela queixa", "Hidratação, perfusão e nível de consciência"],
      tests: [["Exames dirigidos pela representação do problema", "Evitar investigação ampla sem pergunta clínica definida."]],
      discriminators: [
        { id: "discriminator.general.function", text: "O problema impede alimentação, hidratação, locomoção ou atividades habituais?", options: ["Não", "Alimentação", "Hidratação", "Locomoção", "Atividades habituais", "Mais de uma"] },
        { id: "discriminator.general.progression", text: "Houve piora importante nas últimas horas?", options: ["Não", "Sim", "Não sabe informar"] },
        { id: "discriminator.general.missing", text: "Existe algum sintoma importante que ainda não foi registrado?", options: ["Não", "Sim"], detailOnPositive: true, detailRequired: true },
      ],
    },
  ]);

  function normalizeText(value) {
    return String(value || "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLocaleLowerCase("pt-BR");
  }

  function identityFor(definition) {
    if (definition.externalIdentity) return definition.externalIdentity;
    return (
      EXTERNAL_IDENTITIES.get(definition.key) || {
        moduleId: LEGACY_MODULE_IDS[definition.key] || null,
        name: definition.name,
        entityType: definition.entityType,
        entityTypeLabel: ENTITY_TYPE_LABELS[definition.entityType],
        version: VERSION,
        status: "local_prototype",
        terminologyStatus: "candidate",
        contentStatus: "partial",
        sourceIds: [],
      }
    );
  }

  function contentFor(definition) {
    return EXTERNAL_CONTENT.get(definition.key) || definition;
  }

  function runtimeDefinitions() {
    if (!EXTERNAL_MODULES.length) {
      return SYNDROME_DEFINITIONS.map(contentFor);
    }
    const localByKey = new Map(
      SYNDROME_DEFINITIONS.map((definition) => [definition.key, definition]),
    );
    return EXTERNAL_MODULES.map((identity) => {
      const legacyKey = identity.legacyKeys.find((key) => localByKey.has(key));
      const local = legacyKey ? contentFor(localByKey.get(legacyKey)) : null;
      const content = EXTERNAL_CONTENT_BY_MODULE.get(identity.moduleId);
      const modules = local
        ? [...local.modules]
        : [
            SPECIALTY_MODULE_GROUP[identity.primarySpecialty] ||
              "generalmedicine",
          ];
      const discriminators = content?.discriminators || local?.discriminators || [];
      const tests = content?.tests || local?.tests || [];
      return Object.freeze({
        key: legacyKey || identity.moduleId,
        moduleId: identity.moduleId,
        name: identity.name,
        entityType: identity.entityType,
        modules: Object.freeze(modules),
        anchorValues: Object.freeze([
          ...(content?.anchorValues || local?.anchorValues || []),
        ]),
        likely: Object.freeze([
          ...(content?.likely || local?.likely || [identity.name]),
        ]),
        cannotMiss: Object.freeze([
          ...(content?.cannotMiss || local?.cannotMiss || []),
        ]),
        mimics: Object.freeze([
          ...(content?.mimics || local?.mimics || []),
        ]),
        discriminators: Object.freeze([...discriminators]),
        exam: Object.freeze([...(content?.exam || local?.exam || [])]),
        tests: Object.freeze([...tests]),
        definition: content?.definition || null,
        boundaries: content?.boundaries || null,
        requiredManifestations: Object.freeze([
          ...(content?.requiredManifestations || []),
        ]),
        frequentManifestations: Object.freeze([
          ...(content?.frequentManifestations || []),
        ]),
        atypicalManifestations: Object.freeze([
          ...(content?.atypicalManifestations || []),
        ]),
        contraryFindings: Object.freeze([
          ...(content?.contraryFindings || []),
        ]),
        riskFactors: Object.freeze([...(content?.riskFactors || [])]),
        redFlags: Object.freeze([...(content?.redFlags || [])]),
        stopConditions: Object.freeze([...(content?.stopConditions || [])]),
        diagnosticCriteria: Object.freeze([
          ...(content?.diagnosticCriteria || []),
        ]),
        postExamReassessment: Object.freeze([
          ...(content?.postExamReassessment || []),
        ]),
        safetyConduct: Object.freeze([...(content?.safetyConduct || [])]),
        initialTreatment: Object.freeze([
          ...(content?.initialTreatment || []),
        ]),
        definitiveTreatment: Object.freeze([
          ...(content?.definitiveTreatment || []),
        ]),
        destinationReturnFollowup: Object.freeze([
          ...(content?.destinationReturnFollowup || []),
        ]),
        contentVersion: content?.contentVersion || null,
        contentRecordStatus:
          content?.contentRecordStatus || "catalog_without_content",
        externalContentStatus:
          content?.externalContentStatus || identity.contentStatus,
        contentSourceIds: Object.freeze([
          ...(content?.contentSourceIds || []),
        ]),
        externalIdentity: identity,
        isLegacyDefinition: Boolean(legacyKey),
      });
    });
  }

  function configureCatalog(items = []) {
    if (!Array.isArray(items)) {
      throw new TypeError("catalog items must be an array");
    }
    const knownKeys = new Set(
      SYNDROME_DEFINITIONS.map((definition) => definition.key),
    );
    const next = new Map();
    const moduleIds = new Map();
    const externalModules = [];
    for (const item of items) {
      if (!item || typeof item !== "object") continue;
      const legacyKeys = Array.isArray(item.legacy_keys) ? item.legacy_keys : [];
      if (
        typeof item.module_id !== "string" ||
        typeof item.display_name !== "string" ||
        typeof item.entity_type !== "string" ||
        !ENTITY_TYPE_LABELS[item.entity_type]
      ) {
        continue;
      }
      const identity = Object.freeze({
        moduleId: item.module_id,
        name: item.display_name,
        entityType: item.entity_type,
        entityTypeLabel: ENTITY_TYPE_LABELS[item.entity_type],
        primarySpecialty:
          typeof item.primary_specialty === "string"
            ? item.primary_specialty
            : "internal-medicine",
        version: typeof item.version === "string" ? item.version : "unknown",
        status: typeof item.status === "string" ? item.status : "unknown",
        terminologyStatus:
          typeof item.terminology_status === "string"
            ? item.terminology_status
            : "unknown",
        contentStatus:
          typeof item.content_status === "string"
            ? item.content_status
            : "unknown",
        sourceIds: Object.freeze(
          Array.isArray(item.sources)
            ? item.sources
                .map((source) => source?.source_id)
                .filter((sourceId) => typeof sourceId === "string")
            : [],
        ),
        legacyKeys: Object.freeze([...legacyKeys]),
      });
      externalModules.push(identity);
      for (const legacyKey of legacyKeys) {
        if (!knownKeys.has(legacyKey) || next.has(legacyKey)) continue;
        next.set(legacyKey, identity);
        moduleIds.set(item.module_id, legacyKey);
      }
    }
    EXTERNAL_IDENTITIES = next;
    MODULE_ID_TO_LEGACY = moduleIds;
    EXTERNAL_MODULES = Object.freeze(externalModules);
    EXTERNAL_CONTENT = new Map(
      [...EXTERNAL_CONTENT].filter(([legacyKey]) => next.has(legacyKey)),
    );
    EXTERNAL_CONTENT_BY_MODULE = new Map(
      [...EXTERNAL_CONTENT_BY_MODULE].filter(([moduleId]) =>
        externalModules.some((item) => item.moduleId === moduleId),
      ),
    );
    return Object.freeze({
      matched: next.size,
      expected: SYNDROME_DEFINITIONS.length,
      catalogCount: externalModules.length,
      complete:
        next.size === SYNDROME_DEFINITIONS.length &&
        (externalModules.length === 0 || externalModules.length === 300),
    });
  }

  function configureContent(items = []) {
    if (!Array.isArray(items)) {
      throw new TypeError("clinical content items must be an array");
    }
    const localByKey = new Map(
      SYNDROME_DEFINITIONS.map((definition) => [definition.key, definition]),
    );
    const next = new Map();
    const byModule = new Map();
    for (const item of items) {
      if (!item || typeof item !== "object") continue;
      const legacyKey = MODULE_ID_TO_LEGACY.get(item.module_id);
      const local = localByKey.get(legacyKey);
      const arrays = [
        "anchor_values",
        "likely_hypotheses",
        "cannot_miss_hypotheses",
        "mimics",
        "discriminators",
        "physical_examination",
        "complementary_exams",
        "source_ids",
      ];
      if (
        typeof item.module_id !== "string" ||
        typeof item.version !== "string" ||
        typeof item.status !== "string" ||
        typeof item.content_status !== "string" ||
        arrays.some((field) => !Array.isArray(item[field]))
      ) {
        continue;
      }
      const discriminators = item.discriminators
        .filter(
          (question) =>
            question &&
            typeof question.question_id === "string" &&
            typeof question.text === "string" &&
            Array.isArray(question.options),
        )
        .map((question) => ({
          id: question.question_id,
          text: question.text,
          options: [...question.options],
          detailOnPositive: question.detail_on_positive === true,
          detailRequired: question.detail_required === true,
          rationale:
            typeof question.rationale === "string"
              ? question.rationale
              : null,
          sourceIds: Array.isArray(question.source_ids)
            ? [...question.source_ids]
            : [],
        }));
      const tests = item.complementary_exams
        .filter(
          (exam) =>
            exam &&
            typeof exam.name === "string" &&
            typeof exam.clinical_question === "string" &&
            typeof exam.when === "string",
        )
        .map((exam) => [
          exam.name,
          exam.clinical_question,
          exam.when,
          exam.exam_id,
          exam.limitations,
          Array.isArray(exam.source_ids) ? [...exam.source_ids] : [],
        ]);
      if (
        discriminators.length !== item.discriminators.length ||
        tests.length !== item.complementary_exams.length
      ) {
        continue;
      }
      const normalized = Object.freeze({
        ...(local || {}),
        definition:
          typeof item.definition === "string" ? item.definition : null,
        boundaries:
          typeof item.boundaries === "string" ? item.boundaries : null,
        anchorValues: Object.freeze([...item.anchor_values]),
        requiredManifestations: Object.freeze([
          ...(item.required_manifestations || []),
        ]),
        frequentManifestations: Object.freeze([
          ...(item.frequent_manifestations || []),
        ]),
        atypicalManifestations: Object.freeze([
          ...(item.atypical_manifestations || []),
        ]),
        contraryFindings: Object.freeze([...(item.contrary_findings || [])]),
        riskFactors: Object.freeze([...(item.risk_factors || [])]),
        redFlags: Object.freeze([...(item.red_flags || [])]),
        stopConditions: Object.freeze([...(item.stop_conditions || [])]),
        likely: Object.freeze([...item.likely_hypotheses]),
        cannotMiss: Object.freeze([...item.cannot_miss_hypotheses]),
        mimics: Object.freeze([...item.mimics]),
        discriminators: Object.freeze(discriminators),
        exam: Object.freeze([...item.physical_examination]),
        tests: Object.freeze(tests),
        diagnosticCriteria: Object.freeze([
          ...(item.diagnostic_criteria || []),
        ]),
        postExamReassessment: Object.freeze([
          ...(item.post_exam_reassessment || []),
        ]),
        safetyConduct: Object.freeze([...(item.safety_conduct || [])]),
        initialTreatment: Object.freeze([...(item.initial_treatment || [])]),
        definitiveTreatment: Object.freeze([
          ...(item.definitive_treatment || []),
        ]),
        destinationReturnFollowup: Object.freeze([
          ...(item.destination_return_followup || []),
        ]),
        contentVersion: item.version,
        contentRecordStatus: item.status,
        externalContentStatus: item.content_status,
        contentSourceIds: Object.freeze([...item.source_ids]),
      });
      byModule.set(item.module_id, normalized);
      if (legacyKey && local && !next.has(legacyKey)) {
        next.set(legacyKey, normalized);
      }
    }
    EXTERNAL_CONTENT = next;
    EXTERNAL_CONTENT_BY_MODULE = byModule;
    const expected = EXTERNAL_MODULES.length || SYNDROME_DEFINITIONS.length;
    return Object.freeze({
      matched: byModule.size || next.size,
      legacyMatched: next.size,
      expected,
      complete:
        next.size === SYNDROME_DEFINITIONS.length &&
        (EXTERNAL_MODULES.length === 0 || byModule.size === EXTERNAL_MODULES.length),
    });
  }

  function configureRules(items = []) {
    if (!Array.isArray(items)) {
      throw new TypeError("clinical rule items must be an array");
    }
    const clinicalRules = items
      .filter(
        (item) =>
          item &&
          ["support", "oppose", "alarm"].includes(item.effect) &&
          typeof item.output_value === "string" &&
          item.output_value.trim(),
      )
      .map((item) => ({
        ruleId: item.rule_id,
        moduleId: item.module_id,
        version: item.version,
        status: item.status,
        effect: item.effect,
        strength: item.strength,
        target: item.output_value,
        priority: item.priority,
        rationale: item.rationale,
        sourceIds: item.source_ids,
        when: item.when,
      }));
    CLINICAL_RULES = ruleEngine.compileRules(clinicalRules);
    return Object.freeze({
      count: CLINICAL_RULES.length,
      support: CLINICAL_RULES.filter((rule) => rule.effect === "support").length,
      oppose: CLINICAL_RULES.filter((rule) => rule.effect === "oppose").length,
      alarm: CLINICAL_RULES.filter((rule) => rule.effect === "alarm").length,
      clinicalExecutionAllowed: false,
    });
  }

  function flattenValues(answers) {
    return answers.flatMap((answer) => answer.values || []);
  }

  function negativeAnswer(answer) {
    return (
      answer.values?.length > 0 &&
      answer.values.every(
        (value) =>
          NEGATIVE_VALUES.has(value) ||
          value.startsWith("Não ") ||
          value.startsWith("Nenhum"),
      )
    );
  }

  function evidenceFor(definition, input) {
    const values = new Set(flattenValues(input.answers));
    const evidence = definition.anchorValues
      .filter((value) => values.has(value))
      .map((value) => `Achado informado: ${value}.`);
    for (const moduleKey of definition.modules) {
      if (input.selectedModules.includes(moduleKey)) {
        evidence.unshift(`Módulo ${moduleKey} selecionado pelo fluxo.`);
        break;
      }
    }
    if (!evidence.length) {
      evidence.push(`Queixa principal em investigação: ${input.complaint}.`);
    }
    // Discriminator answers are not generic evidence for a syndrome. Their
    // direction must be declared by a syndrome-specific rule in
    // differentialFor; otherwise they remain neutral facts in the audit.
    return [...new Set(evidence)].slice(0, 8);
  }

  function evidenceAgainst(definition, input) {
    return input.answers
      .filter(
        (answer) =>
          definition.modules.includes(answer.module) && negativeAnswer(answer),
      )
      .map(
        (answer) =>
          `${answer.question}: ${answer.values.join(", ")}.`,
      )
      .slice(0, 5);
  }

  function compatibility(evidence) {
    if (evidence.length >= 5) return "alto";
    if (evidence.length >= 3) return "intermediário";
    return "baixo";
  }

  function answerFactKey(answerId) {
    return String(answerId || "")
      .replace(/^discriminator\./, "")
      .replace(/[^a-zA-Z0-9]+/g, "_")
      .replace(/^_|_$/g, "");
  }

  function clinicalFacts(input) {
    const answerValues = {};
    for (const answer of input.answers) {
      const key = answerFactKey(answer.id);
      if (key) answerValues[key] = [...(answer.values || [])];
    }
    return {
      complaint: input.complaint,
      values: [...new Set(flattenValues(input.answers))],
      normalizedNote: ruleEngine.normalizeText(input.note),
      normalized_note: ruleEngine.normalizeText(input.note),
      selectedModules: [...input.selectedModules],
      selected_modules: [...input.selectedModules],
      selectedSyndromeKeys: [...input.selectedSyndromeKeys],
      selected_syndrome_keys: [...input.selectedSyndromeKeys],
      answerValues,
      answer_values: answerValues,
    };
  }

  function clinicalRuleMatches(input, effects, moduleId = null) {
    const effectSet = new Set(effects);
    return ruleEngine
      .evaluateRules(CLINICAL_RULES, clinicalFacts(input))
      .filter(
        (match) =>
          effectSet.has(match.effect) &&
          (!moduleId || match.moduleId === moduleId),
      );
  }

  function safetyAssessment(input) {
    if (!CLINICAL_RULES.some((rule) => rule.effect === "alarm")) {
      return {
        level: "immediate",
        label: "Interromper fluxo: regras de segurança indisponíveis",
        reasons: [
          "O catálogo governado de regras de segurança não foi carregado.",
        ],
        ruleIds: [],
        rules: [],
      };
    }
    const matches = clinicalRuleMatches(input, ["alarm"]);
    const critical = matches.filter(
      (match) => match.strength === "critical",
    );
    const reasons = [...new Set(matches.map((match) => match.target))];
    const rules = matches.map((match) => ({
      ruleId: match.ruleId,
      moduleId: match.moduleId,
      version: match.ruleVersion,
      status: match.ruleStatus,
      strength: match.strength,
      rationale: match.rationale,
      sourceIds: [...match.sourceIds],
    }));
    if (critical.length) {
      return {
        level: "immediate",
        label: "Interromper fluxo e buscar avaliação imediata",
        reasons,
        ruleIds: matches.map((match) => match.ruleId),
        rules,
      };
    }
    if (matches.length) {
      return {
        level: "priority",
        label: "Avaliação clínica prioritária",
        reasons,
        ruleIds: matches.map((match) => match.ruleId),
        rules,
      };
    }
    return {
      level: "continue",
      label: "Fluxo pode continuar, mantendo vigilância",
      reasons: [
        "Nenhum sinal de alarme maior foi identificado pelas regras declarativas carregadas.",
      ],
      ruleIds: [],
      rules: [],
    };
  }

  function problemRepresentation(input) {
    const byId = Object.fromEntries(
      input.answers.map((answer) => [answer.id, answer]),
    );
    const take = (id) => byId[id]?.values?.join(" e ");
    const fragments = [`Pessoa com queixa principal de ${input.complaint}`];
    if (take("symptom.started")) fragments.push(`iniciada ${take("symptom.started").toLocaleLowerCase("pt-BR")}`);
    if (take("symptom.onset")) fragments.push(`com início ${take("symptom.onset").toLocaleLowerCase("pt-BR")}`);
    if (take("symptom.location")) fragments.push(`localizada em ${take("symptom.location").toLocaleLowerCase("pt-BR")}`);
    if (take("symptom.quality")) fragments.push(`descrita como ${take("symptom.quality").toLocaleLowerCase("pt-BR")}`);
    if (take("symptom.intensity")) fragments.push(`intensidade ${take("symptom.intensity")}/10`);
    if (take("symptom.modifiers") && !negativeAnswer(byId["symptom.modifiers"])) {
      fragments.push(`com ${take("symptom.modifiers").toLocaleLowerCase("pt-BR")}`);
    }
    if (take("symptom.associated") && !negativeAnswer(byId["symptom.associated"])) {
      fragments.push(`associada a ${take("symptom.associated").toLocaleLowerCase("pt-BR")}`);
    }
    const riskValues = new Set([
      "Hipertensão",
      "Diabetes",
      "Doença cardíaca",
      "Doença pulmonar",
      "Doença renal",
      "Fuma atualmente",
    ]);
    const risks = flattenValues(input.answers).filter((value) => riskValues.has(value));
    if (risks.length) fragments.push(`com antecedentes relevantes de ${[...new Set(risks)].join(", ").toLocaleLowerCase("pt-BR")}`);
    return `${fragments.join(", ")}.`;
  }

  function activeDefinitions(input) {
    const values = new Set(flattenValues(input.answers));
    const definitions = runtimeDefinitions();
    const exact = definitions.filter((definition) =>
      input.selectedSyndromeKeys.includes(definition.key),
    );
    if (exact.length) return exact;
    const selected = definitions.filter(
      (definition) =>
        definition.isLegacyDefinition !== false &&
        definition.modules.some((module) =>
          input.selectedModules.includes(module),
        ),
    );
    if (selected.length) return selected;
    const matched = definitions.filter((definition) =>
      definition.anchorValues.some((value) => values.has(value)),
    );
    return matched.length
      ? matched.slice(0, 3)
      : definitions.filter(
          (definition) => definition.key === "general_unclassified",
        );
  }

  function differentialFor(definition, input) {
    const identity = identityFor(definition);
    const matches = clinicalRuleMatches(
      input,
      ["support", "oppose"],
      identity.moduleId,
    );
    const supported = matches
      .filter((match) => match.effect === "support")
      .map((match) => match.target);
    const opposed = new Set(
      matches
        .filter((match) => match.effect === "oppose")
        .map((match) => match.target),
    );
    const likely = [
      ...supported,
      ...definition.likely.filter((item) => !opposed.has(item)),
    ];
    const cannotMiss = [...definition.cannotMiss];
    const mimics = definition.mimics.filter(
      (item) => !supported.includes(item) && !opposed.has(item),
    );

    return {
      likely: [...new Set(likely)],
      cannotMiss: [...new Set(cannotMiss)],
      mimics: [...new Set(mimics)],
      rules: matches.map((match) => ({
        ruleId: match.ruleId,
        moduleId: match.moduleId,
        version: match.ruleVersion,
        status: match.ruleStatus,
        effect: match.effect,
        strength: match.strength,
        output: match.target,
        rationale: match.rationale,
        sourceIds: [...match.sourceIds],
      })),
    };
  }

  function analyze(input = {}) {
    const normalized = {
      complaint: String(input.complaint || "Sintoma não informado"),
      note: String(input.note || ""),
      answers: Array.isArray(input.answers) ? input.answers : [],
      selectedModules: Array.isArray(input.selectedModules)
        ? input.selectedModules
        : [],
      selectedSyndromeKeys: Array.isArray(input.selectedSyndromeKeys)
        ? input.selectedSyndromeKeys
        : [],
    };
    const syndromes = activeDefinitions(normalized).map((definition) => {
      const supports = evidenceFor(definition, normalized);
      const identity = identityFor(definition);
      return {
        key: definition.key,
        moduleId: identity.moduleId,
        name: identity.name,
        entityType: identity.entityType,
        entityTypeLabel: identity.entityTypeLabel,
        moduleVersion: identity.version,
        moduleStatus: identity.status,
        terminologyStatus: identity.terminologyStatus,
        contentStatus: identity.contentStatus,
        sourceIds: [...identity.sourceIds],
        contentVersion: definition.contentVersion || null,
        contentRecordStatus:
          definition.contentRecordStatus || "local_prototype",
        contentSourceIds: [...(definition.contentSourceIds || [])],
        compatibility: compatibility(supports),
        supports,
        against: evidenceAgainst(definition, normalized),
        alarms: safetyAssessment(normalized).reasons,
        differential: differentialFor(definition, normalized),
        definition: definition.definition || null,
        boundaries: definition.boundaries || null,
        requiredManifestations: [
          ...(definition.requiredManifestations || []),
        ],
        frequentManifestations: [
          ...(definition.frequentManifestations || []),
        ],
        atypicalManifestations: [
          ...(definition.atypicalManifestations || []),
        ],
        contraryFindings: [...(definition.contraryFindings || [])],
        riskFactors: [...(definition.riskFactors || [])],
        redFlags: [...(definition.redFlags || [])],
        stopConditions: [...(definition.stopConditions || [])],
        physicalExam: [...definition.exam],
        tests: definition.tests.map(
          ([name, question, when, examId, limitations, sourceIds]) => ({
          examId: examId || null,
          name,
          question,
          when:
            when ||
            "Solicitar somente quando a avaliação clínica indicar que o resultado pode mudar a decisão.",
          limitations: limitations || null,
          sourceIds: [...(sourceIds || [])],
        })),
        diagnosticCriteria: [...(definition.diagnosticCriteria || [])],
        postExamReassessment: [
          ...(definition.postExamReassessment || []),
        ],
        safetyConduct: [...(definition.safetyConduct || [])],
        initialTreatment: [...(definition.initialTreatment || [])],
        definitiveTreatment: [...(definition.definitiveTreatment || [])],
        destinationReturnFollowup: [
          ...(definition.destinationReturnFollowup || []),
        ],
      };
    });
    return {
      version: VERSION,
      representation: problemRepresentation(normalized),
      safety: safetyAssessment(normalized),
      syndromes,
      disclaimer:
        "Saída provisória de apoio à organização do raciocínio. Não confirma diagnóstico, não substitui exame físico e exige validação profissional.",
    };
  }

  function discriminatorQuestions(syndromeKeys = [], answeredIds = []) {
    const existing = new Set(answeredIds);
    return runtimeDefinitions().filter((definition) =>
      syndromeKeys.includes(definition.key),
    )
      .flatMap((definition) =>
        definition.discriminators.map((question) => ({
          module: definition.key,
          section: "discriminator",
          syndrome: definition.key,
          ...question,
        })),
      )
      .filter((question) => !existing.has(question.id));
  }

  return Object.freeze({
    version: VERSION,
    analyze,
    configureCatalog,
    configureContent,
    configureRules,
    discriminatorQuestions,
    get syndromeCatalog() {
      return Object.freeze(
        runtimeDefinitions().map((definition) => {
          const identity = identityFor(definition);
          return Object.freeze({
            key: definition.key,
            moduleId: identity.moduleId,
            name: identity.name,
            entityType: identity.entityType,
            entityTypeLabel: identity.entityTypeLabel,
            primarySpecialty: identity.primarySpecialty || null,
            version: identity.version,
            status: identity.status,
            terminologyStatus: identity.terminologyStatus,
            contentStatus: identity.contentStatus,
            sourceIds: Object.freeze([...identity.sourceIds]),
            modules: Object.freeze([...definition.modules]),
          });
        }),
      );
    },
    get prototypeContent() {
      return Object.freeze(
        SYNDROME_DEFINITIONS.map((definition) =>
          Object.freeze({
            legacy_key: definition.key,
            anchor_values: Object.freeze([...definition.anchorValues]),
            likely_hypotheses: Object.freeze([...definition.likely]),
            cannot_miss_hypotheses: Object.freeze([
              ...definition.cannotMiss,
            ]),
            mimics: Object.freeze([...definition.mimics]),
            discriminators: Object.freeze(
              definition.discriminators.map((question) =>
                Object.freeze({
                  question_id: question.id,
                  text: question.text,
                  options: Object.freeze([...question.options]),
                  detail_on_positive: question.detailOnPositive === true,
                  detail_required: question.detailRequired === true,
                }),
              ),
            ),
            physical_examination: Object.freeze([...definition.exam]),
            complementary_exams: Object.freeze(
              definition.tests.map(([name, clinicalQuestion, when], index) =>
                Object.freeze({
                  exam_id: `exam.${definition.key}.${index + 1}`,
                  name,
                  clinical_question: clinicalQuestion,
                  when:
                    when ||
                    "Solicitar somente quando a avaliação clínica indicar que o resultado pode mudar a decisão.",
                }),
              ),
            ),
          }),
        ),
      );
    },
    get syndromeKeys() {
      return Object.freeze(runtimeDefinitions().map((definition) => definition.key));
    },
  });
});
