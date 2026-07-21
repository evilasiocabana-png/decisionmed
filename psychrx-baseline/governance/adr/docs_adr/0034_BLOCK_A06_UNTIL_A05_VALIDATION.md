# ADR 0034 - Block A06 Until A05 Validation

## Status

Accepted

## Contexto

Foi solicitado o Program A06 - Scientific Content Population: NaSSAs. O proprio programa declara dependencia obrigatoria do Program A05.

O Program A05 esta bloqueado porque depende do Program A04, que por sua vez depende do Program A03. O Program A03 ainda nao concluiu ingestion de corpus, revisao editorial e validacao do pipeline SSRI.

## Decisao

Bloquear a execucao do Program A06 ate que o Program A05 esteja desbloqueado ou ate que uma decisao CTO registre uma excecao metodologica formal.

## Alternativas Consideradas

- executar Mirtazapine em paralelo;
- criar estrutura metadata-only de NaSSAs;
- popular NaSSAs usando pipeline ainda nao validado dos SSRIs.

## Justificativa

O A06 tem objetivo de populacao cientifica real. Executa-lo antes de validar os ciclos A03, A04 e A05 criaria expansao de conteudo sem maturidade metodologica suficiente.

## Impacto

Nenhum conteudo NaSSA foi criado. O NEXT_MISSION permanece em A03-002.

## Riscos

- atraso na expansao para NaSSAs;
- dependencia de conclusao do pipeline SSRI/SNRI/NDRI;
- necessidade de corpus e revisores antes da populacao.

## Criterios de Revisao Futura

- A03-002 concluido;
- Program A03 com piloto validado;
- Program A04 e A05 desbloqueados ou excecao CTO documentada;
- reviewer registry preenchido;
- Publication Gate testado com pacote real em draft.

