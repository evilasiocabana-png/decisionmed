# Project Glossary - PsychRx

## Funcao

Este documento consolida termos oficiais para reduzir ambiguidade entre documentos, agentes e implementacoes futuras.

## Termos Oficiais

| Termo Oficial | Uso |
| --- | --- |
| Patient | Pessoa em acompanhamento clinico. |
| Clinical Snapshot | Representacao dinamica do estado clinico atual. |
| Symptom | Manifestacao clinica relatada ou observada. |
| Syndrome | Conjunto organizado de sintomas. |
| DiagnosticHypothesis | Hipotese diagnostica com nivel de confianca. |
| TherapeuticObjective | Objetivo clinico do cuidado. |
| TherapeuticRestriction | Restricao clinica, individual, regulatoria ou de seguranca. |
| TherapeuticStrategy | Estrategia possivel, nao prescricao automatica. |
| PsychopharmacologicalAgent | Agente psicofarmacologico oficial. |
| ClinicalResponse | Resposta clinica observada longitudinalmente. |
| MonitoringPlan | Plano de monitorizacao. |
| EvidenceSource | Fonte cientifica rastreavel. |
| SafetyAlert | Alerta de seguranca clinica. |
| ClinicalExplanation | Explicacao rastreavel do raciocinio. |
| Clinical Experience Layer | Camada que organiza a experiencia de consulta. |
| Clinical Workspace | Ambiente da consulta onde microexperiencias clinicas sao organizadas. |
| Clinical Widget | Unidade basica da experiencia clinica; pode ser card, painel, timeline, lista, modal, overlay ou indicador. |
| Clinical Investigation Panel | Widget que organiza investigacao clinica por lacunas relevantes, substituindo o termo Live Question Panel para novas missoes. |
| Clinical Compass | Widget de orientacao que mostra progresso, suficiencia pendente e estado da consulta sem decidir conduta. |
| Missing Information Widget | Widget que mostra lacunas clinicas ainda nao esclarecidas. |
| Clinical Confidence Widget | Widget futuro para representar confianca clinica sem diagnostico automatico. |
| Consultation Room | Tela principal de consulta. |
| Guided Anamnesis | Apoio a perguntas clinicas durante a consulta. |
| Patient Friendly Mode | Modo de comunicacao acessivel ao paciente. |

## Sinonimos Proibidos

| Nao Usar | Usar |
| --- | --- |
| Drug | PsychopharmacologicalAgent |
| Recommendation | TherapeuticStrategy ou ClinicalSuggestion |
| Live Question Panel | Clinical Investigation Panel |
| Card como unidade arquitetural | Clinical Widget |
| Dashboard como experiencia | Clinical Workspace |
| Auto Prescription | Proibido |
| Bot Clinico | PsychRx nao e chatbot clinico autonomo |
| Final Decision | Medical Decision |
| AI Doctor | Proibido |

## Declaracao Final

O Project Glossary deve ser consultado antes de criar novos documentos, entidades, interfaces, testes ou prompts de missao.
