# 031 - Domain Model

## 1. Objetivo

Este documento define oficialmente o Domain Model do PsychRx.

O Domain Model descreve os conceitos centrais do domínio clínico, suas responsabilidades, fronteiras, relações, invariantes e eventos. Ele organiza a linguagem do projeto antes de qualquer implementação.

Este documento é puramente arquitetural. Não cria código, não define classes, não implementa software, não escolhe tecnologia e não descreve infraestrutura.

## 2. Conceito de Domain Model

O Domain Model é a representação conceitual do universo clínico do PsychRx.

Ele responde à pergunta:

> Quais são os conceitos clínicos fundamentais do PsychRx, como eles se relacionam e quais regras devem permanecer verdadeiras independentemente da tecnologia futura?

No PsychRx, o Domain Model existe para preservar coerência entre:

- paciente;
- sintomas;
- síndromes;
- hipóteses diagnósticas;
- objetivos terapêuticos;
- restrições;
- segurança clínica;
- estratégias terapêuticas;
- psicofármacos;
- evidências;
- resposta clínica;
- monitorização;
- explicabilidade;
- estabilização;
- auditoria.

O Domain Model não é banco de dados, interface, API ou motor clínico. Ele é a linguagem estrutural que sustenta todos esses elementos futuros.

## 3. Responsabilidades

O Domain Model deve:

- definir os conceitos centrais do domínio;
- padronizar a linguagem usada pelo projeto;
- separar o domínio clínico da infraestrutura;
- preservar invariantes clínicas e arquiteturais;
- impedir duplicação de conceitos;
- impedir nomes diferentes para a mesma entidade;
- orientar motores futuros sem implementá-los;
- estabelecer fronteiras entre domínio, conhecimento, evidência, raciocínio, segurança e interface;
- garantir que toda estratégia esteja vinculada a objetivo, segurança, evidência e explicabilidade;
- manter o paciente como centro do sistema.

O Domain Model não deve:

- prescrever;
- gerar recomendações automáticas;
- conter evidência científica hardcoded;
- conter lógica de interface;
- conter regras executáveis;
- substituir julgamento médico;
- decidir conduta clínica.

## 4. Princípios de Modelagem

### Paciente no Centro

Todo conceito clínico deve poder ser relacionado ao `Patient`.

Sintomas, hipóteses, objetivos, restrições, estratégias, resposta, monitorização e estabilização só fazem sentido no contexto do paciente.

### Raciocínio antes de Estratégia

O modelo deve impedir saltos diretos entre sintoma e estratégia.

A ordem conceitual deve preservar:

```text
Patient -> ClinicalSnapshot -> Symptom -> Syndrome -> DiagnosticHypothesis -> TherapeuticObjective -> TherapeuticRestriction -> SafetyAlert -> TherapeuticStrategy
```

### Segurança antes de Comparação

Nenhuma `TherapeuticStrategy` deve existir como alternativa clinicamente discutível sem avaliação de segurança.

### Objetivo antes de Estratégia

Toda `TherapeuticStrategy` deve estar vinculada a pelo menos um `TherapeuticObjective`.

### Evidência antes de Afirmação Clínica

Toda afirmação científica relevante deve estar vinculada a `EvidenceSource`.

### Explicabilidade antes de Saída Clínica

Toda saída clinicamente relevante deve possuir `ClinicalExplanation`.

### Estabilização como Finalidade

O domínio deve convergir para estabilização clínica, não apenas para redução sintomática ou escolha de psicofármaco.

## 5. Separação entre Domínio e Infraestrutura

O Domain Model pertence ao domínio clínico.

Ele não deve depender de:

- interface;
- dashboard;
- banco de dados;
- API;
- framework;
- armazenamento;
- autenticação;
- telas;
- integrações externas;
- detalhes de aplicação.

A infraestrutura futura poderá representar, persistir ou transportar elementos do domínio, mas não deverá redefinir seu significado.

Regra oficial:

> A infraestrutura serve ao domínio; o domínio não se adapta à infraestrutura.

## 6. Separação entre Domínio, Conhecimento e Evidência

O Domain Model define conceitos. Ele não armazena todo conhecimento científico.

A separação deve ser:

- Domain Model: define o que é `Patient`, `Symptom`, `TherapeuticObjective`, `SafetyAlert`, `ClinicalExplanation` e demais conceitos;
- Knowledge Layer: organiza conhecimento clínico-científico estruturado;
- Evidence Layer: registra fontes, qualidade, conflitos, versão e aplicabilidade;
- Reasoning Layer: organiza raciocínio clínico;
- Safety Layer: organiza restrições e alertas de segurança.

O domínio pode referenciar conhecimento e evidência, mas não deve embutir conteúdo científico como regra fixa.

## 7. Entidades

Entidades são conceitos com continuidade, identidade e ciclo de vida clínico.

### Patient

Entidade central do domínio.

Responsabilidade: representar a trajetória clínica longitudinal do paciente.

Relaciona-se com:

- ClinicalSnapshot;
- Symptom;
- DiagnosticHypothesis;
- TherapeuticObjective;
- TherapeuticRestriction;
- TherapeuticStrategy;
- ClinicalResponse;
- MonitoringPlan;
- SafetyAlert;
- ClinicalExplanation;
- estabilização.

### ClinicalSnapshot

Representa o estado clínico atual do paciente em um momento específico.

Responsabilidade: ancorar o raciocínio clínico no presente, preservando relação com a trajetória longitudinal.

### Symptom

Representa manifestação clínica observada, relatada ou monitorada.

Responsabilidade: descrever sofrimento, alteração clínica ou fenômeno relevante para avaliação.

### Syndrome

Representa agrupamento clínico de sintomas.

Responsabilidade: organizar padrões sintomáticos sem fechar diagnóstico automaticamente.

### DiagnosticHypothesis

Representa hipótese diagnóstica em avaliação.

Responsabilidade: organizar critérios favoráveis, critérios contrários, diferenciais, incertezas e nível de confiança.

### TherapeuticObjective

Representa alvo clínico que orienta raciocínio, comparação estratégica e monitorização.

Responsabilidade: impedir estratégia sem direção clínica.

### TherapeuticRestriction

Representa limite clínico, farmacológico, contextual ou individual.

Responsabilidade: modificar, reduzir ou bloquear estratégias quando houver risco, contraindicação, interação, comorbidade, preferência ou dado ausente relevante.

### TherapeuticStrategy

Representa caminho terapêutico conceitual comparável.

Responsabilidade: organizar possibilidade clínica sem equivaler a prescrição.

### PsychopharmacologicalAgent

Representa agente psicofarmacológico no modelo oficial do PsychRx.

Responsabilidade: conectar classe, mecanismo, riscos, efeitos adversos, interações, contraindicações, evidências e monitorização.

### EvidenceSource

Representa fonte científica rastreável.

Responsabilidade: sustentar conhecimento, alertas, comparações e explicações.

### SafetyAlert

Representa alerta de segurança clínica.

Responsabilidade: tornar visível risco, restrição, contraindicação, interação, dado ausente crítico ou necessidade de encaminhamento.

### ClinicalResponse

Representa mudança clínica observada ao longo do tempo.

Responsabilidade: registrar melhora, piora, resposta parcial, ausência de resposta, efeitos adversos, remissão, deterioração, recaída ou recorrência.

### MonitoringPlan

Representa acompanhamento conceitual necessário para avaliar segurança, resposta e estabilização.

Responsabilidade: definir o que precisa ser observado longitudinalmente.

### ClinicalExplanation

Representa justificativa rastreável de uma saída clínica.

Responsabilidade: conectar dados, hipóteses, objetivos, restrições, evidências, riscos, incertezas e papel do médico.

### AuditRecord

Representa registro auditável de evento ou análise.

Responsabilidade: permitir reconstrução de decisões, versões, evidências, alertas e saídas.

## 8. Objetos de Valor

Objetos de valor representam medidas, classificações ou descritores sem identidade própria fora do contexto clínico.

Devem ser imutáveis conceitualmente em relação ao momento registrado.

Objetos de valor oficiais incluem:

- `Dose`;
- `Weight`;
- `Height`;
- `BMI`;
- `QTInterval`;
- `ClinicalScore`;
- `RenalFunction`;
- `HepaticFunction`;
- `BloodPressure`;
- `HeartRate`;
- `EvidenceQuality`;
- `RecommendationStrength`;
- `RiskSeverity`;
- `ConfidenceLevel`;
- `ClinicalPeriod`;
- `EvidenceStatus`;
- `ClinicalJustification`;
- `SourceReference`.

Objetos de valor devem ser usados para reduzir ambiguidade e impedir que medidas clínicas sejam tratadas como texto solto.

## 9. Agregados

Agregados são agrupamentos conceituais que preservam consistência interna.

Este documento define agregados em sentido arquitetural, não como classes ou implementação.

### Patient Aggregate

Raiz conceitual: `Patient`.

Inclui identidade longitudinal, dados clínicos centrais, referências a snapshots, histórico terapêutico, riscos e trajetória.

Invariante principal: todo dado clínico individual deve poder retornar ao paciente.

### ClinicalSnapshot Aggregate

Raiz conceitual: `ClinicalSnapshot`.

Inclui sintomas atuais, síndromes possíveis, hipóteses ativas, objetivos, restrições, riscos, dados ausentes e incertezas.

Invariante principal: nenhum raciocínio clínico deve ocorrer sem snapshot atualizado ou explicitamente validado.

### DiagnosticReasoning Aggregate

Raiz conceitual: `DiagnosticHypothesis`.

Inclui sintomas de suporte, síndromes, diferenciais, nível de confiança e incertezas.

Invariante principal: hipótese não pode existir sem base clínica ou nível de confiança.

### TherapeuticObjective Aggregate

Raiz conceitual: `TherapeuticObjective`.

Inclui objetivo primário, objetivos secundários, critérios de sucesso, conflitos e priorização.

Invariante principal: estratégia não pode existir sem objetivo.

### Safety Aggregate

Raiz conceitual: `SafetyAlert`.

Inclui restrições, riscos, contraindicações, interações, bloqueios, alertas críticos, alertas moderados e necessidade de monitorização.

Invariante principal: segurança clínica precede comparação estratégica.

### Strategy Aggregate

Raiz conceitual: `TherapeuticStrategy`.

Inclui objetivo vinculado, restrições consideradas, evidências, riscos, comparação, explicação e necessidade de monitorização.

Invariante principal: estratégia não pode ser apresentada sem objetivo, segurança, evidência aplicável e explicação.

### Evidence Aggregate

Raiz conceitual: `EvidenceSource`.

Inclui fonte, ano, tipo de evidência, qualidade, força da recomendação, status, conflitos e aplicabilidade.

Invariante principal: conhecimento clínico sem fonte não pode sustentar regra terapêutica.

### Monitoring Aggregate

Raiz conceitual: `MonitoringPlan`.

Inclui indicadores, parâmetros, resposta, efeitos adversos, risco, adesão e estabilidade.

Invariante principal: estabilidade sustentada não pode ser declarada sem acompanhamento longitudinal suficiente.

### Explanation and Audit Aggregate

Raízes conceituais: `ClinicalExplanation` e `AuditRecord`.

Inclui justificativa, dados usados, fontes, versões, incertezas, alertas, saída apresentada e contexto de execução.

Invariante principal: toda saída clínica relevante deve ser explicável e auditável.

## 10. Serviços de Domínio

Serviços de domínio representam responsabilidades conceituais que atravessam múltiplas entidades.

Eles não são implementações neste documento.

### ClinicalSnapshot Coordination

Organiza a construção e atualização conceitual do Clinical Snapshot.

### Diagnostic Reasoning Service

Organiza hipóteses diagnósticas, diferenciais, critérios e incertezas.

### Therapeutic Objective Service

Organiza objetivos primários, secundários, concorrentes, conflitos e critérios de sucesso.

### Constraint Evaluation Service

Organiza restrições terapêuticas, fatores de risco, comorbidades, preferências e dados ausentes.

### Clinical Safety Service

Aplica conceitualmente o contrato de segurança antes de qualquer estratégia.

### Strategy Reasoning Service

Organiza geração e comparação de estratégias sem prescrever.

### Evidence Traceability Service

Garante que conhecimento clínico, alertas e estratégias estejam vinculados a evidências rastreáveis.

### Clinical Explanation Service

Organiza justificativas clínicas rastreáveis.

### Monitoring and Stabilization Service

Organiza acompanhamento longitudinal, resposta, remissão, recaída, recorrência, deterioração e estabilização.

### Audit Trace Service

Garante reconstrução conceitual de eventos, versões, fontes, alertas e saídas.

## 11. Eventos de Domínio

Eventos de domínio representam mudanças clinicamente relevantes.

Eventos oficiais incluem:

- `PatientUpdated`;
- `ClinicalSnapshotCreated`;
- `ClinicalSnapshotUpdated`;
- `SymptomRegistered`;
- `SyndromeIdentified`;
- `DiagnosticHypothesisCreated`;
- `DiagnosticHypothesisRevised`;
- `TherapeuticObjectiveDefined`;
- `TherapeuticObjectiveReprioritized`;
- `TherapeuticRestrictionIdentified`;
- `SafetyAlertIssued`;
- `EvidenceSourceLinked`;
- `EvidenceStatusChanged`;
- `TherapeuticStrategyGenerated`;
- `TherapeuticStrategyCompared`;
- `ClinicalExplanationGenerated`;
- `MonitoringPlanDefined`;
- `ClinicalResponseObserved`;
- `RemissionObserved`;
- `RelapseDetected`;
- `RecurrenceDetected`;
- `ClinicalDeteriorationDetected`;
- `StabilizationStatusUpdated`;
- `AuditRecordCreated`.

Eventos não decidem conduta. Eles registram mudança de estado clínico, raciocínio, evidência ou rastreabilidade.

## 12. Invariantes

Invariantes são regras que devem permanecer verdadeiras em qualquer implementação futura.

Invariantes oficiais:

- nenhum dado clínico individual sem relação com `Patient`;
- nenhum raciocínio sem `ClinicalSnapshot`;
- nenhuma hipótese sem nível de confiança ou incerteza declarada;
- nenhum `TherapeuticObjective` sem vínculo com estado clínico;
- nenhuma `TherapeuticStrategy` sem `TherapeuticObjective`;
- nenhuma estratégia sem avaliação de segurança;
- nenhuma regra terapêutica sem `EvidenceSource`;
- nenhuma informação científica sem fonte;
- nenhum `SafetyAlert` sem justificativa;
- nenhuma recomendação ou comparação sem `ClinicalExplanation`;
- nenhuma estabilidade sustentada sem monitorização longitudinal;
- nenhuma saída clínica relevante sem rastreabilidade;
- nenhuma interface decidindo lógica clínica;
- nenhum motor clínico contendo evidência hardcoded;
- nenhum conhecimento oficial em status inválido ou sem revisão;
- nenhuma mudança estrutural sem ADR quando aplicável.

## 13. Relação com os Documentos Anteriores

Este Domain Model consolida os documentos anteriores:

- `000_MANIFEST.md`: paciente e estabilização como centro do projeto;
- `001_CONSTITUICAO_CLINICA.md`: sistema apoia o médico e não substitui decisão clínica;
- `002_PRINCIPIOS_ARQUITETURAIS.md`: raciocínio antes de prescrição e paciente no centro;
- `003_ONTOLOGIA_PSICOFARMACOLOGIA.md`: entidades fundamentais do universo PsychRx;
- `004_MODELO_DO_PACIENTE.md`: paciente como estrutura longitudinal;
- `005_MODELO_DO_PSICOFARMACO.md`: representação oficial dos psicofármacos;
- `006_FLUXO_DE_DECISAO_CLINICA.md`: sequência clínica de raciocínio;
- `008_CLINICAL_OPERATING_MIND.md`: componentes do cérebro conceitual do sistema;
- `009_CLINICAL_SNAPSHOT.md`: estado clínico atual como ponto de partida;
- `010_MOTOR_DE_ESTABILIZACAO.md`: estabilização como objetivo final;
- `011_KNOWLEDGE_GRAPH.md`: relações, hierarquia e herança semântica;
- `012_DECISION_GRAPH.md`: caminhos de decisão clínica;
- `013_CONSTRAINT_GRAPH.md`: restrições e limites terapêuticos;
- `014_EVIDENCE_GRAPH.md`: evidência como sustentação das decisões;
- `024_THERAPEUTIC_OBJECTIVE_ENGINE.md`: objetivos terapêuticos como direção do raciocínio.

## 14. Limites

Este documento não:

- cria código;
- cria classes;
- implementa software;
- define API;
- define banco de dados;
- escolhe framework;
- cria motores clínicos;
- cria recomendação clínica;
- altera a ontologia sem missão específica;
- substitui documentos de evidência, segurança ou testes.

Ele define o modelo de domínio que futuras implementações deverão respeitar.

## 15. Declaração Final

O Domain Model do PsychRx é a espinha dorsal conceitual do sistema.

Ele organiza paciente, sintomas, síndromes, hipóteses, objetivos, restrições, segurança, estratégias, psicofármacos, evidências, resposta, monitorização, explicabilidade, auditoria e estabilização em uma linguagem comum, rastreável e clinicamente segura.

No PsychRx, nenhuma implementação futura deve redefinir o domínio. Toda implementação deve servir a este modelo, preservar seus invariantes e manter o médico como decisor final.
