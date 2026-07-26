(function exposeDecisionMedSequences(root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  } else {
    root.DecisionMedSequences = api;
  }
})(typeof globalThis === "object" ? globalThis : this, function createSequences() {
  "use strict";

  const VERSION = "0.1.0";
  const COMMON = Object.freeze([
    { id: "symptom.started", text: "Quando começou?", options: ["Hoje", "Há 2 a 7 dias", "Há semanas", "Há meses", "Há anos", "Não sabe informar"] },
    { id: "symptom.onset", text: "O início foi como?", options: ["De repente", "Aos poucos", "Após um evento conhecido", "Não sabe informar"] },
    { id: "symptom.trigger", text: "Algo pareceu desencadear?", options: ["Esforço físico", "Alimentação", "Trauma / queda", "Estresse", "Infecção recente", "Medicamento / produto", "Nada percebido", "Outro"], exclusiveOptions: ["Nada percebido"], multiple: true },
    { id: "symptom.location", text: "Onde é exatamente?", options: ["Peito", "Braço / ombro", "Pescoço / mandíbula", "Costas", "Abdome superior", "Abdome inferior", "Cabeça", "Perna / quadril", "Articulação específica", "Pele", "Olhos", "Região urinária / pélvica", "Corpo todo", "Outro local"] },
    { id: "symptom.intensity", text: "De 0 a 10, qual a intensidade ou o incômodo?", options: ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], scale: true },
    { id: "symptom.pattern", text: "Qual é o padrão ao longo do tempo?", options: ["Contínuo", "Vai e volta", "Acontece em crises", "Apenas em determinada situação", "Outro padrão"] },
    { id: "symptom.modifiers", text: "O que melhora ou piora?", options: ["Repouso melhora", "Esforço piora", "Movimento piora", "Alimentação interfere", "Posição interfere", "Medicamento melhora", "Nada percebido", "Outro"], exclusiveOptions: ["Nada percebido"], multiple: true },
    { id: "symptom.associated", text: "Teve sintomas associados?", options: ["Febre", "Náusea / vômito", "Falta de ar", "Suor frio", "Cansaço incomum", "Tontura / desmaio", "Palpitação", "Fraqueza", "Sangramento", "Nenhum", "Outro"], exclusiveOptions: ["Nenhum"], multiple: true },
    { id: "symptom.previous", text: "Já teve isso antes?", options: ["Nunca", "Sim, parecido", "Sim, mas diferente", "Não sabe informar"], detailOnPositive: true, detailLabel: "Quando aconteceu e o que foi feito?" },
    { id: "symptom.trend", text: "Comparado ao início, agora está?", options: ["Melhor", "Igual", "Pior", "Oscilando"] },
  ]);

  const PROFILES = Object.freeze({
    Dor: [
      { id: "symptom.quality", after: "symptom.location", text: "Como é a dor ou o desconforto?", options: ["Aperto / pressão", "Queimação", "Pontada", "Cólica", "Latejante", "Peso / desconforto", "Choque", "Outro"] },
      { id: "symptom.radiation", after: "symptom.intensity", text: "A dor ou o desconforto se espalha?", options: ["Não", "Braço / ombro", "Costas", "Pescoço / mandíbula", "Abdome superior", "Perna", "Outra região"], multiple: true, exclusiveOptions: ["Não"] },
    ],
    "Falta de ar": [{ id: "symptom.dyspnea_context", after: "symptom.trigger", text: "Em qual situação a falta de ar aparece?", options: ["Ao esforço", "Em repouso", "Ao deitar", "Acorda durante a noite", "Início súbito", "Outro"], multiple: true }],
    Tosse: [{ id: "symptom.cough_type", after: "symptom.trigger", text: "Como é a tosse?", options: ["Seca", "Com catarro claro", "Com catarro amarelo / verde", "Com sangue", "Piora à noite", "Outro"], multiple: true }],
    Febre: [{ id: "symptom.fever_measurement", after: "symptom.trigger", text: "A temperatura foi medida?", options: ["Não foi medida", "Até 37,7 °C", "38 a 38,9 °C", "39 °C ou mais", "Não sabe informar"] }],
    "Náusea / vômito": [{ id: "symptom.digestive_type", after: "symptom.location", text: "O que predomina?", options: ["Náusea sem vômito", "Vômitos", "Não consegue manter líquidos", "Relacionado à alimentação", "Outro"], multiple: true }],
    "Alteração urinária": [{ id: "symptom.urinary_type", after: "symptom.location", text: "Qual alteração urinária predomina?", options: ["Dor / ardência", "Maior frequência", "Urgência", "Sangue", "Jato fraco", "Perda de urina", "Mudança no volume", "Outro"], multiple: true }],
    "Alteração intestinal": [{ id: "symptom.bowel_type", after: "symptom.location", text: "Qual alteração intestinal predomina?", options: ["Diarreia", "Intestino preso", "Sangue nas fezes", "Dor ao evacuar", "Mudança no formato das fezes", "Outro"], multiple: true }],
    Pele: [{ id: "symptom.skin_type", after: "symptom.location", text: "Qual alteração da pele predomina?", options: ["Mancha", "Caroço", "Bolha", "Ferida", "Descamação", "Coceira", "Secreção", "Outro"], multiple: true }],
    Visão: [{ id: "symptom.vision_type", after: "symptom.location", text: "Qual alteração visual predomina?", options: ["Visão embaçada", "Perda de visão", "Visão dupla", "Manchas / flashes", "Dor ocular", "Olho vermelho", "Outro"], multiple: true }],
    Neurológica: [{ id: "symptom.neuro_type", after: "symptom.location", text: "Qual alteração neurológica predomina?", options: ["Perda de força", "Formigamento", "Convulsão", "Confusão", "Alteração da fala", "Dor de cabeça", "Memória / atenção", "Outro"], multiple: true }],
    Ginecológica: [{ id: "symptom.gyne_type", after: "symptom.location", text: "Qual alteração ginecológica predomina?", options: ["Sangramento fora do período", "Dor pélvica", "Corrimento / coceira", "Dor na relação", "Alteração menstrual", "Mama", "Outro"], multiple: true }],
    "Gestação / pós-parto": [{ id: "symptom.obstetric_context", after: "symptom.location", text: "Qual é o contexto atual?", options: ["Gestação confirmada", "Suspeita de gestação", "Até 6 semanas após o parto", "Mais de 6 semanas após o parto", "Outro"] }],
    "Ossos / articulações": [{ id: "symptom.orthopedic_type", after: "symptom.location", text: "Qual alteração musculoesquelética predomina?", options: ["Dor", "Inchaço", "Rigidez", "Trauma / queda", "Limitação de movimento", "Perda de força", "Outro"], multiple: true }],
    "Humor / sono": [{ id: "symptom.mental_type", after: "symptom.trigger", text: "Qual alteração predomina?", options: ["Ansiedade / preocupação", "Humor deprimido", "Irritabilidade", "Insônia", "Sono excessivo", "Pensamentos repetitivos", "Memória / atenção", "Outro"], multiple: true }],
  });

  function cloneQuestion(item) {
    return {
      ...item,
      options: [...item.options],
      ...(item.exclusiveOptions
        ? { exclusiveOptions: [...item.exclusiveOptions] }
        : {}),
    };
  }

  function buildSymptomQuestions(complaint) {
    const generalized = new Set(["Falta de ar", "Tosse", "Febre", "Humor / sono"]);
    const sequence = COMMON
      .filter(
        (item) =>
          !(generalized.has(complaint) && item.id === "symptom.location"),
      )
      .map(cloneQuestion);
    for (const profileQuestion of PROFILES[complaint] || []) {
      const index = sequence.findIndex(
        (item) => item.id === profileQuestion.after,
      );
      sequence.splice(index + 1, 0, cloneQuestion(profileQuestion));
    }
    return sequence.map((item) => ({
      module: "general",
      section: "symptom",
      ...item,
    }));
  }

  return Object.freeze({
    version: VERSION,
    complaints: Object.freeze([...Object.keys(PROFILES), "Outro sintoma"]),
    buildSymptomQuestions,
  });
});
