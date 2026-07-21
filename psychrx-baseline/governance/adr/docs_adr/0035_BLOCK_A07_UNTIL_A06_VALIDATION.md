# ADR 0035 - Block A07 Until A06 Validation

## Status

Accepted

## Contexto

Foi solicitado o Program A07 - Scientific Content Population: TCAs. O proprio programa declara dependencia obrigatoria do Program A06.

O Program A06 esta bloqueado porque depende do Program A05, que depende do Program A04, que depende do Program A03. O Program A03 ainda nao concluiu ingestion de corpus, revisao editorial e validacao do pipeline SSRI.

## Decisao

Bloquear a execucao do Program A07 ate que o Program A06 esteja desbloqueado ou ate que uma decisao CTO registre uma excecao metodologica formal.

## Alternativas Consideradas

- executar TCAs em paralelo;
- criar estrutura metadata-only de TCAs;
- popular campos de seguranca de TCAs usando pipeline ainda nao validado.

## Justificativa

O A07 envolve uma classe farmacologica de alta complexidade, com riscos de cardiotoxicidade, toxicidade em overdose, anticolinergia e monitorizacao. Executa-lo antes de validar os ciclos anteriores ampliaria risco cientifico e arquitetural.

## Impacto

Nenhum conteudo TCA foi criado. O NEXT_MISSION permanece em A03-002.

## Riscos

- atraso na expansao para TCAs;
- dependencia de conclusao do pipeline SSRI/SNRI/NDRI/NaSSA;
- necessidade de corpus e revisores antes da populacao.

## Criterios de Revisao Futura

- A03-002 concluido;
- Program A03 com piloto validado;
- Programs A04, A05 e A06 desbloqueados ou excecao CTO documentada;
- reviewer registry preenchido;
- Publication Gate testado com pacote real em draft;
- criterio especifico para classes de alta complexidade farmacologica aprovado.

