# 065 - Dependency Audit

## 1. Objetivo

Este documento audita as dependencias entre os documentos arquiteturais, clinicos e de governanca do PsychRx.

O objetivo e identificar:

- grafo textual de dependencias;
- dependencias esperadas;
- dependencias proibidas;
- possiveis dependencias ciclicas;
- riscos arquiteturais;
- prioridade de correcao.

Este documento nao implementa software e nao altera a arquitetura. Ele registra a validacao documental da arquitetura existente.

## 2. Escopo Auditado

Foram considerados os documentos presentes em `docs/`, incluindo:

- documentos fundadores `000` a `006`;
- documentos conceituais `007` a `014`;
- documentos de sprint posteriores `024`, `031`, `044`, `051`;
- documentos de governanca arquitetural;
- ADRs;
- politicas de seguranca, evidencia, testes, nomenclatura e guardrails.

Observacao importante: alguns documentos fundadores e estruturais antigos existem com extensao `.md`, mas conteudo em formato binario tipo Word/ZIP. Eles continuam sendo documentos oficiais existentes, mas representam risco de manutencao e revisao textual.

## 3. Grafo Textual Principal

```text
000_MANIFEST
  -> 001_CONSTITUICAO_CLINICA
    -> 002_PRINCIPIOS_ARQUITETURAIS
      -> 003_ONTOLOGIA_PSICOFARMACOLOGIA
        -> 004_MODELO_DO_PACIENTE
        -> 005_MODELO_DO_PSICOFARMACO
          -> 006_FLUXO_DE_DECISAO_CLINICA

006_FLUXO_DE_DECISAO_CLINICA
  -> 008_CLINICAL_OPERATING_MIND
    -> 009_CLINICAL_SNAPSHOT
    -> 024_THERAPEUTIC_OBJECTIVE_ENGINE
    -> 010_MOTOR_DE_ESTABILIZACAO
    -> 011_KNOWLEDGE_GRAPH
    -> 012_DECISION_GRAPH
    -> 013_CONSTRAINT_GRAPH
    -> 014_EVIDENCE_GRAPH

010_BIBLIOTECA_CIENTIFICA
  -> EVIDENCE_TRACEABILITY_POLICY
    -> 014_EVIDENCE_GRAPH
      -> 031_DOMAIN_MODEL
      -> 051_DOMAIN_IMPLEMENTATION_SPEC

CLINICAL_SAFETY_CONTRACT
  -> 013_CONSTRAINT_GRAPH
  -> 012_DECISION_GRAPH
  -> 031_DOMAIN_MODEL
  -> 051_DOMAIN_IMPLEMENTATION_SPEC

031_DOMAIN_MODEL
  -> 044_MODULE_BOUNDARIES
  -> 051_DOMAIN_IMPLEMENTATION_SPEC

ARCHITECTURE_REPOSITORY_STRUCTURE
  -> LAYER_DEPENDENCY_RULES
    -> 044_MODULE_BOUNDARIES
      -> 051_DOMAIN_IMPLEMENTATION_SPEC

CODEX_DEFINITION_OF_DONE
  -> CODEX_MISSION_TEMPLATE
  -> SPRINT_GUARDRAILS

ADR_TEMPLATE
  -> 0001_GOVERNANCA_ARQUITETURAL
    -> ARCHITECTURE_REPOSITORY_STRUCTURE
    -> LAYER_DEPENDENCY_RULES
    -> SPRINT_GUARDRAILS

TESTING_POLICY
  -> 051_DOMAIN_IMPLEMENTATION_SPEC
```

## 4. Dependencias Esperadas por Documento

### 000_MANIFEST.md

Dependencias esperadas: nenhuma.

Papel: documento raiz. Define missao, visao, proposito e filosofia do projeto.

### 001_CONSTITUICAO_CLINICA.md

Dependencias esperadas:

- `000_MANIFEST.md`

Papel: transforma a missao em principios clinicos obrigatorios.

### 002_PRINCIPIOS_ARQUITETURAIS.md

Dependencias esperadas:

- `000_MANIFEST.md`
- `001_CONSTITUICAO_CLINICA.md`

Papel: define principios arquiteturais que governam todos os modulos.

### 003_ONTOLOGIA_PSICOFARMACOLOGIA.md

Dependencias esperadas:

- `000_MANIFEST.md`
- `001_CONSTITUICAO_CLINICA.md`
- `002_PRINCIPIOS_ARQUITETURAIS.md`

Papel: define entidades do universo PsychRx.

### 004_MODELO_DO_PACIENTE.md

Dependencias esperadas:

- `003_ONTOLOGIA_PSICOFARMACOLOGIA.md`

Papel: detalha o paciente como entidade central.

### 005_MODELO_DO_PSICOFARMACO.md

Dependencias esperadas:

- `003_ONTOLOGIA_PSICOFARMACOLOGIA.md`
- `004_MODELO_DO_PACIENTE.md`

Papel: padroniza o psicofarmaco como objeto do dominio.

### 006_FLUXO_DE_DECISAO_CLINICA.md

Dependencias esperadas:

- `001_CONSTITUICAO_CLINICA.md`
- `002_PRINCIPIOS_ARQUITETURAIS.md`
- `003_ONTOLOGIA_PSICOFARMACOLOGIA.md`
- `004_MODELO_DO_PACIENTE.md`
- `005_MODELO_DO_PSICOFARMACO.md`

Papel: define a sequencia clinica de raciocinio.

### 008_CLINICAL_OPERATING_MIND.md

Dependencias esperadas:

- `006_FLUXO_DE_DECISAO_CLINICA.md`
- `009_CLINICAL_SNAPSHOT.md`
- `010_MOTOR_DE_ESTABILIZACAO.md`
- `011_KNOWLEDGE_GRAPH.md`
- `012_DECISION_GRAPH.md`
- `013_CONSTRAINT_GRAPH.md`
- `014_EVIDENCE_GRAPH.md`

Risco: por ser documento integrador, pode parecer depender de documentos posteriores e anteriores simultaneamente. Essa dependencia deve ser tratada como relacao conceitual, nao como ciclo operacional.

### 009_CLINICAL_SNAPSHOT.md

Dependencias esperadas:

- `003_ONTOLOGIA_PSICOFARMACOLOGIA.md`
- `004_MODELO_DO_PACIENTE.md`
- `008_CLINICAL_OPERATING_MIND.md`

Papel: define a representacao dinamica do estado clinico atual.

### 010_MOTOR_DE_ESTABILIZACAO.md

Dependencias esperadas:

- `006_FLUXO_DE_DECISAO_CLINICA.md`
- `009_CLINICAL_SNAPSHOT.md`
- `CLINICAL_SAFETY_CONTRACT.md`

Papel: define estabilizacao como objetivo final do sistema.

### 011_KNOWLEDGE_GRAPH.md

Dependencias esperadas:

- `003_ONTOLOGIA_PSICOFARMACOLOGIA.md`
- `009_CLINICAL_SNAPSHOT.md`
- `010_BIBLIOTECA_CIENTIFICA.md`

Papel: organiza relacoes entre conceitos clinicos.

### 012_DECISION_GRAPH.md

Dependencias esperadas:

- `011_KNOWLEDGE_GRAPH.md`
- `013_CONSTRAINT_GRAPH.md`
- `014_EVIDENCE_GRAPH.md`
- `CLINICAL_SAFETY_CONTRACT.md`

Papel: organiza caminhos de decisao clinica.

### 013_CONSTRAINT_GRAPH.md

Dependencias esperadas:

- `CLINICAL_SAFETY_CONTRACT.md`
- `011_KNOWLEDGE_GRAPH.md`
- `EVIDENCE_TRACEABILITY_POLICY.md`

Papel: organiza restricoes clinicas.

### 014_EVIDENCE_GRAPH.md

Dependencias esperadas:

- `010_BIBLIOTECA_CIENTIFICA.md`
- `EVIDENCE_TRACEABILITY_POLICY.md`
- `012_DECISION_GRAPH.md`
- `013_CONSTRAINT_GRAPH.md`

Papel: conecta evidencias a decisoes, alertas e comparacoes.

### 024_THERAPEUTIC_OBJECTIVE_ENGINE.md

Dependencias esperadas:

- `008_CLINICAL_OPERATING_MIND.md`
- `009_CLINICAL_SNAPSHOT.md`
- `010_MOTOR_DE_ESTABILIZACAO.md`

Papel: define objetivos terapeuticos como direcao do raciocinio.

### 031_DOMAIN_MODEL.md

Dependencias esperadas:

- `003_ONTOLOGIA_PSICOFARMACOLOGIA.md`
- `008_CLINICAL_OPERATING_MIND.md`
- `009_CLINICAL_SNAPSHOT.md`
- `011_KNOWLEDGE_GRAPH.md`
- `012_DECISION_GRAPH.md`
- `013_CONSTRAINT_GRAPH.md`
- `014_EVIDENCE_GRAPH.md`
- `024_THERAPEUTIC_OBJECTIVE_ENGINE.md`

Papel: consolida o dominio.

### 044_MODULE_BOUNDARIES.md

Dependencias esperadas:

- `031_DOMAIN_MODEL.md`
- `ARCHITECTURE_REPOSITORY_STRUCTURE.md`
- `LAYER_DEPENDENCY_RULES.md`

Papel: define limites entre modulos.

### 051_DOMAIN_IMPLEMENTATION_SPEC.md

Dependencias esperadas:

- `031_DOMAIN_MODEL.md`
- `044_MODULE_BOUNDARIES.md`
- `LAYER_DEPENDENCY_RULES.md`
- `TESTING_POLICY.md`
- `EVIDENCE_TRACEABILITY_POLICY.md`
- `CLINICAL_SAFETY_CONTRACT.md`

Papel: converte arquitetura do dominio em especificacao para implementacao futura.

## 5. Dependencias Proibidas

As seguintes dependencias sao proibidas no conjunto documental e devem ser bloqueadas em documentos futuros:

- Domain depender de Application.
- Domain depender de Interface.
- Interface depender diretamente de Knowledge.
- Interface depender diretamente de Evidence.
- Interface depender diretamente de Safety para decidir logica clinica.
- Reasoning depender de dashboard ou interface.
- Knowledge conter regra executavel.
- Evidence depender de Application.
- Evidence depender de Interface.
- Safety depender de Interface.
- Audit decidir conduta clinica.
- Tests criar regra clinica nova.
- Motores clinicos conterem evidencia hardcoded.
- Documento de estrategia depender de interface para definir conteudo clinico.
- Documento de seguranca depender de conveniencia de UX.

## 6. Dependencias Ciclicas Identificadas

### Ciclo Conceitual: Clinical Operating Mind e seus componentes

Possivel ciclo:

```text
008_CLINICAL_OPERATING_MIND
  -> 009_CLINICAL_SNAPSHOT
  -> 008_CLINICAL_OPERATING_MIND
```

Classificacao: ciclo conceitual aceitavel com risco moderado.

Motivo: o Clinical Operating Mind define o papel do Snapshot; o Snapshot declara seu papel dentro do Clinical Operating Mind.

Correcao recomendada: manter a direcao oficial como:

```text
008_CLINICAL_OPERATING_MIND define arquitetura geral.
009_CLINICAL_SNAPSHOT detalha componente.
```

### Ciclo Conceitual: Decision Graph, Constraint Graph e Evidence Graph

Possivel ciclo:

```text
012_DECISION_GRAPH
  -> 013_CONSTRAINT_GRAPH
  -> 014_EVIDENCE_GRAPH
  -> 012_DECISION_GRAPH
```

Classificacao: ciclo conceitual aceitavel com risco alto se virar dependencia operacional.

Motivo: cada grafo explica parte do raciocinio e referencia os demais.

Correcao recomendada: definir ordem canonica:

```text
Knowledge Graph -> Constraint Graph -> Evidence Graph -> Decision Graph
```

O Decision Graph deve consumir restricoes e evidencia; Evidence Graph nao deve depender operacionalmente do Decision Graph.

### Ciclo de Governanca: ADR e Estrutura

Possivel ciclo:

```text
0001_GOVERNANCA_ARQUITETURAL
  -> ARCHITECTURE_REPOSITORY_STRUCTURE
  -> LAYER_DEPENDENCY_RULES
  -> SPRINT_GUARDRAILS
  -> 0001_GOVERNANCA_ARQUITETURAL
```

Classificacao: ciclo de governanca aceitavel.

Motivo: documentos de governanca se reforcam mutuamente.

Correcao recomendada: manter `ADR-0001` como raiz de decisoes estruturais e `SPRINT_GUARDRAILS` como regra operacional.

## 7. Riscos Arquiteturais Identificados

### Risco 1: Duplicidade de numeracao documental

Documentos duplicados por numero:

- `007_ARQUITETURA_DO_MVP.md`
- `007_MOTOR_DE_ESTABILIZACAO.md`
- `008_CLINICAL_OPERATING_MIND.md`
- `008_HIERARQUIA_DE_EVIDENCIAS.md`
- `008_MODELAGEM_DO_DOMINIO.md`
- `009_CLINICAL_SNAPSHOT.md`
- `009_REGRAS_DE_SEGURANCA_CLINICA.md`
- `010_BIBLIOTECA_CIENTIFICA.md`
- `010_MOTOR_DE_ESTABILIZACAO.md`
- `011_GLOSSARIO.md`
- `011_KNOWLEDGE_GRAPH.md`
- `012_DECISION_GRAPH.md`
- `012_ROADMAP.md`
- `013_CONSTRAINT_GRAPH.md`
- `013_RFC.md`
- `014_CHANGELOG.md`
- `014_EVIDENCE_GRAPH.md`

Impacto: alto.

Risco: referencias ambiguas, leituras incompletas e retrabalho.

Prioridade de correcao: P1.

### Risco 2: Documentos `.md` com conteudo binario

Documentos afetados incluem:

- `000_MANIFEST.md`
- `001_CONSTITUICAO_CLINICA.md`
- `002_PRINCIPIOS_ARQUITETURAIS.md`
- `003_ONTOLOGIA_PSICOFARMACOLOGIA.md`
- `004_MODELO_DO_PACIENTE.md`
- `005_MODELO_DO_PSICOFARMACO.md`
- `006_FLUXO_DE_DECISAO_CLINICA.md`
- `008_HIERARQUIA_DE_EVIDENCIAS.md`
- `009_REGRAS_DE_SEGURANCA_CLINICA.md`
- `011_GLOSSARIO.md`
- `012_ROADMAP.md`
- `013_RFC.md`
- `014_CHANGELOG.md`

Impacto: alto.

Risco: dificuldade de diff, revisao, busca textual, PR review e automacao documental.

Prioridade de correcao: P1.

### Risco 3: Clinical Operating Mind como documento integrador

Impacto: medio.

Risco: se tratado como fonte primaria de todos os componentes, pode competir com documentos especializados.

Prioridade de correcao: P2.

Mitigacao: declarar que `008_CLINICAL_OPERATING_MIND.md` define arquitetura geral, enquanto documentos especializados detalham cada componente.

### Risco 4: Evidence Graph e Evidence Traceability Policy com sobreposicao

Impacto: medio.

Risco: duplicacao entre politica e grafo de evidencia.

Prioridade de correcao: P2.

Mitigacao: `EVIDENCE_TRACEABILITY_POLICY.md` deve ser regra obrigatoria; `014_EVIDENCE_GRAPH.md` deve ser modelo relacional conceitual.

### Risco 5: Dois documentos de estabilizacao

Impacto: medio.

Risco: `007_MOTOR_DE_ESTABILIZACAO.md` e `010_MOTOR_DE_ESTABILIZACAO.md` podem divergir.

Prioridade de correcao: P2.

Mitigacao: definir `010_MOTOR_DE_ESTABILIZACAO.md` como versao oficial atual e depreciar ou arquivar o `007`.

### Risco 6: Domain Model e Domain Implementation Spec podem se confundir

Impacto: medio.

Risco: `031_DOMAIN_MODEL.md` e `051_DOMAIN_IMPLEMENTATION_SPEC.md` podem repetir conceitos.

Prioridade de correcao: P3.

Mitigacao: manter `031` como arquitetura conceitual e `051` como especificacao de implementacao sem codigo.

## 8. Prioridade de Correcao

### P1 - Corrigir antes de implementacao

- Resolver ou documentar duplicidade de numeracao.
- Converter documentos fundadores binarios para Markdown legivel, preservando conteudo.
- Criar indice canonico dos documentos oficiais.
- Definir quais documentos duplicados por numero sao oficiais, substituidos ou legados.

### P2 - Corrigir antes de motores clinicos

- Definir ordem canonica entre Knowledge Graph, Constraint Graph, Evidence Graph e Decision Graph.
- Declarar documento oficial unico de estabilizacao.
- Separar claramente politica de evidencia e grafo de evidencia.
- Atualizar referencias internas para nomes canonicos.

### P3 - Corrigir antes de interface

- Validar que Interface nao referencia Knowledge, Evidence, Safety ou Reasoning diretamente.
- Criar testes de dependencias documentais.
- Validar nomenclatura oficial em todos os documentos novos.

## 9. Ordem Canonica Recomendada

```text
000_MANIFEST
001_CONSTITUICAO_CLINICA
002_PRINCIPIOS_ARQUITETURAIS
003_ONTOLOGIA_PSICOFARMACOLOGIA
004_MODELO_DO_PACIENTE
005_MODELO_DO_PSICOFARMACO
006_FLUXO_DE_DECISAO_CLINICA
008_CLINICAL_OPERATING_MIND
009_CLINICAL_SNAPSHOT
010_MOTOR_DE_ESTABILIZACAO
010_BIBLIOTECA_CIENTIFICA
011_KNOWLEDGE_GRAPH
013_CONSTRAINT_GRAPH
014_EVIDENCE_GRAPH
012_DECISION_GRAPH
024_THERAPEUTIC_OBJECTIVE_ENGINE
031_DOMAIN_MODEL
044_MODULE_BOUNDARIES
051_DOMAIN_IMPLEMENTATION_SPEC
065_DEPENDENCY_AUDIT
```

Observacao: a ordem canonica acima nao resolve a duplicidade de nomes por si so. Ela apenas define a leitura recomendada ate que os documentos sejam renomeados, versionados ou depreciados formalmente.

## 10. Declaracao Final

A auditoria de dependencias mostra que o PsychRx possui uma arquitetura documental rica, mas com riscos de ambiguidade por duplicidade de numeracao, documentos binarios com extensao Markdown e ciclos conceituais entre documentos integradores.

Nenhum desses riscos impede a continuidade documental, mas todos devem ser tratados antes da implementacao de motores clinicos. A prioridade imediata e transformar a documentacao fundadora em base textual auditavel, definir documentos canonicos e impedir que ciclos conceituais se tornem dependencias operacionais.
