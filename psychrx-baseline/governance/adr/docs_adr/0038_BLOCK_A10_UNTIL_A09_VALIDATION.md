# ADR 0038 - Block A10 Until A09 Validation

## Status

Accepted

## Contexto

Foi solicitado o Program A10 - Scientific Content Population: First-Generation Antipsychotics. O proprio programa declara dependencia obrigatoria do Program A09, alem de Safety Engine e Evidence Runtime.

O Program A09 esta bloqueado porque depende do Program A08, que depende do Program A07, que depende do Program A06, que depende do Program A05, que depende do Program A04, que depende do Program A03. O Program A03 ainda nao concluiu ingestion de corpus, revisao editorial e validacao do pipeline SSRI.

FGAs representam classe de alta criticidade, com riscos extrapiramidais, discinesia tardia, sindrome neuroleptica maligna, hiperprolactinemia, QT, formulacoes injetaveis e LAIs.

## Decisao

Bloquear a execucao do Program A10 ate que o Program A09 esteja desbloqueado ou ate que uma decisao CTO registre uma excecao metodologica formal.

## Alternativas Consideradas

- executar FGAs em paralelo;
- criar estrutura metadata-only de FGAs;
- iniciar apenas Safety Engine compatibility;
- popular riscos de alta criticidade usando pipeline ainda nao validado.

## Justificativa

O A10 mistura conhecimento farmacologico complexo com seguranca clinica de alto impacto. Executa-lo antes de validar o pipeline cientifico aumentaria risco de conteudo incompleto, mal rastreado ou inadvertidamente operacionalizavel.

## Impacto

Nenhum conteudo FGA foi criado. O NEXT_MISSION permanece em A03-002.

## Riscos

- atraso na expansao para antipsicoticos;
- dependencia de conclusao do pipeline das classes anteriores;
- necessidade de criterios especificos de seguranca antes da populacao.

## Criterios de Revisao Futura

- A03-002 concluido;
- Program A03 com piloto validado;
- Programs A04-A09 desbloqueados ou excecao CTO documentada;
- reviewer registry preenchido;
- Publication Gate testado com pacote real em draft;
- criterios especificos para antipsicoticos e Safety Engine aprovados.

