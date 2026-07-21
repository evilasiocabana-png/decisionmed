# 032 - Clinical Knowledge Objects

## 1. Objetivo

Definir os objetos oficiais de conhecimento clinico do PsychRx, sem implementar software, banco de dados, classes ou APIs.

## 2. Missao

A missao deste documento e estabelecer quais unidades de conhecimento podem existir no modelo computacional, quais responsabilidades possuem e quais limites devem respeitar.

## 3. Principios

Todo objeto de conhecimento deve ser:

- rastreavel;
- versionavel;
- validavel;
- explicavel;
- separado de logica executavel;
- aderente a Ontologia e nomenclatura oficial.

## 4. Guideline

Guideline representa uma diretriz clinica publicada por sociedade, instituicao ou grupo autorizado.

Deve conter escopo, populacao, ano, metodologia, recomendacoes de fonte, limites, conflitos e status de revisao.

Guideline nao e decisao clinica automatica.

## 5. Recommendation

Recommendation, neste modelo, significa recomendacao contida em fonte cientifica externa, como guideline ou consenso.

Para evitar conflito com a nomenclatura oficial do PsychRx, Recommendation nao deve ser usada como saida assistencial do sistema. Quando o PsychRx organizar uma possibilidade de acao, o termo preferencial permanece TherapeuticStrategy ou ClinicalSuggestion, conforme governanca terminologica.

## 6. Evidence

Evidence representa uma unidade de evidencia cientifica.

Deve conter fonte, tipo de estudo, ano, qualidade, populacao, desfechos, aplicabilidade, conflitos e status.

Evidence sustenta conhecimento, mas nao executa decisao.

## 7. DrugKnowledge

DrugKnowledge representa conhecimento estruturado sobre um PsychopharmacologicalAgent.

Pode incluir indicacoes cientificas, efeitos adversos, interacoes, contraindicações, monitorizacao e restricoes, sempre com fonte rastreavel.

DrugKnowledge nao deve conter prescricao automatica.

## 8. Contraindication

Contraindication representa uma condicao que torna uma estrategia inadequada, proibida, arriscada ou dependente de avaliacao adicional.

Deve indicar se e absoluta, relativa, regulatoria, contextual ou dependente de monitorizacao.

## 9. DrugInteraction

DrugInteraction representa relacao clinicamente relevante entre agentes, substancias ou condicoes que modifica seguranca.

Deve conter mecanismo conceitual, gravidade, evidencia, manejo conceitual, necessidade de alerta e limites de aplicabilidade.

## 10. TherapeuticObjective

TherapeuticObjective representa o alvo clinico que orienta o raciocinio.

Ele deve anteceder qualquer TherapeuticStrategy e estar vinculado a Clinical Snapshot, hipoteses, sintomas, funcionalidade, qualidade de vida e estabilizacao.

## 11. MonitoringRecommendation

MonitoringRecommendation representa recomendacao de monitorizacao presente em fonte cientifica ou regulatoria.

Internamente, deve alimentar MonitoringPlan ou necessidades conceituais de acompanhamento, sem substituir decisao medica.

## 12. ClinicalRule

ClinicalRule representa regra clinica conceitual validada e rastreavel.

Ela nao deve ser algoritmo hardcoded. Deve expressar uma relacao clinica governada, como "condicao X exige avaliacao de seguranca Y", com fonte, status, aplicabilidade e limites.

## 13. Campos Minimos

Todo objeto deve declarar:

- identificador conceitual;
- nome oficial;
- tipo;
- descricao;
- fonte;
- status;
- versao;
- data de revisao;
- aplicabilidade;
- relacoes;
- limites;
- criterios de validacao.

## 14. Limites

Objetos de conhecimento nao prescrevem, nao substituem medico, nao executam logica e nao devem conter tecnologia.

## 15. Declaracao Final

Clinical Knowledge Objects sao as unidades que tornam o conhecimento clinico do PsychRx estruturado, governavel e auditavel.

No PsychRx, um objeto de conhecimento so e oficial quando possui fonte, versao, status, relacoes e limites claros.
