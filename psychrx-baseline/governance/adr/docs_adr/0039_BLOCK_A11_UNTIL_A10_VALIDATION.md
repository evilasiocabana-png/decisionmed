# ADR 0039 - Block A11 Until A10 Validation

## Status

Accepted

## Contexto

Foi solicitado o Program A11 - Scientific Content Population: Second-Generation Antipsychotics. O proprio programa declara dependencia obrigatoria do Program A10, alem de Safety Engine e Evidence Runtime.

O Program A10 esta bloqueado porque depende do Program A09, que depende do Program A08, que depende do Program A07, que depende do Program A06, que depende do Program A05, que depende do Program A04, que depende do Program A03. O Program A03 ainda nao concluiu ingestion de corpus, revisao editorial e validacao do pipeline SSRI.

SGAs representam classe de alta heterogeneidade e alto impacto de seguranca, com riscos metabolicos, QT, EPS, prolactina, agranulocitose, miocardite, formulacoes LAI e monitorizacao laboratorial.

## Decisao

Bloquear a execucao do Program A11 ate que o Program A10 esteja desbloqueado ou ate que uma decisao CTO registre uma excecao metodologica formal.

## Alternativas Consideradas

- executar SGAs em paralelo;
- criar estrutura metadata-only de SGAs;
- iniciar apenas LAI registry;
- popular clozapina ou riscos metabolicos usando pipeline ainda nao validado.

## Justificativa

O A11 combina conhecimento farmacologico complexo com seguranca clinica critica. Executa-lo antes de validar o pipeline cientifico e os programas predecessores criaria risco de conhecimento incompleto, mal rastreado ou inadvertidamente operacionalizavel.

## Impacto

Nenhum conteudo SGA foi criado. O NEXT_MISSION permanece em A03-002.

## Riscos

- atraso na expansao para SGAs;
- dependencia de conclusao do pipeline das classes anteriores;
- necessidade de criterios especificos de seguranca, LAI e clozapina antes da populacao.

## Criterios de Revisao Futura

- A03-002 concluido;
- Program A03 com piloto validado;
- Programs A04-A10 desbloqueados ou excecao CTO documentada;
- reviewer registry preenchido;
- Publication Gate testado com pacote real em draft;
- criterios especificos para SGAs, clozapina, LAIs e Safety Engine aprovados.

