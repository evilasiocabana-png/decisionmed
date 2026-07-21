# 144 - Consultation Layout

## 1. Objetivo

Definir o layout conceitual da consulta no PsychRx como base da Clinical Experience Layer.

Este documento descreve como a experiencia da consulta deve ser organizada antes de qualquer Dashboard definitivo, tablet view, mobile view ou implementacao de interface.

## 2. Missao

Criar uma estrutura de consulta que permita ao medico enxergar, durante o atendimento:

- quem e o paciente;
- qual e o estado clinico atual;
- quais dados ainda faltam;
- quais riscos precisam ser avaliados;
- quais objetivos clinicos estao em discussao;
- quais estrategias podem ser comparadas futuramente;
- qual monitorizacao sera necessaria;
- quais explicacoes e incertezas devem permanecer visiveis.

O layout organiza a consulta.

O layout nao decide conduta.

O layout nao prescreve.

## 3. Principios

1. Paciente no centro.
2. Medico como decisor final.
3. Seguranca antes de estrategia.
4. Perguntas antes de conclusao.
5. Snapshot antes de comparacao.
6. Riscos sempre visiveis.
7. Estrategias sempre como alternativas revisaveis.
8. Monitorizacao como parte da consulta.
9. Explicabilidade e rastreabilidade sempre presentes.
10. Interface como apresentacao, nao como motor clinico.

## 4. Estrutura Conceitual

O Consultation Layout deve organizar a consulta em quatro regioes conceituais:

```text
REGIAO 1 - Patient Context
REGIAO 2 - Clinical Inquiry
REGIAO 3 - Safety and Strategy
REGIAO 4 - Monitoring and Explanation
```

## 5. Regiao 1 - Patient Context

Finalidade: manter o paciente como referencia central da consulta.

Conteudos previstos:

- Patient Header Card;
- Clinical Snapshot Card;
- sintomas atuais;
- dados relevantes do tratamento atual;
- contexto longitudinal;
- status de informacoes incompletas.

Regras:

- nao deve reduzir o paciente a diagnostico;
- nao deve ocultar incertezas;
- nao deve apresentar conclusao clinica final;
- deve deixar claro o estado atual do raciocinio.

## 6. Regiao 2 - Clinical Inquiry

Finalidade: organizar o que ainda precisa ser perguntado, confirmado ou monitorado.

Conteudos previstos:

- Live Question Panel;
- lacunas clinicas;
- perguntas de seguranca;
- perguntas diagnosticas;
- perguntas de contexto;
- perguntas de adesao e efeitos adversos.

Regras:

- perguntas de seguranca possuem prioridade;
- toda pergunta deve estar ligada a uma incerteza;
- perguntas nao devem induzir conduta;
- o medico pode aceitar, ignorar ou justificar.

## 7. Regiao 3 - Safety and Strategy

Finalidade: garantir que risco clinico preceda qualquer discussao de estrategia.

Conteudos previstos:

- Risk Panel;
- Objectives Card;
- Strategy Card;
- restricoes clinicas;
- alertas relevantes;
- fatores favoraveis e desfavoraveis.

Regras:

- Risk Panel deve aparecer antes de Strategy Card;
- Strategy Card nao pode prescrever;
- Strategy Card nao pode escolher pelo medico;
- nenhuma estrategia deve aparecer sem justificativa futura;
- nenhuma estrategia deve contornar seguranca.

## 8. Regiao 4 - Monitoring and Explanation

Finalidade: manter a consulta orientada por seguimento, explicacao e rastreabilidade.

Conteudos previstos:

- Monitoring Card;
- Evidence Summary futuro;
- Clinical Explanation futura;
- Consultation Timeline;
- proximos marcos de acompanhamento;
- incertezas ainda abertas.

Regras:

- monitorizacao deve acompanhar qualquer estrategia discutida;
- explicacao deve separar dado, inferencia, risco e incerteza;
- timeline deve preservar historico;
- nada deve ser apagado sem rastreabilidade futura.

## 9. Ordem de Leitura da Consulta

O layout deve orientar a atencao clinica nesta ordem:

```text
Patient
-> Clinical Snapshot
-> Questions
-> Risks
-> Objectives
-> Strategies
-> Monitoring
-> Explanation
```

Essa ordem impede que o sistema pule diretamente para estrategia antes de contexto, perguntas e seguranca.

## 10. Desktop Conceitual

Representacao textual:

```text
+----------------------+----------------------+----------------------+
| Patient Context      | Clinical Inquiry     | Safety and Strategy  |
| Patient Header       | Live Questions       | Risk Panel           |
| Snapshot             | Missing Data         | Objectives           |
| Current Treatment    | Safety Questions     | Strategy Card        |
+----------------------+----------------------+----------------------+
| Monitoring and Explanation                                          |
| Monitoring Card | Timeline | Evidence Summary | Open Uncertainties  |
+---------------------------------------------------------------------+
```

## 11. Tablet Conceitual

Representacao textual:

```text
[Patient Context]
[Clinical Inquiry]
[Safety and Strategy]
[Monitoring and Explanation]
```

O tablet deve priorizar empilhamento claro, com Risk Panel antes de Strategy Card.

## 12. Mobile Conceitual

Representacao textual:

```text
[Patient]
[Snapshot]
[Questions]
[Risks]
[Objectives]
[Strategy]
[Monitoring]
[Explanation]
```

O mobile deve funcionar como card stack, sem esconder riscos atras de estrategia.

## 13. Componentes Dependentes

Esta missao prepara as seguintes missoes:

- `145_PATIENT_HEADER_CARD.md`;
- `146_CURRENT_MEDICATION_CARD.md`;
- `147_LIVE_QUESTION_PANEL.md`;
- `148_CLINICAL_SNAPSHOT_CARD.md`;
- `149_OBJECTIVES_CARD.md`;
- `150_RISK_PANEL.md`;
- `151_STRATEGY_CARD.md`;
- `152_MONITORING_CARD.md`;
- `153_CONSULTATION_BASELINE.md`.

## 14. O Que Nao Pertence ao Consultation Layout

Nao pertence a este documento:

- implementacao de UI;
- escolha de framework;
- codigo;
- API;
- banco de dados;
- algoritmo clinico;
- prescricao;
- regra terapeutica;
- recomendacao automatica;
- IA clinica;
- decisao final.

## 15. Criterios de Aceite

O Consultation Layout esta aceito quando:

- organiza a consulta sem implementar software;
- deixa o paciente como primeiro eixo visual;
- coloca perguntas antes de conclusao;
- coloca Risk Panel antes de Strategy Card;
- impede Strategy Card de parecer prescricao;
- prepara cards reutilizaveis para desktop, tablet e mobile;
- preserva medico como decisor final;
- preserva rastreabilidade, explicabilidade e seguranca.

## 16. Relacao com Documentos Oficiais

Depende de:

- `docs/adr/0005_CLINICAL_EXPERIENCE_LAYER.md`;
- `docs/adr/0009_CLINICAL_EXPERIENCE_PRECEDES_DASHBOARD.md`;
- `docs/119_CLINICAL_EXPERIENCE_BASELINE.md`;
- `docs/PROGRAM_07_CLINICAL_EXPERIENCE_LAYER.md`;
- `docs/PROJECT_DEPENDENCIES.md`;
- `docs/PROJECT_GLOSSARY.md`.

## Declaracao Final

O Consultation Layout define a organizacao conceitual da consulta no PsychRx antes do Dashboard. Ele cria a base reutilizavel da Clinical Experience Layer, mantendo o paciente no centro, o medico como decisor final, o Risk Panel antes de qualquer Strategy Card e a experiencia clinica livre de prescricao automatica.
