# ADR 0037 - Block A09 Until A08 Validation

## Status

Accepted

## Contexto

Foi solicitado o Program A09 - Scientific Content Population: Atypical Antidepressants. O proprio programa declara dependencia obrigatoria do Program A08.

O Program A08 esta bloqueado porque depende do Program A07, que depende do Program A06, que depende do Program A05, que depende do Program A04, que depende do Program A03. O Program A03 ainda nao concluiu ingestion de corpus, revisao editorial e validacao do pipeline SSRI.

## Decisao

Bloquear a execucao do Program A09 ate que o Program A08 esteja desbloqueado ou ate que uma decisao CTO registre uma excecao metodologica formal.

## Alternativas Consideradas

- executar antidepressivos atipicos em paralelo;
- criar estrutura metadata-only de antidepressivos atipicos;
- popular mecanismos multimodais usando pipeline ainda nao validado.

## Justificativa

O A09 envolve mecanismos multimodais, perfis cognitivos, sono, funcao sexual, peso, sedacao e monitorizacao. Esses campos exigem corpus, revisao editorial e rastreabilidade por campo antes de qualquer publicacao.

## Impacto

Nenhum conteudo de antidepressivo atipico foi criado. O NEXT_MISSION permanece em A03-002.

## Riscos

- atraso na expansao para antidepressivos atipicos;
- dependencia de conclusao do pipeline das classes anteriores;
- necessidade de criterios adicionais para mecanismos multimodais.

## Criterios de Revisao Futura

- A03-002 concluido;
- Program A03 com piloto validado;
- Programs A04-A08 desbloqueados ou excecao CTO documentada;
- reviewer registry preenchido;
- Publication Gate testado com pacote real em draft;
- criterio especifico para mecanismos multimodais aprovado.

