# ADR 0019 - Clinical Timeline Engine Architecture

## Status

Accepted.

## Contexto

O PsychRx precisa representar longitudinalmente a sequencia de Clinical Snapshots sem transformar essa sequencia em prontuario oficial ou decisao clinica.

## Decisao

Criar `clinical_timeline/` como pacote independente, integrado ao Runtime apos Snapshot, produzindo `ClinicalTimeline` read-only.

## Alternativas

- Usar Snapshot Index como timeline: rejeitado por falta de transicoes e navegacao.
- Persistir timeline como prontuario: rejeitado por escopo e seguranca.

## Consequencias

Workspace pode navegar historicamente por snapshots e transicoes estruturais.

## Riscos

Confundir Timeline com registro clinico oficial.

## Mitigacoes

Documentacao, testes e linguagem read-only explicita.

## Declaracao Final

Clinical Timeline Engine representa evolucao computacional, nao prontuario, recomendacao ou prescricao.
