# Program A03 Blocked Report - Scientific Content Population: SSRIs

## Status

Parcialmente liberado.

A fundacao estrutural do Program A03 foi liberada apos o encerramento do Program A02.5. A populacao cientifica real permanece bloqueada.

## O Que Foi Executado

- planejamento do Program A03;
- matriz de fontes candidatas;
- template de rastreabilidade por campo;
- gate editorial;
- atualizacao da proxima missao;
- A03 Phase 1 - Scientific Foundation;
- registries vazios;
- portfolio SSRI metadata-only;
- baseline estrutural da Phase 1;
- A03-011 - Drug Portfolio Definition;
- A03-012 - Drug Portfolio Editorial Registry;
- A03-013 - Drug Portfolio Source Binding;
- A03-014 - Portfolio Directory Generation;
- A03-015 - Drug Template Generation;
- A03-016 - Portfolio Registry Linking;
- A03-017 - Portfolio Traceability Initialization;
- A03-018 - Editorial Status Framework;
- A03-019 - Portfolio Quality Assurance;
- A03-020 - Phase 2 Baseline;
- ADR 0045 - Phase 3 refactor;
- A03-021 - Scientific Drug Profile Initialization.

## O Que Nao Foi Executado

- populacao cientifica completa de Fluoxetine;
- populacao cientifica completa dos demais SSRIs;
- preenchimento de Drug Profiles com valores cientificos;
- classificacao de evidencia;
- afirmacoes de mecanismo, PK, PD, seguranca, interacao ou contraindicacao;
- validacao cientifica por campo;
- aprovacao editorial;
- publicacao no Knowledge Layer;
- consumo pelo Evidence Runtime.

## Motivo do Bloqueio

O pedido exige conteudo cientifico real completo e aprovacao editorial. O repositorio ainda nao possui corpus local validado nem registro de revisores editoriais. Gerar conteudo completo sem isso violaria:

- Evidence Traceability Policy;
- Scientific Validation Framework;
- Knowledge Governance Platform;
- Publication Gate;
- ADR 0030.

## Dependencia Inserida

O bloqueio do Program A03 passa a depender explicitamente do novo programa intermediario:

```text
PROGRAM A02.5 - SSRI Source Corpus Intake
```

A antiga navegacao `MISSION A03-002 - SSRI Source Corpus Intake` foi reclassificada como:

```text
MISSION A02.5-002 - SSRI Source Corpus Intake
```

Essa mudanca nao altera o conteudo da missao. Ela apenas corrige a responsabilidade arquitetural: ingestao de corpus pertence ao Program A02.5; populacao cientifica de SSRIs pertence ao Program A03.

## Risco Evitado

- conhecimento clinico sem fonte;
- recomendacao terapeutica implícita;
- posologia sem governanca;
- falsa validacao editorial;
- rastreabilidade incompleta.

## Caminho para Desbloqueio

1. concluir o Program A02.5;
2. carregar corpus oficial ou autorizar fontes especificas;
3. registrar bibliografia completa;
4. definir revisor editorial;
5. aprovar criterio de extracao por campo;
6. popular apenas campos em `draft`;
7. validar semanticamente;
8. revisar conflitos;
9. publicar somente apos checklist completo.

## Estado Atual da Navegacao

O Program A02.5 foi concluido formalmente e o Program A03 foi parcialmente liberado para estrutura e governanca metadata-only.

O estado atual autorizado e:

- A03 Phase 1 concluida;
- A03-011 concluida como definicao editorial do portfolio;
- A03-012 concluida como registro editorial do portfolio;
- A03-013 concluida como source binding metadata-only;
- A03-014 concluida como directory generation metadata-only;
- A03-015 concluida como empty template generation metadata-only;
- A03-016 concluida como registry linking metadata-only;
- A03-017 concluida como traceability initialization metadata-only;
- A03-018 concluida como editorial status framework metadata-only;
- A03-019 concluida como structural QA;
- A03-020 concluida como Phase 2 baseline e gate;
- ADR 0045 refatorou a Phase 3;
- A03-021 concluida como Scientific Drug Profile Initialization.

Nota historica: em um ciclo anterior, `NEXT_MISSION.md` apontava para `MISSION A03-026 - INDICATION_MODELING`. O estado atual deve ser resolvido por `governance/execution/NEXT_MISSION.md`.

Registro historico da tentativa bloqueada inicial:

```text
docs/A03-001_BLOCKED_BY_A02_5.md
```

A tentativa bloqueada permanece preservada apenas como historico de governanca. Ela nao representa mais o estado atual do Program A03.

## Declaracao Final

O Program A03 pode avancar para modelagem cientifica controlada por dominio. Ele nao deve avancar para recomendacao, prescricao, consumo em runtime ou publicacao cientifica sem gates especificos, fontes rastreadas por campo e revisao editorial.


