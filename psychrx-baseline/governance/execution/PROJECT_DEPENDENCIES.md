# Project Dependencies - PsychRx

## Funcao

Este documento registra dependencias conceituais e arquiteturais entre camadas, programas e componentes do PsychRx.

## Dependencia Clinica Central

```text
Patient
-> Clinical Snapshot
-> Question Engine
-> Diagnostic Reasoning
-> Therapeutic Objectives
-> Constraint Engine
-> Safety First Engine
-> Strategy Generation
-> Strategy Comparison
-> Evidence Evaluation
-> Clinical Explanation
-> Monitoring Engine
-> Longitudinal Follow-up
-> Stabilization
```

## Dependencia de Conhecimento

```text
Scientific Library
-> Evidence Graph
-> Knowledge Graph
-> Constraint Graph
-> Decision Graph
-> Clinical Reasoning
```

## Dependencia de Software

```text
Domain
-> Application
-> Clinical Experience
-> Interfaces

Knowledge
-> Evidence
-> Reasoning
-> Safety
-> Application
```

## Dependencia de Experiencia Clinica

```text
Software Platform
-> Clinical Workspace
-> Clinical Kernel Integration
-> Knowledge Population
-> Dashboard
-> Mobile Experience
```

Clinical Workspace deve existir antes do Clinical Kernel Integration. Knowledge Population deve existir antes do Clinical Runtime usar conhecimento cientifico. Dashboard e Mobile devem consumir componentes do Workspace. Eles nao devem definir fluxo de consulta, cards clinicos ou logica de decisao.

## Dependencia Nuclear do Operating Mind

```text
Clinical Runtime
-> Safety Engine
-> Evidence Runtime
-> Therapeutic Optimization Engine
-> Clinical Explanation Engine
-> Clinical Snapshot Engine
-> Clinical Timeline Engine
-> Clinical Navigation Engine
-> Clinical Operating Mind
-> Clinical Workspace
```

Clinical Operating Mind consolida a ordem nuclear dos motores. Ele nao substitui Runtime, nao decide conduta, nao prescreve e nao permite que Workspace chame motores diretamente.

## Dependencia de Qualidade Clinica Estrutural

```text
Clinical Operating Mind
-> Clinical Quality & Error Reduction Engine
-> Publication Gate
-> Clinical Workspace
```

Clinical Quality valida completude, consistencia, rastreabilidade e explicabilidade antes da publicacao visual. Ele nao interpreta evidencia, nao altera Snapshot, nao resolve conflitos e nao recomenda conduta.

## Dependencia de Pesquisa Clinica

```text
Clinical Operating Mind
-> Clinical Quality & Error Reduction Engine
-> Clinical Research Platform
-> Promotion Pipeline
-> Governance Review
```

Clinical Research Platform e ambiente isolado. Ela nao executa no Clinical Runtime, nao altera pacientes, nao modifica producao e nao promove componentes sem ADR.

## Dependencia de Validacao Cientifica

```text
Scientific Sources
-> Scientific Validation Framework
-> Knowledge Layer
-> Evidence Runtime
-> Clinical Operating Mind
```

Scientific Validation Framework governa a entrada de conhecimento cientifico. O Runtime nunca acessa literatura diretamente. Evidence Runtime consome apenas conhecimento previamente validado e versionado.

## Dependencia de Governanca Semantica

```text
Scientific Validation Framework
-> Knowledge Governance Platform
-> Knowledge Layer
-> Knowledge Graph
-> Evidence Runtime
-> Clinical Operating Mind
```

Knowledge Governance Platform governa estrutura semantica. Aprovacao cientifica isolada e insuficiente para ingestao: ontologia, entidades, relacionamentos e taxonomia tambem precisam estar semanticamente consistentes.

## Dependencia do Digital Clinical Twin

```text
Clinical Operating Mind
-> Clinical Snapshot Engine
-> Clinical Timeline Engine
-> Clinical Quality
-> Knowledge Governance Platform
-> Digital Clinical Twin Platform
-> Clinical Workspace
```

Digital Clinical Twin representa estado computacional longitudinal. Ele nao representa paciente real, nao substitui prontuario, nao executa Runtime e nao prescreve.

## Dependencia de Simulacao Clinica

```text
Digital Clinical Twin Platform
-> Clinical Simulation Platform
-> Clinical Research Platform
```

Clinical Simulation Platform opera apenas sobre clones do Digital Clinical Twin. Ela nao altera Twin oficial, Runtime, Knowledge Layer, Evidence Runtime ou Clinical Operating Mind.

## Dependencia de Inteligencia Clinica

```text
Clinical Operating Mind
-> Clinical Quality
-> Scientific Validation Framework
-> Knowledge Governance Platform
-> Clinical Intelligence Platform
```

Clinical Intelligence Platform e consumidora da arquitetura. Ela nao controla lifecycle, nao executa Runtime, nao implementa IA real nesta fase e nao permite outputs sem trace, contrato, permissao e validacao de qualidade.

## Dependencia da Official Scientific Knowledge Base

```text
Knowledge Population
-> Scientific Validation Framework
-> Knowledge Governance Platform
-> Official Scientific Knowledge Base
-> Evidence Runtime
-> Clinical Operating Mind
```

Official Scientific Knowledge Base e a fonte estrutural canonica para conhecimento cientifico futuro. Ela nao publica conteudo sem validacao cientifica, governanca semantica, aprovacao editorial e versao atribuida.

## Dependencia da Psychopharmacology Library Population

```text
Official Scientific Knowledge Base
-> Psychopharmacology Library Population
-> Scientific Validation Framework
-> Knowledge Governance Platform
-> Evidence Runtime
```

Psychopharmacology Library Population registra pacotes e metadados farmacologicos. No Program A02, o pacote SSRI permanece `not_populated`, `not_validated` e `not_published`.

## Dependencia da SSRI Scientific Content Population

```text
Psychopharmacology Library Population
-> SSRI Source Corpus Intake (Program A02.5)
-> Field Level Traceability
-> Scientific Validation Framework
-> Knowledge Governance Platform
-> Editorial Review Gate
-> Publication Gate
-> Evidence Runtime
```

SSRI Scientific Content Population foi concluido como pacote cientifico interno draft. Program A04 foi inicializado e esta bloqueado em A04-003 porque o SNRI Source Corpus ainda nao existe. Program A04.0 foi criado para produzir o SNRI Scientific Corpus.

## Dependencia da SSRI Source Corpus Intake

```text
Psychopharmacology Library Population
-> Source Discovery
-> Source Corpus Intake
-> Metadata Normalization
-> Source Validation
-> Editorial Registration
-> Corpus Publication
-> SSRI Scientific Content Population
```

SSRI Source Corpus Intake e o Program A02.5. Ele nao popula medicamentos e nao cria afirmacoes clinicas. Ele apenas prepara o corpus cientifico rastreavel que desbloqueara o Program A03.

Estado atual: Program A02.5 esta concluido. Source Discovery, Source Corpus Intake, Metadata Normalization, Source Validation, Editorial Registration, Corpus Publication e Program Completion Report estao concluidos. Program A03 foi liberado apenas para fundacao estrutural e portfolio editorial metadata-only.

## Dependencia Atual do Program A03

```text
Program A02.5 Completion Report
-> Program A03 Phase 1 Structural Foundation
-> Program A03 Phase 2 Drug Portfolio Definition
-> ADR 0045 Phase 3 Refactor
-> A03-021 Scientific Drug Profile Initialization
-> A03-022 Mechanism of Action Modeling
-> A03-023 Receptor and Neurotransmitter Modeling
-> A03-024 Pharmacokinetic Modeling
-> A03-025 Pharmacodynamic Modeling
-> A03-026 Indication Modeling
-> A03-027 Posology Modeling
-> A03-028 Contraindication Modeling
-> A03-029 Safety Modeling
-> A03-030 Phase 3 Sprint 1 Baseline
-> CTO Gate Review
```

A03 Phase 1 esta concluida. A03-011 a A03-020 estao concluidas como infraestrutura metadata-only da Phase 2 e baseline aprovada. ADR 0045 refatorou a Phase 3 para dominios cientificos do Modelo do Psicofarmaco. A03-021 a A03-030 estao concluidas como modelagem estrutural controlada e baseline. Phase 3.5 foi criada para governar aquisicao cientifica. Phase 4 AUTO foi bloqueada em A03-036 porque o corpus nao possui texto-fonte extraivel. Recomendacao, prescricao e runtime permanecem proibidos.

## Dependencia da SNRI Scientific Content Population

```text
SSRI Scientific Content Population
-> Validated SSRI Pipeline
-> SNRI Scientific Content Population
```

SNRI Scientific Content Population depende da validacao do pipeline SSRI. Program A04 nao pode iniciar populacao real enquanto A03 estiver bloqueado.

## Dependencia da NDRI Scientific Content Population

```text
SNRI Scientific Content Population
-> Validated SNRI Pipeline
-> NDRI Scientific Content Population
```

NDRI Scientific Content Population depende da conclusao do Program A04 ou de excecao CTO formal. Program A04 foi concluido pelo gate A04-016, e Program A05 esta autorizado para iniciar em A05-001. Populacao real dentro de A05 continua condicionada aos gates internos, fonte, rastreabilidade e validacao.

## Dependencia da NaSSA Scientific Content Population

```text
NDRI Scientific Content Population
-> Validated NDRI Pipeline
-> NaSSA Scientific Content Population
```

NaSSA Scientific Content Population depende do Program A05 ou de excecao CTO formal. Program A06 nao pode iniciar populacao real enquanto A05 estiver bloqueado.

## Dependencia da TCA Scientific Content Population

```text
NaSSA Scientific Content Population
-> Validated NaSSA Pipeline
-> TCA Scientific Content Population
```

TCA Scientific Content Population depende do Program A06 ou de excecao CTO formal. Program A07 nao pode iniciar populacao real enquanto A06 estiver bloqueado.

## Dependencia da MAOI Scientific Content Population

```text
TCA Scientific Content Population
-> Validated TCA Pipeline
-> MAOI Scientific Content Population
```

MAOI Scientific Content Population depende do Program A07 ou de excecao CTO formal. Program A08 nao pode iniciar populacao real enquanto A07 estiver bloqueado.

## Dependencia da Atypical Antidepressants Scientific Content Population

```text
MAOI Scientific Content Population
-> Validated MAOI Pipeline
-> Atypical Antidepressants Scientific Content Population
```

Atypical Antidepressants Scientific Content Population depende do Program A08 ou de excecao CTO formal. Program A09 nao pode iniciar populacao real enquanto A08 estiver bloqueado.

## Dependencia da First-Generation Antipsychotics Scientific Content Population

```text
Atypical Antidepressants Scientific Content Population
-> Validated Atypical Antidepressants Pipeline
-> First-Generation Antipsychotics Scientific Content Population
-> Safety Engine
-> Evidence Runtime
```

First-Generation Antipsychotics Scientific Content Population depende do Program A09 ou de excecao CTO formal. Program A10 nao pode iniciar populacao real enquanto A09 estiver bloqueado.

## Dependencia da Second-Generation Antipsychotics Scientific Content Population

```text
First-Generation Antipsychotics Scientific Content Population
-> Validated FGA Pipeline
-> Second-Generation Antipsychotics Scientific Content Population
-> Safety Engine
-> Evidence Runtime
```

Second-Generation Antipsychotics Scientific Content Population depende do Program A10 ou de excecao CTO formal. Program A11 nao pode iniciar populacao real enquanto A10 estiver bloqueado.

## Dependencia da Mood Stabilizers Scientific Content Population

```text
Second-Generation Antipsychotics Scientific Content Population
-> Validated SGA Pipeline
-> Mood Stabilizers Scientific Content Population
-> Safety Engine
-> Evidence Runtime
```

Mood Stabilizers Scientific Content Population depende do Program A11 ou de excecao CTO formal. Program A12 nao pode iniciar populacao real enquanto A11 estiver bloqueado.

## Dependencia da Anxiolytics & Hypnotics Scientific Content Population

```text
Mood Stabilizers Scientific Content Population
-> Validated Mood Stabilizers Pipeline
-> Anxiolytics & Hypnotics Scientific Content Population
-> Safety Engine
-> Evidence Runtime
```

Anxiolytics & Hypnotics Scientific Content Population dependia do Program A12 ou de excecao CTO formal. Dependencia satisfeita: Program A13 foi concluido como pacote interno nao-runtime de mecanismo.

## Dependencia da ADHD Medications Scientific Content Population

```text
Anxiolytics & Hypnotics Scientific Content Population
-> Validated Anxiolytics & Hypnotics Pipeline
-> ADHD Medications Scientific Content Population
-> Safety Engine
-> Evidence Runtime
```

ADHD Medications Scientific Content Population dependia do Program A13 ou de excecao CTO formal. Dependencia satisfeita: Program A14 foi concluido como pacote interno nao-runtime de mecanismo.

## Dependencia da Cognitive Enhancers & Dementia-Related Psychopharmacology Scientific Content Population

```text
ADHD Medications Scientific Content Population
-> Validated ADHD Medications Pipeline
-> Cognitive Enhancers & Dementia-Related Psychopharmacology Scientific Content Population
-> Safety Engine
-> Evidence Runtime
-> Clinical Operating Mind
```

Cognitive Enhancers & Dementia-Related Psychopharmacology Scientific Content Population dependia do Program A14 ou de excecao CTO formal. Dependencia satisfeita: Program A15 foi concluido como pacote interno nao-runtime de mecanismo.

## Dependencias Proibidas

```text
Domain -> Application
Domain -> Interface
Interface -> Infrastructure
Interface -> Clinical Decision
Knowledge -> Executable Rule
Reasoning -> Hardcoded Evidence
Dashboard -> Clinical Conduct
Dashboard -> Clinical Experience Definition
Clinical Kernel -> Workspace Definition
Workspace -> Direct Engine Calls
Clinical Operating Mind -> Prescription
Clinical Operating Mind -> Autonomous Clinical Decision
Clinical Quality -> Clinical Recommendation
Clinical Quality -> Snapshot Mutation
Clinical Quality -> Evidence Interpretation
Clinical Research Platform -> Clinical Runtime Execution
Clinical Research Platform -> Production Mutation
Clinical Research Platform -> Clinical Recommendation
Scientific Validation Framework -> Clinical Runtime Execution
Scientific Validation Framework -> Clinical Case Interpretation
Scientific Validation Framework -> Clinical Recommendation
Evidence Runtime -> Direct Literature Access
Knowledge Governance Platform -> Clinical Runtime Execution
Knowledge Governance Platform -> Scientific Evidence Validation
Knowledge Governance Platform -> Clinical Recommendation
Digital Clinical Twin -> Real Patient Representation
Digital Clinical Twin -> Official Medical Record
Digital Clinical Twin -> Clinical Runtime Execution
Digital Clinical Twin -> Prescription
Clinical Simulation Platform -> Official Twin Mutation
Clinical Simulation Platform -> Clinical Runtime Execution
Clinical Simulation Platform -> Production Export
Clinical Simulation Platform -> Clinical Recommendation
Clinical Intelligence Platform -> Autonomous Clinical Decision
Clinical Intelligence Platform -> Prescription
Clinical Intelligence Platform -> Operating Mind Control
Clinical Intelligence Platform -> Opaque Output
Official Scientific Knowledge Base -> Hardcoded Therapeutic Rule
Official Scientific Knowledge Base -> Unvalidated Scientific Content
Official Scientific Knowledge Base -> Direct Clinical Runtime Execution
Official Scientific Knowledge Base -> Prescription
Psychopharmacology Library Population -> Scientific Claim Without Source
Psychopharmacology Library Population -> Dose Recommendation
Psychopharmacology Library Population -> Therapeutic Strategy
Psychopharmacology Library Population -> Prescription
SSRI Scientific Content Population -> Unreviewed Field Publication
SSRI Scientific Content Population -> Source-Free Field Value
SSRI Scientific Content Population -> Self-Assigned Editorial Approval
SSRI Scientific Content Population -> Runtime Consumption Before Publication Gate
SSRI Scientific Content Population -> Execution Before A02.5 Corpus Publication
SSRI Scientific Content Population -> Phase 3 Scientific Domain Skipping
SSRI Scientific Content Population -> Mechanism Modeling Before A03-021 Profile Initialization
SSRI Source Corpus Intake -> Medication Field Population
SSRI Source Corpus Intake -> Therapeutic Recommendation
SSRI Source Corpus Intake -> Evidence Runtime Consumption
SNRI Scientific Content Population -> Execution Before A03 Validation
SNRI Scientific Content Population -> Parallel Scientific Population Without Gate
NDRI Scientific Content Population -> Execution Before A04 Validation
NDRI Scientific Content Population -> Bupropion Population Without Validated Pipeline
NaSSA Scientific Content Population -> Execution Before A05 Validation
NaSSA Scientific Content Population -> Mirtazapine Population Without Validated Pipeline
TCA Scientific Content Population -> Execution Before A06 Validation
TCA Scientific Content Population -> Complex Safety Profile Without Validated Pipeline
MAOI Scientific Content Population -> Execution Before A07 Validation
MAOI Scientific Content Population -> High Risk Interaction Content Without Validated Pipeline
Atypical Antidepressants Scientific Content Population -> Execution Before A08 Validation
Atypical Antidepressants Scientific Content Population -> Multimodal Mechanism Content Without Validated Pipeline
First-Generation Antipsychotics Scientific Content Population -> Execution Before A09 Validation
First-Generation Antipsychotics Scientific Content Population -> High Impact Safety Content Without Validated Pipeline
First-Generation Antipsychotics Scientific Content Population -> Safety Engine Consumption Before Publication Gate
Second-Generation Antipsychotics Scientific Content Population -> Execution Before A10 Validation
Second-Generation Antipsychotics Scientific Content Population -> Clozapine Monitoring Without Validated Pipeline
Second-Generation Antipsychotics Scientific Content Population -> Safety Engine Consumption Before Publication Gate
Mood Stabilizers Scientific Content Population -> Execution Before A11 Validation
Mood Stabilizers Scientific Content Population -> Serum Level Content Without Validated Pipeline
Mood Stabilizers Scientific Content Population -> Safety Engine Consumption Before Publication Gate
Anxiolytics & Hypnotics Scientific Content Population -> Execution Before A12 Validation
Anxiolytics & Hypnotics Scientific Content Population -> Dependence Content Without Validated Pipeline
Anxiolytics & Hypnotics Scientific Content Population -> Safety Engine Consumption Before Publication Gate
ADHD Medications Scientific Content Population -> Execution Before A13 Validation
ADHD Medications Scientific Content Population -> Controlled Substance Content Without Validated Pipeline
ADHD Medications Scientific Content Population -> Cardiovascular Safety Content Without Validated Pipeline
ADHD Medications Scientific Content Population -> Pediatric Monitoring Content Without Validated Pipeline
ADHD Medications Scientific Content Population -> Safety Engine Consumption Before Publication Gate
Cognitive Enhancers & Dementia-Related Psychopharmacology Scientific Content Population -> Execution Before A14 Validation
Cognitive Enhancers & Dementia-Related Psychopharmacology Scientific Content Population -> Older Adult Safety Content Without Validated Pipeline
Cognitive Enhancers & Dementia-Related Psychopharmacology Scientific Content Population -> Dementia Stage Mapping Without Validated Pipeline
Cognitive Enhancers & Dementia-Related Psychopharmacology Scientific Content Population -> Safety Engine Consumption Before Publication Gate
```

## Dependencia do Project Execution Protocol

```text
Project Audit
-> Program X01 Project Execution Protocol
-> Codex Execution Protocol
-> State Resolution Protocol
-> Execute Mission Command
-> NEXT_MISSION
-> Program A03 Continuation
```

Program X01 governa a execucao state-driven do projeto. Ele nao altera arquitetura clinica, nao cria conteudo cientifico, nao autoriza runtime e nao substitui gates.

Proxima missao autorizada:

```text
EXECUTE PROGRAM R01
-> R01-002 ROADMAP_REFACTORING_REVIEW
```

`EXECUTE PROGRAM A04` deve bloquear ate Program A04.0 concluir o SNRI Scientific Corpus.

`EXECUTE PROGRAM A04.0` esta pausado em A04.0-005 ate a revisao R01 decidir se o projeto continua a fila antiga ou migra para pipelines parametrizados.

Runtime clinico permanece bloqueado.

## Dependencia do Roadmap Refactoring

```text
Roadmap Bloat Audit
-> Program R01 Roadmap Refactoring
-> R01-001 200 Mission Model
-> R01-002 Review
-> R01-003 Migration Execution Plan
-> R01-004 Pipeline Implementation
-> Resume A04.0-005 OR migrate to Pipeline Model
```

R01 nao altera arquitetura clinica, nao cria conteudo cientifico e nao executa runtime. Ele governa a forma futura de execucao.

R01-003 criou o plano de migracao, fases, riscos, matriz de conversao e sequencia de execucao. R01-004 deve decidir se o modelo parametrizado sera ativado e como a missao pausada A04.0-005 sera retomada.

Auto execution is allowed for the current phase through:

```text
EXECUTE PHASE A03-04 AUTO
EXECUTE UNTIL BLOCK
```

Automatic execution must stop at the next gate, blocker or validation failure.

## Dependencia para Implementacao

```text
Architecture Docs
-> ADR
-> Contracts
-> Tests
-> Implementation
-> Audit
-> Status Update
-> Next Mission Update
```

## Declaracao Final

O Project Dependencies impede que o PsychRx evolua com acoplamento indevido entre conhecimento, raciocinio, software e interface.




