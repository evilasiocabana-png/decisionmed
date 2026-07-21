# ADR 0040 - Block A12 Until A11 Validation

## Status

Accepted

## Contexto

Foi solicitado o Program A12 - Scientific Content Population: Mood Stabilizers. O proprio programa declara dependencia obrigatoria do Program A11, alem de Safety Engine e Evidence Runtime.

O Program A11 esta bloqueado porque depende do Program A10, que depende do Program A09, que depende do Program A08, que depende do Program A07, que depende do Program A06, que depende do Program A05, que depende do Program A04, que depende do Program A03. O Program A03 ainda nao concluiu ingestion de corpus, revisao editorial e validacao do pipeline SSRI.

Mood Stabilizers envolvem conteudo de alta criticidade: niveis sericos, toxicidade, monitorizacao renal, hepatica, hematologica, dermatologica, riscos na gestacao, interacoes e mapeamento por fase do transtorno bipolar.

## Decisao

Bloquear a execucao do Program A12 ate que o Program A11 esteja desbloqueado ou ate que uma decisao CTO registre uma excecao metodologica formal.

## Alternativas Consideradas

- executar estabilizadores do humor em paralelo;
- criar estrutura metadata-only para estabilizadores;
- iniciar apenas modelo de niveis sericos;
- popular litio ou lamotrigina usando pipeline ainda nao validado.

## Justificativa

O A12 combina conhecimento farmacologico, monitorizacao e seguranca com alto potencial de se converter em conduta clinica. Executa-lo antes de validar o pipeline cientifico criaria risco de conhecimento incompleto, mal rastreado ou operacionalizavel antes do Publication Gate.

## Impacto

Nenhum conteudo de estabilizador do humor foi criado. O NEXT_MISSION permanece em A03-002.

## Riscos

- atraso na expansao para estabilizadores do humor;
- dependencia de conclusao do pipeline das classes anteriores;
- necessidade de criterios especificos de seguranca, monitorizacao e fase bipolar antes da populacao.

## Criterios de Revisao Futura

- A03-002 concluido;
- Program A03 com piloto validado;
- Programs A04-A11 desbloqueados ou excecao CTO documentada;
- reviewer registry preenchido;
- Publication Gate testado com pacote real em draft;
- criterios especificos para Mood Stabilizers, monitorizacao, niveis sericos e Safety Engine aprovados.

