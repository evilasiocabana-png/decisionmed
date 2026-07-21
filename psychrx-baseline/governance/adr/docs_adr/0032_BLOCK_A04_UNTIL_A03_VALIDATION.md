# ADR 0032 - Block A04 Until A03 Validation

## Status

Accepted

## Contexto

Foi solicitado o Program A04 - Scientific Content Population: SNRIs. O proprio programa declara dependencia obrigatoria do Program A03.

O Program A03, entretanto, esta apenas iniciado e bloqueado para conteudo cientifico real ate ingestao de corpus, revisao editorial e validacao por campo.

## Decisao

Bloquear a execucao do Program A04 ate que o Program A03 valide o pipeline cientifico para SSRIs.

## Alternativas Consideradas

- executar A04 em paralelo com A03;
- criar apenas estrutura metadata-only para SNRIs;
- popular SNRIs usando fontes candidatas sem validar o ciclo SSRI.

## Justificativa

O A04 tem objetivo de populacao cientifica real. Executa-lo antes do A03 transformaria a ordem oficial de populacao em formalidade vazia e aumentaria risco de conhecimento sem rastreabilidade editorial.

## Impacto

O NEXT_MISSION permanece em A03-002. O A04 fica documentado como bloqueado, sem criar conteudo cientifico de SNRIs.

## Riscos

- atraso na expansao para SNRIs;
- necessidade de concluir o ciclo SSRI antes de escalar;
- dependencia de fontes e revisores.

## Criterios de Revisao Futura

- A03-002 concluido;
- reviewer registry definido;
- primeiro medicamento SSRI validado como piloto;
- Publication Gate testado com pacote real em draft;
- decisao CTO para replicar pipeline em A04.

