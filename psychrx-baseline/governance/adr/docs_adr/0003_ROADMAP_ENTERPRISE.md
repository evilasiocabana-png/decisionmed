# ADR 0003 - Roadmap Enterprise do PsychRx

## ID da Decisao

ADR-0003

## Data

2026-06-30

## Status

Aceita como baseline documental inicial

## Contexto

O PsychRx evoluiu rapidamente em documentos arquiteturais, cientificos, conceituais e de engenharia. A sequencia anterior continha duplicidades de numeracao, lacunas e documentos criados fora de uma visao enterprise completa.

O CTO definiu uma reorganizacao em sprints de longo prazo, com separacao entre arquitetura, conhecimento cientifico, experiencia clinica, API, persistencia, auditoria, validacao, seguranca, IA assistiva, GPTs, agentes e producao.

## Decisao

Adotar `docs/ROADMAP_ENTERPRISE.md` como referencia oficial de planejamento documental e evolutivo.

Criar os documentos conceituais dos Sprints 14-17 (`112-143`) porque estes foram explicitamente definidos e ainda nao existiam.

Nao renomear nem sobrescrever documentos antigos nesta decisao.

Registrar inconsistencias e lacunas em `docs/ROADMAP_RECONCILIATION_REPORT.md`.

## Alternativas Consideradas

1. Renumerar todos os documentos antigos imediatamente.
2. Criar apenas o roadmap sem documentos 112-143.
3. Manter o roadmap antigo sem reconciliacao.
4. Adotar roadmap enterprise preservando historico e documentando lacunas.

A alternativa 4 foi escolhida por reduzir risco de perda historica e evitar reescrita de documentos fundadores.

## Justificativa

A mudanca cria uma visao enterprise sem quebrar a base documental existente. Ela permite evoluir UX clinica, dashboard medico, mobile e API sem iniciar software prematuramente e sem alterar a Constituicao Clinica.

## Impacto

- cria nova referencia de roadmap;
- explicita trilhas paralelas;
- define backlog futuro ate Sprint 30;
- cria baseline documental dos Sprints 14-17;
- preserva documentos anteriores.

## Riscos

- duplicidade temporaria de numeracao;
- confusao entre roadmap antigo e enterprise;
- necessidade futura de matriz de equivalencia;
- existencia de arquivos `.md` com conteudo binario de Word.

## Documentos Afetados

- `docs/ROADMAP_ENTERPRISE.md`
- `docs/ROADMAP_RECONCILIATION_REPORT.md`
- `PROJECT_STATUS.md`
- `docs/112_CLINICAL_WORKFLOW.md` ate `docs/143_API_BASELINE.md`

## Criterios de Revisao Futura

Esta ADR deve ser revisada quando:

- houver decisao de renumerar documentos antigos;
- os sprints 144-259 forem decompostos em missoes;
- a arquitetura sair da fase documental para implementacao;
- for definida politica de migracao dos `.md` binarios.

## Declaracao Final

O Roadmap Enterprise passa a orientar a evolucao do PsychRx sem apagar o historico existente e sem autorizar implementacao clinica prematura.
