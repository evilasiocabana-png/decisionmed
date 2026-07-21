# ADR 0008 - Program 06 Reconciliation

## Status

Aceito.

## Data

2026-06-30

## Contexto

O usuario solicitou a execucao do Programa 06.

Durante a verificacao obrigatoria, foi identificada uma divergencia entre documentos:

- `MASTER_DEVELOPMENT_PLAN.md` define `PROGRAM 06` como `Software Platform`.
- `PROJECT_TREE.md` registrava historicamente `PROGRAM 06` como `Architecture Validation`.

Pela ordem de prevalencia definida no MDP, o `MASTER_DEVELOPMENT_PLAN.md` governa a estrutura enterprise oficial.

## Decisao

Executar o Programa 06 como:

```text
PROGRAM 06 - Software Platform
```

Criar `docs/PROGRAM_06_SOFTWARE_PLATFORM.md` como registro oficial do programa.

Manter `065_DEPENDENCY_AUDIT.md` como documento historico de auditoria arquitetural, sem trata-lo como definidor do Programa 06.

## Alternativas Consideradas

### Seguir o PROJECT_TREE historico

Rejeitada. O MDP tem maior autoridade como indice mestre.

### Renumerar todos os programas imediatamente

Rejeitada. Renumeracao ampla aumenta risco de inconsistencia e deve ocorrer em sprint propria de reconciliacao.

### Criar registro do Programa 06 e documentar o conflito

Aceita. Resolve a execucao atual com menor risco e preserva rastreabilidade.

## Impacto

- Programa 06 passa a ser oficialmente Software Platform.
- `PROJECT_TREE.md` deve refletir o MDP para o Programa 06.
- `PROGRAM_06_SOFTWARE_PLATFORM.md` passa a ser documento de referencia do programa.
- `PROGRAM_06_EXECUTION_REPORT.md` registra a execucao oficial.

## Riscos

- Documentos historicos ainda podem conter numeracao antiga.
- Missoes 052-064 continuam como lacuna documental.
- Software Platform ainda nao deve receber logica clinica.

## Mitigacoes

- Registrar a reconciliacao nesta ADR.
- Nao renumerar documentos antigos silenciosamente.
- Atualizar `PROJECT_STATUS.md`, `PROJECT_PROGRESS.md` e `NEXT_MISSION.md`.
- Manter software existente em modo read-only.

## Documentos Afetados

- `docs/PROGRAM_06_SOFTWARE_PLATFORM.md`
- `docs/PROGRAM_06_EXECUTION_REPORT.md`
- `governance/execution/PROJECT_TREE.md`
- `governance/execution/PROJECT_STATUS.md`
- `governance/execution/PROJECT_PROGRESS.md`
- `governance/execution/NEXT_MISSION.md`
- `governance/execution/PROJECT_INDEX.md`

## Criterios de Revisao Futura

Revisar quando:

- houver sprint especifica para reconciliar toda a numeracao enterprise;
- missoes 052-064 forem recriadas ou absorvidas;
- Software Platform deixar de ser apenas baseline read-only;
- houver implementacao clinica real.

## Declaracao Final

O Programa 06 deve ser tratado como Software Platform, conforme o Master Development Plan, preservando a auditoria 065 como documento historico e impedindo renumeracao silenciosa da arquitetura.
