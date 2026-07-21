# ADR 0041 - Block A13 Until A12 Validation

## Status

Accepted

## Contexto

Foi solicitado o Program A13 - Scientific Content Population: Anxiolytics & Hypnotics. O proprio programa declara dependencia obrigatoria do Program A12, alem de Safety Engine e Evidence Runtime.

O Program A12 esta bloqueado porque depende do Program A11, que depende do Program A10, que depende do Program A09, que depende do Program A08, que depende do Program A07, que depende do Program A06, que depende do Program A05, que depende do Program A04, que depende do Program A03. O Program A03 ainda nao concluiu ingestion de corpus, revisao editorial e validacao do pipeline SSRI.

Anxiolytics & Hypnotics envolvem conteudo de alta sensibilidade: dependencia, tolerancia, abstinencia, sedacao, quedas, depressao respiratoria, prejuizo cognitivo e uso em idosos.

## Decisao

Bloquear a execucao do Program A13 ate que o Program A12 esteja desbloqueado ou ate que uma decisao CTO registre uma excecao metodologica formal.

## Alternativas Consideradas

- executar Anxiolytics & Hypnotics em paralelo;
- criar estrutura metadata-only para benzodiazepines e Z-drugs;
- iniciar apenas modelo de dependencia;
- popular alprazolam ou zolpidem usando pipeline ainda nao validado.

## Justificativa

O A13 combina conhecimento farmacologico, seguranca, dependencia e potencial de uso indevido. Executa-lo antes de validar o pipeline cientifico criaria risco de conhecimento incompleto, mal rastreado ou operacionalizavel antes do Publication Gate.

## Impacto

Nenhum conteudo de Anxiolytics & Hypnotics foi criado. O NEXT_MISSION permanece em A03-002.

## Riscos

- atraso na expansao para ansioliticos e hipnoticos;
- dependencia de conclusao do pipeline das classes anteriores;
- necessidade de criterios especificos de seguranca, dependencia, abstinencia e idosos antes da populacao.

## Criterios de Revisao Futura

- A03-002 concluido;
- Program A03 com piloto validado;
- Programs A04-A12 desbloqueados ou excecao CTO documentada;
- reviewer registry preenchido;
- Publication Gate testado com pacote real em draft;
- criterios especificos para dependencia, abstinencia e Safety Engine aprovados.

