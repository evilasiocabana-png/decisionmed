# ADR 0018 - Clinical Snapshot Engine Architecture

## Status

Accepted.

## Contexto

O PsychRx precisa consolidar Runtime, Safety, Evidence, Optimization e Explanation em um artefato unico, imutavel e rastreavel para consumo do Clinical Workspace.

## Decisao

Criar `clinical_snapshot/` como pacote independente, integrado ao Runtime apos Explanation, produzindo `ClinicalSnapshot` como read model primario.

## Alternativas Consideradas

- Widgets chamarem motores diretamente: rejeitado por acoplamento.
- Snapshot ser prontuario: rejeitado por escopo e seguranca.
- Snapshot mutavel: rejeitado por perda de reproducibilidade.

## Consequencias

Workspace pode evoluir consumindo Snapshot como fonte unica.

## Riscos

Confundir Snapshot com prontuario ou decisao clinica.

## Mitigacoes

Documentacao, testes e status read-only explicito.

## Documentos Afetados

PROJECT_STATUS, PROJECT_PROGRESS, PROJECT_TREE, PROJECT_INDEX, NEXT_MISSION e PROGRAM_15_BASELINE.

## Criterios de Revisao Futura

Revisar no Program 16 - Clinical Timeline Engine.
