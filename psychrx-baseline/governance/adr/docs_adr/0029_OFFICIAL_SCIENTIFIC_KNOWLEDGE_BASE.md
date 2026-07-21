# ADR 0029 - Official Scientific Knowledge Base

## Status

Accepted

## Contexto

A arquitetura estrategica inicial do PsychRx foi encerrada e o projeto entrou em tracks especializados. O primeiro track necessario e a expansao de conhecimento cientifico.

## Decisao

Criar `scientific_knowledge/` como base estrutural oficial para contratos, schemas, pacotes, validacao, workflow editorial e catalogos de metadados.

## Alternativas Consideradas

- popular diretamente `knowledge_library/`;
- inserir conhecimento no Evidence Runtime;
- manter apenas documentos sem contratos executaveis.

## Justificativa

Separar a base cientifica oficial reduz acoplamento, evita hardcoding de conhecimento e cria uma etapa clara entre governanca cientifica e consumo pelo Evidence Runtime.

## Impacto

O projeto passa a possuir uma camada propria para conhecimento cientifico estruturado, ainda vazia de conteudo clinico validado.

## Riscos

- confundir schema com conteudo validado;
- popular conhecimento sem revisao;
- usar catalogos de metadados como fonte assistencial.

## Criterios de Revisao Futura

- primeiro pacote cientifico validado;
- primeira diretriz importada;
- primeira populacao de psicofarmaco;
- integracao real com Evidence Runtime.

