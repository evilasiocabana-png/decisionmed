# Naming Conventions

## 1. Proposito

Este documento define a nomenclatura oficial do projeto PsychRx.

Seu objetivo e reduzir ambiguidade terminologica, evitar retrabalho e impedir que diferentes nomes sejam usados para o mesmo conceito clinico ou arquitetural.

Todo documento, modelo, teste, contrato futuro ou implementacao futura deve usar os termos oficiais definidos aqui.

## 2. Regra Geral

Cada conceito central deve possuir um nome canonico.

Sinônimos nao autorizados nao devem ser usados em documentos oficiais, nomes de entidades, contratos, testes, exemplos ou futuras implementacoes.

Quando um termo alternativo aparecer em fonte externa, ele pode ser citado apenas como linguagem da fonte, mas deve ser mapeado para o termo oficial do PsychRx.

## 3. Termos Oficiais

| Termo oficial | Uso no PsychRx |
|---|---|
| `Patient` | Unidade clinica longitudinal central do sistema. |
| `Symptom` | Manifestacao clinica observada ou relatada. |
| `Syndrome` | Agrupamento clinico de sintomas. |
| `DiagnosticHypothesis` | Hipotese diagnostica em avaliacao, com nivel de confianca. |
| `TherapeuticObjective` | Alvo clinico que orienta o raciocinio e a estrategia. |
| `TherapeuticRestriction` | Restricao clinica, farmacologica, contextual ou individual. |
| `TherapeuticStrategy` | Caminho terapeutico conceitual comparavel, sem equivaler a prescricao. |
| `PsychopharmacologicalAgent` | Medicamento ou agente psicofarmacologico representado oficialmente. |
| `ClinicalResponse` | Mudanca clinica observada ao longo do tempo. |
| `MonitoringPlan` | Plano conceitual de acompanhamento clinico. |
| `ClinicalSnapshot` | Representacao dinamica do estado clinico atual do paciente. |
| `EvidenceSource` | Fonte cientifica rastreavel. |
| `SafetyAlert` | Alerta de seguranca clinica. |
| `ClinicalExplanation` | Justificativa rastreavel de uma saida clinica. |

## 4. Patient

### Termo oficial

`Patient`

### Definicao

Representa a unidade clinica longitudinal central do PsychRx.

### Nao usar

- Client;
- User;
- Subject;
- Case, quando se referir ao paciente;
- Person, quando se referir ao objeto clinico central.

### Observacao

`User` pode existir apenas para pessoa que usa o sistema, como medico ou operador. Nunca deve substituir `Patient`.

## 5. Symptom

### Termo oficial

`Symptom`

### Definicao

Representa manifestacao clinica observada, relatada ou monitorada.

### Nao usar

- Complaint;
- Manifestation;
- Finding, quando o conceito for sintoma;
- Signal, quando o conceito for sintoma clinico relatado.

### Observacao

Sinais objetivos podem ser descritos separadamente quando necessario, mas sintomas psiquiatricos devem usar `Symptom`.

## 6. Syndrome

### Termo oficial

`Syndrome`

### Definicao

Representa agrupamento clinico de sintomas que sugere padrao psicopatologico ou estado clinico.

### Nao usar

- Cluster, quando o conceito for sindrome;
- SymptomGroup;
- Pattern, quando o conceito for agrupamento sindromico.

## 7. DiagnosticHypothesis

### Termo oficial

`DiagnosticHypothesis`

### Definicao

Representa hipotese diagnostica em avaliacao, sempre diferenciada de diagnostico definitivo.

### Nao usar

- Diagnosis, quando ainda houver incerteza;
- DiagnosticGuess;
- DiagnosticOption;
- Differential, quando se tratar da hipotese principal.

### Observacao

`Diagnosis` so deve ser usado quando o conceito exigir diagnostico estabelecido. O PsychRx deve preferir `DiagnosticHypothesis` quando houver raciocinio em andamento.

## 8. TherapeuticObjective

### Termo oficial

`TherapeuticObjective`

### Definicao

Representa alvo clinico que orienta raciocinio, comparacao estrategica e monitorizacao.

### Nao usar

- Goal;
- Target;
- TreatmentGoal;
- ClinicalGoal;
- OutcomeGoal.

### Observacao

O termo oficial evita ambiguidade entre meta clinica, desfecho de estudo e objetivo de interface.

## 9. TherapeuticRestriction

### Termo oficial

`TherapeuticRestriction`

### Definicao

Representa restricao que limita, bloqueia ou modifica uma estrategia terapeutica.

### Nao usar

- Constraint, quando se referir ao conceito clinico oficial;
- Limitation;
- Blocker;
- RiskRule;
- ClinicalConstraint.

### Observacao

`Constraint Graph` pode permanecer como nome arquitetural do documento, mas o objeto clinico deve usar `TherapeuticRestriction`.

## 10. TherapeuticStrategy

### Termo oficial

`TherapeuticStrategy`

### Definicao

Representa caminho terapeutico conceitual comparavel, sem equivaler a prescricao automatica.

### Nao usar

- Recommendation;
- Prescription;
- Treatment;
- Plan, quando o conceito for estrategia;
- Intervention;
- Suggestion, quando se tratar da estrategia estruturada.

### Observacao

Nao usar `Recommendation` se o termo oficial for `TherapeuticStrategy` ou `ClinicalSuggestion`.

`ClinicalSuggestion` pode ser usado apenas para sugestao explicativa, fraca, nao prescritiva e derivada de uma analise, quando for formalmente definido em documento proprio.

## 11. PsychopharmacologicalAgent

### Termo oficial

`PsychopharmacologicalAgent`

### Definicao

Representa medicamento, substancia ou agente psicofarmacologico dentro do modelo oficial do PsychRx.

### Nao usar

- Drug;
- Medication;
- Medicine;
- Compound;
- Molecule;
- PharmaAgent.

### Observacao

Nao usar `Drug` se o termo oficial for `PsychopharmacologicalAgent`.

`Medication` pode aparecer em linguagem comum de interface ou texto explicativo para usuario, mas nao deve substituir o nome canonico em modelo, contrato, documento tecnico ou teste.

## 12. ClinicalResponse

### Termo oficial

`ClinicalResponse`

### Definicao

Representa mudanca clinica observada em sintomas, funcionalidade, qualidade de vida, tolerabilidade, risco ou estabilizacao.

### Nao usar

- Response;
- TreatmentResponse;
- Outcome;
- Result;
- Effect, quando o conceito for resposta clinica global.

## 13. MonitoringPlan

### Termo oficial

`MonitoringPlan`

### Definicao

Representa plano conceitual de acompanhamento clinico.

### Nao usar

- FollowUpPlan;
- TrackingPlan;
- ObservationPlan;
- SurveillancePlan;
- MonitoringSchedule.

### Observacao

`MonitoringPlan` nao e ordem clinica automatica. E estrutura de acompanhamento para apoiar julgamento medico.

## 14. ClinicalSnapshot

### Termo oficial

`ClinicalSnapshot`

### Definicao

Representa o estado clinico atual do paciente em um momento especifico.

### Nao usar

- Snapshot;
- PatientSnapshot;
- ClinicalState;
- CaseState;
- CurrentCase.

### Observacao

Usar sempre `ClinicalSnapshot` para evitar confusao com estados internos de software.

## 15. EvidenceSource

### Termo oficial

`EvidenceSource`

### Definicao

Representa fonte cientifica rastreavel usada para sustentar conhecimento, alerta, comparacao ou explicacao.

### Nao usar

- Source;
- Reference;
- Citation;
- Paper, quando se referir a fonte em sentido amplo;
- EvidenceItem.

### Observacao

`Reference` e `Citation` podem aparecer em contexto bibliografico, mas o conceito oficial do dominio deve ser `EvidenceSource`.

## 16. SafetyAlert

### Termo oficial

`SafetyAlert`

### Definicao

Representa alerta de seguranca clinica gerado por risco, contraindicação, interacao, dado ausente critico ou fator de vulnerabilidade.

### Nao usar

- Alert;
- Warning;
- RiskAlert;
- ClinicalAlert;
- SafetyWarning.

### Observacao

O termo oficial reforca que o alerta pertence ao dominio de seguranca clinica.

## 17. ClinicalExplanation

### Termo oficial

`ClinicalExplanation`

### Definicao

Representa justificativa rastreavel de uma saida clinica, conectando dados, hipoteses, objetivos, riscos, evidencias e incertezas.

### Nao usar

- Explanation;
- Rationale;
- Justification;
- ReasoningOutput;
- ExplanationText.

### Observacao

`ClinicalExplanation` nao e texto decorativo. E parte da explicabilidade obrigatoria do PsychRx.

## 18. Termos Proibidos sem Autorizacao

Os seguintes termos nao devem ser usados como substitutos dos termos oficiais:

- Drug;
- Recommendation;
- Prescription;
- Treatment, quando significar estrategia;
- Plan, quando significar estrategia;
- Client;
- Case, quando significar paciente;
- Source, quando significar EvidenceSource;
- Alert, quando significar SafetyAlert;
- Goal, quando significar TherapeuticObjective;
- Constraint, quando significar TherapeuticRestriction.

## 19. Uso em Documentos Futuros

Novos documentos devem:

- usar os termos oficiais;
- evitar sinonimos nao autorizados;
- explicar qualquer termo novo antes de usa-lo;
- atualizar este documento quando novo termo canonico for aprovado;
- atualizar a Ontologia quando novo conceito clinico for introduzido.

## 20. Regra de Revisao

Em Pull Requests, qualquer novo nome deve ser verificado contra este documento.

Um PR deve ser revisado se:

- introduzir sinonimo para conceito existente;
- usar termo proibido;
- criar nova entidade clinica sem atualizar Ontologia;
- usar `Recommendation` para estrategia;
- usar `Drug` para agente psicofarmacologico;
- usar `Goal` para objetivo terapeutico;
- usar `Alert` para alerta de seguranca.

## 21. Declaracao Final

A nomenclatura oficial do PsychRx protege o projeto contra ambiguidades conceituais. Cada nome deve apontar para um conceito claro, documentado e rastreavel.

Quando nomes diferentes descrevem o mesmo conceito, o sistema perde coerencia. Por isso, os termos oficiais definidos aqui devem orientar documentos, testes, contratos e futuras implementacoes.
