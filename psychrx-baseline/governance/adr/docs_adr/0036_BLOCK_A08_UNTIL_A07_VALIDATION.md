# ADR 0036 - Block A08 Until A07 Validation

## Status

Accepted

## Contexto

Foi solicitado o Program A08 - Scientific Content Population: MAOIs. O proprio programa declara dependencia obrigatoria do Program A07.

O Program A07 esta bloqueado porque depende do Program A06, que depende do Program A05, que depende do Program A04, que depende do Program A03. O Program A03 ainda nao concluiu ingestion de corpus, revisao editorial e validacao do pipeline SSRI.

MAOIs representam classe de alta criticidade clinica, com riscos associados a interacoes medicamentosas, interacoes alimentares, washout, switching, crise hipertensiva e toxicidade serotoninergica.

## Decisao

Bloquear a execucao do Program A08 ate que o Program A07 esteja desbloqueado ou ate que uma decisao CTO registre uma excecao metodologica formal.

## Alternativas Consideradas

- executar MAOIs em paralelo;
- criar estrutura metadata-only de MAOIs;
- popular campos de seguranca de MAOIs usando pipeline ainda nao validado;
- iniciar apenas interacoes alimentares e washout.

## Justificativa

O A08 envolve conhecimento de seguranca de alto impacto. Executa-lo antes de validar os ciclos anteriores poderia introduzir informacao clinica incompleta, mal rastreada ou falsamente validada.

## Impacto

Nenhum conteudo MAOI foi criado. O NEXT_MISSION permanece em A03-002.

## Riscos

- atraso na expansao para MAOIs;
- dependencia de conclusao do pipeline das classes anteriores;
- necessidade de criterios adicionais de seguranca antes da populacao.

## Criterios de Revisao Futura

- A03-002 concluido;
- Program A03 com piloto validado;
- Programs A04, A05, A06 e A07 desbloqueados ou excecao CTO documentada;
- reviewer registry preenchido;
- Publication Gate testado com pacote real em draft;
- criterio especifico para classes de alto risco aprovado.

