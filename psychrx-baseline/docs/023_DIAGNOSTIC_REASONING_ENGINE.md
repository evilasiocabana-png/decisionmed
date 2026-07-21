# 023 - Diagnostic Reasoning Engine

## 1. Definicao

O Diagnostic Reasoning Engine e o motor conceitual responsavel por construir, avaliar e atualizar hipoteses diagnosticas dentro do Clinical Operating Mind do PsychRx.

Ele nao produz diagnostico final automatico. Sua funcao e organizar o raciocinio diagnostico de modo rastreavel, explicavel e revisavel pelo medico.

## 2. Missao

A missao do Diagnostic Reasoning Engine e transformar sintomas, sindromes, contexto clinico e trajetoria longitudinal em hipoteses diagnosticas estruturadas, acompanhadas de nivel de confianca, criterios favoraveis, criterios contrarios e incertezas.

## 3. Responsabilidades

- Organizar sintomas e sindromes em hipoteses diagnosticas.
- Diferenciar hipotese, sindrome e diagnostico estabelecido.
- Identificar diagnosticos diferenciais.
- Explicitar criterios de exclusao e confirmacao.
- Atribuir nivel conceitual de confianca.
- Atualizar hipoteses quando o Clinical Snapshot mudar.
- Integrar lacunas ao Question Engine.
- Preservar rastreabilidade do raciocinio diagnostico.

## 4. Entradas Conceituais

- Clinical Snapshot atualizado.
- Sintomas atuais e historicos.
- Sindromes possiveis.
- Curso temporal.
- Funcionalidade.
- Comorbidades.
- Dados contextuais.
- Respostas terapeuticas previas.
- Dados ausentes apontados pelo Question Engine.
- Evidencias clinicas e criterios diagnosticos rastreaveis quando aplicaveis.

## 5. Saidas Conceituais

- Hipoteses diagnosticas em avaliacao.
- Diagnosticos diferenciais relevantes.
- Dados que favorecem cada hipotese.
- Dados que enfraquecem cada hipotese.
- Criterios de exclusao pendentes.
- Criterios de confirmacao pendentes.
- Nivel de confianca.
- Incertezas diagnosticas.
- Perguntas adicionais para o Question Engine.

## 6. Formacao de Hipoteses

A formacao de hipoteses deve partir do paciente e do Clinical Snapshot, nao de uma estrategia terapeutica previamente desejada.

Uma hipotese diagnostica deve nascer da combinacao entre sintomas, sindromes, curso temporal, impacto funcional, historia clinica, fatores contextuais e dados de seguranca.

Hipoteses nao devem ser apresentadas como conclusoes definitivas quando houver dados insuficientes.

## 7. Diagnosticos Diferenciais

Diagnosticos diferenciais representam possibilidades clinicas que podem explicar parcialmente ou totalmente o estado atual do paciente.

O motor deve registrar:

- por que o diferencial foi considerado;
- quais dados o favorecem;
- quais dados o contradizem;
- quais informacoes faltam para reduzir incerteza;
- qual impacto o diferencial teria sobre objetivos, riscos e estrategias.

## 8. Criterios de Exclusao

Criterios de exclusao sao dados que reduzem a plausibilidade de uma hipotese ou impedem sua sustentacao naquele momento.

Eles podem incluir curso temporal incompatível, sintomas ausentes essenciais, condicoes medicas alternativas, uso de substancias, delirium, intoxicacao, abstinencia ou explicacao melhor por outro quadro.

Exclusao deve ser documentada como raciocinio, nao como regra automatica.

## 9. Criterios de Confirmacao

Criterios de confirmacao sao dados que aumentam a plausibilidade de uma hipotese.

Eles devem ser interpretados em conjunto com contexto, curso, funcionalidade, seguranca e evidencias. Um criterio isolado nao deve ser convertido em diagnostico final automatico.

## 10. Niveis de Confianca

O nivel de confianca deve expressar o quanto a hipotese esta sustentada pelos dados disponiveis.

Categorias conceituais possiveis:

- baixa confianca;
- confianca moderada;
- alta confianca;
- confianca insuficiente por dados ausentes;
- confianca limitada por conflito de informacoes.

O nivel de confianca deve ser revisavel.

## 11. Atualizacao Longitudinal

Hipoteses diagnosticas devem ser atualizadas quando surgirem novos Clinical Snapshots, respostas inesperadas, deterioracao, remissao, recaida, recorrencia, eventos adversos ou novos dados contextuais.

Mudanca de hipotese deve preservar o historico do raciocinio: o que mudou, por que mudou e quais consequencias clinicas decorrem da mudanca.

## 12. Integracao com Question Engine

O Diagnostic Reasoning Engine depende do Question Engine para reduzir incertezas diagnosticas.

Quando faltarem dados essenciais, o motor deve gerar demandas conceituais de pergunta, em vez de assumir uma conclusao.

## 13. Integracao com Clinical Snapshot

O Clinical Snapshot e o ponto de entrada do raciocinio diagnostico.

Nenhuma hipotese deve surgir fora do Snapshot. Quando o Snapshot muda, as hipoteses devem poder ser mantidas, revisadas, rebaixadas, substituidas ou suspensas.

## 14. Limites

O Diagnostic Reasoning Engine nao deve:

- emitir diagnostico final automatico;
- substituir avaliacao medica;
- criar entidade clinica fora da Ontologia;
- ignorar dados ausentes;
- ocultar incerteza;
- usar resposta a medicamento como confirmacao unica;
- transformar diagnostico em recomendacao terapeutica.

## 15. Declaracao Final

O Diagnostic Reasoning Engine organiza hipoteses diagnosticas sem substituir o julgamento medico.

No PsychRx, diagnosticar conceitualmente e explicitar possibilidades, evidencias, lacunas e incertezas antes de qualquer objetivo ou estrategia terapeutica.
