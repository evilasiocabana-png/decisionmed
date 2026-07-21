# ADR 0033 - Block A05 Until A04 Validation

## Status

Accepted

## Contexto

Foi solicitado o Program A05 - Scientific Content Population: NDRIs. O proprio programa declara dependencia obrigatoria do Program A04.

O Program A04 esta bloqueado porque depende do Program A03, que ainda nao concluiu ingestion de corpus, revisao editorial e validacao do pipeline SSRI.

## Decisao

Bloquear a execucao do Program A05 ate que o Program A04 esteja desbloqueado ou ate que uma decisao CTO registre uma excecao metodologica formal.

## Alternativas Consideradas

- executar Bupropion em paralelo;
- criar estrutura metadata-only de NDRIs;
- popular NDRIs usando o pipeline ainda nao validado dos SSRIs.

## Justificativa

O A05 tem objetivo de populacao cientifica real. Executa-lo antes de validar os ciclos A03 e A04 criaria expansao de conteudo sem maturidade metodologica suficiente.

## Impacto

Nenhum conteudo NDRI foi criado. O NEXT_MISSION permanece em A03-002.

## Riscos

- atraso na expansao para NDRIs;
- dependencia de conclusao do pipeline SSRI/SNRI;
- necessidade de corpus e revisores antes da populacao.

## Criterios de Revisao Futura

- A03-002 concluido;
- Program A03 com piloto validado;
- Program A04 desbloqueado ou excecao CTO documentada;
- reviewer registry preenchido;
- Publication Gate testado com pacote real em draft.

